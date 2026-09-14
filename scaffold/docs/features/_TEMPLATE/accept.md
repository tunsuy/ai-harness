# Accept Report: {{FEATURE_TITLE}}

> 状态：`in_progress` | `PASS` | `FAIL`  
> 风险分层：`S` | `A` | `B`  
> Brief：`brief.md`（须 `approved`）  
> 实现 task / PR：  
> 日期：YYYY-MM-DD  
> Accept 角色会话：（勿与 Builder 长会话混用）

## 工程准出

| 检查 | 结果 | 证据 |
|------|------|------|
| check / lint / test（项目约定） | PASS / FAIL | 命令 + 摘要 |
| smoke / 行为验证（若适用） | PASS / FAIL / N/A | |

## AC 对照

| AC | 结果 | 证据（命令、路径、日志摘要；勿只写「ok」） |
|----|------|------------------------------------------|
| AC-1 | PASS / FAIL | |
| AC-2 | PASS / FAIL | |
| AC-3 | PASS / FAIL | |

## 风险层人工勾选

| 项 | 需要？ | 结果 |
|----|--------|------|
| S：人审业务正确性 / 租户或金额语义 | S 必填 | PASS / FAIL / N/A |
| A：主路径人感抽检 | A 建议 | PASS / FAIL / N/A |
| B：可省略人感 | B | N/A |

## Verdict

**PASS** 或 **FAIL**

### FAIL 时

- 打回阶段：`build` / `design` / `define`
- 阻塞项：
- 禁止：Accept 角色直接改产品代码「顺手修」

### PASS 后

- [ ] handoff 更新；准备 `pr-merge`（若适用）
- [ ] roadmap / glossary 已同步
- [ ] 若有可编码返工根因 → `harness-feedback` 或更新项目 accept checklist
