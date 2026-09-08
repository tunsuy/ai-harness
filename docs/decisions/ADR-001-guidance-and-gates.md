# ADR-001: 指导层与门禁层双轨

- 状态：已接受
- 日期：2026-09-08
- 来源：TokenStore ADR-010（框架化）

## 决策

Harness = **事前指导** + **事后门禁**。

| 轨 | 职责 | 载体 |
|----|------|------|
| 指导 | 定域、开样板、走 golden path | `architecture.md` + playbooks + glossary |
| 门禁 | 兜住绕过与漂移 | check 脚本 + lint + smoke + agent hooks |

AGENTS.md 只做短地图；细节下沉。不引入重型变更提案状态机填导航坑。

## 后果

新项目先有 shape + ownership，再堆 linter。
