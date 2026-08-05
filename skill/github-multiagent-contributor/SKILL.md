---
name: github-multiagent-contributor
description: Add, remove, or verify multi-agent contributor identities (Codex, Claude, and 33 real GitHub bot accounts) on any GitHub repository, using a verified co-author kit. Use when the user asks to make agents or bots appear as contributors on the Contributors page, to add or remove co-author identities, or to verify them.
---

# GitHub Multi-Agent Contributor

让任意 Agent 用最少配置，为任意 GitHub 仓库添加 / 移除 / 验证「共同作者贡献者」身份（Codex、Claude、33 个真实 Bot 账号）。

## 何时使用

- 用户要求「给某个仓库加 codex / claude / 某 bot 作为 contributor」；
- 添加、移除或验证共同作者贡献者身份；
- 排查「为什么 Contributors 页面没出现某身份」。

## 前提

- Agent 已认证 GitHub，且对目标仓库有推送分支 / 开 PR 权限（合并可由仓库主人确认）。
- 目标环境有 `git` 与 `python3`；套件下载走 public 仓库直连，无需登录。

## 流程

### 1. 一键安装套件（在目标仓库目录内）

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/academic-door/github-multiagent-contributor/main/scripts/fetch-kit.sh)
```

自动下载 `scripts/build_contributors.py` 与 `docs/` 到当前仓库。

### 2. 查看可用身份

```bash
python scripts/build_contributors.py --list
```

两类已验证身份：GitHub 官方注册 AI 身份（codex、claude）+ 33 个真实 Bot 账号（renovate[bot]、mergify[bot] 等）。可任意选择单个或组合。

### 3. 添加身份（自动建分支 + 提交 + 尾注）

```bash
python scripts/build_contributors.py --apply --tools codex,claude,renovate
# 或 --bots（全部 Bot）/ --all（全部身份）；身份数量随意
git push -u origin <分支名>
```

推送后打开 PR；合并（squash 即可）后身份进入 Contributors 页面。

### 4. 移除身份（停止再新增）

```bash
python scripts/build_contributors.py --remove --tools renovate
```

同时从目录与脚本删除该身份；并提醒更新 `AGENT_CHECKIN_AUTHORS`。注意：只影响未来，历史提交仍计入页面。

### 5. 验证

```bash
python scripts/build_contributors.py --check --tools codex,renovate   # 输出 PRESENT / ABSENT
```

## 合并与核验

- 合并用 squash（或保留提交信息），尾注会完整保留（已实测 6/24/3 条）。
- Contributors 页面聚合有延迟（几分钟到 1 小时），刚合并看不到属正常。
- 同一提交内共用邮箱的身份会被 squash 按邮箱去重（如 Codex 与 ChatGPT 同为 noreply@openai.com）。

## 注意事项

- 不伪造身份：只使用目录中 GitHub 能识别的真实邮箱。
- 归因透明：共同作者尾注是归因记录，不代表工具真实参与了每个提交。
- 移除不抹历史：`--remove` 只停止未来新增；从页面抹去历史需重写默认分支（高风险，不推荐）。

## 参考

- 完整操作手册：`docs/add-contributors-with-agent.md`
- 身份目录：`docs/contributor-catalog.md`
- 验证报告：`docs/verification-report.md`
