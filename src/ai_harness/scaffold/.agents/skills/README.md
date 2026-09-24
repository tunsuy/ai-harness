# Skills 分层

## 一等公民（进 scaffold git）

产品流水线，所有项目默认有：

| skill | 用途 |
|-------|------|
| `product-brief` | Define |
| `product-concept` | Concept Sketch（可选，Brief 后原型前的无约束发散） |
| `product-accept` | Accept |
| `product-prototype` | 方案 A 静态原型闸 |

路径：`.agents/skills/`（Claude 镜像：`.claude/skills/`）。

## UI 推荐包（lock 还原，不整包 vendoring 进引擎）

第三方 UI / 动效 skill（体积大、上游常变）。脚手架只提交 **`skills-lock.json`** 钉版本；新项目一条命令装齐，**禁止让 agent 重新 Glob/探索找 skill**。

```bash
make skills-ui
# 等价: bash scripts/install-ui-skills.sh
# 底层: npx skills experimental_install
```

当前推荐包（与 TokenStore 验证过的同一把锁）：

- Emil：`animate` / `prototype` / `review-animations` / `improve-animations` / …
- `impeccable`
- `refactoring-ui`
- Stitch 官方：`enhance-prompt` / `stitch::generate-design` / `stitch::manage-design-system`（需先配 Stitch MCP；**准入映射见引擎 PRODUCT_PIPELINE**——design-md / screen→code 类默认禁，不进本锁）

更新某 skill：`npx skills update <name> -y`，再提交新的 `skills-lock.json`。之后 `ai-harness upgrade` 会视项目锁为已漂移，不自动快进（提示手动合并）。

## 不要做的事

- ❌ 每个新项目让 AI「自己找一套 UI skill」
- ❌ 把 impeccable 全文拷进 ai-harness 当默认源码树（用 lock + install）
- ❌ 把业务专用 skill 写进引擎 lock（留在产品仓）
