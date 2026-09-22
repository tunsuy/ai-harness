#!/usr/bin/env python3
"""Self-check deny-dangerous-shell patterns (run: python3 scripts/test_deny_shell.py)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".cursor/hooks/deny-dangerous-shell.py"


def run(cmd: str) -> tuple[str, bool]:
    p = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps({"command": cmd}),
        text=True,
        capture_output=True,
        check=False,
    )
    out = (p.stdout or "").strip()
    denied = (
        '"permission": "deny"' in out
        or '"permissionDecision": "deny"' in out
        or '"allow_tool": false' in out
    )
    return out, denied


def main() -> int:
    cases = [
        ("gh pr merge 1 --squash", True),
        ("cd /tmp && gh pr merge 1 --squash", True),
        ("FOO=1 gh pr merge 1", True),
        ("make pr-merge PR=1", False),
        ("bash scripts/pr-merge.sh 1", False),
        ("git push -u origin HEAD && gh pr create --title 'docs: idle on main'", False),
        ("git commit -m 'Block bare gh pr merge via hooks'", False),
        ("git push origin main", True),
        ("git push -u origin main", True),
        ("git push origin HEAD:main", True),
        ("git clean -fd", True),
        ("git clean -f", True),
        ("git clean -n", False),
        ("git checkout -f", True),
        ("git checkout main", False),
        ("rm -rf /", True),
        ("rm -rf /*", True),
        ("rm -fr /", True),
        ("rm -Rf /", True),
        ("rm -f -r /", True),
        ("rm -r -f /", True),
        ("rm -rf --no-preserve-root /", True),
        ("rm -rf / && echo done", True),
        ("rm -rf /home", True),
        ("rm -f notes.txt", False),
        ("rm file.txt", False),
        ("git rm -f staged.txt", False),
        ("echo 'docs: 修复 rm -rf / 漏拦'", False),
        ("echo 'FOO=1' > .env", True),
        ("echo 'FOO=1' >> .env.local", True),
        ("cat secret.txt > deploy/secrets/app.key", True),
        ("echo 'test' | tee deploy/secrets/app.key", True),
        ("cp /tmp/val .env", True),
        ("cat deploy/etc/dev.env", False),
        ("grep SECRET deploy/etc/dev.env", False),
    ]
    fail = 0
    for cmd, want_deny in cases:
        _, denied = run(cmd)
        ok = denied == want_deny
        print(f"{'PASS' if ok else 'FAIL'}: deny={denied} want={want_deny} :: {cmd[:72]}")
        if not ok:
            fail += 1
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
