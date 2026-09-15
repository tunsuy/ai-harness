#!/usr/bin/env bash
# 从 skills-lock.json 还原推荐 UI skill 包（Emil / impeccable / refactoring-ui）。
# 产品流水线 skills（product-brief 等）已在 scaffold 内，无需本命令。
#
# 用法:
#   make skills-ui
#   bash scripts/install-ui-skills.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

LOCK="$ROOT/skills-lock.json"
if [ ! -f "$LOCK" ]; then
  echo "REFUSE: missing $LOCK" >&2
  exit 1
fi

echo "==> install UI skills from skills-lock.json"
npx --yes skills experimental_install

echo "✓ UI skills restored under .agents/skills/ (and agent mirrors if configured)"
echo "  First-party product skills remain: product-brief / product-accept / product-prototype"
echo "  List: npx skills list"
