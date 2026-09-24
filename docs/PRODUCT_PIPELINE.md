# OPC 产品开发流水线（通用）

> 一人公司 / AI-native 默认流程。工程执行仍走 harness（handoff / playbook / check）；本文件补齐 **定义 → 验收** 两段，减少「能跑但不对味」的返工。

## 一句话

**先写清成功标准，再实现；实现与验收分离；人只守不可逆闸门。**

## 四阶段

```
Define ──► Design ──► Build ──► Accept ──► Learn
  ↑人闸1     ↑人闸2              ↑人闸3
             （可先经 Concept Sketch 选方向；含 UI 原型确认，若适用）
```

| 阶段 | 角色（agent） | 产出物 | 禁止 |
|------|---------------|--------|------|
| **Define** | Product Brief | `docs/features/<id>/brief.md`（PRFAQ-lite） | 写业务代码、定技术栈 |
| **Design** | Spec / Architect + **UI Prototype**（若有界面） | ADR stub（若难逆转）+ `task_id` + playbook 骨架；有 UI 时还有 `prototype.md` + 可访问预览链接 | 实现；Brief 未过闸不动；**原型未确认不得改业务代码** |
| **Build** | Builder（现有 harness） | 按 playbook 实现 + check/smoke | 改 Brief/验收标准；改已确认的原型方向（须回 Design） |
| **Accept** | Acceptance | `docs/features/<id>/accept.md` verdict | 「顺手修」；FAIL 必须打回 Build |
| **Learn** | 任意 → harness-feedback | 更新 accept checklist / invariants / playbook | 只在聊天说「下次注意」 |

## 人闸（不可逆）

1. **概念**：值不值得做（对照产品定位 / roadmap）
2. **Brief**：范围、非目标、验收标准是否可测
3. **UI 原型**（有新页/新布局时）：预览链接确认后再进 Build
4. **Ship**：Accept = PASS 且风险分层要求的人工勾选完成

中间劳动（调研稿、ADR 草稿、原型 HTML、编码、跑测）交给 agent。

## Concept Sketch（可选，Stitch 等概念工具）

> 适用：Brief 通过后、进原型闸**之前**，想先看「产品长什么样」的几个方向（信息架构 / 页面上有什么 / 密度与气质）。也可前移到 Brief 之前当纯想法生成用。**可选增强，不是任何闸的前置条件**（与 OpenDesign 同级待遇）。

**粒度两档**（准入判断）：

- **feature 级**：`docs/features/<id>/brief.md` 为 `approved`——为单个 feature 选形态。画的是该 feature 的页面。
- **产品级**（整个产品先看形态）：`docs/prd.md` 方向已锁定即可（无须等任何 Brief）——为整个产品选信息架构。对象记为 `platform-ui`，产出隔离在 `docs/features/platform-ui/concept/`；画的是壳 + 核心列表页 + 主业务对象的全貌。

**定位：发散，不收敛。** Stitch（或任何 AI 概念生成工具）在**无约束**下天马行空出方向——不看 DESIGN.md、不碰 token、不跑 lint。约束下的收敛是原型闸的事，两件事不压在同一轮：方向没想清前，token 合规的原型画得再好也是白画。**方向差异必须落在信息架构上**（导航结构 / 主视图是什么 / 业务对象如何呈现）；颜色气质差异不算方向。

```
Brief approved ──► Concept Sketch（无约束发散，选方向）
                        ↓ 人闸：选产品形态（不是选样式）
                   Prototype Gate（方案 A，token 约束下重做）
                        ↓ 人闸：确认原型
                   Build
```

三条边界：

1. **产出隔离**：Stitch 产出只放 `docs/features/<id>/concept/`（产品级：`docs/features/platform-ui/concept/`；或仅留链接，不进仓库）；**禁止**进 `prototype/`——整套原型纪律（design-lint / 组件覆盖检查）不为它开豁免，也不适用（本来就没打算让它合规）。静态产出不是生产源，更不是规范来源。
2. **人闸问的是产品形态**：这页面该有什么、不该有什么、信息架构对不对。**必答一句：「这上面有哪些东西是我的准入文档（Brief / PRD）没定义的？」** 概念工具会替你发明功能/字段/流程；人闸对选中方向**逐条判定**——「回流准入文档」或「砍」，发明回流通去须记明（改 Brief/AC、平台壳导航清单等）；**未选中方向的发明不判**（概念稿作废存档）。禁止视觉工具偷偷做产品决策。
3. **选中方向后进原型闸**：原型按项目 DESIGN.md 与 tokens **重做**，不临摹 Stitch 的值（色值/圆角/间距一概不回流）；方向参考记入 `prototype.md` 第 1 节。

