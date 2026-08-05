# GitHub Multi-Agent Contributor Workflow

中文 | [English](README.en.md)

一套面向 GitHub 仓库的**多智能体贡献者方案**：让 Codex、Claude 及其他可验证的 Agent / Bot，以可追溯的共同作者身份进入 Contributors 页面；并配套每日自动 Check-in 与真实 PR 协作两种模式。

## 核心能力

| 能力 | 说明 | 人工 Review |
| --- | --- | --- |
| 🔁 自动 Check-in | 每日写入一条透明活动记录，携带配置的共同作者尾注 | 默认不需要 |
| 🤝 真实 PR 协作 | Agent 在独立分支完成开发、文档或测试，通过 PR 合并 | 按风险决定 |
| 📦 一键接入 | 任意 Agent 一条命令把贡献者套件装入目标仓库 | 合并时确认 |

## 快速开始（给任意仓库加贡献者身份）

任何 Agent（Codex / Claude Code / Gemini CLI / Cursor 等）都可在目标仓库内执行：

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/academic-door/github-multiagent-contributor/main/scripts/fetch-kit.sh)
python scripts/build_contributors.py --apply --tools codex,claude,renovate
```

第一条命令自动安装套件（public 仓库直连，无需登录）；第二条命令自动创建分支、写入 `Co-Authored-By` 尾注并提交，随后推送并打开 PR；合并后身份即进入 Contributors 页面。

> 接入风格：默认只提交归属记录 CSV（干净，推荐）；需要「自包含」（套件入库、仓库内直接 `--remove` / `--check`）时，给 `--apply` 加 `--commit-kit`。

> 前提：Agent 已认证 GitHub（可推送分支 / 开 PR）。身份邮箱必须是 GitHub 能识别的真实 Agent / Bot 身份，禁止伪造。

### 交给你的 Agent 去实现

不想自己敲命令？在任意 Agent 会话（Codex / Claude Code / Gemini CLI / Cursor）里直接说：

> 用 https://github.com/academic-door/github-multiagent-contributor 这套方案，给 `<目标仓库>` 加 codex、claude、renovate 作为 contributor。

`codex、claude、renovate` 只是示例——**任意一个或任意组合都可以**，例如「加 codex」「加 codex 和 renovate」「把目录里的 bot 都加上」，数量随意。

Agent 会自行完成：下载套件 → `--apply` 建分支并写入尾注 → 推送分支 → 打开 PR。你只需在合并前确认。

## 作为 Skill 使用

本仓库自带可发布 Skill：`skill/github-multiagent-contributor/`（含 `SKILL.md` 与 `agents/openai.yaml`，兼容主流 Agent Skill 格式）。

- **本机安装**：把 `skill/github-multiagent-contributor/` 复制到你的 Agent 的 skills 目录（Codex 用 `.agents/skills/`，Claude Code 用 `~/.claude/skills/`）。
- **发布分享**：可直接把该目录上传到支持 Agent Skills 的平台供他人安装。
- **使用**：安装后，对该 Agent 说「用 github-multiagent-contributor 给 X 仓库加 codex、claude」即可，Agent 会按 skill 指引自动完成。

## 身份目录

[contributor-catalog.md](docs/contributor-catalog.md) 收录两类**已验证**身份（共 35 个）：

- ✅ **GitHub 官方注册的 AI 身份**：codex、claude —— 尾注即计入页面。
- 🤖 **真实 GitHub Bot 账号**（33 个）：dependabot[bot]、renovate[bot]、mergify[bot] 等 —— 邮箱可解析到真实账号，必然进入页面。

选择脚本 `scripts/build_contributors.py` 支持任意组合：

```text
python scripts/build_contributors.py --list                    # 查看全部身份
python scripts/build_contributors.py --tools codex,renovate    # 选择任意组合
python scripts/build_contributors.py --bots                    # 全部真实 Bot 账号
python scripts/build_contributors.py --all                     # 全部身份
python scripts/build_contributors.py --remove --tools renovate # 移除身份（停止再新增）
python scripts/build_contributors.py --check --tools codex     # 验证是否已进入提交
```

共同作者尾注仅作归因，不代表工具真实参与了每个提交。本仓库 Contributors 页面已验证 **42 个身份**，完整结论见 [验证报告](docs/verification-report.md)。

## 自动 Check-in（每日透明记录）

启用后，GitHub Actions 每天运行一次（00:17 Asia/Shanghai，双 cron 兜底）：

```text
定时运行
→ 更新 activity/agent-checkins.csv（每个日期最多一条）
→ 创建自动提交
→ 写入配置的 Co-Authored-By 尾注
→ 贡献记录进入默认分支
```

仓库变量：

```text
AGENT_CHECKIN_ENABLED=true
AGENT_CHECKIN_AUTHORS=Codex <noreply@openai.com>;Claude <noreply@anthropic.com>
```

- 默认身份为本仓库的 Codex、Claude 与两位维护者；其他仓库请用 `AGENT_CHECKIN_AUTHORS` 设置自己的身份组合（英文分号分隔）。
- 需允许 GitHub Actions 写入默认分支。
- GitHub 定时任务偶发跳跑：若当天未见记录，可在 Actions 页面手动 **Run workflow** 补跑（CSV 按日期去重）。

详细说明见 [自动 Check-in 文档](docs/scheduled-agent-checkin.md)。

## 真实 PR 协作模式

```text
Issue 定义目标与验收标准
→ Agent 创建独立分支
→ 修改代码、文档或测试
→ 创建 Pull Request
→ GitHub Actions 自动检查
→ 按风险决定是否 Review
→ 维护者确认并合并
```

日常小修复可由主维护者直接处理；重大功能、架构调整、数据变更与正式发布，建议要求其他 Agent 或人类协作者 Review。

## 应用到已有仓库

- **只加贡献者身份**：使用上文「快速开始」的一条命令即可，无需复制整套模板。
- **完整协作流程**：需要 Issue→PR→CI→Review 全套时，再复制 `AGENTS.md`、Issue/PR 模板、`tests.yml`、邮箱/卫生门禁脚本与 `tests/`。

## Contributor 归属规则

Contributor 来自进入默认分支的提交作者归属：

- Agent 的代码提交可通过其真实作者身份归属；
- 人类账号代提交时，可使用真实的 `Co-Authored-By` 尾注；
- GitHub App 或 Bot 以其真实身份提交时，可单独出现在 Contributors；
- Issue、评论、Review 或 Actions 运行本身不会自动产生 Contributor。

Contributor 图只是提交归属的结果，不应替代代码质量、测试与人工风险判断。

## 隐私与安全

本项目不包含 Token、密码、私人数据或个人邮箱。公开仓库接入前，请确认：

- GitHub 邮箱隐私已开启；
- 提交邮箱检查通过；
- Agent 只访问仓库中明确授权的内容；
- 本地数据、未上传的 PDF、桌面软件和私有环境不会被云端 Agent 自动读取；
- 研究结论、数据隐私与发布风险由维护者最终确认。

## 许可证

本项目采用 [MIT License](LICENSE)。复制或改造时请保留许可证声明。
