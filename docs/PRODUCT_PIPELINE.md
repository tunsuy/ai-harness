# OPC 产品开发流水线（通用）

> 一人公司 / AI-native 默认流程。工程执行仍走 harness（handoff / playbook / check）；本文件补齐 **定义 → 验收** 两段，减少「能跑但不对味」的返工。

## 一句话

**先写清成功标准，再实现；实现与验收分离；人只守不可逆闸门。**

## 四阶段

```
Define ──► Design ──► Build ──► Accept ──► Learn
  ↑人闸1     ↑人闸2              ↑人闸3
             （含 UI 原型确认，若适用）
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

## UI Prototype Gate（方案 A：静态原型，不依赖 OpenDesign）

> 适用：新页面、改布局/信息架构、明显视觉方向选择。  
> 豁免：纯文案/色值微调、已知组件内单点改（可标 `prototype_exempt`）；碰钱/租户/鉴权的逻辑仍走 Brief+Accept，与原型闸独立。

**默认路径（云端 agent / 微信协作）：**

1. Brief = `approved` 后进入 Design。
2. Agent 只写 `docs/features/<id>/prototype/` 下的**自包含静态 HTML**（可多变体 `v1/` `v2/`），**不改** `apps/` / `packages/` / `services/` 等实现树。
3. 发布可点开的 HTTPS（或内网）预览链接；更新 `docs/features/<id>/prototype.md`（状态 `pending`）。
4. 人确认变体（微信口令：`确认 A` / `确认 B` / `改：…` / `重出`）→ `prototype.md` 标 `confirmed` + 选中变体。
5. 再进 Build：按项目 UI 规范与 tokens **重做进生产组件**；静态原型不是生产源。

模板：`scaffold/docs/features/_TEMPLATE/prototype.md`（项目可镜像到 `docs/features/_TEMPLATE/`）。

OpenDesign 等外部设计工具为可选增强，**不是本闸前置条件**。

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
- [ ] 产品：`accept.md` 对每条 AC 有证据（命令、截图路径、日志摘要）
- [ ] Accept verdict = `PASS`
- [ ] S 层：人感 / 业务勾选完成
- [ ] 文档：roadmap / handoff / glossary 该改的已改
- [ ] 若返工根因可编码 → 开 `harness-feedback` 或更新 accept checklist

## Agent 角色约定

| 角色 | 何时用 | 工具边界 |
|------|--------|----------|
| **Brief** | 新 feature / 大改范围 | 只写 `docs/features/**`；可读定位/roadmap/ADR |
| **Architect** | DoR 中需 ADR 或跨域方案 | 写 ADR / task / playbook；不写业务实现 |
| **UI Prototype** | Design 阶段有界面 | 只写 `docs/features/<id>/prototype/**` + `prototype.md`；挂项目 DESIGN；按需用 `docs/design/references/` 选老师并记入 prototype；等人确认 |
| **Critic** | 门面级 / 整页重做首轮，送人闸前 | **fresh-session**（不与出稿者共用上下文）：只读变体 + DESIGN 质量锚 + 参照记录，写 `prototype.md`「评审」节（逐变体逐条打分 + 排序 + 最大风险一句）；**不改 HTML、不做顺手修** |
| **Builder** | Brief=`approved`、原型已确认（或豁免）、且 DoR 齐 | 现有 playbook；不改 AC；按确认变体落地 |
| **Accept** | Build 自检完成 | 只读 + 跑验证；写 `accept.md`；不改产品代码 |

独立会话优于同一会话「扮演多个角色」。Accept 不得与 Builder 共用未清上下文的长会话；Critic 同理，不得与 UI Prototype 共用。

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
- 不一上来造 10+ agent；OPC 默认 Brief + Accept，Architect / Critic 按痛点加
- 不在 Write hook 里拦每一文件（成本高）；靠 `make check-harness` / `pr-merge` 与 ADR 闸同级失败
