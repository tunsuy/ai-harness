# ADR-002: 知识库 SSOT —— 约定推导，禁文件清单膨胀

- 状态：已接受
- 日期：2026-09-08
- 来源：TokenStore ADR-011（框架化）

## 决策

1. `domains.yaml` 只登记**域元数据**（summary / writer / tables / exemplar…），禁止 `owned_files` 式全量枚举。
2. `architecture.md` 域表由 `kb-gen` 生成；标记区禁手改。
3. `tasks.yaml` 路由任务 → playbook + must_read；冷启动用 `context-pack`，禁止先全库 Glob/Grep。
4. 默认 scaffold 使用 `conventions.mode: metadata_only`；路径级归属由项目自行加约定。

## 后果

维护成本 O(域)，不是 O(文件)。
