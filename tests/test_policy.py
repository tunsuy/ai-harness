#!/usr/bin/env python3
"""Smoke: policy_lib deny formatting + forbidden path helper."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS = ROOT / "scaffold" / ".cursor" / "hooks"
sys.path.insert(0, str(HOOKS))

from policy_lib import is_antigravity, is_codex  # noqa: E402


def test_detect_hosts():
    assert is_codex({"hook_event_name": "PreToolUse", "tool_name": "Bash"})
    assert is_antigravity({"toolCall": {"args": {"CommandLine": "ls"}}})


def test_deny_scripts_shell():
    script = HOOKS / "deny-dangerous-shell.py"
    p = subprocess.run(
        [sys.executable, str(script)],
        input=json.dumps({"command": "git push --force origin main"}),
        capture_output=True,
        text=True,
        check=False,
    )
    assert p.returncode == 0, p.stderr
    out = json.loads(p.stdout)
    assert out.get("permission") == "deny"


def test_deny_env_path():
    script = HOOKS / "deny-forbidden-paths.py"
    p = subprocess.run(
        [sys.executable, str(script)],
        input=json.dumps({"tool_input": {"path": ".env.local"}}),
        capture_output=True,
        text=True,
        check=False,
    )
    assert p.returncode == 0, p.stderr
    out = json.loads(p.stdout)
    assert out.get("permission") == "deny", out


if __name__ == "__main__":
    test_detect_hosts()
    test_deny_scripts_shell()
    test_deny_env_path()
    print("ok")
