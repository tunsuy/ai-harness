# Antigravity / Gemini CLI

本仓库以 [`AGENTS.md`](../AGENTS.md) 为跨工具入口。请遵守其中开场三步、验证分级与禁区。

硬拦（agy CLI）：[`.agents/hooks.json`](hooks.json) → 共用 [`.cursor/hooks/deny-*.py`](../.cursor/hooks/)。

产品流水线 skills（与 Claude 镜像）：[`.agents/skills/`](skills/)（`product-brief` / `product-accept` / `product-prototype`）。

说明：Antigravity **IDE** 当前可能不执行 PreToolUse；请用 `agy` CLI，或依赖 `make check-harness` / CI。
