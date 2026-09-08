# {{PROJECT_NAME}} harness 开场（Always On）

开场三步：

1. 读 `docs/harness/handoff.md`，执行 `make handoff`
2. `make context-pack TASK=… DOMAIN=…`，只读清单；从 Next 续作
3. 禁止先全库盲目探索

阶段结束：更新 handoff + `make wip-save MSG="…"`（仅 `ai/*`|`feat/*`）。

入口：`AGENTS.md`；硬约定：`docs/harness/invariants.md`。
硬拦由 `.agents/hooks.json`（agy CLI）执行；IDE 侧 hooks 可能尚未接线，仍以 CI/check 为准。
