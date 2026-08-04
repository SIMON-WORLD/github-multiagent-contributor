# GitHub Multi-Agent Contributor Workflow

[中文](README.md) | English

A multi-agent contributor solution for GitHub repositories: let Codex, Claude, and other verifiable agents/bots appear on the Contributors page with traceable co-author identities, backed by daily automated check-ins and real PR collaboration.

## Core capabilities

| Capability | Description | Human review |
| --- | --- | --- |
| 🔁 Scheduled check-in | Append a transparent daily activity record with configured co-author trailers | Not required by default |
| 🤝 Real PR collaboration | Agents implement development, docs, or tests on isolated branches and merge via PR | Decide by risk |
| 📦 One-command install | Any agent installs the contributor kit into a target repository with one command | Confirm on merge |

## Quick start (add contributor identities to any repository)

Any agent (Codex / Claude Code / Gemini CLI / Cursor, etc.) can run this inside the target repository:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/academic-door/github-multiagent-contributor/main/scripts/fetch-kit.sh)
python scripts/build_contributors.py --apply --tools codex,claude,renovate
```

The first command installs the kit (public raw URL, no login required); the second creates a branch, writes `Co-Authored-By` trailers, and commits, then pushes and opens a PR. Once merged, the identities appear on the Contributors page.

> Prerequisite: the agent must be authenticated to GitHub (able to push branches / open PRs). Identity emails must be real, GitHub-recognized agent/bot identities; forging is forbidden.

### Let your agent do it

Do not want to type the commands yourself? Just tell any agent session (Codex / Claude Code / Gemini CLI / Cursor):

> Use https://github.com/academic-door/github-multiagent-contributor to add codex, claude and renovate as contributors to `<target repository>`.

`codex, claude, renovate` is just an example — **any one or any combination works**, e.g. "add codex", "add codex and renovate", or "add all the bots from the catalog". The count is up to you.

The agent will: download the kit → `--apply` to create a branch with trailers → push the branch → open a PR. You only confirm before the merge.

## Identity catalog

[contributor-catalog.md](docs/contributor-catalog.md) lists two **verified** identity classes (35 in total):

- ✅ **GitHub-registered AI identities**: codex, claude — trailers count on the page.
- 🤖 **Real GitHub bot accounts** (33): dependabot[bot], renovate[bot], mergify[bot], etc. — emails resolve to real accounts, so they always appear.

The selection script `scripts/build_contributors.py` supports any combination:

```text
python scripts/build_contributors.py --list                    # list all identities
python scripts/build_contributors.py --tools codex,renovate    # pick any combination
python scripts/build_contributors.py --bots                    # all real bot accounts
python scripts/build_contributors.py --all                     # all identities
python scripts/build_contributors.py --remove --tools renovate # remove an identity (stop future use)
python scripts/build_contributors.py --check --tools codex     # verify presence in recent commits
```

Co-author trailers are attribution only and do not claim the tool actually participated in every commit. This repository verified **42 identities** on the Contributors page; full findings are in the [verification report](docs/verification-report.md).

## Scheduled check-in (daily transparent record)

When enabled, GitHub Actions runs once a day (00:17 Asia/Shanghai, dual-cron fallback):

```text
Scheduled run
→ Update activity/agent-checkins.csv (at most one record per date)
→ Create an automated commit
→ Add configured Co-Authored-By trailers
→ Record the commit on the default branch
```

Repository variables:

```text
AGENT_CHECKIN_ENABLED=true
AGENT_CHECKIN_AUTHORS=Codex <noreply@openai.com>;Claude <noreply@anthropic.com>
```

- The default in this repository is Codex, Claude and the two maintainers; other repositories should set `AGENT_CHECKIN_AUTHORS` to their own identity set (semicolon-separated).
- GitHub Actions must be allowed to write to the default branch.
- GitHub scheduled runs are occasionally skipped: if no record appears, trigger **Run workflow** manually on the Actions page (CSV is deduplicated by date).

See [Scheduled Agent Check-in](docs/scheduled-agent-checkin.md).

## Real PR collaboration

```text
Issue defines the goal and acceptance criteria
→ Agent creates an isolated branch
→ Agent changes code, documentation, or tests
→ Pull Request is opened
→ GitHub Actions run checks
→ Review is required when risk warrants it
→ Maintainer confirms and merges
```

Routine maintenance can be handled directly by the maintainer. Require human or agent review for major features, architecture changes, data changes, and releases.

## Apply to an existing repository

- **Contributor identities only**: use the one-command quick start above; no need to copy the whole template.
- **Full collaboration flow**: for Issue→PR→CI→review, additionally copy `AGENTS.md`, Issue/PR templates, `tests.yml`, the email/hygiene gate scripts and `tests/`.

## Contributor attribution

Contributors are derived from commit authorship reaching the default branch:

- Agent-authored commits can use the agent's real author identity;
- Human-mediated commits may carry a genuine `Co-Authored-By` trailer;
- GitHub Apps and Bots can appear under their real identity when they commit;
- Issues, comments, reviews, and Actions runs do not create Contributors by themselves.

The Contributor graph is an attribution result, not a substitute for tests, review, or human risk decisions.

## Privacy and security

This project contains no tokens, passwords, private data, or personal email addresses. Before enabling it in a public repository:

- Enable GitHub email privacy;
- Keep commit-email checks passing;
- Limit agents to explicitly authorized repository content;
- Do not assume cloud agents can access local data, PDFs, desktop applications, or private environments;
- Keep research, privacy, and release decisions with the maintainer.

## License

Released under the [MIT License](LICENSE). Retain the license notice when copying or adapting this workflow.
