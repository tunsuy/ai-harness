# Playbook: 示例 —— 新增功能（请改成真实 golden path）

> 这是 scaffold 示例。换成「唯一样板文件 + 方法形状」的真实步骤。  
> **入口**：非微改前先走 `define-feature`（Brief `approved`）与 DoR；合入前走 `accept-feature`。

## Golden path

1. 确认 `docs/features/<id>/brief.md` 为 `approved`（否则先 `TASK=define-feature`）
2. `make context-pack TASK=example-add-feature DOMAIN=<域>`
3. 打开域 `exemplar` 与 `docs/architecture.md` 对应行
4. 按项目分层约定实现（在此写清：改哪些层、禁改哪些）；**不改** Brief AC
5. 更新 handoff → `make wip-save MSG="…"`
6. `make check-harness` + 项目 lint/test/smoke
7. 交 `accept-feature`（本 playbook 不算产品准出完成）

## 完成自检

- [ ] 未先全库探索
- [ ] 域元数据仍准确（必要时 `kb-gen`）
- [ ] 工程 Verify 勾选完成
- [ ] 已交接 Accept（或 handoff Next 写明）