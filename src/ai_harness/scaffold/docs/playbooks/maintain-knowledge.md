# Playbook: 维护知识库（SSOT）

> 约定推导归属，**不要**把每个源文件抄进 yaml。

## 何时改 yaml

| 触发 | 改什么 |
|------|--------|
| 新业务域 | `domains:` 加元数据（summary/writer/tables/exemplar） |
| 新任务类型 | `tasks.yaml` + playbook；新功能先 Brief 再挂 `task_id`（勿直接 `brief_exempt`） |
| 产品流水线字段 | `require_brief_approved` / `require_adr_accepted` / `require_accept_pass` / `brief_exempt` |
| 禁写路径 | `policy.yaml` |
| 仅改已有域内约定文件 | **通常不用改 yaml** |

## Golden path

1. 编辑 `docs/harness/domains.yaml`
2. `make kb-gen`
3. 按项目约定落文件；概念变化 → `docs/glossary.md`
4. `make check-harness`

## 冷启动

```bash
make context-pack TASK=example-add-feature DOMAIN=example
```
