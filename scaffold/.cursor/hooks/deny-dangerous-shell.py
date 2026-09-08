#!/usr/bin/env python3
"""危险 shell 硬拦：Cursor / Claude / Codex 共用。"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from policy_lib import emit_allow, emit_deny, extract_command, load_payload  # noqa: E402

DENY_PATTERNS = [
    (r"\bgit\s+push\s+.*--force\b|\bgit\s+push\s+-f\b", "禁止 force push"),
    (r"\bgit\s+push\b.*\b(main|master)\b", "禁止直推 main/master"),
    (r"\bgit\s+reset\s+--hard\b", "禁止 git reset --hard"),
    (r"\brm\s+(-[a-zA-Z]*f[a-zA-Z]*|--force).*/\b|\brm\s+-rf\s+/\b", "禁止危险 rm -rf /"),
    (r"curl[^\n]*\|\s*(ba)?sh\b|wget[^\n]*\|\s*(ba)?sh\b", "禁止 curl|sh / wget|sh"),
    (r"\bsudo\s+rm\b|\bchmod\s+-R\s+777\b", "禁止高危权限操作"),
]


def main() -> int:
    payload = load_payload()
    cmd = extract_command(payload)
    for pat, reason in DENY_PATTERNS:
        if re.search(pat, cmd, re.I):
            return emit_deny(f"harness deny: {reason} — {cmd[:120]}（ADR-013）", payload)
    return emit_allow(payload)


if __name__ == "__main__":
    raise SystemExit(main())
