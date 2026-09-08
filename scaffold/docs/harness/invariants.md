# 硬性技术约定（违反即 bug）

> 机器门禁：`make check-harness` + 项目 lint/smoke + **agent hooks**。
> AGENTS.md 只索引本文；新增约定必须同步加检查，只写文档视同没有。

1. **（示例）替换为本项目硬约定** —— 金额、密钥、存储、服务边界等。
2. **知识库**：域元数据只写 `docs/harness/domains.yaml`；禁手改 architecture 域表标记区。
3. **进度**：handoff + `wip-save`（仅 `ai/*`|`feat/*`）；聊天不是交接物。
4. **禁写**：见 `docs/harness/policy.yaml`。
