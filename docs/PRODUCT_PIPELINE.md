# OPC 产品开发流水线（通用）

> 一人公司 / AI-native 默认流程。工程执行仍走 harness（handoff / playbook / check）；本文件补齐 **定义 → 验收** 两段，减少「能跑但不对味」的返工。

## 一句话

**先写清成功标准，再实现；实现与验收分离；人只守不可逆闸门。**

## 四阶段

```
Define ──► Design ──► Build ──► Accept ──► Learn
  ↑人闸1     ↑人闸2              ↑人闸3
```

| 阶段 | 角色（agent） | 产出物 | 禁止 |
|------|---------------|--------|------|
| **Define** | Product Brief | `docs/features/<id>/brief.md`（PRFAQ-lite） | 写业务代码、定技术栈 |
| **Design** | Spec / Architect | ADR stub（若难逆转）+ `task_id` + 实现 playbook 骨架 | 实现；Brief 未过闸不动 |
| **Build** | Builder（现有 harness） | 按 playbook 实现 + check/smoke | 改 Brief/验收标准 |
| **Accept** | Acceptance | `docs/features/<id>/accept.md` verdict | 「顺手修」；FAIL 必须打回 Build |
| **Learn** | 任意 → harness-feedback | 更新 accept checklist / invariants / playbook | 只在聊天说「下次注意」 |

## 人闸（不可逆）

1. **概念**：值不值得做（对照产品定位 / roadmap）
2. **Brief**：范围、非目标、验收标准是否可测
3. **Ship**：Accept = PASS 且风险分层要求的人工勾选完成

中间劳动（调研稿、ADR 草稿、编码、跑测）交给 agent。

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
| **Builder** | Brief=`approved` 且 DoR 齐 | 现有 playbook；不改 AC |
| **Accept** | Build 自检完成 | 只读 + 跑验证；写 `accept.md`；不改产品代码 |

独立会话优于同一会话「扮演多个角色」。Accept 不得与 Builder 共用未清上下文的长会话。

## 与工程 harness 的关系

| 层 | 文件 |
|----|------|
| 产品流水线 SSOT | 本文件（引擎说明）+ 项目 `docs/product-pipeline.md` 附录 |
| Feature 工件 | `docs/features/<id>/` |
| HOW | `define-feature` / `accept-feature` + 业务 playbook |
| 进度 | `handoff.md`（`phase: define\|design\|build\|accept` + `feature:`） |
| **机械门禁** | `kb_sync.py check`（Brief 抢跑）/ `check-ship`（Accept PASS；`pr-merge` 调用） |
| 踩坑回流 | `harness-feedback` + features/_checklist 滚动项 |

**不替代** domains / tasks / check / smoke；是在其前增加 DoR，在其后增加产品准出。

## 机械门禁（约束 agent，不只是文档）

| 闸 | 何时 FAIL | 实现 |
|----|-----------|------|
| Brief 抢跑 | `active` + codeish diff（services/pkg/apps/api/migrations），且 Brief 未 `approved` | `kb_sync check` ← `make check` |
| phase=build/design 无 feature | 同上且 task 非 `brief_exempt` | 同上 |
| `require_brief_approved` | task 声明的 brief 未 approved 却改代码 | 同 ADR 闸 |
| Accept 准出 | 合入时 `handoff.feature` 已挂且 accept ≠ PASS | `kb_sync check-ship` ← `pr-merge` |

`tasks.yaml` 字段：

```yaml
require_brief_approved:
  - docs/features/foo/brief.md
require_accept_pass: true   # 可选；挂了 feature 且非 exempt 时合入也会查
brief_exempt: true          # 微改 / 流水线前存量 playbook
```

默认豁免：`define-feature` / `accept-feature` / `maintain-knowledge` / `harness-feedback` / `resume` / `troubleshoot` / `l1-micro`。

## 刻意不做

- 不照搬大厂 10 人评审会 / 专职 QA 编制
- 不计费 / 账本类产品不当 Research Preview「先发后补」
- 不一上来造 10+ agent；OPC 默认 Brief + Accept，Architect 按痛点加
- 不在 Write hook 里拦每一文件（成本高）；靠 `make check` / `pr-merge` 与 ADR 闸同级失败
