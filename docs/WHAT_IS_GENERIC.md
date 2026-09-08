# 什么进公共包，什么留在项目里

## 进 `ai-harness`（引擎）

| 能力 | 形态 |
|------|------|
| 指导 + 门禁双轨叙事 | 框架 ADR + AGENTS 骨架 |
| 域元数据 SSOT + 冷启动反探索 | `domains.yaml` / `tasks.yaml` schema + `kb_sync.py` |
| 会话交接 + git WIP | `handoff.md` + `handoff.sh` + `wip-save.sh` |
| Agent 硬拦适配 | `policy_lib` + Cursor/Claude/Codex/Antigravity hooks |
| 失败回流 | playbook `harness-feedback.md` |
| 可配置禁写 | `docs/harness/policy.yaml` |
| Make 目标 | `Makefile.harness.mk` |

## 留在每个项目（填充物）

| 内容 | 为何 |
|------|------|
| `invariants.md` 业务硬约定 | 金额、密钥、拓扑因产品而异 |
| `domains.yaml` 真实域 | 归属与表是产品知识 |
| 业务 playbook | HOW 绑定样板文件 |
| 语言/栈门禁 | golangci、depguard、DDL 检查 |
| 行为 smoke / `ci-smoke` | 断言产品链路，不是 harness 本身 |
| `policy.yaml` 里的只读树 | 如某仓的 `vendor/`、`sub2api/` |

## 约定

1. **scaffold 默认 `conventions.mode: metadata_only`**：只强制 exemplar / 域表同步 / 任务路径；不假设 Go console 布局。
2. 需要 TokenStore 式「文件名=域名」时，在项目里扩展 `kb_sync.py` 或参考 `examples/`。
3. `ai-harness upgrade`（规划）只更新引擎文件清单，永不覆盖 `domains.yaml` / `invariants.md` / `handoff.md`。
