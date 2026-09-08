# Playbook: 维护知识库（SSOT）

> 约定推导归属，**不要**把每个源文件抄进 yaml。

## 何时改 yaml

| 触发 | 改什么 |
|------|--------|
| 新业务域 | `domains:` 加元数据（summary/writer/tables/exemplar） |
| 新任务类型 | `tasks.yaml` + playbook |
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
