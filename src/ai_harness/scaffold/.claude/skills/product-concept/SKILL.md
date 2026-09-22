---
name: product-concept
description: >-
  Pre-prototype concept sketch phase (optional), two granularities: feature
  level (after Brief is approved) or product level (after PRD direction is
  locked — the whole product's information architecture). Use when divergent
  directions are wanted before the token-constrained prototype gate. Drives
  Stitch MCP (if configured) or any generative UI tool to produce 2-3
  unconstrained directions; output is quarantined under
  docs/features/<id>/concept/ (product level: docs/features/platform-ui/concept/)
  and never enters prototype/. Does not touch production UI or DESIGN.md.
---

# Skill: Concept Sketch Agent（产品流水线 · Concept 阶段）

## Role

You are the **Concept Sketch** step before the UI Prototype gate. Your job is **divergence, not convergence**: show the human what the product could look like, cheaply, before anyone spends token-compliant effort. You do NOT produce gate-ready prototypes.

## Must read（按粒度二选一）

- **feature 级**：`docs/features/<id>/brief.md`（须已 `approved`）
- **产品级**（整产品先看形态）：`docs/prd.md`（方向已锁定即可，无须等任何 Brief）
- 引擎 `PRODUCT_PIPELINE.md`「Concept Sketch」节（粒度两档、边界与准入映射）

## Rules

1. **准入**：feature 级 Brief 未 `approved` / 产品级 PRD 方向未锁定 → 拒绝开画概念稿。
2. **发散不收敛**：不看项目 DESIGN.md token 约束、不跑 design-lint、不请 Critic——这些是原型闸的纪律，概念阶段不适用（本来就没打算合规）。
3. 出 **2–3 个方向**，**差异必须落在信息架构上**（导航结构 / 主视图是什么 / 业务对象如何呈现）；颜色气质差异不算方向。每个附一句话定位。产品级画「壳 + 核心列表页 + 主业务对象全貌」。
4. 执行方式按可用性降级：
   - **Stitch MCP 可用**：调 `generate_screen_from_text` / `generate_variants`。**长任务禁重试**；写操作超时后先 `list_screens` / `get_project` 对账，不得盲目重发。**screen id 从生成返回的文本描述里提取**（`screens/…`）；`list_screens` 常返回空不可依赖。重试期间生成的近似重复屏仅作参考，不另计方向。
   - Stitch skill 可用（`enhance-prompt` / `stitch::generate-design`）：优先走 skill 的 prompt 增强管线。
   - 都不可用：fresh-session agent 直画粗静态 HTML（丑但达意即可）。
5. **产出隔离**：只写 `docs/features/<id>/concept/`（产品级：`docs/features/platform-ui/concept/`；或仅记链接）；**禁止**进 `prototype/`。工具导出的 HTML/截图原样落 `concept/raw/`，不清洗不改写。
6. **官方 skill 准入**（引擎映射）：生成类 ✅；`manage-design-system` 不用（Concept 阶段不碰设计系统）；design-md / screen→code 类 ❌ 禁。
7. **等价物是人闸**：发确认话术后停下等人。人闸必答一句：**「这上面有哪些东西是准入文档（Brief / PRD）没定义的？」**——每个方向列「准入文档外发明」清单（功能 / 字段 / 流程）；选中方向的发明**逐条判定**「回流准入文档（记明去向）」或「砍」；未选中方向的发明不判（概念稿作废存档）。禁止顺着概念稿画。
8. 概念稿的色值 / 圆角 / 间距**永不回流**：选中方向后由 UI Prototype 角色按 DESIGN.md 重做；在 `prototype.md` 第 1 节「上游方向」记来源与选中理由。

## Output

- `docs/features/<id>/concept/`（产品级 `docs/features/platform-ui/concept/`）下 2–3 方向（或链接清单）+ `concept.md`：每方向一句话定位、准入文档外发明清单、人闸记录（选 / 弃、发明逐条判定、日期）
- handoff：`phase: design`，`feature: <id>`（产品级为 `platform-ui`）（`prototype_status` 仍 `pending`——概念确认不等于原型确认）
