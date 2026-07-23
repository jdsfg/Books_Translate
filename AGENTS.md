# AGENTS.md

## Cursor Cloud specific instructions

This repo is a **Python 3 CLI translation pipeline** (no web app, no service, no
third-party runtime deps for the core workflow). The two scripts are
`pipeline/translate_book.py` (state machine: `status`/`next`/`commit`/`assemble`/`verify`/`titles`)
and `pipeline/translate/verify_translation.py` (structure/number/glossary checker).
Canonical state lives in `pipeline/translate/<book>/checkpoint.json` and
`pipeline/translate/<book>/blocks/<id>.md`; assembled `sources/<book>.zh.md` is a
derived artifact and is git-ignored.

### The one non-obvious gotcha: the `WORK_ROOT` Windows-path shim

`translate_book.py` hardcodes a **Windows** working root
(`WORK_ROOT = Path(r"D:\...\书库抓取工具\translate")`). On Linux that string is
treated as a single relative directory name (backslashes are literal), so the
scripts look for checkpoints in the wrong place, `book.load()` returns `None`, and
`status` crashes with `TypeError: 'NoneType' object is not subscriptable`. Running
any command in that broken state also creates a junk directory named
`D:\...\translate` in the repo root.

Fix (already handled by the startup update script — do **not** edit the shared
scripts): create a symlink whose name is exactly `WORK_ROOT` pointing at the real
`pipeline/translate`, from the repo root. The update script does this by reading
`WORK_ROOT` from the module so it stays correct even if the constant changes:

```
python3 -c "import importlib.util as u,os,shutil; s=u.spec_from_file_location('tb','pipeline/translate_book.py'); m=u.module_from_spec(s); s.loader.exec_module(m); n=str(m.WORK_ROOT); os.path.islink(n) and os.remove(n); (os.path.isdir(n) and not os.path.islink(n)) and shutil.rmtree(n); os.path.exists(n) or os.symlink('pipeline/translate', n)"
```

Consequences of the shim:
- Always run the CLI **from the repo root** (`/workspace`); the symlink and the
  relative target only resolve from there.
- The symlink (name starts with `D:\`) is **not** git-ignored. Never `git add` it.
- If you ever see a real `D:\...` directory (not a symlink) in the repo root, a
  command was run before the shim existed — delete it and re-run the shim command.

### Running things (see `README.md`, `CLOUD_AGENT.md`, `pipeline/translate/翻译流水线_FOR_AGENTS.md` for the full contract)

Use repo-relative source paths, e.g. `sources/<book>.md`:

```
python3 pipeline/translate_book.py status   "sources/复杂性科学入门.md"
python3 pipeline/translate_book.py next     "sources/复杂性科学入门.md" --ctx
python3 pipeline/translate_book.py commit   "sources/<book>.md" <block-id> --file <tmpfile>   # MUST use --file
python3 pipeline/translate_book.py assemble "sources/<book>.md"
python3 pipeline/translate/verify_translation.py "sources/<book>.md" --force-arabic --glossary pipeline/translate/glossary_<domain>.md
```

Notes:
- There is no lint step and no automated test suite; `verify_translation.py` is the
  quality gate. It exits `1` when `ERROR > 0`; per `STATUS.md` some books
  (e.g. `复杂性科学入门`) still have known structural `ERROR`s pending audit, so a
  non-zero verify exit is expected and does **not** mean the environment is broken.
- `commit` requires `--file`; stdin input is intentionally disabled (it hangs).
- Optional `auto` retry mode (`retry --auto`) needs the `requests` package plus
  `TB_API_URL`/`TB_API_KEY`; not required for the normal manual workflow.
- Per `CLOUD_AGENT.md`, do not run `init`/`lock-titles`, do not edit the shared
  scripts/styles/glossaries, and do not commit temporary files or `.zh.md` output.
