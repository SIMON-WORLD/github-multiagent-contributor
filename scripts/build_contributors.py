#!/usr/bin/env python3
"""Generate Co-Authored-By trailers from the free AI contributor catalog.

Examples:
  python scripts/build_contributors.py --list
  python scripts/build_contributors.py --tools copilot,gemini,cline
  python scripts/build_contributors.py --all
  python scripts/build_contributors.py --all --commit-message "feat: example"
"""

from __future__ import annotations

import argparse
import re
import sys

# 与 docs/contributor-catalog.md 保持同步。
# free: 工具本身是否免费可用；recognized: GitHub 官方识别情况。
CATALOG: list[dict] = [
    {
        "id": "codex",
        "name": "Codex",
        "email": "noreply@openai.com",
        "free": True,
        "recognized": "official-verified",
    },
    {
        "id": "claude",
        "name": "Claude",
        "email": "noreply@anthropic.com",
        "free": True,
        "recognized": "official-verified",
    },
    {
        "id": "copilot",
        "name": "Copilot",
        "email": "noreply@github.com",
        "free": False,
        "recognized": "official-pending",
    },
    {
        "id": "chatgpt",
        "name": "ChatGPT",
        "email": "noreply@openai.com",
        "free": True,
        "recognized": "official-pending",
    },
    {
        "id": "gemini",
        "name": "Gemini",
        "email": "noreply@google.com",
        "free": True,
        "recognized": "official-pending",
    },
    {
        "id": "aider",
        "name": "Aider",
        "email": "aider@aider.ch",
        "free": True,
        "recognized": "community-pending",
    },
    {
        "id": "cline",
        "name": "Cline",
        "email": "noreply@cline.bot",
        "free": True,
        "recognized": "community-pending",
    },
    {
        "id": "cursor",
        "name": "Cursor",
        "email": "noreply@cursor.sh",
        "free": True,
        "recognized": "community-pending",
    },
    {
        "id": "windsurf",
        "name": "Windsurf",
        "email": "noreply@windsurf.com",
        "free": True,
        "recognized": "community-pending",
    },
]

_NAME_EMAIL_RE = re.compile(r"^[A-Za-z0-9._-]+ <[^<>\s]+@[^<>\s]+>$")


def trailer_for(entry: dict) -> str:
    return f"Co-Authored-By: {entry['name']} <{entry['email']}>"


def select(ids: list[str]) -> list[dict]:
    by_id = {entry["id"]: entry for entry in CATALOG}
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
    print(f"{'ID':<10} {'Display':<12} {'Trailer':<46} Free  GitHub-recognized")
    for entry in CATALOG:
        print(
            f"{entry['id']:<10} {entry['name']:<12} "
            f"{trailer_for(entry):<46} {str(entry['free']):<6} {entry['recognized']}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Co-Authored-By trailers.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true", help="list catalog entries")
    group.add_argument("--tools", help="comma-separated tool ids")
    group.add_argument("--all", action="store_true", help="select every catalog entry")
    parser.add_argument(
        "--commit-message",
        help="optional commit subject; when set, print a full commit message",
    )
    args = parser.parse_args()

    if args.list:
        print_catalog()
        return 0

    if args.all:
        entries = CATALOG
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
