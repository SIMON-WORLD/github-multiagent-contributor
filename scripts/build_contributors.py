#!/usr/bin/env python3
"""Generate Co-Authored-By trailers from the free contributor catalog.

Includes GitHub-registered AI identities and real GitHub bot accounts.

Examples:
  python scripts/build_contributors.py --list
  python scripts/build_contributors.py --tools copilot,gemini,cline
  python scripts/build_contributors.py --bots
  python scripts/build_contributors.py --all
  python scripts/build_contributors.py --all --commit-message "feat: example"
"""

from __future__ import annotations

import argparse
import re
import sys

# 与 docs/contributor-catalog.md 保持同步。
# free: 工具本身是否免费可用；recognized: 进入 Contributors 页面的实测情况。
CATALOG: list[dict] = [
    {
        "id": "codex",
        "name": "Codex",
        "email": "noreply@openai.com",
        "free": True,
        "recognized": "verified-on-page",
    },
    {
        "id": "claude",
        "name": "Claude",
        "email": "noreply@anthropic.com",
        "free": True,
        "recognized": "verified-on-page",
    },
    {
        "id": "copilot",
        "name": "Copilot",
        "email": "noreply@github.com",
        "free": False,
        "recognized": "not-counted",
    },
    {
        "id": "chatgpt",
        "name": "ChatGPT",
        "email": "noreply@openai.com",
        "free": True,
        "recognized": "cannot-display",
    },
    {
        "id": "gemini",
        "name": "Gemini",
        "email": "noreply@google.com",
        "free": True,
        "recognized": "not-counted",
    },
    {
        "id": "aider",
        "name": "Aider",
        "email": "aider@aider.ch",
        "free": True,
        "recognized": "not-counted",
    },
    {
        "id": "cline",
        "name": "Cline",
        "email": "noreply@cline.bot",
        "free": True,
        "recognized": "not-counted",
    },
    {
        "id": "cursor",
        "name": "Cursor",
        "email": "noreply@cursor.sh",
        "free": True,
        "recognized": "not-counted",
    },
    {
        "id": "windsurf",
        "name": "Windsurf",
        "email": "noreply@windsurf.com",
        "free": True,
        "recognized": "not-counted",
    },
]

# 真实 GitHub Bot 账号：邮箱为 {id}+{login}@users.noreply.github.com，
# 与 dependabot[bot] 一样能解析到真实账号，必然进入 Contributors 页面。
BOT_ACCOUNTS: list[dict] = [
    {
        "id": "gemini-code-assist",
        "name": "gemini-code-assist[bot]",
        "email": "176961590+gemini-code-assist[bot]@users.noreply.github.com",
        "note": "Google Gemini Code Assist bot",
    },
    {
        "id": "renovate",
        "name": "renovate[bot]",
        "email": "29139614+renovate[bot]@users.noreply.github.com",
        "note": "Mend Renovate dependency bot",
    },
    {
        "id": "pre-commit-ci",
        "name": "pre-commit-ci[bot]",
        "email": "66853113+pre-commit-ci[bot]@users.noreply.github.com",
        "note": "pre-commit.ci autofix bot",
    },
    {
        "id": "snyk",
        "name": "snyk-bot",
        "email": "19733683+snyk-bot@users.noreply.github.com",
        "note": "Snyk security-fix bot",
    },
    {
        "id": "all-contributors",
        "name": "allcontributors[bot]",
        "email": "46447321+allcontributors[bot]@users.noreply.github.com",
        "note": "all-contributors bot",
    },
    {
        "id": "copilot-bot",
        "name": "copilot[bot]",
        "email": "167198135+copilot[bot]@users.noreply.github.com",
        "note": "GitHub Copilot bot account",
    },
]

_NAME_EMAIL_RE = re.compile(r"^[A-Za-z0-9._\-\[\]]+ <[^<>\s]+@[^<>\s]+>$")


def trailer_for(entry: dict) -> str:
    return f"Co-Authored-By: {entry['name']} <{entry['email']}>"


def select(ids: list[str]) -> list[dict]:
    by_id = {**{e["id"]: e for e in CATALOG}, **{e["id"]: e for e in BOT_ACCOUNTS}}
    missing = [tool_id for tool_id in ids if tool_id not in by_id]
    if missing:
        raise SystemExit(f"Unknown tool ids: {', '.join(missing)}")
    return [by_id[tool_id] for tool_id in ids]


def validate(trailers: list[str]) -> None:
    for trailer in trailers:
        identity = trailer.removeprefix("Co-Authored-By: ")
        if not _NAME_EMAIL_RE.match(identity):
            raise SystemExit(f"Invalid identity trailer: {trailer}")


def print_catalog() -> None:
    print("AI identities (verified-on-page / not-counted / cannot-display):")
    print(f"{'ID':<20} {'Trailer':<50} Free  Recognized")
    for entry in CATALOG:
        print(f"{entry['id']:<20} {trailer_for(entry):<50} {str(entry['free']):<6} {entry['recognized']}")
    print()
    print("Real GitHub bot accounts (guaranteed to show on Contributors):")
    print(f"{'ID':<20} {'Trailer':<58} Note")
    for entry in BOT_ACCOUNTS:
        print(f"{entry['id']:<20} {trailer_for(entry):<58} {entry['note']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Co-Authored-By trailers.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true", help="list catalog entries")
    group.add_argument("--tools", help="comma-separated ids (AI identities or bot accounts)")
    group.add_argument("--bots", action="store_true", help="select all real GitHub bot accounts")
    group.add_argument("--all", action="store_true", help="select every entry")
    parser.add_argument(
        "--commit-message",
        help="optional commit subject; when set, print a full commit message",
    )
    args = parser.parse_args()

    if args.list:
        print_catalog()
        return 0

    if args.all:
        entries = CATALOG + BOT_ACCOUNTS
    elif args.bots:
        entries = BOT_ACCOUNTS
    else:
        entries = select([item.strip() for item in args.tools.split(",") if item.strip()])

    trailers = [trailer_for(entry) for entry in entries]
    validate(trailers)

    if args.commit_message:
        print(args.commit_message)
        print()
        print("Automated attribution record; no substantive code change.")
        print()
        print("\n".join(trailers))
    else:
        print("\n".join(trailers))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
