# docs/design/

项目视觉与布局规范（**填充物**）。引擎只提供骨架与参照库取法；色板、壳、页模板因产品而异。

| 路径 | 用途 |
|------|------|
| `DESIGN.md` | Token / 气质 / Do·Don't / **质量锚** / **`lint:` 门禁配置**（Google Stitch 兼容；本仓 SSOT） |
| `console-ui.md` 或等价 | 壳与页模板（List / Report / …）——可按产品改名 |
| `references.md` | 本仓「取什么 / 不取什么」摘要（相对 awesome 库） |
| `references/` | 设计参照库：按轮选老师、学模式不搬值；见 [references/README.md](references/README.md) |

## Agent 默认顺序

1. 读本仓 `DESIGN.md`（只许用其中 token）
2. 有新页/重设计 → 按 `references/README.md` 取 1–2 个老师，记录进当轮 `prototype.md`
3. 按页模板写原型 / 实现；禁止散落 hex、禁止把参照品牌色搬进生产
4. 每版写完跑 **Layer-1 门禁**：`node scripts/design-lint.js <原型目录或实现树>`——表外色值/圆角/字号/字重 = error 必须清零；冲突时先改 DESIGN.md（走参照对照 + 记录）再改产物

流水线闸门见 `docs/product-pipeline.md`「UI 原型闸」。
