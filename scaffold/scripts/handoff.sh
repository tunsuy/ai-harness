#!/usr/bin/env bash
# 打印会话交接板摘要 + git 短状态（ADR-012）
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HF="$ROOT/docs/harness/handoff.md"
[ -f "$HF" ] || { echo "缺少 $HF"; exit 1; }

echo "=== handoff ==="
# frontmatter between first two ---
awk '
  /^---$/ { n++; next }
  n==1 { print }
  n>=2 { exit }
' "$HF"

echo "=== Next ==="
awk '
  /^## Next$/ { p=1; next }
  /^## / { if(p) exit }
  p { print }
' "$HF"

echo "=== git ==="
if git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "branch: $(git -C "$ROOT" branch --show-current 2>/dev/null)"
  git -C "$ROOT" status -sb
else
  echo "(非 git 仓库)"
fi
echo "=== 续作 ==="
echo "1. 读 docs/harness/handoff.md + git log --oneline -5"
echo "2. make context-pack TASK=<task> DOMAIN=<domain>"
echo "3. 从 Next 续作；阶段结束: 更新 handoff + make wip-save MSG=\"…\""
