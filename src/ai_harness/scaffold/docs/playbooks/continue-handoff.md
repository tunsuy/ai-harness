# Playbook: 跨会话续作（Handoff + Git WIP）

> **意图** → `docs/harness/handoff.md`；**代码** → 特性分支 git。聊天不是交接物。

## 新会话（续作）

1. **读** `docs/harness/handoff.md`。
2. `make handoff` + `git log --oneline -5`（看最近 `wip:`）。
3. 若 `status: idle` → 开新任务并写入 handoff；切到 `ai/*` 或 `feat/*`。
4. 若 `active|blocked`：
   ```bash
   make context-pack TASK=<handoff.task> DOMAIN=<handoff.domain>
   ```
5. 核对 `git status` / `git diff` 与 Files；**从 Next 第 1 条续作**。
6. 做完一条可验证步骤 → 更新 handoff → **`make wip-save MSG="…"`**。
7. 换会话 / 中断前：更新 handoff + `wip-save`（有脏文件时）。

## 开工（新任务）

1. `git checkout -b ai/<主题>`（或 `feat/<主题>`），勿在 main 上堆 WIP。
2. handoff：`status: active`、task/domain/goal、有序 Next；有 feature 时填 `phase` / `feature` /（有 UI 时）`prototype_status`。
3. `make context-pack` → 写代码。
4. 阶段性：`make wip-save MSG="domain: 做完了什么"`。

## 收工

1. Verify 打勾；需要则正式 commit（可整理多个 `wip:`）。
2. handoff → `idle`（合入后 `pr-merge` 也会尝试自动复位）。
3. 知识变更走 maintain-knowledge。
4. **默认合入 main（站立授权）**：`ai/*`|`feat/*` 任务收工或用户说「合并」时，**直接** push → `gh pr create` → **`make pr-merge PR=<n>`**（脚本内等 CI 全绿再 squash；失败则修再跑），**禁止再问「要不要开 PR / 合不合并」**。禁 force-push / 直推 main / 裸 `gh pr merge`（hooks 硬拦）。

## 禁止

- ❌ 只靠聊天说「下次继续」
- ❌ 在 main 上 `wip-save`
- ❌ 续作时丢开 handoff / 最近 wip 重新全库探索
- ❌ 把密钥写进 handoff 或 commit
- ❌ 收工后反复征求合并许可（默认合并）
