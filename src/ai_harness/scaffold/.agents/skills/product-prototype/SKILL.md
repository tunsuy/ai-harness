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
- `docs/design/DESIGN.md`（若有；含「质量锚」与 `lint:` 门禁配置）+ `docs/design/references/README.md`
- `docs/features/<id>/brief.md`（须已 `approved`）

## Rules

1. Brief 未 `approved` → 拒绝开写原型。
2. 只写 `docs/features/<id>/prototype/vN/` + `prototype.md`；**禁止**改 `apps/` / `packages/` / `src/` 等实现树。
3. 若上游有 Concept Sketch（Stitch 等概念工具出的方向，`concept/` 或链接）：原型**重做**该方向（信息架构 / 页面内容），**不临摹其样式值**——色值/圆角/间距一概不回流，一切以 DESIGN.md token 与参照库为准；在 `prototype.md` 第 1 节「上游方向」记录来源。无 Concept 时跳过此条。
3. **开画前组件覆盖检查**：列出本页全部组件，逐个对 DESIGN.md 找规范行——没有规范行的组件**先补规范再画**（值从参照库对照得出，写进 DESIGN.md 并在 prototype.md 记「本轮补规范」）。禁止临场拍值等人闸纠正。
4. 有明显布局/视觉探索时：先按参照库取法选 1–2 个老师，在 `prototype.md` 记录「问题 → 老师 → 学到什么」；**学模式，不搬品牌 hex/字体/logo**。
5. **每版写完必过 Layer-1 设计门禁**：`node scripts/design-lint.js docs/features/<id>/prototype/vN`——error（表外色值/圆角/字号/字重）清零才送闸；warning 逐条确认有 SSOT 依据。lint 与设计决策冲突时**先改 DESIGN.md（走参照对照 + 记录）再改原型**；禁止为过闸往 token 表塞无出处的值。
6. ~~送人闸前两段式自评 / fresh-session Critic~~ **已按 ADR-006 移除**（2026-09-24）：组件覆盖检查 + design-lint 0 error 后直接送闸；第一眼质量由 token 机械闸 + 人闸肉眼把关兜底。**不拍截图不贴图**——人想看效果打开预览链接。
7. 变体须有可访问预览链接（基址见项目 product-pipeline 附录）——链接即人闸材料（ADR-006）。
8. 发出确认话术后 **停下** 等人：`确认 A` / `确认 B` / `改：…` / `重出`。
9. 确认前禁止进入 Build；豁免须在 `prototype.md` 写清理由并标 `exempt`。Build 期不要求配套浏览器 E2E suite（ADR-006）。
10. 静态 HTML **不是**生产源；确认后由 Builder 映射进真实组件。

## Output

- `prototype.md` 状态 `pending` → 人确认后 `confirmed`（或 `exempt`）；自查清单（覆盖检查 / design-lint）逐项勾完；设计约束段含参照记录（若本轮用了老师）
- handoff：`phase: design`，`prototype_status: pending|confirmed|exempt`，`feature: <id>`
