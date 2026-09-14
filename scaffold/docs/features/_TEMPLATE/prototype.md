# UI Prototype: {{FEATURE_TITLE}}

> 状态：`pending` | `confirmed` | `revise` | `exempt`  
> 对应 Brief：`brief.md`  
> 日期：YYYY-MM-DD  
> 方案：**A（静态 HTML）** — 不依赖 OpenDesign

## 1. 是否需要本闸

- [ ] 需要（新页 / 新布局 / 明显视觉方向）
- [ ] 豁免（写明理由）→ 状态改 `exempt`

## 2. 设计约束

- 遵循项目 `docs/design/`（若有）或仓库约定的 DESIGN / UI 规范
- 静态原型不是生产源；确认后由 Builder 映射进真实组件

## 3. 变体

| 变体 | 目录 | 预览链接 | 一句话差异 |
|------|------|----------|------------|
| A | `prototype/v1/` | https://… | |
| B | `prototype/v2/` | https://… | |

```text
docs/features/<id>/prototype/v1/index.html
```

## 4. 协作确认话术

```text
【原型待确认】feature: <id>
链接 A: …
请回复：确认 A | 确认 B | 改：… | 重出
```

## 5. 人闸记录

| 项 | 值 |
|----|-----|
| 结论 | confirmed / revise / exempt |
| 选中变体 | |
| 谁 / 渠道 / 日期 | |
| 补充意见 | |

## 6. Build 交接

- [ ] `confirmed` 或 `exempt`
- [ ] handoff：`phase: build` + `prototype_status: confirmed|exempt`
