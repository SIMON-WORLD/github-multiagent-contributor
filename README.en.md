# GitHub Agent Contributor Workflow

[中文](README.md) | English

A reusable GitHub workflow for involving Codex, Claude, and other verifiable agents in repository work, automated checks, Pull Requests, and attributable Contributor records.

This project provides two complementary modes:

| Mode | Purpose | Human review |
| --- | --- | --- |
| Scheduled check-in | Append a transparent daily activity record with configured agent co-authors | Not required by default |
| Real PR collaboration | Let an agent implement code, documentation, or tests on an isolated branch and merge through a Pull Request | Decide by risk |

## Scheduled check-in

When enabled, GitHub Actions runs:

```text
Scheduled run (once a day, 00:17 Asia/Shanghai)
→ Update activity/agent-checkins.csv (at most one record per date)
→ Create an automated commit
→ Add configured Co-Authored-By trailers
→ Record the commit on the default branch
```

This records automation activity; it does not claim that an agent completed substantive development or research that day. It is disabled by default.

Repository variables:

```text
AGENT_CHECKIN_ENABLED=true
AGENT_CHECKIN_AUTHORS=Codex <noreply@openai.com>;Claude <noreply@anthropic.com>
```

- The default in this repository is Codex, Claude and the two maintainers; **other repositories should set `AGENT_CHECKIN_AUTHORS` to their own identity set** (semicolon-separated).
- GitHub Actions must be allowed to write to the default branch. Each identity email must belong to a real, GitHub-recognized agent or bot identity. Do not forge addresses.
- Note: GitHub scheduled runs are occasionally skipped. If no record appears for the day, open the `Scheduled Agent Check-in` workflow on the Actions page and click **Run workflow** (the CSV is deduplicated by date, so no duplicates).

See [Scheduled Agent Check-in](docs/scheduled-agent-checkin.md).

## Verified co-author catalog (optional)

To add more identities to the Contributors page, use the [contributor catalog](docs/contributor-catalog.md) and the [selection script](scripts/build_contributors.py):

```text
python scripts/build_contributors.py --list                  # list all identities
python scripts/build_contributors.py --tools codex,renovate  # pick a subset
python scripts/build_contributors.py --bots                  # all real bot accounts (always show)
python scripts/build_contributors.py --all --commit-message "feat: x"  # generate a commit message with trailers
```

Identities are split into two groups (verified in this repository):

- **Group A**: codex, claude (GitHub-registered AI identities; trailers count on the page).
- **Group C**: 33 real GitHub bot accounts (e.g. dependabot[bot], renovate[bot], mergify[bot]; emails resolve to real accounts, so they always appear).

Append the generated `Co-Authored-By:` lines to a commit and merge it into the default branch. This is attribution only and does not claim the tool actually participated in every commit. This repository reached 42 identities on the Contributors page; full findings are in the [verification report](docs/verification-report.md).

## Real PR collaboration

Use this mode for substantive development, fixes, and documentation:

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

**Existing repositories do not need the whole template.** Copy the pieces you need:

```text
docs/contributor-catalog.md        # identity catalog (choose which identities)
docs/verification-report.md        # verification findings (optional reference)
scripts/build_contributors.py      # identity selection script
.github/workflows/scheduled-agent-checkin.yml   # daily check-in (optional)
docs/scheduled-agent-checkin.md    # check-in docs (optional)
```

Then:

1. Use `build_contributors.py` to choose identities, put the trailers in a commit and merge it into the default branch (one-off).
2. Optional: add `scheduled-agent-checkin.yml`, set `AGENT_CHECKIN_ENABLED=true` and `AGENT_CHECKIN_AUTHORS` to carry the identities daily.
3. Refresh the Contributors page to verify.

Repositories that also want the full agent collaboration flow (Issue→PR→CI→review) can additionally copy `AGENTS.md`, Issue/PR templates, `tests.yml`, the email/hygiene gate scripts and `tests/`.

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
