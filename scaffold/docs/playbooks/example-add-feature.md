# Playbook: 示例 —— 新增功能（请改成真实 golden path）

> 这是 scaffold 示例。换成「唯一样板文件 + 方法形状」的真实步骤。

## Golden path

1. `make context-pack TASK=example-add-feature DOMAIN=<域>`
2. 打开域 `exemplar` 与 `docs/architecture.md` 对应行
3. 按项目分层约定实现（在此写清：改哪些层、禁改哪些）
4. 更新 handoff → `make wip-save MSG="…"`
5. `make check-harness` + 项目 lint/test/smoke

## 完成自检

- [ ] 未先全库探索
- [ ] 域元数据仍准确（必要时 `kb-gen`）
- [ ] Verify 勾选完成
