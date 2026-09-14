# Playbook: 验收 Feature（Accept）

> 角色：**Acceptance Agent**。对照 Brief AC 出 verdict；**不改产品代码**。FAIL 打回 Build/Design/Define。

## 何时用

- Builder 自检完成，准备合入 / ship 前
- 人要求「按验收标准验一遍」

## Golden path

1. `make context-pack TASK=accept-feature`
2. 确认 `docs/features/<id>/brief.md` 为 `approved`
3. 复制/填写 `accept.md`（或更新已有）
4. 跑项目约定的工程准出（check / test / smoke）
5. **逐条** AC：执行或观察，写入证据（命令与摘要）
6. 按风险分层完成人工勾选栏（S 必等人）
7. Verdict：`PASS` 或 `FAIL`
8. FAIL → handoff 写明打回阶段与阻塞项；**不要**在本角色里修代码
9. PASS → 更新 handoff；交人闸 Ship / `pr-merge`
10. `make wip-save MSG="accept: <id> PASS|FAIL"`

## 完成自检

- [ ] 每条 AC 有证据，无空「ok」
- [ ] 未修改业务实现文件
- [ ] FAIL 时未「顺手修」；PASS 时工程准出为绿

## 与 Builder 隔离

Accept 使用新会话或清空后的会话；不要带着「我刚写完这段」的上下文自审。
