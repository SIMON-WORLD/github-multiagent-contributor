# 验证报告：共同作者 → Contributors 页面

本报告记录 `github-multiagent-contributor` 仓库关于「用 `Co-Authored-By` 尾注让身份进入 Contributors 页面」的完整实测结论，供迁移到其他仓库时直接参考。

- 验证时间：2026-08-03 ~ 2026-08-04
- 验证仓库：https://github.com/SIMON-WORLD/github-multiagent-contributor
- 最终结果：Contributors 页面 **42 个身份**（截至 2026-08-04 实测；每日 check-in 会持续累计贡献次数）

## 1. 机制原理

GitHub 会解析进入默认分支的提交中的 `Co-Authored-By: Name <email>` 尾注；只要 email 能解析到
「GitHub 已注册的 AI 身份」或「真实 GitHub 账号」，该身份就会计入仓库 Contributors 页面。

```text
提交（含 Co-Authored-By 尾注）
→ 合并/推入默认分支
→ GitHub 聚合（几分钟到 1 小时延迟）
→ 身份出现在 Contributors 页面
```

## 2. 身份有效性实测（结论）

| 分组 | 身份 | 是否进入页面 | 结论 |
|---|---|---|---|
| A | codex（noreply@openai.com）、claude（noreply@anthropic.com） | ✅ | GitHub 官方注册 AI 身份，尾注即生效 |
| C | 33 个真实 GitHub Bot 账号（`ID+login@users.noreply.github.com`） | ✅ 全部 | 邮箱解析到真实账号，必然显示 |
| B（已移除） | Gemini/Copilot 的 noreply 邮箱、ChatGPT、Aider、Cline、Cursor、Windsurf | ❌ | 未注册/同邮箱冲突，不进页面 |

要点：

- `Gemini <noreply@google.com>`、`Copilot <noreply@github.com>` 在提交页有专属头像，但仍**不计入**页面统计。
- `ChatGPT <noreply@openai.com>` 与 Codex 同邮箱，GitHub 解析为 codex 身份，无法独立显示。
- 社区身份（Aider/Cline/Cursor/Windsurf 等）仅作提交级归因，不进页面。
- 真实 Bot 账号必须用官方格式 `{id}+{login}@users.noreply.github.com`（id 用 GitHub users API 核实）。

## 3. 42 个身份构成

- 人类/系统：SIMON-WORLD、ukinch605、github-actions[bot]、dependabot[bot]、web-flow
- A 组 AI：codex、claude
- C 组 Bot（33）：gemini-code-assist[bot]、renovate[bot]、pre-commit-ci[bot]、snyk-bot、
  allcontributors[bot]、copilot[bot]、claude[bot]、cursor[bot]、qodo-merge[bot]、mergify[bot]、
  kodiakhq[bot]、github-merge-queue[bot]、scala-steward、pyup-bot、mend[bot]、greenkeeper[bot]、
  dependabot-preview[bot]、semantic-release-bot、codecov[bot]、github-classroom[bot]、
  github-learning-lab[bot]、first-timers[bot]、request-info[bot]、stale[bot]、todo[bot]、
  welcome[bot]、wip[bot]、hound[bot]、stickler-ci[bot]、release-drafter[bot]、pypi[bot]、
  npm[bot]、octokit[bot]

完整目录见 `docs/contributor-catalog.md`；批量生成尾注用 `scripts/build_contributors.py`（`--bots` 输出全部 33 个）。

## 4. 注意事项

- **页面聚合有延迟**：合并后 Contributors 页面可能几分钟到 1 小时才更新，不是失败。
- **squash 合并保留尾注**：仓库只允许 squash 时，尾注会从分支提交带入合并提交（已实测 6/24/3 条都完整保留）。
- **同邮箱去重**：同一提交里两个身份共用邮箱时，GitHub squash 会按邮箱去重（只保留一个）。
- **定时任务会跳跑**：GitHub 定时 check-in 偶发不触发；工作流已用双 cron 兜底，仍缺失时可手动 Run workflow（CSV 按日期去重）。
- **真实 bot 也分类型**：C 组里部分是合并队列/依赖机器人（会真正提交），部分是评论/检查类（仅作身份展示）；按需选择。

## 5. 迁移到其他仓库（快速版）

1. **一键安装**：`bash <(curl -fsSL https://raw.githubusercontent.com/SIMON-WORLD/github-multiagent-contributor/main/scripts/fetch-kit.sh)`（自动下载 `build_contributors.py` 与 `docs/`）。
2. **选择身份**：`python scripts/build_contributors.py --tools codex,renovate,snyk` 或 `--bots`；自助建分支+提交用 `--apply --tools ...`。
3. 合并进默认分支，刷新 Contributors 页面核对。
4. **想每日自动**：设 `AGENT_CHECKIN_ENABLED=true` 与 `AGENT_CHECKIN_AUTHORS`（自己的身份组合）。
5. **移除 / 验证**：`--remove --tools renovate`、`--check --tools codex`。
