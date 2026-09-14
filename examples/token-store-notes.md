# 从 TokenStore 风格接到 ai-harness

TokenStore 是第一个完整消费者：路径约定（`services/console/{domain}.go`）、金额/Key invariants、三平面 smoke、**产品流水线**（`docs/product-pipeline.md` + `define-feature` / `accept-feature`）。

## 建议迁移步骤（可选，不自动改 TokenStore）

1. 用本仓 `scaffold/.cursor/hooks/policy_lib.py` 对齐多宿主响应（若有漂移）。
2. 禁写路径用 `docs/harness/policy.yaml`（`.env*` 等）；按需加 `readonly_path_prefixes`。
3. 保留 TokenStore 专用 `kb_sync.py` 路径检查；公共包默认是 `metadata_only`。
4. AGENTS 仍只做地图；框架 ADR 可链到 `ai-harness/docs/decisions`。
5. 产品流水线：引擎说明见 `docs/PRODUCT_PIPELINE.md`；项目附录风险分层与 `docs/features/` 留在业务仓。

## 新项目不要复制

不要把 TokenStore 的 `invariants.md` / 域表当作默认——从 `ai-harness init` 空壳填自己的。  
Brief/Accept 模板与 playbook 已在 scaffold；按项目填写 `product-pipeline` 附录即可。
