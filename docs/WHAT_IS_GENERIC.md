# 什么进公共包，什么留在项目里

## 进 `ai-harness`（引擎）

| 能力 | 形态 |
|------|------|
| 指导 + 门禁双轨叙事 | 框架 ADR + AGENTS 骨架 |
| 域元数据 SSOT + 冷启动反探索 | `domains.yaml` / `tasks.yaml` schema + `kb_sync.py` |
| 会话交接 + git WIP | `handoff.md` + `handoff.sh` + `wip-save.sh` |
| Agent 硬拦适配 | `policy_lib` + Cursor/Claude/Codex/Antigravity hooks（含 repo-root 解析） |
| 产品流水线 skills | `.agents/skills/` + `.claude/skills/`：`product-brief` / `product-accept` / `product-prototype` |
| UI skill 推荐包 | scaffold `skills-lock.json` + `make skills-ui`（`npx skills experimental_install`）；不整包 vendoring |
| 冷启动 Always-On | `.cursor/rules` + `.agents/rules`（含默认 `pr-merge`） |
| 失败回流 | playbook `harness-feedback.md` |
| 产品流水线（定义/验收） | `docs/PRODUCT_PIPELINE.md` + scaffold `define-feature` / `accept-feature` + `docs/features/_TEMPLATE/` |
| 产品机械门禁 | scaffold `kb_sync.py`：`check`（Brief/ADR 抢跑、handoff.task）/ `check-ship`（Accept PASS）；零依赖 YAML fallback |
| 合入闸 | `pr-merge.sh` + hooks 禁裸 `gh pr merge`；合入后 handoff 复位 idle |
| UI 原型模板 | `_TEMPLATE/prototype.md` + `_accept-checklist.md` 骨架 |
| 设计参照库 | `docs/design/references/`（取法 + stripe 样例）；项目 `DESIGN.md` 骨架 |
| 可配置禁写 | `docs/harness/policy.yaml` |
| Make 目标 | `Makefile.harness.mk`（含 `check-ship` / `pr-merge`） |
| stale handoff | `handoff.sh` + session-start：main 上 `status: active` 警告 |

## 留在每个项目（填充物）

| 内容 | 为何 |
|------|------|
| `invariants.md` 业务硬约定 | 金额、密钥、拓扑因产品而异 |
| `domains.yaml` 真实域 | 归属与表是产品知识 |
| 业务 playbook | HOW 绑定样板文件 |
| `docs/product-pipeline.md` 附录 | 风险分层 S 的业务定义、准出命令；scaffold 提供空模板 |
| `docs/features/<id>/` | 具体 Brief / Accept 工件 |
| 语言/栈门禁 | golangci、depguard、DDL 检查 |
| 行为 smoke / `ci-smoke` | 断言产品链路，不是 harness 本身 |
| `policy.yaml` 里的只读树 | 如某仓的 `vendor/`、生成物目录 |
| `docs/design/DESIGN.md` 与页模板 | 色板/气质/壳是产品填充物；引擎只给骨架 + 参照库取法 |
| 第三方 UI skills 的**源码树** | 由 `skills-lock` + `make skills-ui` 还原；引擎只锁版本不默认提交大树 |

## 约定

1. **scaffold 默认 `conventions.mode: metadata_only`**：只强制 exemplar / 域表同步 / 任务路径；不假设 Go console 布局。
2. 需要 TokenStore 式「文件名=域名」时，在项目里扩展 `kb_sync.py` 或参考 `examples/`。
3. `ai-harness upgrade`（规划）只更新引擎文件清单，永不覆盖 `domains.yaml` / `invariants.md` / `handoff.md`。
