# Playbook: 定义 Feature（Define）

> 角色：**Product Brief Agent**。只产出 Brief；不写业务代码、不定技术栈。

## 何时用

- 新功能 / 大改范围 / roadmap 新行进排期前
- 返工根因是「做完了才发现不是用户要的」

## Golden path

1. `make context-pack TASK=define-feature`
2. 读产品定位（roadmap / invariants / 已有 ADR 索引），确认不踩禁区
3. 复制 `docs/features/_TEMPLATE/` → `docs/features/<id>/`
4. 写 `brief.md`：客户结果、谁/场景、成功指标、**非目标**、可测 AC、风险分层
5. 开放问题列清；能自己查的查完再停
6. **停下来等人闸**：概念 + Brief → `approved` 或 `revise`
7. 人闸通过后更新 handoff：`phase: design` 或直接进入 Architect（ADR/task）
8. `make wip-save MSG="brief: <id> draft|approved"`

## 完成自检

- [ ] Brief 状态明确；AC 无「尽量/更好」等不可测词
- [ ] 非目标已写
- [ ] 未改 `services/` / `pkg/` / `apps/` 等实现树
- [ ] 未创建实现 PR（Define 阶段无实现）

## 下一步

- 难逆转 → ADR（Design）
- DoR 齐 → 实现 task 的 Builder playbook
- 模板说明见仓库 `docs/PRODUCT_PIPELINE.md`（引擎）或项目 `docs/product-pipeline.md`
