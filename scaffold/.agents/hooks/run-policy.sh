#!/usr/bin/env bash
# Antigravity 要求尽量用绝对路径；此包装解析仓库根再调共用策略脚本。
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
exec python3 "$ROOT/.cursor/hooks/$1"
