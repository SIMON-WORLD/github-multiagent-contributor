#!/usr/bin/env python3
"""Generate Co-Authored-By trailers from the verified contributor catalog.

Only identities proven to enter the Contributors page are included:
- A group: codex, claude (GitHub-registered AI identities)
- C group: real GitHub bot accounts (guaranteed to show)

Examples:
  python scripts/build_contributors.py --list
  python scripts/build_contributors.py --tools codex,renovate
  python scripts/build_contributors.py --bots
  python scripts/build_contributors.py --all
  python scripts/build_contributors.py --bots --commit-message "feat: example"
"""

from __future__ import annotations

import argparse
import re
import sys

# A 组：已验证计入 Contributors 页面的 AI 身份。
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
]

# C 组：真实 GitHub Bot 账号，邮箱为 {id}+{login}@users.noreply.github.com，
# 与 dependabot[bot] 一样能解析到真实账号，必然进入 Contributors 页面。
BOT_ACCOUNTS: list[dict] = [
    {
        "id": "gemini-code-assist",
        "name": "gemini-code-assist[bot]",
        "email": "176961590+gemini-code-assist[bot]@users.noreply.github.com",
        "note": "Google Gemini Code Assist 官方 bot",
    },
    {
        "id": "renovate",
        "name": "renovate[bot]",
        "email": "29139614+renovate[bot]@users.noreply.github.com",
        "note": "Mend Renovate 依赖机器人",
    },
    {
        "id": "pre-commit-ci",
        "name": "pre-commit-ci[bot]",
        "email": "66853113+pre-commit-ci[bot]@users.noreply.github.com",
        "note": "pre-commit.ci 自动修复",
    },
    {
        "id": "snyk",
        "name": "snyk-bot",
        "email": "19733683+snyk-bot@users.noreply.github.com",
        "note": "Snyk 安全修复",
    },
    {
        "id": "all-contributors",
        "name": "allcontributors[bot]",
        "email": "46447321+allcontributors[bot]@users.noreply.github.com",
        "note": "all-contributors 名单机器人",
    },
    {
        "id": "copilot-bot",
        "name": "copilot[bot]",
        "email": "167198135+copilot[bot]@users.noreply.github.com",
        "note": "GitHub Copilot 官方 bot 账号",
    },
    {
        "id": "claude-bot",
        "name": "claude[bot]",
        "email": "209825114+claude[bot]@users.noreply.github.com",
        "note": "Anthropic Claude 官方 bot 账号",
    },
    {
        "id": "cursor-bot",
        "name": "cursor[bot]",
        "email": "206951365+cursor[bot]@users.noreply.github.com",
        "note": "Cursor AI 官方 bot 账号",
    },
    {
        "id": "qodo-merge",
        "name": "qodo-merge[bot]",
        "email": "185363710+qodo-merge[bot]@users.noreply.github.com",
        "note": "Qodo Merge（PR-Agent）AI 审查/合并 bot",
    },
    {
        "id": "mergify",
        "name": "mergify[bot]",
        "email": "37929162+mergify[bot]@users.noreply.github.com",
        "note": "Mergify 合并队列",
    },
    {
        "id": "kodiakhq",
        "name": "kodiakhq[bot]",
        "email": "49736102+kodiakhq[bot]@users.noreply.github.com",
        "note": "Kodiak 合并队列",
    },
    {
        "id": "github-merge-queue",
        "name": "github-merge-queue[bot]",
        "email": "118344674+github-merge-queue[bot]@users.noreply.github.com",
        "note": "GitHub Merge Queue",
    },
    {
        "id": "scala-steward",
        "name": "scala-steward",
        "email": "43047562+scala-steward@users.noreply.github.com",
        "note": "Scala 依赖更新机器人",
    },
    {
        "id": "pyup",
        "name": "pyup-bot",
        "email": "16239342+pyup-bot@users.noreply.github.com",
        "note": "Python 依赖更新机器人",
    },
    {
        "id": "mend",
        "name": "mend[bot]",
        "email": "241224340+mend[bot]@users.noreply.github.com",
        "note": "Mend 安全扫描 bot",
    },
    {
        "id": "greenkeeper",
        "name": "greenkeeper[bot]",
        "email": "23040076+greenkeeper[bot]@users.noreply.github.com",
        "note": "npm 依赖 bot（已停用）",
    },
    {
        "id": "dependabot-preview",
        "name": "dependabot-preview[bot]",
        "email": "27856297+dependabot-preview[bot]@users.noreply.github.com",
        "note": "Dependabot 旧版 bot（已停用）",
    },
    {
        "id": "semantic-release",
        "name": "semantic-release-bot",
        "email": "32174276+semantic-release-bot@users.noreply.github.com",
        "note": "semantic-release 发布/提交 bot",
    },
    {
        "id": "codecov",
        "name": "codecov[bot]",
        "email": "22429695+codecov[bot]@users.noreply.github.com",
        "note": "Codecov 覆盖率 bot",
    },
    {
        "id": "github-classroom",
        "name": "github-classroom[bot]",
        "email": "66690702+github-classroom[bot]@users.noreply.github.com",
        "note": "GitHub Classroom",
    },
    {
        "id": "github-learning-lab",
        "name": "github-learning-lab[bot]",
        "email": "37936606+github-learning-lab[bot]@users.noreply.github.com",
        "note": "GitHub Learning Lab",
    },
    {
        "id": "first-timers",
        "name": "first-timers[bot]",
        "email": "31459394+first-timers[bot]@users.noreply.github.com",
        "note": "first-timers 引导 bot",
    },
    {
        "id": "request-info",
        "name": "request-info[bot]",
        "email": "30733101+request-info[bot]@users.noreply.github.com",
        "note": "request-info 信息补充 bot",
    },
    {
        "id": "stale",
        "name": "stale[bot]",
        "email": "26384082+stale[bot]@users.noreply.github.com",
        "note": "stale 过期关闭 bot",
    },
    {
        "id": "todo",
        "name": "todo[bot]",
        "email": "32347756+todo[bot]@users.noreply.github.com",
        "note": "todo 转 Issue bot",
    },
    {
        "id": "welcome",
        "name": "welcome[bot]",
        "email": "30606887+welcome[bot]@users.noreply.github.com",
        "note": "welcome 欢迎 bot",
    },
    {
        "id": "wip",
        "name": "wip[bot]",
        "email": "29805525+wip[bot]@users.noreply.github.com",
        "note": "WIP 状态检查 bot",
    },
    {
        "id": "hound",
        "name": "hound[bot]",
        "email": "30008653+hound[bot]@users.noreply.github.com",
        "note": "Hound 代码风格审查 bot",
    },
    {
        "id": "stickler-ci",
        "name": "stickler-ci[bot]",
        "email": "41810448+stickler-ci[bot]@users.noreply.github.com",
        "note": "Stickler CI 风格检查 bot",
    },
    {
        "id": "release-drafter",
        "name": "release-drafter[bot]",
        "email": "40829082+release-drafter[bot]@users.noreply.github.com",
        "note": "Release Drafter 发布草稿 bot",
    },
    {
        "id": "pypi",
        "name": "pypi[bot]",
        "email": "253595658+pypi[bot]@users.noreply.github.com",
        "note": "PyPI 官方 bot",
    },
    {
        "id": "npm",
        "name": "npm[bot]",
        "email": "38296568+npm[bot]@users.noreply.github.com",
        "note": "npm 官方 bot",
    },
    {
        "id": "octokit",
        "name": "octokit[bot]",
        "email": "171388558+octokit[bot]@users.noreply.github.com",
        "note": "GitHub 官方 Octokit bot",
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
    print("A. AI identities verified on the Contributors page:")
    print(f"{'ID':<20} {'Trailer':<50} Free  Recognized")
    for entry in CATALOG:
        print(f"{entry['id']:<20} {trailer_for(entry):<50} {str(entry['free']):<6} {entry['recognized']}")
    print()
    print("C. Real GitHub bot accounts (guaranteed to show on Contributors):")
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
