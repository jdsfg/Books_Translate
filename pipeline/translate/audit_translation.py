#!/usr/bin/env python3
"""Deterministic quality gate for translation pull requests.

This complements ``verify_translation.py`` with repository, checkpoint,
completion-marker, question/list, duplicate-content, and residue checks.  It
does not attempt to judge semantic translation quality; an independent
source/translation review is still required before final acceptance.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]
TRANSLATE_ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = TRANSLATE_ROOT / "review_config.json"

QUESTION_RE = re.compile(r"(?im)^\s*(?:[-*]\s*)?\*{0,2}Q\s*(\d+)\s*[.)]")
LIST_RE = re.compile(r"(?m)^\s*(?:[-+*]|\d+[.)])\s+")
PLACEHOLDER_RE = re.compile(r"\b(?:XXX|YYY|fff)\b")
COMMON_ENGLISH_RE = re.compile(
    r"\b(?:because|crew|desirable|however|outside|probable|therefore|"
    r"what|when|where|which|would|should|could)\b",
    re.IGNORECASE,
)
ENGLISH_RUN_RE = re.compile(r"\b[a-z]{3,}(?:\s+[a-z]{3,}){2,}\b")
FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
URL_RE = re.compile(r"https?://\S+")
CHAPTER_RE = re.compile(r"^(c\d{2})_")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tb = load_module("translate_book_audit", REPO_ROOT / "pipeline" / "translate_book.py")
vt = load_module("verify_translation_audit", TRANSLATE_ROOT / "verify_translation.py")


@dataclass
class Finding:
    level: str
    code: str
    message: str
    book: str = ""
    block: str = ""


@dataclass
class VerifyRun:
    glossary: str
    errors: int
    warnings: int
    details: list[str] = field(default_factory=list)


@dataclass
class BookResult:
    book: str
    done: int = 0
    total: int = 0
    pending: int = 0
    failed: int = 0
    complete: bool = False
    assembled: bool = False
    verify: list[VerifyRun] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)

    @property
    def errors(self) -> int:
        return sum(f.level == "ERROR" for f in self.findings)

    @property
    def warnings(self) -> int:
        return sum(f.level == "WARN" for f in self.findings)


def sha12(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def chapter_of(block_id: str) -> str:
    if block_id == "intro" or block_id.startswith("intro_b"):
        return "intro"
    match = CHAPTER_RE.match(block_id)
    return match.group(1) if match else "other"


def strip_non_prose(text: str) -> str:
    text = FENCED_CODE_RE.sub("", text)
    text = INLINE_CODE_RE.sub("", text)
    return URL_RE.sub("", text)


def normalized_paragraphs(text: str, minimum: int = 120) -> set[str]:
    paragraphs = set()
    for paragraph in re.split(r"\n\s*\n", strip_non_prose(text)):
        normalized = re.sub(r"[\s*_`#>]+", "", paragraph)
        if len(normalized) >= minimum:
            paragraphs.add(normalized)
    return paragraphs


def question_ids(text: str) -> Counter[str]:
    return Counter(QUESTION_RE.findall(strip_non_prose(text)))


def list_count(text: str) -> int:
    return len(LIST_RE.findall(strip_non_prose(text)))


def git_changed_paths(base_ref: str) -> list[str]:
    proc = subprocess.run(
        ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def load_config(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != 1 or not isinstance(data.get("books"), dict):
        raise ValueError(f"unsupported review config: {path}")
    return data


def changed_books(config: dict, paths: Iterable[str]) -> list[str]:
    selected = set()
    for path in paths:
        for name, settings in config["books"].items():
            work_prefix = f"pipeline/translate/{name}/"
            if path.startswith(work_prefix) or path == settings["source"]:
                selected.add(name)
    return sorted(selected)


def audit_changed_paths(paths: Iterable[str]) -> list[Finding]:
    findings = []
    for path in paths:
        p = Path(path)
        name = p.name
        prohibited = (
            (path.startswith("sources/") and name.endswith(".zh.md"))
            or name.startswith("_tmp_")
            or name.endswith(".log")
            or "__pycache__" in p.parts
            or name.endswith((".pyc", ".pyo"))
        )
        if prohibited:
            findings.append(
                Finding("ERROR", "PROHIBITED_FILE", f"PR contains generated/temporary file: {path}")
            )
    return findings


def add_finding(
    result: BookResult,
    level: str,
    code: str,
    message: str,
    block: str = "",
) -> None:
    result.findings.append(Finding(level, code, message, result.book, block))


def run_verify(source: Path, glossary: Path | None, force_arabic: bool) -> VerifyRun:
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        errors, warnings = vt.verify_book(
            str(source),
            force_arabic=force_arabic,
            glossary=str(glossary) if glossary else None,
            strict=False,
        )
    noteworthy = [
        line.strip()
        for line in output.getvalue().splitlines()
        if "[ERROR]" in line or "[WARN]" in line
    ]
    return VerifyRun(
        glossary=str(glossary.relative_to(REPO_ROOT)) if glossary else "(none)",
        errors=errors,
        warnings=warnings,
        details=noteworthy[:20],
    )


def audit_book(name: str, settings: dict) -> BookResult:
    result = BookResult(book=name)
    source = REPO_ROOT / settings["source"]
    work = TRANSLATE_ROOT / name
    checkpoint = work / "checkpoint.json"

    if not source.exists():
        add_finding(result, "ERROR", "SOURCE_MISSING", f"missing source: {settings['source']}")
        return result
    if not checkpoint.exists():
        add_finding(result, "ERROR", "CHECKPOINT_MISSING", f"missing checkpoint: {checkpoint}")
        return result

    book = tb.Book(str(source))
    state = book.load()
    if not state:
        add_finding(result, "ERROR", "CHECKPOINT_INVALID", "checkpoint did not load")
        return result

    blocks = sorted(state.get("blocks", []), key=lambda item: item.get("order", -1))
    ids = [item.get("id", "") for item in blocks]
    orders = [item.get("order") for item in blocks]
    result.total = len(blocks)
    result.done = sum(item.get("status") == "done" for item in blocks)
    result.pending = sum(item.get("status") == "pending" for item in blocks)
    result.failed = sum(item.get("status") == "failed" for item in blocks)
    result.complete = result.done == result.total and result.pending == 0 and result.failed == 0

    if len(ids) != len(set(ids)):
        add_finding(result, "ERROR", "DUPLICATE_BLOCK_ID", "checkpoint contains duplicate block IDs")
    if len(orders) != len(set(orders)):
        add_finding(result, "ERROR", "DUPLICATE_BLOCK_ORDER", "checkpoint contains duplicate orders")

    chapter_source: dict[str, list[str]] = defaultdict(list)
    chapter_translation: dict[str, list[str]] = defaultdict(list)
    translated: list[tuple[dict, str, str]] = []

    for item in blocks:
        block_id = item.get("id", "")
        status = item.get("status")
        source_text = item.get("src")
        if source_text is None:
            try:
                source_text = book.src_of(block_id)
            except Exception as exc:  # pragma: no cover - defensive reporting
                add_finding(result, "ERROR", "SOURCE_BLOCK_MISSING", str(exc), block_id)
                continue
        if item.get("src_sha") and sha12(source_text) != item["src_sha"]:
            add_finding(
                result,
                "ERROR",
                "SOURCE_SHA_MISMATCH",
                "checkpoint source hash does not match its source text",
                block_id,
            )
        if status != "done":
            continue

        block_path = work / "blocks" / f"{block_id}.md"
        if not block_path.exists():
            add_finding(result, "ERROR", "BLOCK_FILE_MISSING", str(block_path), block_id)
            continue
        translation = block_path.read_text(encoding="utf-8")
        if item.get("out_sha") and sha12(translation) != item["out_sha"]:
            add_finding(
                result,
                "ERROR",
                "OUTPUT_SHA_MISMATCH",
                "block was changed without updating checkpoint via commit --file",
                block_id,
            )

        chapter = chapter_of(block_id)
        chapter_source[chapter].append(source_text)
        chapter_translation[chapter].append(translation)
        translated.append((item, source_text, translation))

        prose = strip_non_prose(translation)
        placeholders = sorted(set(PLACEHOLDER_RE.findall(prose)))
        if placeholders:
            add_finding(
                result,
                "ERROR",
                "PLACEHOLDER",
                f"suspicious placeholders remain: {placeholders}",
                block_id,
            )
        english = sorted(set(match.group(0) for match in COMMON_ENGLISH_RE.finditer(prose)))
        runs = ENGLISH_RUN_RE.findall(prose)
        if english or runs:
            samples = english + runs[:2]
            add_finding(
                result,
                "WARN",
                "ENGLISH_RESIDUE",
                f"review ordinary English candidates: {samples}",
                block_id,
            )

        paragraphs = [
            re.sub(r"[\s*_`#>]+", "", p)
            for p in re.split(r"\n\s*\n", prose)
            if len(re.sub(r"[\s*_`#>]+", "", p)) >= 120
        ]
        duplicates = [p for p, count in Counter(paragraphs).items() if count > 1]
        if duplicates:
            add_finding(
                result,
                "ERROR",
                "DUPLICATE_PARAGRAPH",
                f"translation repeats {len(duplicates)} long paragraph(s) inside the block",
                block_id,
            )

    for chapter in sorted(chapter_source):
        source_text = "\n\n".join(chapter_source[chapter])
        translation = "\n\n".join(chapter_translation[chapter])
        source_questions = question_ids(source_text)
        translated_questions = question_ids(translation)
        if source_questions != translated_questions:
            add_finding(
                result,
                "ERROR",
                "QUESTION_MISMATCH",
                f"{chapter}: source Q={dict(source_questions)}, translation Q={dict(translated_questions)}",
            )
        source_lists = list_count(source_text)
        translated_lists = list_count(translation)
        if source_lists != translated_lists:
            add_finding(
                result,
                "WARN",
                "LIST_COUNT",
                f"{chapter}: source list items={source_lists}, translation={translated_lists}",
            )

    for previous, current in zip(translated, translated[1:]):
        previous_item, previous_source, previous_translation = previous
        current_item, current_source, current_translation = current
        if chapter_of(previous_item["id"]) != chapter_of(current_item["id"]):
            continue
        translated_overlap = normalized_paragraphs(previous_translation) & normalized_paragraphs(
            current_translation
        )
        source_overlap = normalized_paragraphs(previous_source) & normalized_paragraphs(current_source)
        unexplained = translated_overlap - source_overlap
        if unexplained:
            add_finding(
                result,
                "ERROR",
                "ADJACENT_DUPLICATION",
                f"{previous_item['id']}→{current_item['id']} repeats "
                f"{len(unexplained)} long paragraph(s) not repeated in source",
                current_item["id"],
            )

    done_flag = work / f"DONE_{name}.flag"
    misplaced_flag = TRANSLATE_ROOT / f"DONE_{name}.flag"
    if misplaced_flag.exists():
        add_finding(
            result,
            "ERROR",
            "DONE_MISPLACED",
            f"move completion marker into {work.relative_to(REPO_ROOT)}",
        )
    if result.complete:
        if not done_flag.exists():
            add_finding(result, "ERROR", "DONE_MISSING", f"missing {done_flag.relative_to(REPO_ROOT)}")
        else:
            done_text = done_flag.read_text(encoding="utf-8")
            if not re.search(r"ERROR\s*[=:]\s*0\b", done_text, re.IGNORECASE):
                add_finding(result, "ERROR", "DONE_ERROR_GATE", "DONE flag does not record ERROR=0")
            progress_patterns = (
                re.escape(f"{result.done}/{result.total}"),
                re.escape(f"{result.done} / {result.total}"),
            )
            if not any(re.search(pattern, done_text) for pattern in progress_patterns):
                add_finding(
                    result,
                    "WARN",
                    "DONE_PROGRESS",
                    f"DONE flag does not clearly record {result.done}/{result.total}",
                )
    elif done_flag.exists():
        add_finding(result, "ERROR", "DONE_PREMATURE", "DONE flag exists before all blocks are complete")

    try:
        with tempfile.TemporaryDirectory(prefix="translation-assemble-") as tmp:
            book.zh_path = Path(tmp) / f"{name}.zh.md"
            book.assemble()
            result.assembled = book.zh_path.exists() and book.zh_path.stat().st_size > 0
            if not result.assembled:
                add_finding(result, "ERROR", "ASSEMBLE_EMPTY", "assemble produced no output")
    except Exception as exc:
        add_finding(result, "ERROR", "ASSEMBLE_FAILED", str(exc))

    glossaries = settings.get("glossaries") or [None]
    for glossary_name in glossaries:
        glossary = REPO_ROOT / glossary_name if glossary_name else None
        if glossary is not None and not glossary.exists():
            add_finding(
                result,
                "ERROR",
                "GLOSSARY_MISSING",
                f"missing glossary: {glossary_name}",
            )
            continue
        verify_run = run_verify(source, glossary, bool(settings.get("force_arabic")))
        result.verify.append(verify_run)
        if verify_run.errors:
            add_finding(
                result,
                "ERROR",
                "VERIFY_ERROR",
                f"{verify_run.glossary}: ERROR={verify_run.errors}, WARN={verify_run.warnings}",
            )
        elif verify_run.warnings:
            add_finding(
                result,
                "WARN",
                "VERIFY_WARN",
                f"{verify_run.glossary}: ERROR=0, WARN={verify_run.warnings}",
            )

    return result


def render_report(
    results: list[BookResult],
    global_findings: list[Finding],
    changed: list[str],
) -> str:
    total_errors = sum(result.errors for result in results) + sum(
        finding.level == "ERROR" for finding in global_findings
    )
    verdict = "BLOCK" if total_errors else "MECHANICAL PASS"
    lines = [
        "<!-- translation-quality-gate -->",
        f"# Translation quality gate: {verdict}",
        "",
        "> This is a deterministic mechanical gate. Final acceptance still requires an ",
        "> independent source/translation semantic review.",
        "",
    ]
    if changed:
        lines.extend(["Changed paths were evaluated from the PR diff.", ""])
    if results:
        lines.extend(
            [
                "| Book | Progress | Assemble | Verify | Findings |",
                "|---|---:|---|---|---:|",
            ]
        )
        for result in results:
            verify = "; ".join(
                f"{Path(run.glossary).name}: E{run.errors}/W{run.warnings}"
                for run in result.verify
            ) or "not run"
            lines.append(
                f"| {result.book} | {result.done}/{result.total} | "
                f"{'OK' if result.assembled else 'FAIL'} | {verify} | "
                f"E{result.errors}/W{result.warnings} |"
            )
        lines.append("")
    else:
        lines.extend(["No registered book content changed.", ""])

    all_findings = global_findings + [
        finding for result in results for finding in result.findings
    ]
    errors = [finding for finding in all_findings if finding.level == "ERROR"]
    warnings = [finding for finding in all_findings if finding.level == "WARN"]
    if errors:
        lines.extend(["## Blocking findings", ""])
        for finding in errors:
            location = "/".join(part for part in (finding.book, finding.block) if part)
            prefix = f"`{location}` " if location else ""
            lines.append(f"- **{finding.code}**: {prefix}{finding.message}")
        lines.append("")
    if warnings:
        lines.extend(["## Review warnings", ""])
        for finding in warnings[:40]:
            location = "/".join(part for part in (finding.book, finding.block) if part)
            prefix = f"`{location}` " if location else ""
            lines.append(f"- **{finding.code}**: {prefix}{finding.message}")
        if len(warnings) > 40:
            lines.append(f"- … {len(warnings) - 40} additional warnings omitted from the comment.")
        lines.append("")
    if not all_findings:
        lines.extend(["No mechanical findings.", ""])
    lines.append(f"Result: **{verdict}**")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--all", action="store_true", help="audit every registered book")
    parser.add_argument("--book", action="append", default=[], help="audit one named book")
    parser.add_argument("--changed-since", help="audit books touched since this git ref/SHA")
    parser.add_argument("--report", type=Path, default=Path("translation-audit.md"))
    parser.add_argument("--json-report", type=Path)
    args = parser.parse_args()

    config = load_config(args.config)
    changed: list[str] = []
    global_findings: list[Finding] = []
    if args.changed_since:
        changed = git_changed_paths(args.changed_since)
        global_findings.extend(audit_changed_paths(changed))

    if args.all:
        selected = sorted(config["books"])
    elif args.book:
        selected = args.book
    elif args.changed_since:
        selected = changed_books(config, changed)
    else:
        parser.error("choose --all, --book, or --changed-since")

    unknown = [name for name in selected if name not in config["books"]]
    if unknown:
        for name in unknown:
            global_findings.append(
                Finding("ERROR", "BOOK_NOT_REGISTERED", f"book is absent from review config: {name}")
            )
        selected = [name for name in selected if name in config["books"]]

    results = [audit_book(name, config["books"][name]) for name in selected]
    report = render_report(results, global_findings, changed)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(report, encoding="utf-8")
    print(report)

    if args.json_report:
        payload = {
            "results": [asdict(result) for result in results],
            "global_findings": [asdict(finding) for finding in global_findings],
        }
        args.json_report.parent.mkdir(parents=True, exist_ok=True)
        args.json_report.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    errors = sum(result.errors for result in results) + sum(
        finding.level == "ERROR" for finding in global_findings
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
