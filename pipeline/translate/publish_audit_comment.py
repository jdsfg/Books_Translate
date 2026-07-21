#!/usr/bin/env python3
"""Create or update the translation quality-gate comment on a GitHub PR."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


MARKER = "<!-- translation-quality-gate -->"
API_ROOT = "https://api.github.com"


def request_json(url: str, token: str, method: str = "GET", payload: dict | None = None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(url, data=data, method=method)
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("Authorization", f"Bearer {token}")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    request.add_header("User-Agent", "books-translate-quality-gate")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def publish(repository: str, pull_request: int, body: str, token: str) -> str:
    comments_url = f"{API_ROOT}/repos/{repository}/issues/{pull_request}/comments"
    comments = request_json(f"{comments_url}?per_page=100", token)
    existing = next((comment for comment in comments if MARKER in comment.get("body", "")), None)
    if existing:
        request_json(existing["url"], token, "PATCH", {"body": body})
        return "updated"
    request_json(comments_url, token, "POST", {"body": body})
    return "created"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True, help="owner/repository")
    parser.add_argument("--pull-request", type=int, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print("GITHUB_TOKEN is not set; skipping PR comment", file=sys.stderr)
        return 0

    body = args.report.read_text(encoding="utf-8")
    if MARKER not in body:
        body = f"{MARKER}\n{body}"
    if len(body) > 60_000:
        body = body[:59_000] + "\n\n_Report truncated; inspect the workflow artifact for full details._\n"

    try:
        action = publish(args.repository, args.pull_request, body, token)
    except urllib.error.HTTPError as exc:
        # Fork PRs may receive a read-only token. The check result remains authoritative.
        if exc.code in (401, 403):
            print(f"GitHub token cannot publish comments ({exc.code}); skipping", file=sys.stderr)
            return 0
        raise
    print(f"{action} translation audit comment")
    return 0


if __name__ == "__main__":
    sys.exit(main())
