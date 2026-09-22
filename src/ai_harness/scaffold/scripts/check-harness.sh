#!/usr/bin/env bash
# Harness 自检：关键文件 + KB sync
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
pass=0
fail=0

check() {
  local name="$1"
  shift
  if "$@"; then
    echo "  [PASS] $name"
    pass=$((pass + 1))
  else
    echo "  [FAIL] $name"
    fail=$((fail + 1))
  fi
}

echo "==> harness files"
for f in \
  AGENTS.md \
  docs/harness/domains.yaml \
  docs/harness/tasks.yaml \
  docs/harness/policy.yaml \
  docs/harness/handoff.md \
  docs/harness/handoff.template.md \
  docs/harness/invariants.md \
  docs/architecture.md \
  docs/product-pipeline.md \
  docs/features/_TEMPLATE/brief.md \
  docs/features/_TEMPLATE/accept.md \
  docs/features/_TEMPLATE/prototype.md \
  docs/design/references/README.md \
  docs/design/DESIGN.md \
  docs/features/_accept-checklist.md \
  docs/playbooks/define-feature.md \
  docs/playbooks/accept-feature.md \
  docs/playbooks/continue-handoff.md \
  .agents/skills/product-brief/SKILL.md \
  .agents/skills/product-accept/SKILL.md \
  .agents/skills/product-prototype/SKILL.md \
  scripts/kb_sync.py \
  scripts/pr-merge.sh \
  .cursor/hooks.json \
  .cursor/hooks/policy_lib.py \
  .cursor/hooks/deny-dangerous-shell.py \
  .agents/hooks.json
do
  check "$f" test -f "$f"
done

echo "==> KB"
if python3 scripts/kb_sync.py check; then
  pass=$((pass + 1))
else
  fail=$((fail + 1))
fi

echo "harness check: ${pass} 通过, ${fail} 失败"
[ "$fail" -eq 0 ]
