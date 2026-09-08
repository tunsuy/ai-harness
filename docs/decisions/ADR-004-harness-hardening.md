# ADR-004: Harness 加固 —— hooks、行为验证、失败回流

- 状态：已接受
- 日期：2026-09-08
- 来源：TokenStore ADR-013（框架化）

## 决策

1. **Agent hooks**：Cursor / Claude / Codex / Antigravity 共用策略脚本；响应格式由 `policy_lib` 适配。
2. **禁写可配置**：`docs/harness/policy.yaml`（默认 `.env*`；项目加只读树）。
3. **行为验证**：项目自备 smoke；「lint 绿 ≠ 完成」。
4. **失败回流**：`harness-feedback` playbook——错一次就加 check/hook，禁止只口头提醒。
5. Antigravity **IDE** 可能不跑 PreToolUse；以 CLI/`agy` + CI 为准。
