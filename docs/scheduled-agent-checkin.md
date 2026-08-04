# Scheduled Agent Check-in

本功能是可选的每日连续性记录。它会追加 `activity/agent-checkins.csv`，并在提交尾注中记录配置的 Agent 身份。记录明确标注为自动 check-in，不代表当天发生了实质性代码开发。

## 开启

在目标仓库的 **Settings → Secrets and variables → Actions → Variables** 中设置：

| 变量 | 值 |
| --- | --- |
| `AGENT_CHECKIN_ENABLED` | `true` |
| `AGENT_CHECKIN_AUTHORS` | `Codex <noreply@openai.com>;Claude <noreply@anthropic.com>;...` |

- 本仓库默认身份为 Codex、Claude 与两位维护者；**其他仓库请把 `AGENT_CHECKIN_AUTHORS` 设为你们自己的身份组合**（英文分号分隔，可含 `[bot]` 名字）。
- 可选维护者提交变量：`GIT_AUTHOR_NAME`（默认 `github-actions[bot]`）、`GIT_AUTHOR_EMAIL`（默认 `41898282+github-actions[bot]@users.noreply.github.com`）。

## 运行方式

- 每天 **00:17**（Asia/Shanghai）定时运行，另设 **08:17** 兜底（GitHub 定时偶发跳跑）；实际提交通常约 01:15 落盘。
- 也可在 Actions 页面手动 **Run workflow**。
- CSV 按日期去重：每天最多生成一条记录、一个提交；补跑不会重复。

## 分支保护前提

工作流需要向默认分支写入。如果默认分支要求所有变更必须经过 PR，定时直推会失败。可选方案：

- 为 `github-actions[bot]` 配置绕过权限；
- 允许该工作流直接推送；
- 或关闭“必须通过 PR”但保留 CI 检查。

不要为了本功能关闭邮箱门禁；默认提交邮箱使用 GitHub Actions 的 noreply 地址。

## 署名边界

`AGENT_CHECKIN_AUTHORS` 只应填写真实、已注册且允许用于署名的 Agent / Bot 身份；不要伪造邮箱。自动 check-in 是透明的连续性记录，不应描述为 Agent 当天完成了代码、研究或审查。真实任务仍应通过 Issue、分支、PR、CI 和 Review 记录。

## 关闭

将 `AGENT_CHECKIN_ENABLED` 改为 `false` 或删除该变量即可停止定时提交。
