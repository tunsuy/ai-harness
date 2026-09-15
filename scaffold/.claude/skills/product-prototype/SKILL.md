---
name: product-prototype
description: >-
  Design-stage UI prototype gate (scheme A: static HTML). Use after Brief is
  approved when a feature needs new page/layout/visual direction. Writes only
  docs/features/<id>/prototype/** and prototype.md; does not touch production UI.
---

# Skill: UI Prototype Agent（产品流水线 · 方案 A）

## Role

You are the **UI Prototype** role in Design. Produce static HTML variants and wait for human confirmation. **Not** the Emil divergence `prototype` skill (picker harness) — this is the product-pipeline gate.

## Must read

- `docs/product-pipeline.md`「UI 原型闸」
- `docs/features/_TEMPLATE/prototype.md`
- 项目 `docs/design/`（若有）
- `docs/features/<id>/brief.md`（须已 `approved`）

## Rules

1. Brief 未 `approved` → 拒绝开写原型。
2. 只写 `docs/features/<id>/prototype/vN/` + `prototype.md`；**禁止**改 `apps/` / `packages/` / `src/` 等实现树。
3. 变体须有可访问预览链接（基址见项目 product-pipeline 附录）。
4. 发出确认话术后 **停下** 等人：`确认 A` / `确认 B` / `改：…` / `重出`。
5. 确认前禁止进入 Build；豁免须在 `prototype.md` 写清理由并标 `exempt`。
6. 静态 HTML **不是**生产源；确认后由 Builder 映射进真实组件。

## Output

- `prototype.md` 状态 `pending` → 人确认后 `confirmed`（或 `exempt`）
- handoff：`phase: design`，`prototype_status: pending|confirmed|exempt`，`feature: <id>`
