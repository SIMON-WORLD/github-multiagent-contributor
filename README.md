# GitHub Agent Workflow Template

中文 | [English](README.en.md)

用于在 GitHub 上建立可审计、可复用的 AI Agent 协作流程。

本模板将任务定义、分支开发、自动检查、代码审查和人工合并组织成统一流程：

```text
Issue 定义目标与验收标准
→ Agent 在独立分支实现
→ Pull Request 提交变更
→ GitHub Actions 自动检查
→ Agent 或人工 Review
→ 维护者确认风险
→ 合并到 main
```

## 适用场景

- 需要让 Codex、Claude 等云端 Agent 参与仓库开发。
- 希望所有 AI 变更都经过分支和 Pull Request，而不是直接修改 `main`。
- 需要在任务开始前明确修改范围、验收标准和隐私边界。
- 希望用 GitHub Actions 自动执行测试、文档检查和提交邮箱检查。
- 需要将同一套协作约定复制到多个软件、研究工具、网站、数据管道或模板仓库。

## 核心能力

- **Issue 模板：** 统一记录目标、背景、允许修改的文件、验收标准和隐私要求。
- **Agent 约定：** 通过 `AGENTS.md` 规定工作范围、验证方式和禁止事项。
- **Pull Request 模板：** 要求提交变更摘要、测试结果、风险说明和隐私确认。
- **自动检查：** 对测试、仓库卫生和提交邮箱执行 GitHub Actions 检查。
- **分支保护：** 可要求 CI 通过、至少 1 次批准并解决全部 Review 对话后才能合并。

## 工作边界

云端 Agent 适合处理仓库内的代码、文档、配置、测试和 Pull Request。它通常无法访问本地设备上的专有数据、桌面软件环境或未上传的私有文件；这类任务应由具备相应本地访问权限的工具完成。无论使用哪种 Agent，业务判断、数据隐私和发布风险都应由维护者最终确认。

本模板不包含任何个人项目、凭据、邮箱、私有数据或本地路径。复制模板后，请根据目标仓库补充项目自身的构建命令和测试命令。

## 快速应用

将下列文件复制到目标仓库：

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

然后按以下顺序使用：

1. 使用 `Agent Task` 模板创建 Issue，写明目标、范围和验收标准。
2. 在 Codex、Claude 或其他云端 Agent 中指定仓库和 Issue 编号，要求从 `main` 创建独立分支。
3. 要求 Agent 只修改 Issue 允许范围内的文件，运行测试并创建 Pull Request。
4. 查看 Pull Request 的 diff、Actions 检查结果和 Review 意见。
5. 由维护者确认代码正确性、研究判断、隐私和发布风险后合并。

更完整的配置说明见 [GitHub Agent 协作流程](docs/github-agent-workflow.zh-CN.md)。

## Contributor 记录

GitHub Contributors 根据进入默认分支的提交作者归属计算。云端 Agent 的代码审查、Issue 评论或 Actions 运行本身不会产生 Contributor 记录。Agent 参与的变更通常以三种方式归属：

- **人类作者：** 人类维护者自己编写并提交的更改，保留人类作者身份。
- **共同作者署名：** Agent 实际编写、经人类账号提交的更改，应在提交信息中添加 `Co-Authored-By` 尾注(例如 `Co-Authored-By: Claude <noreply@anthropic.com>`)。提交进入默认分支后，该 Agent 会显示为共同作者。
- **机器人身份：** 通过 GitHub App 等集成以受认可的 bot 身份直接提交时，该身份可单独出现在 Contributors 中。

无论采用哪种归属方式，Issue、Pull Request、CI 和 Review 记录才是协作流程的核心产物；Contributor 图标只是提交作者归属的副产品，不作为本模板的验收标准。

### 让 Agent 稳定成为 Contributor 的两条前提

共同作者署名能否真正出现在 Contributors 列表，取决于两个容易被忽略的前提：

1. **尾注邮箱必须能对应到一个真实注册的 GitHub 账号。** GitHub 只有在能把 `Co-Authored-By` 的邮箱匹配到某个已注册用户或 bot 时，才会把它计入 Contributors。`Claude <noreply@anthropic.com>` 与 `Codex <noreply@openai.com>` 均已绑定各自的官方身份，可直接使用；随意编写的邮箱不会产生任何 Contributor，只会留下一行无归属的尾注。请使用 Agent 的真实身份邮箱，不要伪造。

2. **合并前先开启维护者的邮箱隐私，避免个人邮箱污染 `main`。** 当仓库只允许 Squash 合并，或使用 GitHub 的 “Update branch (rebase)” 时，GitHub 可能用维护者 GitHub 档案里的公开邮箱生成新提交。一旦这是个人邮箱，就会进入 `main` 并被 `scripts/check_commit_emails.py` 在后续 PR 中判红。合并前请每位维护者在 GitHub `Settings → Emails` 勾选 **Keep my email addresses private** 与 **Block command line pushes that expose my email**，使所有提交使用 `@users.noreply.github.com` 地址。

复现清单(任意仓库让 Claude 与 Codex 都成为 Contributor)：

- [ ] 复制“快速应用”列出的 9 个文件；
- [ ] 开启分支保护(要求 CI 通过、至少 1 次批准)；
- [ ] 所有真人维护者开启 GitHub 邮箱隐私；
- [ ] 每个 Agent 各让一个带真实身份尾注的提交进入默认分支(`Co-Authored-By: Claude <noreply@anthropic.com>`、`Co-Authored-By: Codex <noreply@openai.com>`)；
- [ ] 全程走 Issue → 分支 → PR → CI → Review → 合并。

## 可选的每日 Agent check-in

如果希望在每个仓库中自动保留 Codex、Claude 等身份的连续性记录，可复制 [Scheduled Agent Check-in](docs/scheduled-agent-checkin.md) 工作流并将 `AGENT_CHECKIN_ENABLED` 设为 `true`。它只追加透明的 `activity/agent-checkins.csv` 记录，并在提交中保留配置的 `Co-Authored-By` 尾注；记录明确标注为自动 check-in，不等同于当天完成了实质性代码或研究工作。默认关闭。启用前请确认 Actions 能向默认分支写入，并保留提交邮箱门禁。

## 许可证

本模板采用 [MIT License](LICENSE)。你可以复制、修改和集成到自己的项目中，并应保留许可证声明。
