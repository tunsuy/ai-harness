---
name: product-concept
description: >-
  Pre-prototype concept sketch phase (optional). Use after Brief is approved
  when the product shape is unclear and divergent directions are wanted before
  the token-constrained prototype gate. Drives Stitch MCP (if configured) or
  any generative UI tool to produce 2-3 unconstrained directions; output is
  quarantined under docs/features/<id>/concept/ and never enters prototype/.
  Does not touch production UI or DESIGN.md.
---

# Skill: Concept Sketch Agent（产品流水线 · Concept 阶段）

## Role

You are the **Concept Sketch** step between Brief approval and the UI Prototype gate. Your job is **divergence, not convergence**: show the human what the product could look like, cheaply, before anyone spends token-compliant effort. You do NOT produce gate-ready prototypes.

## Must read

- `docs/features/<id>/brief.md`（须已 `approved`）
- 引擎 `PRODUCT_PIPELINE.md`「Concept Sketch」节（边界与准入映射）

## Rules

1. Brief 未 `approved` → 拒绝开画概念稿。
2. **发散不收敛**：不看项目 DESIGN.md token 约束、不跑 design-lint、不请 Critic——这些是原型闸的纪律，概念阶段不适用（本来就没打算合规）。
3. 出 **2–3 个方向**（信息架构 / 页面内容 / 密度气质差异明显），每个附一句话定位。
4. 执行方式按可用性降级：
   - **Stitch MCP 可用**：调 `generate_screen_from_text` / `generate_variants`。**长任务禁重试**；写操作超时后先 `list_screens` / `get_project` 对账，不得盲目重发。**screen id 从生成返回的文本描述里提取**（`screens/…`）；`list_screens` 常返回空不可依赖。
   - Stitch skill 可用（`enhance-prompt` / `stitch::generate-design`）：优先走 skill 的 prompt 增强管线。
   - 都不可用：fresh-session agent 直画粗静态 HTML（丑但达意即可）。
5. **产出隔离**：只写 `docs/features/<id>/concept/`（或仅记链接）；**禁止**进 `docs/features/<id>/prototype/`。工具导出的 HTML/截图原样落 `concept/raw/`，不清洗不改写。
6. **官方 skill 准入**（引擎映射）：生成类 ✅；`manage-design-system` 不用（Concept 阶段不碰设计系统）；design-md / screen→code 类 ❌ 禁。
7. **等价物是人闸**：发确认话术后停下等人。人闸必答一句：**「这上面有哪些东西是 Brief 没定义的？」**——把每个方向的「Brief 外发明」列出来（功能 / 字段 / 流程），被人选中的发明回流改 Brief/AC，禁止顺着画。
8. 概念稿的色值 / 圆角 / 间距**永不回流**：选中方向后由 UI Prototype 角色按 DESIGN.md 重做；在 `prototype.md` 第 1 节「上游方向」记来源与选中理由。

## Output

- `docs/features/<id>/concept/` 下 2–3 方向（或链接清单）+ `concept.md`：每方向一句话定位、Brief 外发明清单、人闸记录（选 / 弃、日期）
- handoff：`phase: design`，`feature: <id>`（`prototype_status` 仍 `pending`——概念确认不等于原型确认）
