# AGENTS.md — {{PROJECT_NAME}} AI 入口（地图，不是手册）

> **对话易失，仓库持久。** 细节不堆在此：硬约定 → `docs/harness/invariants.md`；架构 → `docs/architecture.md`；进度 → `docs/harness/handoff.md`。

## 一句话

{{PROJECT_ONE_LINER}}

## 产品流水线（定义 / 验收）

新功能默认：`define-feature` →（必要则 ADR）→ 实现 playbook → `accept-feature` → 合入。  
DoR/DoD 与角色边界见引擎说明；项目可加 `docs/product-pipeline.md` 附录。Brief/Accept 工件在 `docs/features/<id>/`。

禁止：Brief 未 `approved` 就开业务实现；Accept 角色改产品代码「顺手修」。

## 开场三步（每次会话）

1. 读 `docs/harness/handoff.md` → `make handoff`（+ `git log --oneline -5`）
2. 续作或新任务：`make context-pack TASK=… DOMAIN=…` → **只读清单** → 从 Next / playbook 写
3. 阶段结束：更新 handoff → `make wip-save MSG="…"`（仅 `ai/*`|`feat/*`）

禁止：先全库盲目探索；把进度只留在聊天里。

## 命令

```bash
make check-harness      # KB sync + harness 文件存在性
make kb-gen             # domains.yaml → architecture 域表
make context-pack TASK=resume DOMAIN=
make handoff
make wip-save MSG="…"
```

一次性：`pip3 install -r scripts/requirements-kb.txt`

## 验证分级

| 改动 | 最低验证 |
|------|----------|
| 任意 | `make check-harness`（再加项目自己的 build/lint） |
| 域/表/样板 | + `make kb-gen` 且 check 绿 |
| 产品链路 | 项目自备 smoke（lint 绿 ≠ 完成） |

## 禁区

- ❌ main 上 `wip-save` / force push / 直推 main（agent hooks 硬拦）
- ❌ 写入 `policy.yaml` 声明的只读路径 / `.env*`
- ❌ 手改 architecture 域表标记区（改 yaml + `kb-gen`）
- （在 `docs/harness/invariants.md` 补产品禁区）

## 去哪查

| 要什么 | 文件 |
|--------|------|
| 硬约定 | [docs/harness/invariants.md](docs/harness/invariants.md) |
| 架构 | [docs/architecture.md](docs/architecture.md) |
| 域/任务 | [docs/harness/domains.yaml](docs/harness/domains.yaml) · [tasks.yaml](docs/harness/tasks.yaml) |
| 进度 | [docs/harness/handoff.md](docs/harness/handoff.md) · `make wip-save` |
| HOW | [docs/playbooks/](docs/playbooks/) |
| Feature Brief / Accept | [docs/features/](docs/features/) · `define-feature` / `accept-feature` |
| 踩坑回流 | [docs/playbooks/harness-feedback.md](docs/playbooks/harness-feedback.md) |
| 硬拦策略 | [docs/harness/policy.yaml](docs/harness/policy.yaml) |
| WHY | [docs/decisions/](docs/decisions/) |

本 harness 由 [ai-harness](https://github.com/tunsuy/ai-harness) 初始化。
