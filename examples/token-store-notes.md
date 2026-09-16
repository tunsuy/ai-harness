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
- **（2026-09-16，keys-redesign 八轮人闸反馈回灌）**：
  - Layer-1 设计门禁 `scaffold/scripts/design-lint.js` + `make design-lint`：硬编码色值/圆角/字号/字重必须命中项目 DESIGN.md token 表；token 表**自动解析自 front matter**（TokenStore 首版是硬编码表，通用化时改为解析器 + `lint:` 配置块）；`lint.baseline` 已知漂移基线（SSOT 已改、代码禁改期的过渡，折回后必须删条目——机制来自 tokens.css 四条真实漂移）
  - 三层设计门禁架构（PRODUCT_PIPELINE「机械门禁」）：L1 token 合规（已带）→ L2 组件结构 AST（Build 期）→ L3 质量锚 Playwright 自动核对（Accept 期）
  - 质量锚方法论进 DESIGN.md 骨架：默认八条（一页一语法 / 节奏量级 / 产品工件锚 / 字号阶梯 / 密度一致 / 断点完整 / CJK 已知坑 / 双语韧性）+「观感先于核对」两段式
  - 流程硬化进原型闸：**组件覆盖检查**（无规范行的组件先补规范再画，禁临场拍值）、每版必过 design-lint、**两段式自评**（禁第一稿直送人闸）、Critic 两段式评审节进 `_TEMPLATE/prototype.md`
  - 参照库扩容：awesome-design-md 补 vercel / posthog；新增 `cn-design-systems/`（Ant/Arco/TDesign 源码级 token 对照——整页观感与单格取值两库分工）
  - 治理模式进 DESIGN.md 骨架提示：色板纪律五条 / 用色决策表 / 组件规格矩阵（全变体×全状态）/ 表格列对齐成对声明

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
