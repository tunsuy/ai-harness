# docs/harness — 知识库与 harness 运行时

| 文件 | 角色 |
|------|------|
| `invariants.md` | 硬约定全文（AGENTS 只索引） |
| `domains.yaml` | 域元数据（约定推导归属） |
| `tasks.yaml` | 任务 → playbook / must_read（含 `define-feature` / `accept-feature`） |
| `policy.yaml` | agent hooks 禁写策略 |
| `handoff.md` | 意图 / Next（可标 `phase: define\|design\|build\|accept`） |
| `handoff.template.md` | 收工重置 |

产品定义/验收工件在 `docs/features/`；流水线说明见引擎 `docs/PRODUCT_PIPELINE.md`。

```bash
make handoff
make context-pack TASK=resume
make wip-save MSG="…"
make kb-gen && make check-harness
```
