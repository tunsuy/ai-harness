#!/usr/bin/env bash
# 打印会话交接板摘要 + git 短状态
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
current_branch=""
if git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  current_branch="$(git -C "$ROOT" branch --show-current 2>/dev/null || true)"
  echo "branch: $current_branch"
  git -C "$ROOT" status -sb
else
  echo "(非 git 仓库)"
fi

# 防呆检查：在 main 分支上却处于 active 状态
hf_status="$(awk -F: '/^status:/ {gsub(/[ "]/, "", $2); print $2; exit}' "$HF")"
if [[ "$current_branch" =~ ^(main|master)$ ]] && [ "$hf_status" = "active" ]; then
  echo
  echo "⚠️  [STALE HANDOFF 警告] 当前在 $current_branch 分支，但 handoff.md 仍为 status: active！"
  echo "    若上一任务已合并，请及时将 handoff.md 复位为 status: idle，或创建特性分支后再开始新任务。"
fi

echo "=== 续作 ==="
echo "1. 读 docs/harness/handoff.md + git log --oneline -5"
echo "2. make context-pack TASK=<task> DOMAIN=<domain>"
echo "3. 从 Next 续作；阶段结束: 更新 handoff + make wip-save MSG=\"…\""
