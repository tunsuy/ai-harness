#!/usr/bin/env bash
# 等 PR CI 全绿再 squash merge。
# 裸 `gh pr merge` 由 agent hooks 硬拦；收工请走本脚本或 `make pr-merge`。
#
# 用法:
#   make pr-merge PR=12
#   bash scripts/pr-merge.sh 12
#   bash scripts/pr-merge.sh          # 当前分支对应 PR
#
# 环境:
#   PR_MERGE_TIMEOUT_SEC  最长等待秒数（默认 1800）
#                          取值须 ≥ 项目最慢 PR CI job；最慢 job 超过默认值时勿靠反复
#                          re-arm 硬扛——要么调大本值，要么把慢 job 后置到 main push（见
#                          引擎 ADR-005 验证分层）。900 时代的实测教训：17min smoke 必超
#                          900s，每次合入都要人工 re-arm，摩擦真实存在。
#   PR_MERGE_INTERVAL_SEC 轮询间隔（默认 10）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PR="${1:-${PR:-}}"
if [ -z "$PR" ]; then
  PR="$(gh pr view --json number -q .number 2>/dev/null || true)"
fi
if [ -z "$PR" ]; then
  echo "Usage: make pr-merge PR=<n>   # 或在已关联 PR 的分支上: bash scripts/pr-merge.sh" >&2
  exit 2
fi

TIMEOUT_SEC="${PR_MERGE_TIMEOUT_SEC:-1800}"
INTERVAL_SEC="${PR_MERGE_INTERVAL_SEC:-10}"
deadline=$((SECONDS + TIMEOUT_SEC))

echo "==> pr-merge: waiting for CI on PR #${PR} (timeout ${TIMEOUT_SEC}s)"

# 推送后 checks 可能尚未创建；先等到至少有一条，再 --watch
while true; do
  if [ "$SECONDS" -ge "$deadline" ]; then
    echo "REFUSE: timed out waiting for CI checks on PR #${PR}" >&2
    gh pr checks "$PR" 2>&1 || true
    exit 1
  fi
  set +e
  out="$(gh pr checks "$PR" --json name,bucket,state 2>/dev/null)"
  ec=$?
  set -e
  # exit 8 = pending（已有 checks）；0 = 已结束；其它可能尚无 checks
  if [ "$ec" -eq 0 ] || [ "$ec" -eq 8 ]; then
    count="$(printf '%s' "$out" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(len(d) if isinstance(d,list) else 0)' 2>/dev/null || echo 0)"
    if [ "${count:-0}" -gt 0 ]; then
      break
    fi
  fi
  echo "… checks not listed yet; sleep ${INTERVAL_SEC}s"
  sleep "$INTERVAL_SEC"
done

set +e
gh pr checks "$PR" --watch --fail-fast --interval "$INTERVAL_SEC"
watch_ec=$?
set -e
if [ "$watch_ec" -ne 0 ]; then
  echo "REFUSE: CI failed or incomplete on PR #${PR} (exit ${watch_ec}); fix then re-run make pr-merge" >&2
  gh pr checks "$PR" 2>&1 || true
  exit 1
fi

# 双检：所有 check bucket 必须为 pass/skipping（防 watch 边界误报）
bad="$(gh pr checks "$PR" --json name,bucket 2>/dev/null | python3 -c '
import json, sys
rows = json.load(sys.stdin)
ok = {"pass", "skipping"}
bad = [r.get("name","?") for r in rows if r.get("bucket") not in ok]
print("\n".join(bad))
')"
if [ -n "$bad" ]; then
  echo "REFUSE: non-green checks on PR #${PR}:" >&2
  printf '%s\n' "$bad" | sed 's/^/  /' >&2
  exit 1
fi

echo "==> pr-merge: product ship gate (Brief/Accept)"
python3 "$ROOT/scripts/kb_sync.py" check-ship

echo "==> pr-merge: CI green; squash merging PR #${PR}"
gh pr merge "$PR" --squash --delete-branch
echo "PR #${PR} merged ✓"

# 自动防呆：合入后将本地 handoff.md 复位为 status: idle，避免切回 main 后残留 active
HF="$ROOT/docs/harness/handoff.md"
if [ -f "$HF" ] && grep -q '^status: active' "$HF"; then
  echo "==> pr-merge: auto-reset local handoff.md to status: idle"
  if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' 's/^status: active/status: idle/' "$HF" 2>/dev/null || true
  else
    sed -i 's/^status: active/status: idle/' "$HF" 2>/dev/null || true
  fi
fi
