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

## 开工（新任务）

1. `git checkout -b ai/<主题>`（或 `feat/<主题>`），勿在 main 上堆 WIP。
2. handoff：`status: active`、task/domain/goal、有序 Next。
3. `make context-pack` → 写代码。
4. 阶段性：`make wip-save MSG="domain: 做完了什么"`。

## 收工

1. Verify 打勾；需要则正式 commit（可整理多个 `wip:`）。
2. handoff → `idle`（可参考 `handoff.template.md`）。
3. 知识变更走 maintain-knowledge；开 PR。

## 禁止

- ❌ 只靠聊天说「下次继续」
- ❌ 在 main 上 `wip-save`
- ❌ 续作时丢开 handoff / 最近 wip 重新全库探索
- ❌ 把密钥写进 handoff 或 commit
