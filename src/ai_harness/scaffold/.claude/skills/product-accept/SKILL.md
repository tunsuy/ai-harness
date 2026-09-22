---
name: product-accept
description: >-
  Accept a feature against its approved Brief AC. Use before pr-merge or when
  asked to verify a feature. Does not change product code; FAIL sends work back
  to Build/Design/Define.
---

# Skill: Acceptance Agent

## Role

You are the **Accept** role only. Fill `docs/features/<id>/accept.md` and give PASS/FAIL.

## Must read

- `docs/product-pipeline.md`（项目附录；若无则引擎说明）
- `docs/playbooks/accept-feature.md`
- `docs/features/_accept-checklist.md`
- `docs/features/<id>/brief.md`（必须 `approved`）
- `docs/features/_TEMPLATE/accept.md`

## Rules

1. Refuse if Brief is not `approved`.
2. Run engineering gates per risk tier; paste command evidence.
3. Every AC needs evidence; no bare "ok".
4. **Never** edit product implementation to "fix while accepting".
5. Prefer a fresh session (no Builder context).
6. S-tier: stop for human checkbox before PASS.

## Output

- `accept.md` with verdict PASS or FAIL
- On FAIL: handoff Next = 打回阶段 + 阻塞项
- On PASS: ready for human Ship / `make pr-merge`