**执行方式（Stitch 官方 MCP + skills）**：Stitch 提供官方远程 MCP（`https://stitch.googleapis.com/mcp`，`X-Goog-Api-Key` 认证，key 在 stitch 设置页生成；属用户/项目一次性配置，不进引擎）。Concept 阶段可由 agent 直接驱动 MCP（`generate_screen_from_text` / `generate_variants`），官方 skills 经 `skills-lock` 锁版本引入。**MCP 尖锐边界须知**：生成是长任务且禁重试；写操作超时后先读后写对账，不得盲目重发。**官方 skill 准入映射**：

| 官方 skill | 准入 | 理由 |
|---|---|---|
| `enhance-prompt` / `stitch::generate-design` | ✅ Concept / 原型阶段用 | 本职是出方向与屏幕 |
| `stitch::manage-design-system` | ⚠️ 仅 Build 期辅助（上传项目 DESIGN.md 供 Stitch 消费） | SSOT 在仓库，Stitch 只当消费者 |
| `design-md` / `taste-design` / `extract-design-md` / `stitch::react-components` 等 code 类 | ❌ 默认禁 | 从 Stitch 反向生成 DESIGN.md 违反「值须有参照出处」；screen→code 绕过原型闸 + design-lint |

## UI Prototype Gate（方案 A：静态原型，不依赖 OpenDesign）

> 适用：新页面、改布局/信息架构、明显视觉方向选择。  
> 豁免：纯文案/色值微调、已知组件内单点改（可标 `prototype_exempt`）；碰钱/租户/鉴权的逻辑仍走 Brief+Accept，与原型闸独立。

**默认路径（云端 agent / 微信协作）：**

1. Brief = `approved` 后进入 Design。
2. Agent 只写 `docs/features/<id>/prototype/` 下的**自包含静态 HTML**（可多变体 `v1/` `v2/`），**不改** `apps/` / `packages/` / `services/` 等实现树。
3. **组件覆盖检查**（每轮开画前）：列出本页用到的全部组件（按钮 / 输入框 / 选择器 / 复选框 / 弹窗 / 徽章 / 表格 / …），逐个对项目 `DESIGN.md` 找规范行——**任何没有规范行的组件，必须先补规范再画**：值从 `docs/design/references/` 对照得出、写进 DESIGN.md，并在 prototype.md 记「本轮补规范」清单。禁止先画再等人闸纠正（TokenStore keys v4 教训：控件高度 34px 系临场拍值，SSOT 从未定义，人闸被迫当第一道规范审）。已过覆盖检查的组件后续页面直接继承，不再逐页仲裁。
4. 每版写完必过 **Layer 1 设计门禁**：`node scripts/design-lint.js docs/features/<id>/prototype/vN`——表外硬编码色值 / 圆角 / 字号 / 字重 = error，清零才送闸；高度 / 间距 / rgba = warning，逐条确认有 SSOT 依据。lint 与设计决策冲突时**先改 DESIGN.md（走参照对照 + 记录）再改原型**；禁止为过闸临场拍值、禁止往 token 表塞无出处的值。
5. ~~送人闸前两段式自评 / fresh-session Critic~~ **已按 ADR-006 移除**（2026-09-24，agentory 实测：免 Critic 照走通质量未降；第一眼质量兜底 = design-lint 机械闸 + 人闸肉眼）。**工作流不产截图**（ADR-006）：agent 不拍图不贴图不看图，人想看打开预览链接。
6. 发布可点开的 HTTPS（或内网）预览链接 → 更新 `docs/features/<id>/prototype.md`（状态 `pending`）。
7. 人确认变体（微信口令：`确认 A` / `确认 B` / `改：…` / `重出`）→ `prototype.md` 标 `confirmed` + 选中变体。
8. 再进 Build：按项目 UI 规范与 tokens **重做进生产组件**；静态原型不是生产源。Build 期不要求配套浏览器 E2E suite（ADR-006：行为验证归 ADR-005 分层——开发期走 L0 预览 + 工程门禁，全量回归兜底归 L2 main；「缺 suite」不构成返工项）。

模板：`scaffold/docs/features/_TEMPLATE/prototype.md`（项目可镜像到 `docs/features/_TEMPLATE/`）。

