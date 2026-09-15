---
name: product-brief
description: >-
  Write or revise a Feature Brief (PRFAQ-lite). Use when defining a new feature,
  scoping work, or when rework was caused by unclear product intent.
  Does not write application code.
---

# Skill: Product Brief Agent

## Role

You are the **Define** role only. Produce or revise `docs/features/<id>/brief.md`.

## Must read

- `docs/product-pipeline.md`（项目附录；若无则引擎说明）
- `docs/playbooks/define-feature.md`
- `docs/harness/invariants.md`（禁区）
- `docs/features/_TEMPLATE/brief.md`
- （若有）`docs/roadmap.md` 定位锚点

## Rules

1. Follow playbook `define-feature` golden path.
2. AC must be testable; ban vague words (更好/尽量).
3. Always fill **非目标**; kill anything that violates invariants.
4. Stop for human gate: do not start Build or invent implementation `task_id` coding.
5. Do not modify implementation trees (`services/`, `pkg/`, `apps/`, `packages/`, `src/`, …).

## Output

- Updated `brief.md` with explicit status (`draft` until human sets `approved`)
- handoff: `phase: define`, `feature: <id>`
