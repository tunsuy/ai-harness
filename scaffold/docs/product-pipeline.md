# 产品流水线附录（项目填充）

> 通用方案见引擎 `ai-harness` 的 `docs/PRODUCT_PIPELINE.md`。  
> 本文件只写 **本项目填充物**：风险分层、准出命令、UI 原型预览方式、与 roadmap/ADR 的衔接。

## 流程（与通用一致）

```
define-feature → UI 原型确认（若有界面）→（ADR 若需要）→ 实现 task/playbook → accept-feature → make pr-merge
```

| 阶段 | task_id | 人闸 |
|------|---------|------|
| Define | `define-feature` | Brief → `approved` |
| Design | UI Prototype + ADR | 原型 `confirmed`（或 `exempt`）；ADR `已接受`（若开闸） |
| Build | 业务 task | — |
| Accept | `accept-feature` | Ship（S 层必人工勾选） |

`l1-micro`（已知文件的单点微改）可跳过 Brief；碰钱/租户/鉴权等 **不可** 用微改逃避 Accept。

## UI 原型闸（方案 A · 默认）

**不部署 OpenDesign。** Agent 按本仓设计规范写出静态 HTML，发预览链接，人确认后再 Build。

每轮流程（完整版见引擎 `docs/PRODUCT_PIPELINE.md`「UI Prototype Gate」）：

```
组件覆盖检查 → 画变体 → design-lint 每版过闸 → 两段式自评 → Critic（fresh-session） → 预览链接送人闸
```

- **组件覆盖检查**：本页用到的每个组件在项目 `DESIGN.md` 必须有规范行；没有的先补规范（值从参照库对照得出）再画，禁止临场拍值等人闸纠正。
- **design-lint（Layer 1 机械门禁）**：`make design-lint DESIGN_LINT_TARGETS="docs/features/<id>/prototype/vN"`——表外色值/圆角/字号/字重 = error 必须清零；warning 逐条确认有 SSOT 依据。冲突时先改 DESIGN.md 再改原型。
- **两段式自评**：先以第一次打开页面的用户身份看三档截图（1440/1024/375）修掉不适感，再按 DESIGN.md「质量锚」逐条自查。禁止第一稿直接送人闸。

### 设计参照（每轮原型建议）

开写静态 HTML 前：按 [`docs/design/references/README.md`](design/references/README.md) 为当轮问题选 1–2 个老师品牌，把「问题 → 老师 → 学到什么」写进 `prototype.md` 设计约束段。学模式不搬 hex；晋升经验才改本仓 `DESIGN.md`。

### 何时必须 / 可 `exempt`

- 必须：新页、改壳/信息架构、明显布局或视觉方向
- 可豁免：文案 / 色值微调、已知组件内单字段（在 `prototype.md` 写清理由）
- **门面级新页 / 整页重做首轮**：≥2 结构性变体 + 送闸前 **fresh-session Critic 评审**（逐变体按质量锚打分 + 排序 + 最大风险，写 `prototype.md`「评审」节；见引擎「Agent 角色约定」）

### 预览链接（项目填写）

| 项 | 值 |
|----|-----|
| 基址 URL | （例：`https://preview.example/<feature-id>/vN/`） |
| 映射目录 | `docs/features/<id>/prototype/vN/` |
| 鉴权 | |

### 确认口令

```text
确认 A | 确认 B | 改：… | 重出
```

未确认前 Builder **禁止**实现该 feature 的 UI/业务页。

## 风险分层（项目填写）

| 层 | 典型改动 | 准出 |
|----|----------|------|
| **S** | （钱 / 租户 / 鉴权 / 不可逆数据…） | 工程门禁 + AC 证据 + **人审** |
| **A** | （核心业务路径…） | 工程门禁 + AC 证据 |
| **B** | （文案 / 动效 / 纯展示…） | 工程门禁 + 轻量 AC |

永久禁区写在 `docs/harness/invariants.md`；Define 即 kill。

## 工程准出命令（Accept 填写证据时用）

```bash
make check-harness
# 再加项目 build / lint / test / smoke …
```

「lint 绿 ≠ 完成」——行为以项目 smoke 为准。

## DoR（进 Build）

除通用 DoR 外，本项目额外：

- [ ] 与 roadmap 定位一致（若有）
- [ ] `require_adr_accepted` 已在实现 task 上声明（若适用）
- [ ] 有 UI 且未豁免 → `docs/features/<id>/prototype.md` 为 `confirmed`

## 工件位置

- Brief / Accept / Prototype：`docs/features/<id>/`
- 模板：`docs/features/_TEMPLATE/`
- 滚动准出：`docs/features/_accept-checklist.md`

## handoff 约定

```text
phase: define | design | build | accept
feature: <id>
prototype_status: pending | confirmed | exempt   # 有 UI 时必填
```

Accept FAIL → Next 写打回阶段。原型被否 → `phase: design` + `prototype_status: pending`，禁止直接 Build。

## 机械门禁

| 命令 | 闸 |
|------|-----|
| `make check-harness`（含 `kb_sync check`） | Brief/ADR 抢跑 |
| `make check-ship` / `make pr-merge` | Accept PASS |
| `make context-pack` | WARN：未 approved Brief / 提议中 ADR |
| `make design-lint`（Layer 1） | DESIGN.md 表外硬编码值：色值/圆角/字号/字重 = error 阻断；高度/间距/rgba = warning |

> design-lint 的 token 表自动解析自 `docs/design/DESIGN.md` front matter；项目在 `lint:` 块配 `targets`（实现树默认扫描范围）/ `heights` / `baseline`（已知历史漂移，折回后必须删条目）。接入项目 CI 时把 `node scripts/design-lint.js` 放进前端 workflow（纯 node 零依赖，可先于依赖安装跑）。

> 原型闸默认以文档 + handoff 约束；若抢跑成常态，可在 `kb_sync` 加 `require_prototype_confirmed`。
