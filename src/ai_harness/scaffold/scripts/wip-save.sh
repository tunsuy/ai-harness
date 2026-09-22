#!/usr/bin/env bash
# 特性分支 WIP 快照提交（ADR-012）：代码进度以 git 为准，配合 handoff.md。
# 用法: make wip-save MSG="key: CreateKey handler done"
# 环境: PUSH=1 时额外 git push；默认只本地 commit。
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

MSG="${MSG:-}"
if [ -z "$MSG" ]; then
  echo "Usage: make wip-save MSG=\"short progress note\"" >&2
  exit 2
fi

branch="$(git branch --show-current 2>/dev/null || true)"
case "$branch" in
  ai/*|feat/*) ;;
  *)
    echo "REFUSE: WIP 保存只允许在 ai/* 或 feat/* 分支（当前: ${branch:-detached}）" >&2
    exit 1
    ;;
esac

# 不提交密钥类文件
git add -A
# 常见密钥文件名防御（仍以 .gitignore 为准）
git reset -q -- .env .env.* 2>/dev/null || true

if git diff --cached --quiet; then
  echo "无变更可提交（工作区干净或仅有被排除文件）"
  exit 0
fi

git commit -m "$(cat <<EOF
wip: ${MSG}

EOF
)"

echo "WIP saved on ${branch}: $(git rev-parse --short HEAD)"
if [ "${PUSH:-0}" = "1" ]; then
  git push -u origin HEAD
fi
