# AGENTS.md

This repository supports cloud-agent collaboration through GitHub Issues, branches, pull requests, CI, and human review.

## Core Rule

Agents must not push directly to `main`. Create a branch, make scoped changes, open a pull request, and wait for review.

## Standard Workflow

1. Read the linked Issue first.
2. Confirm the allowed files and constraints.
3. Create a branch from `main`.
4. Implement the smallest change that satisfies the acceptance criteria.
5. Run relevant tests.
6. Open a pull request using the repository PR template.
7. Do not merge your own PR unless the maintainer explicitly asks.

## Scope Control

Agents may modify only files allowed by the Issue or the maintainer prompt.

If a needed change is outside the allowed scope, explain the reason in the PR and stop before making that change.

## Privacy Rules

Never commit:

- API keys, tokens, passwords, cookies, or session data
- personal email addresses
- local absolute paths
- private research data
- unpublished datasets
- credentials for Codex, Claude, OpenAI, Anthropic, GitHub, or other services

Use GitHub noreply addresses for commits when possible.

## Authorship Rules

Do not forge another agent's identity.

If Codex, Claude, or another agent is the real author of a commit, it may use its own recognized bot or noreply identity. If a human author made the change, keep the human author.

## Review Rules

Reviewers should check:

- whether the change matches the Issue
- whether tests pass
- whether privacy rules are respected
- whether the PR introduces hidden scope expansion
- whether research claims, data interpretation, or release decisions still need human judgment

## Contributor Identity Self-Serve

Any agent can add, remove, or verify co-author contributor identities with the self-serve script:

- List identities: `python scripts/build_contributors.py --list`
- Add identities (branch + commit with trailers): `python scripts/build_contributors.py --apply --tools codex,claude,renovate`
- Remove identities (from catalog + script): `python scripts/build_contributors.py --remove --tools renovate`
- Verify presence: `python scripts/build_contributors.py --check --tools codex`

Read `docs/add-contributors-with-agent.md` and `docs/contributor-catalog.md` before changing identities.
