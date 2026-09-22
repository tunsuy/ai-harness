#!/usr/bin/env python3
"""sessionStart / PreInvocation：开场三步。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from policy_lib import is_antigravity, is_codex  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
HF = ROOT / "docs/harness/handoff.md"
POLICY = ROOT / "docs/harness/policy.yaml"


def project_name() -> str:
    if POLICY.is_file():
        try:
            import yaml

            data = yaml.safe_load(POLICY.read_text(encoding="utf-8")) or {}
            if isinstance(data, dict) and data.get("project_name"):
                return str(data["project_name"])
        except Exception:
            pass
    return "{{PROJECT_NAME}}"


def handoff_status() -> str:
    if not HF.is_file():
        return "missing"
    for line in HF.read_text(encoding="utf-8").splitlines():
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip().split()[0]
    return "unknown"


def get_current_branch() -> str:
    import subprocess

    try:
        r = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        return r.stdout.strip()
    except Exception:
        return ""


def read_payload() -> dict:
    if sys.stdin.isatty():
        return {}
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return {}
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}


def main() -> int:
    payload = read_payload()
    st = handoff_status()
    br = get_current_branch()
    name = project_name()
    stale_note = ""
    if br in ("main", "master") and st == "active":
        stale_note = (
            "\n⚠️  注意：当前在 main 分支但 handoff 为 active！"
            "若前一任务已合入，请复位 status: idle。"
        )
    ctx = (
        f"{name} harness 开场：\n"
        f"1. 读 docs/harness/handoff.md（当前 status={st}，branch={br or 'unknown'}）"
        f"+ make handoff{stale_note}\n"
        "2. active/blocked → make context-pack TASK=<task> DOMAIN=<domain>，从 Next 续作\n"
        "3. 禁止先全库探索；用 context-pack 只读清单\n"
        "4. 阶段结束：更新 handoff + make wip-save MSG=…（仅 ai/*|feat/*）\n"
        "入口：AGENTS.md；硬约定：docs/harness/invariants.md"
    )
    if is_antigravity(payload):
        print(json.dumps({"additionalContext": ctx, "allow_tool": True}))
        return 0
    if is_codex(payload) or payload.get("hook_event_name") == "SessionStart":
        print(json.dumps({"systemMessage": ctx}))
        return 0
    print(json.dumps({"additional_context": ctx}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
