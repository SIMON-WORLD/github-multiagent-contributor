# 免费 AI 共同作者（Co-Author）目录

本目录用于把一个仓库的 Contributors 页面快速“铺满”免费的 AI 工具身份。
原理：GitHub 会识别提交信息中的 `Co-Authored-By` 尾注；当这些提交进入默认分支后，
对应 AI 工具身份会出现在仓库 Contributors 页面（本仓库已验证 Codex、Claude 生效）。

> 透明披露：共同作者尾注只用于署名归因，不代表对应工具真实参与了每一个提交；
> 本仓库把它当作“归因记录”功能使用，与 `activity/agent-checkins.csv` 配套。

## 身份清单（按可信度排序）

| ID | 展示名 | 尾注格式 | 工具本身免费？ | GitHub 识别情况 | 备注 |
|---|---|---|---|---|---|
| codex | Codex | `Codex <noreply@openai.com>` | 有免费额度 | ✅ 官方识别（本仓库已验证） | OpenAI 官方 no-reply 邮箱 |
| claude | Claude | `Claude <noreply@anthropic.com>` | 有免费额度 | ✅ 官方识别（本仓库已验证） | Anthropic 官方 no-reply 邮箱 |
| copilot | GitHub Copilot | `Copilot <noreply@github.com>` | ❌ 需 Copilot 付费计划 | ✅ 官方识别（待本仓库验证） | 免费加署名，但实际使用要订阅 |
| chatgpt | ChatGPT | `ChatGPT <noreply@openai.com>` | ✅ 免费 | ✅ 官方识别（待本仓库验证） | 与 Codex 同域，需单独提交展示 |
| gemini | Gemini / Gemini Code Assist | `Gemini <noreply@google.com>` | ✅ 免费额度 | ✅ 官方识别（本仓库已验证） | Google 官方 no-reply 邮箱 |
| aider | Aider | `Aider <aider@aider.ch>` | ✅ 免费（开源） | ⚠️ 社区标准（待验证） | 开源 CLI，可配置自动加尾注 |
| cline | Cline | `Cline <noreply@cline.bot>` | ✅ 免费额度 | ⚠️ 社区标准（待验证） | VS Code 开源扩展 |
| cursor | Cursor | `Cursor <noreply@cursor.sh>` | ✅ 免费额度 | ⚠️ 社区标准（待验证） | 默认不加尾注，仅测试展示 |
| windsurf | Windsurf | `Windsurf <noreply@windsurf.com>` | ✅ 免费额度 | ⚠️ 社区标准（待验证） | 默认走提交信息/文件头识别 |

说明：
- 「GitHub 识别情况」以 GitHub 官方支持与社区观察为准；未经验证的条目合并后需人工
  查看 Contributors 页面确认。
- 付费工具（如 Copilot）也可以免费添加署名身份，本目录保留但标注清楚。
- 邮箱统一使用官方 no-reply / 工具官方邮箱，避免暴露真实邮箱。
- `chatgpt` 与 `codex` 共用 `noreply@openai.com`：同一提交里两者并存时，GitHub 在
  squash 合并时会按邮箱去重（实测只保留 Codex）。想单独展示 ChatGPT，需要单独提交，
  且该提交不要携带 Codex 尾注。

## 如何把身份加到一个提交

```bash
# 列出全部身份
python scripts/build_contributors.py --list

# 选择部分身份（逗号分隔 ID）
python scripts/build_contributors.py --tools copilot,gemini,cline

# 选择全部
python scripts/build_contributors.py --all

# 直接生成带尾注的完整提交信息
python scripts/build_contributors.py --all --commit-message "feat: example"
```

把生成的 `Co-Authored-By:` 行追加到 commit message 末尾再提交即可。
提交进入默认分支（直接 push 或 squash 合并均可保留尾注）后，刷新 Contributors 页面验证。

## 迁移到其他仓库（三步）

1. 复制本目录的 `docs/contributor-catalog.md` 和 `scripts/build_contributors.py` 到目标仓库。
2. 用 `build_contributors.py` 选择要添加的身份，把尾注写进提交信息并合并进默认分支。
3. 刷新目标仓库 Contributors 页面，核对出现哪些身份。

### 可选：让每日 check-in 自动携带选中的身份

参考 `.github/workflows/scheduled-agent-checkin.yml`：
- 默认会携带本目录全部免费身份；
- 若只想保留部分身份，在目标仓库设置变量 `AGENT_CHECKIN_AUTHORS`，用英文分号分隔，
  例如 `Codex <noreply@openai.com>;Gemini <noreply@google.com>;Cline <noreply@cline.bot>`；
- 开启方式：设置仓库变量 `AGENT_CHECKIN_ENABLED=true`，然后手动运行一次该工作流。
