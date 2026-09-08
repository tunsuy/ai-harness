# Playbook: Agent 踩坑 → 加固 Harness

> anytime the agent makes a mistake, engineer the harness so it never happens again.

## 何时触发

- AI 写错落位 / 改了禁区 / 漏验证却报完成
- 人 review 发现「文档写了但可绕过」
- smoke/CI 新失败模式可编码

## Golden path（按优先级）

1. **能机器查？** → 加 check / `kb_sync` / linter → `make check-harness` 必须红
2. **能调用前拦？** → 加 `.cursor/hooks/*` 或改 `policy.yaml`
3. **是高频 HOW？** → 改 playbook + exemplar
4. **是域边界？** → 改 `domains.yaml` → `make kb-gen`
5. **是决策？** → 项目 ADR；禁区 → invariants 一行
6. **仅概念？** → glossary

禁止：只在聊天里说「下次注意」。

## 完成自检

- [ ] 复现原错误路径：门禁或 hook 会 FAIL/deny
- [ ] AGENTS 仍保持短地图
- [ ] `make check-harness` 绿；若动链路 → 项目 smoke
