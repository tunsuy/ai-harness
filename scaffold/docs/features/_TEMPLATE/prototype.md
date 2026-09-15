# UI Prototype: {{FEATURE_TITLE}}

> 状态：`pending` | `confirmed` | `revise` | `exempt`  
> 对应 Brief：`brief.md`  
> 日期：YYYY-MM-DD  
> 方案：**A（静态 HTML）** — 不依赖 OpenDesign

## 1. 是否需要本闸

- [ ] 需要（新页 / 新布局 / 明显视觉方向）
- [ ] 豁免（理由：纯文案 / 已知组件内单点 / …）→ 状态改 `exempt`，跳过第 3–6 节人闸

## 2. 设计约束（必读后开写）

- 遵循项目 `docs/design/DESIGN.md`（若有）与页模板文档
- 预览基址与发布方式见项目 `docs/product-pipeline.md` 附录（若有）
- **静态原型不是生产源**；确认后由 Builder 映射进真实组件
- **参照记录**（推荐；见 `docs/design/references/README.md`）：

| 问题 | 老师品牌 | 学到什么（模式，非 hex） |
|------|----------|--------------------------|
| | | |

## 3. 变体

| 变体 | 目录 | 预览链接 | 一句话差异 |
|------|------|----------|------------|
| A | `prototype/v1/` | https://… | |
| B | `prototype/v2/` | https://… | |

静态文件约定：

```text
docs/features/<id>/prototype/
  v1/index.html    # 自包含；可内联 CSS
  v2/index.html    # 可选第二方向
```

## 4. 评审（门面级 / 整页重做首轮必填）

> 由 **fresh-session Critic** 在送人闸前填写（不与出稿者共用上下文）；只写本节，不改 HTML、不做顺手修。

| 变体 | 质量锚逐条（过 / 不过 + 定位到段） | 排序 | 最大风险 |
|------|-----------------------------------|------|----------|
| A | ① … ② … ③ … ④ … ⑤ … ⑥ … | | |
| B | | | |

**Critic 结论**：推荐变体 + 一句理由；给落稿者的最优先修改（若有）。

## 5. 协作确认话术（agent 发出）

```text
【原型待确认】feature: <id>
链接 A: …
链接 B: …（若有）
评审：Critic 推荐 <变体>——<一句理由>（详见 prototype.md「评审」节）
请回复：确认 A | 确认 B | 改：… | 重出
```

## 6. 人闸记录

| 项 | 值 |
|----|-----|
| 结论 | confirmed / revise / exempt |
| 选中变体 | A / B / … |
| 谁 | |
| 渠道 | 微信 / … |
| 日期 | |
| 补充意见 | |

## 7. Build 交接

- [ ] 状态已为 `confirmed` 或 `exempt`
- [ ] handoff：`phase: build` + `prototype_status: confirmed|exempt`
- [ ] Builder 按选中变体映射到生产组件（**禁止**把静态 HTML 当生产源直接合入）
