# ai-harness

AI 原生项目开发维护的**公共 harness 引擎**：指导层 + 门禁层 + 跨会话交接 + 多 IDE 硬拦。

从 [TokenStore](https://github.com/tunsuy/token-store) 实践抽离（ADR 思路见 `docs/decisions/`）。**业务约定不进本仓默认值**——每个项目自己填 `domains.yaml` / `invariants.md`。

## 一句话

对话易失，仓库持久。新项目：`init` 一次，以后不再从零讨论「AI 怎么在这个仓里干活」。

## 快速开始

```bash
# 在目标项目根目录
pipx install 'git+https://github.com/tunsuy/ai-harness.git'
# 或开发态
python3 -m pip install -e /path/to/ai-harness

ai-harness init --name MyApp --one-liner "一句话产品定义"
# 或
python3 -m ai_harness init --name MyApp

# 已有项目对齐新版引擎（只刷引擎文件，不碰业务填充）
ai-harness upgrade
ai-harness upgrade --dry-run   # 只看会改什么
```

然后：

1. 改 `docs/harness/invariants.md`、`domains.yaml`、`policy.yaml`
2. 写业务 playbook；`tasks.yaml` 挂上路由
3. Makefile 已 include `Makefile.harness.mk`（或按提示手动加）
4. `pip3 install -r scripts/requirements-kb.txt` → `make kb-gen && make check-harness`
5. 有 UI：填 `docs/design/DESIGN.md`（tokens + `lint:` 块）→ `make design-lint`
6. 已有项目跟新版引擎：`ai-harness upgrade`（先 `--dry-run`）

## 仓库结构

| 路径 | 职责 |
|------|------|
| `scaffold/` | `init` 拷贝到目标仓的模板 |
| `src/ai_harness/` | CLI（`init` / `upgrade`） |
| `docs/WHAT_IS_GENERIC.md` | 引擎 vs 项目填充物边界 |
| `docs/PRODUCT_PIPELINE.md` | OPC 产品流水线：Define → Design → Build → Accept |
| `docs/decisions/` | 框架级 ADR（指导/门禁/SSOT/handoff/硬拦） |
| `examples/` | 如何从 TokenStore 风格接约定 |

## 装进项目后你会得到

- 短地图 `AGENTS.md` + Gemini/Antigravity 入口
- `docs/harness/{domains,tasks,policy,handoff,invariants}`
- `make handoff` / `context-pack` / `wip-save` / `kb-gen` / `check-harness`
- `make design-lint`：Layer-1 设计门禁——硬编码值必须命中项目 `DESIGN.md` token 表（front matter 自动解析，零依赖）
- Cursor / Claude / Codex / Antigravity 共用策略脚本（`policy.yaml` 可配禁写路径）

## 边界（必读）

见 [docs/WHAT_IS_GENERIC.md](docs/WHAT_IS_GENERIC.md)。不要把金额、平面拓扑、某语言落位塞进本包默认 scaffold。

## 与 TokenStore

TokenStore 仍是第一个完整消费者；用 `ai-harness upgrade` 对齐 hooks/脚本/playbook/参照库等**引擎清单**。  
永不覆盖：`domains.yaml` / `invariants.md` / `handoff.md` / `policy.yaml` / `tasks.yaml` / `DESIGN.md` / `product-pipeline.md` / `AGENTS.md` 等项目填充（见 `docs/WHAT_IS_GENERIC.md`）。