OpenDesign 等外部设计工具为可选增强，**不是本闸前置条件**。

### 工序分级（防一刀切满配；ADR-006 后自评/Critic 列已删）

上述 1–8 为门面级新页的满配工序；**其余改动按下表减配**，agent 不得对低级改动擅自跑满配（多变体是成本）：

| 改动类型 | 组件检查 | design-lint | 变体数 |
|----------|---------|------------|--------|
| 门面级新页 / 整页重做首轮 | ✅ | ✅ | ≥2（概念轮已发散则 1） |
| 普通新页（已知组件组合、无新布局语法） | ✅ | ✅ | 1 |
| 已有页局部改（区块增删、组件内布局） | 按需（用到新组件才查） | ✅ | 1 |
| 文案 / 色值 / 间距微调（不动布局） | ❌ | ✅ | exempt（跳过整轮原型，prototype.md 写理由） |

**不可省的底线**（分级不减配）：

- design-lint 对任何进原型/代码树的 UI 改动必跑（CI 已自动化，零人工成本）
- Brief 未 `approved` 禁止进 Build；碰钱 / 租户 / 鉴权不可用微改逃避 Accept
- 人闸确认不可省——减配的是工序，不是确认本身（exempt 也属于一种人闸结论，需在 prototype.md 记录）

## Feature Brief（PRFAQ-lite）

半页即可。必填：

- 客户结果（新闻稿式一句话）
- 谁 / 场景
- 成功指标（可观察）
- **非目标**（明确不做什么）
- 验收标准 AC（Given/When/Then 或可勾选清单）
- 风险分层（S / A / B）
- 开放问题

模板：`scaffold/docs/features/_TEMPLATE/brief.md`

## 风险分层（准出）

| 层 | 含义 | 准出 |
|----|------|------|
| **S** | 钱、租户隔离、鉴权、不可逆数据 | 工程门禁 + AC 证据 + **人必审** |
| **A** | 核心业务路径 | 工程门禁 + AC 证据；人抽检 |
| **B** | UI 文案、动效、非关键展示 | 工程门禁 + 轻量 AC；可更多自动化 |

项目在 `invariants` / 本仓附录里定义「什么算 S」。

## Definition of Ready（进 Build 前）

- [ ] Brief 人闸通过（状态 `approved`）
- [ ] AC 可测、无歧义，覆盖主路径 + 至少一条异常
- [ ] 非目标已写
- [ ] 若难逆转 / 跨服务 / 碰钱或租户 → ADR `已接受`
- [ ] 有 UI 且未 `prototype_exempt` → `prototype.md` 状态 `confirmed`（含预览链接与选中变体）
- [ ] `tasks.yaml` 有实现 `task_id` + playbook 骨架
- [ ] roadmap（若有）已挂 `task_id`

## Definition of Done（准出 / Ship）

- [ ] 工程：项目约定的 check / lint / test / smoke 绿
- [ ] 产品：`accept.md` 对每条 AC 有证据（命令、路径、日志摘要；不产截图——ADR-006，取证 = 命令输出 / API 直打 / 单测 / 亲测记录）
- [ ] Accept verdict = `PASS`
- [ ] S 层：人感 / 业务勾选完成
- [ ] 文档：roadmap / handoff / glossary 该改的已改
- [ ] 若返工根因可编码 → 开 `harness-feedback` 或更新 accept checklist

## Agent 角色约定

| 角色 | 何时用 | 工具边界 |
|------|--------|----------|
| **Brief** | 新 feature / 大改范围 | 只写 `docs/features/**`；可读定位/roadmap/ADR |
| **Architect** | DoR 中需 ADR 或跨域方案 | 写 ADR / task / playbook；不写业务实现 |
| **UI Prototype** | Design 阶段有界面 | 只写 `docs/features/<id>/prototype/**` + `prototype.md`；挂项目 DESIGN；**开画前组件覆盖检查**（无规范行的组件先补规范）；**每版必过 `design-lint`**（Layer 1，error 清零）；按需用 `docs/design/references/` 选老师并记入 prototype；发预览链接等人确认。~~两段式自评 / Critic~~ 已按 ADR-006 移除；不拍截图 |
| ~~**Critic**~~ | ~~所有送人闸的原型，送闸前~~ | **已按 ADR-006 移除**（fresh-session 评审为纯开销：第一眼质量兜底 = design-lint 机械闸 + 人闸肉眼；agentory 实测免 Critic 照走通质量未降）。项目坚持要评审的，自行在项目附录加回并记 ADR |
| **Builder** | Brief=`approved`、原型已确认（或豁免）、且 DoR 齐 | 现有 playbook；不改 AC；按确认变体落地 |
| **Accept** | Build 自检完成 | 只读 + 跑验证；写 `accept.md`；不改产品代码 |

