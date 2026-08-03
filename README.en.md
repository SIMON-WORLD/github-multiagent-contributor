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
Scheduled run
→ Update activity/agent-checkins.csv
→ Create an automated commit
→ Add configured Co-Authored-By trailers
→ Record the commit on the default branch
```

This records automation activity; it does not claim that an agent completed substantive development or research that day. It writes at most one record per date and is disabled by default.

Repository variables:

```text
AGENT_CHECKIN_ENABLED=true
AGENT_CHECKIN_AUTHORS=Codex <noreply@openai.com>;Claude <noreply@anthropic.com>
```

GitHub Actions must be allowed to write to the default branch. Each identity email must belong to a real, GitHub-recognized agent or bot identity. Do not forge addresses. The default carries every free AI co-author identity in the catalog below; set `AGENT_CHECKIN_AUTHORS` to keep only a subset.

See [Scheduled Agent Check-in](docs/scheduled-agent-checkin.md).

## Free AI co-author catalog (optional)

To quickly add more free AI tool identities to the Contributors page, use the [contributor catalog](docs/contributor-catalog.md) and the [selection script](scripts/build_contributors.py):

```text
python scripts/build_contributors.py --list                  # list all identities
python scripts/build_contributors.py --tools copilot,gemini  # pick a subset
python scripts/build_contributors.py --all --commit-message "feat: x"  # generate a commit message with trailers
```

Append the generated `Co-Authored-By:` lines to a commit and merge it into the default branch; the identity then appears on the Contributors page. This is attribution only and does not claim the tool actually participated in every commit.

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

## Apply to another repository

Copy the following components:

```text
AGENTS.md
.github/ISSUE_TEMPLATE/agent-task.yml
.github/pull_request_template.md
.github/workflows/tests.yml
.github/workflows/scheduled-agent-checkin.yml
docs/
scripts/check_commit_emails.py
scripts/check_repository_hygiene.py
scripts/build_contributors.py
tests/
```

Then:

1. Add the target repository's build and test commands.
2. Place `scheduled-agent-checkin.yml` under `.github/workflows/`.
3. Set `AGENT_CHECKIN_ENABLED` and `AGENT_CHECKIN_AUTHORS`.
4. Grant Actions `Contents: write` permission.
5. Run Check-in once and inspect the commit, CSV record, and Contributors.
6. To add more free AI identities, select them with `build_contributors.py` and merge a commit carrying the trailers.
7. Use Issue → branch → PR → CI → review → merge for real tasks.

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
