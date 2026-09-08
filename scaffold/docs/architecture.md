# 架构（项目填写）

> 平面 × 层 × 域。域表由 `make kb-gen` 从 `docs/harness/domains.yaml` 生成——**勿手改标记区**。

## 总览

（描述服务/模块拓扑、依赖方向。）

## 域目录

<!-- BEGIN_DOMAINS_TABLE -->
| 域 | 定义与不变量 | 写所有者 | 表 / 缓存 | 样板 |
|----|--------------|----------|-----------|------|
| **example** | 示例域——请改成真实业务域并删除本条 | app | — | `docs/playbooks/example-add-feature.md` |
<!-- END_DOMAINS_TABLE -->

## 跨域规则

（谁可以读谁的表 / 共享包边界。）

## 新域准入

1. 在 `domains.yaml` 加元数据 + exemplar  
2. `make kb-gen && make check-harness`  
3. 补 playbook（若为高频 HOW）