独立会话优于同一会话「扮演多个角色」。Accept 不得与 Builder 共用未清上下文的长会话。

## 与工程 harness 的关系

| 层 | 文件 |
|----|------|
| 产品流水线 SSOT | 本文件（引擎说明）+ 项目 `docs/product-pipeline.md` 附录 |
| Feature 工件 | `docs/features/<id>/` |
| HOW | `define-feature` / `accept-feature` + 业务 playbook |
| 进度 | `handoff.md`（`phase: define\|design\|build\|accept` + `feature:`；有 UI 时加 `prototype_status: pending\|confirmed\|exempt`） |
| **机械门禁** | `kb_sync.py check`（Brief 抢跑）/ `check-ship`（Accept PASS；`pr-merge` 调用） |
| 踩坑回流 | `harness-feedback` + features/_checklist 滚动项 |

**不替代** domains / tasks / check / smoke；是在其前增加 DoR，在其后增加产品准出。

## 机械门禁（约束 agent，不只是文档）

| 闸 | 何时 FAIL | 实现 |
|----|-----------|------|
| Brief 抢跑 | `active` + codeish diff（services/pkg/apps/packages/api/src/migrations），且 Brief 未 `approved` | `kb_sync check` ← `make check-harness` |
| phase=build/design 无 feature | 同上且 task 非 `brief_exempt` | 同上 |
| `require_brief_approved` | task 声明的 brief 未 approved 却改代码 | 同 ADR 闸 |
| `require_adr_accepted` | task 声明的 ADR 仍「提议中」却改代码 | `kb_sync check` |
| handoff.task | `active\|blocked` 时 task 空或不在 tasks.yaml | `kb_sync check` |
| Accept 准出 | 合入时 `handoff.feature` 已挂且 accept ≠ PASS | `kb_sync check-ship` ← `pr-merge` |
| 裸 merge | agent 直接 `gh pr merge` | hooks 硬拦；须 `make pr-merge` |
| 设计 token 合规（Layer 1） | 实现树 / 原型出现 DESIGN.md 表外硬编码色值、圆角、字号、字重 | `scripts/design-lint.js` ← `make design-lint` / CI；token 表自动解析自 DESIGN.md front matter，项目只填 `lint:` 块；已知历史漂移登记 `lint.baseline`（降级不阻断，**折回后必须删条目**） |

**设计门禁三层**（TokenStore keys-redesign 实践固化）：**Layer 1 token 合规**（`design-lint.js`，值级——「值对了吗」，scaffold 已带）；**Layer 2 组件结构**（AST 检查按钮层级纪律 / 表头单元格对齐成对声明等结构规则——「结构对了吗」，项目进 Build 期按需落）；**Layer 3 质量锚自动核对**（Playwright 渲染取实测值逐锚核对——「页面对了吗」，Accept 期按需落）。三层互不替代；L1 之外两层引擎不预置实现，只在文档固化架构位。

原型闸目前以 **文档 + handoff `prototype_status`** 约束；未默认并入 `kb_sync` 硬 FAIL。若抢跑成常态，再加 `require_prototype_confirmed`。

`tasks.yaml` 字段：

```yaml
require_brief_approved:
  - docs/features/foo/brief.md
require_adr_accepted:
  - docs/decisions/ADR-XXX.md
require_accept_pass: true   # 可选；挂了 feature 且非 exempt 时合入也会查
brief_exempt: true          # 微改 / 流水线前存量 playbook
```

默认豁免：`define-feature` / `accept-feature` / `maintain-knowledge` / `harness-feedback` / `resume` / `troubleshoot` / `l1-micro`。

## 刻意不做

- 不照搬大厂 10 人评审会 / 专职 QA 编制
- 不计费 / 账本类产品不当 Research Preview「先发后补」
- 不一上来造 10+ agent；OPC 默认 Brief + Accept，Architect 按痛点加
- 不在 Write hook 里拦每一文件（成本高）；靠 `make check-harness` / `pr-merge` 与 ADR 闸同级失败
