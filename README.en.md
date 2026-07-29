# GitHub Agent Workflow Template

[中文](README.md) | English

A reusable, auditable workflow for collaborating with AI coding agents on GitHub.

The template organizes task definition, branch-based implementation, automated checks, review, and human approval into one repeatable process:

```text
Issue defines the goal and acceptance criteria
→ Agent implements on an isolated branch
→ Pull Request proposes the change
→ GitHub Actions run automated checks
→ Agent or human reviews the change
→ Maintainer confirms risk
→ Merge into main
```

## Use Cases

- Involving Codex, Claude, or other cloud agents in repository work.
- Requiring every agent change to go through a branch and Pull Request.
- Defining file scope, acceptance criteria, and privacy boundaries before implementation.
- Running tests, repository hygiene checks, and commit-email checks automatically.
- Reusing the same collaboration policy across software, research tools, websites, data pipelines, and templates.

## Included Capabilities

- **Issue template:** records the objective, context, allowed files, acceptance criteria, and privacy requirements.
- **Agent policy:** `AGENTS.md` defines scope, validation, and prohibited actions.
- **Pull Request template:** requests a change summary, test results, risk notes, and privacy confirmation.
- **Automated checks:** GitHub Actions run tests, repository hygiene checks, and commit-email checks.
- **Branch protection:** can require passing CI, at least one approval, and resolved review conversations before merge.

## Scope and Boundaries

Cloud agents are suited to repository-native code, documentation, configuration, tests, and Pull Requests. They generally cannot access proprietary data, desktop environments, or private files that have not been uploaded; use a tool with the required local access for those tasks. Maintainers remain responsible for business decisions, data privacy, and release risk.

This template contains no personal projects, credentials, private data, or local paths. After copying it, add the build and test commands specific to the target repository.

## Quick Start

Copy these files into the target repository:

```text
AGENTS.md
.github/ISSUE_TEMPLATE/agent-task.yml
.github/pull_request_template.md
.github/workflows/tests.yml
docs/github-agent-workflow.zh-CN.md
scripts/check_commit_emails.py
scripts/check_repository_hygiene.py
tests/test_commit_emails.py
tests/test_repository_hygiene.py
```

Then:

1. Create an Issue with the `Agent Task` template.
2. Point Codex, Claude, or another cloud agent at the repository and Issue number, and ask it to create an isolated branch from `main`.
3. Require the agent to stay within the allowed scope, run tests, and open a Pull Request.
4. Inspect the diff, Actions results, and review feedback.
5. Merge only after the maintainer confirms correctness, privacy, and release risk.

See [GitHub Agent Workflow](docs/github-agent-workflow.zh-CN.md) for configuration details.

## Contributor Records

GitHub attributes Contributors from commits that reach the default branch with an author identity associated with a GitHub account. A cloud agent's code review, Issue comment, or Actions run does not by itself create a Contributor record. Agent-assisted changes are typically attributed in one of three ways:

- **Human author:** changes written and committed by a human maintainer keep the human author identity.
- **Co-author trailer:** changes written by an agent but committed through a human account should carry a `Co-Authored-By` trailer (for example `Co-Authored-By: Claude <noreply@anthropic.com>`). Once the commit reaches the default branch, the agent appears as a co-author.
- **Bot identity:** changes committed directly under a recognized bot identity (for example via a GitHub App integration) can appear in Contributors under that identity.

In every case, Issues, Pull Requests, CI, and review records are the primary workflow artifacts; the Contributor view is a by-product of commit authorship and is not an acceptance criterion for this template.

### Two prerequisites for agents to reliably become Contributors

Whether a co-author trailer actually shows up in the Contributors list depends on two easily missed prerequisites:

1. **The trailer email must map to a real, registered GitHub account.** GitHub only counts a `Co-Authored-By` address toward Contributors when it can match the email to a registered user or bot. `Claude <noreply@anthropic.com>` and `Codex <noreply@openai.com>` are each bound to their official identities and can be used directly; an arbitrary made-up email produces no Contributor at all—it just leaves an unattributed trailer. Use the agent's real identity email; never forge one.

2. **Enable maintainers' email privacy before merging, so personal emails do not pollute `main`.** When a repository allows only Squash merges, or when GitHub's “Update branch (rebase)” is used, GitHub may generate a new commit using the maintainer's public profile email. If that is a personal address, it lands on `main` and will fail `scripts/check_commit_emails.py` on the next PR. Before merging, have each maintainer enable **Keep my email addresses private** and **Block command line pushes that expose my email** under GitHub `Settings → Emails`, so all commits use an `@users.noreply.github.com` address.

Reproduction checklist (make both Claude and Codex Contributors in any repo):

- [ ] Copy the 9 files listed under “Quick Start”;
- [ ] Enable branch protection (require passing CI and at least one approval);
- [ ] Turn on GitHub email privacy for every human maintainer;
- [ ] Land one commit per agent on the default branch carrying its real identity trailer (`Co-Authored-By: Claude <noreply@anthropic.com>`, `Co-Authored-By: Codex <noreply@openai.com>`);
- [ ] Run the full Issue → branch → PR → CI → Review → merge cycle.

## License

This template is released under the [MIT License](LICENSE). You may copy, modify, and integrate it into your projects while retaining the license notice.
