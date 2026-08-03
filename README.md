# GitHub Agent Contributor Workflow

中文 | [English](README.en.md)

一个可复制到任意 GitHub 仓库的 Agent 协作方案，用于让 Codex、Claude 及其他可验证的 GitHub Agent 参与提交、自动检查和 Pull Request 协作，并在需要时形成可追溯的 Contributor 记录。

本项目包含两种互补模式：

| 模式 | 作用 | 是否需要人工 Review |
| --- | --- | --- |
| 自动 Check-in | 每日写入一条透明活动记录，并保留配置的 Agent 共同作者署名 | 默认不需要 |
| 真实 PR 协作 | Agent 在独立分支完成代码、文档或测试任务，再通过 Pull Request 合并 | 按项目风险决定 |

## 自动 Check-in 模式

启用后，GitHub Actions 按计划运行：

```text
定时运行
→ 更新 activity/agent-checkins.csv
→ 创建自动提交
→ 写入 Codex / Claude 等 Co-Authored-By 尾注
→ 贡献记录进入默认分支
```

它只记录自动化活动，不声称 Agent 当天完成了实质性开发或研究工作。每个日期最多写入一条记录，默认关闭。

启用所需仓库变量：

```text
AGENT_CHECKIN_ENABLED=true
AGENT_CHECKIN_AUTHORS=Codex <noreply@openai.com>;Claude <noreply@anthropic.com>
```

还需要允许 GitHub Actions 向默认分支写入。身份邮箱必须是 GitHub 能识别的真实 Agent 或 Bot 身份；不要伪造邮箱。默认会携带全部免费 AI 共同作者身份（见下方目录）；只想保留部分身份时，用 `AGENT_CHECKIN_AUTHORS` 变量覆盖即可。

详细说明见 [自动 Check-in 文档](docs/scheduled-agent-checkin.md)。

## 免费共同作者目录（可选）

想快速让更多免费 AI 工具身份出现在 Contributors 页面，可以直接使用本仓库的 [免费共同作者目录](docs/contributor-catalog.md) 与 [选择脚本](scripts/build_contributors.py)：

```text
python scripts/build_contributors.py --list                  # 查看全部身份
python scripts/build_contributors.py --tools copilot,gemini  # 选择部分身份
python scripts/build_contributors.py --all --commit-message "feat: x"  # 生成带尾注的提交信息
```

把生成的 `Co-Authored-By:` 行追加到提交信息并合并进默认分支，即可在 Contributors 页面看到对应身份。它只做归因，不代表对应工具真实参与了每个提交。

## 真实 PR 协作模式

适合实际开发、修复和文档任务：

```text
Issue 定义目标与验收标准
→ Agent 创建独立分支
→ 修改代码、文档或测试
→ 创建 Pull Request
→ GitHub Actions 自动检查
→ 按风险决定是否 Review
→ 维护者确认并合并
```

日常小修复可以由主维护者直接处理；重大功能、架构调整、数据变更和正式发布，建议要求其他 Agent 或人类协作者 Review。

## 快速应用到其他仓库

复制以下组件：

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

然后：

1. 根据目标仓库补充测试和构建命令。
2. 将 `scheduled-agent-checkin.yml` 放入目标仓库的 `.github/workflows/`。
3. 设置 `AGENT_CHECKIN_ENABLED` 与 `AGENT_CHECKIN_AUTHORS`。
4. 确认 Actions 具有 `Contents: write` 权限。
5. 手动运行一次 Check-in，再检查提交、CSV 记录和 Contributors。
6. 想添加更多免费 AI 身份时，用 `build_contributors.py` 选择身份并合并一个带尾注的提交。
7. 有真实任务时，使用 Issue → 分支 → PR → CI → Review → 合并流程。

## Contributor 归属规则

Contributor 来自进入默认分支的提交作者归属：

- Agent 的代码提交可以通过真实作者身份归属；
- 人类账号代提交时，可以使用真实的 `Co-Authored-By` 尾注；
- GitHub App 或 Bot 以其真实身份提交时，可以单独出现在 Contributors；
- Issue、评论、Review 或 Actions 运行本身不会自动产生 Contributor。

Contributor 图只是提交归属的结果，不应替代代码质量、测试和人工风险判断。

## 隐私与安全边界

本项目不包含 Token、密码、私人数据或个人邮箱。公开仓库接入前，应确认：

- GitHub 邮箱隐私已开启；
- 提交邮箱检查通过；
- Agent 只访问仓库中明确授权的内容；
- 本地数据、未上传的 PDF、桌面软件和私有环境不会被云端 Agent 自动读取；
- 研究结论、数据隐私和发布风险由维护者最终确认。

## 许可证

本项目采用 [MIT License](LICENSE)。复制或改造时请保留许可证声明。
