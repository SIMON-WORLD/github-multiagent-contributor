# 给 Agent 的操作手册：添加 / 移除 / 验证共同作者贡献者

本文写给**任意编程 Agent**（Codex、Claude Code、Gemini CLI、Cursor 等）阅读。
目标：在**任意 GitHub 仓库**里，用最少配置把「共同作者」身份变成 Contributors 页面的贡献者，
或反过来移除某个身份。

前置条件（仓库内已有本套件）：

```text
scripts/build_contributors.py     # 自助脚本（必须）
docs/contributor-catalog.md       # 身份目录（必须）
```

## 快速开始（三步）

### 1. 查看可选身份

```bash
python scripts/build_contributors.py --list
```

输出两组：
- **A 组**：codex、claude（GitHub 官方注册 AI 身份，尾注即计入页面）
- **C 组**：33 个真实 GitHub Bot 账号（如 renovate[bot]、mergify[bot] 等，必显示）

### 2. 添加身份（自动建分支 + 提交 + 尾注）

```bash
# 选择部分身份
python scripts/build_contributors.py --apply --tools codex,claude,renovate

# 或全部真实 Bot 账号
python scripts/build_contributors.py --apply --bots

# 自定义提交标题
python scripts/build_contributors.py --apply --tools codex,renovate --subject "chore: attribute identities"
```

脚本会：新建分支 `contributor/add-<n>` → 追加 `activity/contributor-attributions.csv` 记录 → 用带
`Co-Authored-By:` 尾注的提交信息提交。随后按脚本提示推送并开 PR：

```bash
git push -u origin <分支名>
```

PR 合并（squash 即可，尾注会保留）后，刷新仓库 Contributors 页面核对。

### 3. 移除身份（停止再新增）

```bash
python scripts/build_contributors.py --remove --tools renovate
```

会同时从 `build_contributors.py` 和 `contributor-catalog.md` 里删除该身份，之后不再被选中。
**还要**把仓库变量 `AGENT_CHECKIN_AUTHORS` 里对应的身份删掉（如果 check-in 在用）。
注意：`--remove` 只影响未来；**历史提交仍会计入 Contributors 页面**，想从页面抹去需重写历史（高风险，不推荐）。

### 验证

```bash
# 检查最近 100 个提交里是否出现某身份（PRESENT / ABSENT）
python scripts/build_contributors.py --check --tools codex,renovate
```

## 通用注意事项（所有 Agent 都适用）

- 合并请用 squash（或保留提交信息的 merge）；squash 会保留尾注（已实测 6/24/3 条都完整）。
- Contributors 页面聚合有延迟（几分钟到 1 小时），刚合并看不到是正常的。
- 同一提交里两个身份共用邮箱时，GitHub squash 会按邮箱去重（如 Codex 与 ChatGPT 同为 noreply@openai.com，只保留一个）。
- 不要伪造身份：只使用目录里列出的、GitHub 能识别的真实邮箱。
- 本仓库还提供 `AGENTS.md` / `CLAUDE.md`，按你的 Agent 类型读对应文件即可；上面的命令在 git + python 环境通用，与具体 Agent 无关。
