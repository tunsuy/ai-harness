# ADR-003: 会话交接 —— handoff 管意图，git WIP 管代码

- 状态：已接受
- 日期：2026-09-08
- 来源：TokenStore ADR-012（框架化）

## 决策

| 轨 | 载体 | 管什么 |
|----|------|--------|
| 意图 | `docs/harness/handoff.md` | goal、Next、Blockers、Verify |
| 代码 | 特性分支 `wip:` commit | 可 diff / 可回滚快照 |

`wip-save` **仅**允许 `ai/*` | `feat/*`；禁止 main。聊天不是交接物。
