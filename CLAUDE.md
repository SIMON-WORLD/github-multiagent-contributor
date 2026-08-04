# CLAUDE.md

本仓库支持 Agent 协作（Issue → 分支 → PR → CI → Review → 合并）。

## 核心规则

- 不要直接推 `main`：建分支、做改动、开 PR、等 Review。
- 只改 Issue 或维护者明确允许的文件；不要覆盖已有配置。
- 不提交密钥、Token、个人邮箱、本地绝对路径、私有数据。
- 不伪造其他 Agent 身份；使用 GitHub noreply 或已识别的 bot 身份。

## 贡献者身份自助（共同作者 → Contributors）

给本仓库添加 / 移除 / 验证共同作者贡献者身份时，使用自助脚本：

```bash
# 查看可选身份（A 组：codex/claude；C 组：33 个真实 Bot 账号）
python scripts/build_contributors.py --list

# 添加（自动建分支 + 提交 + 尾注）
python scripts/build_contributors.py --apply --tools codex,claude,renovate

# 移除（从目录与脚本删除，停止再新增）
python scripts/build_contributors.py --remove --tools renovate

# 验证最近 100 提交是否出现该身份
python scripts/build_contributors.py --check --tools codex
```

操作说明见 `docs/add-contributors-with-agent.md` 与 `docs/contributor-catalog.md`。
