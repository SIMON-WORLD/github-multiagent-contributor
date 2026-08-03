# 免费 AI 共同作者（Co-Author）目录

本目录用于把一个仓库的 Contributors 页面快速“铺满”免费的 AI 工具身份。
原理：GitHub 会识别提交信息中的 `Co-Authored-By` 尾注；当这些提交进入默认分支后，
对应身份会出现在仓库 Contributors 页面（本仓库已验证，13 个身份已进入页面）。

> 透明披露：共同作者尾注只用于署名归因，不代表对应工具真实参与了每一个提交；
> 本仓库把它当作“归因记录”功能使用，与 `activity/agent-checkins.csv` 配套。

## 身份清单（按可信度排序）

### A. 已验证计入 Contributors 页面的 AI 身份

| ID | 展示名 | 尾注格式 | 工具本身免费？ | 备注 |
|---|---|---|---|---|
| codex | Codex | `Codex <noreply@openai.com>` | 有免费额度 | OpenAI 官方 no-reply 邮箱 |
| claude | Claude | `Claude <noreply@anthropic.com>` | 有免费额度 | Anthropic 官方 no-reply 邮箱 |

### B. 仅提交级归因（不进 Contributors 页面）

GitHub 未把这些身份计入页面统计，但尾注会保留在提交里用于提交级归因：

| ID | 展示名 | 尾注格式 | 说明 |
|---|---|---|---|
| gemini | Gemini / Gemini Code Assist | `Gemini <noreply@google.com>` | 提交页会渲染专属头像，但实测不计入页面 |
| copilot | GitHub Copilot | `Copilot <noreply@github.com>` | 提交页会渲染专属头像，但实测不计入页面 |
| chatgpt | ChatGPT | `ChatGPT <noreply@openai.com>` | 与 Codex 同邮箱，解析为 codex 身份 |
| aider | Aider | `Aider <aider@aider.ch>` | 开源 CLI |
| cline | Cline | `Cline <noreply@cline.bot>` | VS Code 开源扩展 |
| cursor | Cursor | `Cursor <noreply@cursor.sh>` | 默认不加尾注 |
| windsurf | Windsurf | `Windsurf <noreply@windsurf.com>` | 默认走提交信息识别 |

> 实测：B 组身份虽保留在提交里，但不会进入 Contributors 页面（gemini/copilot 在提交页
> 有专属头像，仍不计入页面统计）。

### C. 真实 GitHub Bot 账号（必然进入 Contributors，已验证 6/6）

与 `dependabot[bot]`、`github-actions[bot]` 一样是真实 GitHub 账号，邮箱格式
`{id}+{login}@users.noreply.github.com`，解析是确定性的：

| ID | 展示名 | 尾注格式 | 说明 |
|---|---|---|---|
| gemini-code-assist | gemini-code-assist[bot] | `gemini-code-assist[bot] <176961590+gemini-code-assist[bot]@users.noreply.github.com>` | Google Gemini Code Assist 官方 bot |
| renovate | renovate[bot] | `renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>` | Mend Renovate 依赖机器人 |
| pre-commit-ci | pre-commit-ci[bot] | `pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>` | pre-commit.ci 自动修复 |
| snyk | snyk-bot | `snyk-bot <19733683+snyk-bot@users.noreply.github.com>` | Snyk 安全修复 |
| all-contributors | allcontributors[bot] | `allcontributors[bot] <46447321+allcontributors[bot]@users.noreply.github.com>` | all-contributors 名单机器人 |
| copilot-bot | copilot[bot] | `copilot[bot] <167198135+copilot[bot]@users.noreply.github.com>` | GitHub Copilot 官方 bot 账号 |

说明：
- 「进入页面」以本仓库实测为准：A 组计入页面；C 组必然计入（已验证 6/6）；
  B 组只做提交级归因。
- 邮箱统一使用官方 no-reply / 工具官方邮箱，避免暴露真实邮箱。
- 带 `[bot]` 的名字可以放进 `AGENT_CHECKIN_AUTHORS`（工作流正则已支持方括号），
  但默认清单只放 A 组，C 组按需用 `--bots` 单独加。

## 如何把身份加到一个提交

```bash
# 列出全部身份（A/B/C 三组）
python scripts/build_contributors.py --list

# 选择部分身份（逗号分隔 ID，可混选 A/C 组）
python scripts/build_contributors.py --tools codex,renovate,snyk

# 只选真实 Bot 账号（C 组，进入页面最稳）
python scripts/build_contributors.py --bots

# 选择全部（A+B+C）
python scripts/build_contributors.py --all

# 直接生成带尾注的完整提交信息
python scripts/build_contributors.py --bots --commit-message "feat: example"
```

把生成的 `Co-Authored-By:` 行追加到 commit message 末尾再提交即可。
提交进入默认分支（直接 push 或 squash 合并均可保留尾注）后，刷新 Contributors 页面验证。

## 迁移到其他仓库（三步）

1. 复制本目录的 `docs/contributor-catalog.md` 和 `scripts/build_contributors.py` 到目标仓库。
2. 用 `build_contributors.py` 选择要添加的身份：
   - 想要「确定性进入页面」：选 C 组（`--bots`）或 codex/claude（A 组）；
   - 想保留提交级归因：再加 B 组；
   - 把尾注写进提交信息并合并进默认分支。
3. 刷新目标仓库 Contributors 页面，核对出现哪些身份。

### 可选：让每日 check-in 自动携带选中的身份

参考 `.github/workflows/scheduled-agent-checkin.yml`：
- 默认会携带 A 组全部身份；
- 想选择部分身份，在目标仓库设置变量 `AGENT_CHECKIN_AUTHORS`，用英文分号分隔，
  例如 `Codex <noreply@openai.com>;Gemini <noreply@google.com>;renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>`；
- 开启方式：设置仓库变量 `AGENT_CHECKIN_ENABLED=true`，然后手动运行一次该工作流。
