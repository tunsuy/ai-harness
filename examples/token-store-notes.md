# 从 TokenStore 风格接到 ai-harness

TokenStore 是第一个完整消费者：路径约定（`services/console/{domain}.go`）、金额/Key invariants、三平面 smoke、**产品流水线**（`docs/product-pipeline.md` + `define-feature` / `accept-feature`）。

## 已从 TokenStore 上游回 scaffold 的通用能力

- `pr-merge.sh` + `check-ship`；hooks 禁裸 `gh pr merge`
- shell hook 加固（直推 main、`git clean -f`、`.env` 重定向等）+ `test_deny_shell.py`
- `kb_sync`：YAML fallback、`require_adr_accepted`、handoff.task、加强 Brief 闸、`packages/` codeish、pack WARN
- handoff `phase` / `feature` / `prototype_status`；stale handoff 警告
- 原型模板打磨、`_accept-checklist` 骨架、product-pipeline 附录模板
- 产品 skills：`product-brief` / `product-accept` / `product-prototype`
- hooks 用 `git rev-parse --show-toplevel` / `$CLAUDE_PROJECT_DIR` 解析仓根（cwd 无关）
- cold-start 规则默认 `pr-merge`
- 设计参照库：`docs/design/references/` 取法（awesome-design-md 落库、按轮选老师、学模式不搬值）+ stripe 样例

## 仍留在 TokenStore（勿回灌引擎）

- `kb_sync.check_domains` 路径约定、roadmap 硬依赖、`check-conventions`、业务 playbook
- 预览机 IP / systemd 运维段、金额/租户门禁、去 `policy.yaml` 化的禁写实现
- 本仓 `DESIGN.md` / `console-ui.md` 色板与页模板正文（引擎只有骨架）
- 第三方 UI skills（impeccable / Emil 等）的**源码树**仍可不进引擎；推荐包已用 scaffold `skills-lock.json` + `make skills-ui` 固化，新项目一条命令还原，无需再探索

## 建议对齐步骤（可选，不自动改 TokenStore）

1. 用本仓 `scaffold/.cursor/hooks/policy_lib.py` 对齐多宿主响应（若有漂移）。
2. 禁写路径用 `docs/harness/policy.yaml`（`.env*` 等）；按需加 `readonly_path_prefixes`。
3. 保留 TokenStore 专用 `kb_sync.py` 路径检查；公共包默认是 `metadata_only`。
4. AGENTS 仍只做地图；框架 ADR 可链到 `ai-harness/docs/decisions`。
5. 产品流水线：引擎说明见 `docs/PRODUCT_PIPELINE.md`；项目附录风险分层与 `docs/features/` 留在业务仓。

## 新项目不要复制

不要把 TokenStore 的 `invariants.md` / 域表当作默认——从 `ai-harness init` 空壳填自己的。  
Brief/Accept 模板与 playbook 已在 scaffold；按项目填写 `product-pipeline` 附录即可。
