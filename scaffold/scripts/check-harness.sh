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
  docs/harness/invariants.md \
  docs/architecture.md \
  .cursor/hooks.json \
  .cursor/hooks/policy_lib.py \
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
