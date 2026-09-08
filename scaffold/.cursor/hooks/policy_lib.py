#!/usr/bin/env python3
"""Shared agent-hook policy helpers (Cursor / Claude / Codex / Antigravity)."""
from __future__ import annotations

import json
import re
import sys
from typing import Any


def load_payload() -> dict[str, Any]:
    try:
        data = json.load(sys.stdin)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}


def is_antigravity(payload: dict[str, Any]) -> bool:
    if isinstance(payload.get("toolCall"), dict):
        return True
    if "conversationId" in payload and ("transcriptPath" in payload or "modelName" in payload):
        return True
    return False


def is_codex(payload: dict[str, Any]) -> bool:
    if is_antigravity(payload):
        return False
    if payload.get("hook_event_name") in {"PreToolUse", "SessionStart", "PermissionRequest"}:
        return True
    if "tool_name" in payload and "session_id" in payload:
        return True
    return False


def emit_allow(payload: dict[str, Any] | None = None) -> int:
    payload = payload or {}
    if is_antigravity(payload):
        print(json.dumps({"allow_tool": True, "decision": "allow"}))
        return 0
    if is_codex(payload):
        print(json.dumps({}))
        return 0
    print(json.dumps({"permission": "allow"}))
    return 0


def emit_deny(msg: str, payload: dict[str, Any] | None = None) -> int:
    """Format deny for each host agent."""
    payload = payload or {}
    if is_antigravity(payload):
        # Antigravity CLI: top-level allow_tool / decision（勿包 hookSpecificOutput）
        print(
            json.dumps(
                {
                    "allow_tool": False,
                    "deny_reason": msg,
                    "decision": "deny",
                    "reason": msg,
                }
            )
        )
        return 0
    if is_codex(payload):
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": payload.get("hook_event_name") or "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": msg,
                    },
                    "systemMessage": msg,
                }
            )
        )
        return 2
    print(
        json.dumps(
            {
                "permission": "deny",
                "user_message": msg,
                "agent_message": msg,
            }
        )
    )
    return 0


def tool_call(payload: dict[str, Any]) -> dict[str, Any]:
    tc = payload.get("toolCall")
    return tc if isinstance(tc, dict) else {}


def tool_input(payload: dict[str, Any]) -> dict[str, Any]:
    ti = payload.get("tool_input") or payload.get("input") or {}
    if isinstance(ti, dict):
        return ti
    args = tool_call(payload).get("args")
    return args if isinstance(args, dict) else {}


def extract_command(payload: dict[str, Any]) -> str:
    if isinstance(payload.get("command"), str):
        return payload["command"]
    # Antigravity: toolCall.args.CommandLine
    args = tool_call(payload).get("args")
    if isinstance(args, dict):
        for k in ("CommandLine", "commandLine", "Command", "command", "cmd"):
            if isinstance(args.get(k), str):
                return args[k]
    ti = tool_input(payload)
    for k in ("command", "cmd", "script", "CommandLine", "commandLine"):
        if isinstance(ti.get(k), str):
            return ti[k]
    return ""


_PATCH_FILE_RE = re.compile(
    r"^\*\*\*\s+(?:Add|Update|Delete|Move)\s+File:\s+(.+)$", re.M
)


def extract_paths(payload: dict[str, Any]) -> list[str]:
    paths: list[str] = []

    def add(p: str) -> None:
        p = p.replace("\\", "/").strip().strip('"').strip("'")
        if p and p not in paths:
            paths.append(p)

    for key in ("path", "file_path", "filePath", "target_file", "TargetFile", "Path"):
        v = payload.get(key)
        if isinstance(v, str):
            add(v)

    args = tool_call(payload).get("args")
    if isinstance(args, dict):
        for key in ("path", "Path", "file_path", "FilePath", "target_file", "TargetFile", "filePath"):
            v = args.get(key)
            if isinstance(v, str):
                add(v)
        # multi replace may carry FilePath
        for key in ("contents", "Content", "content", "new_content"):
            pass

    ti = tool_input(payload)
    for key in ("path", "file_path", "filePath", "target_file", "Path", "TargetFile"):
        v = ti.get(key)
        if isinstance(v, str):
            add(v)

    for key in ("input", "patch", "diff", "content"):
        raw = ti.get(key) if key in ti else payload.get(key)
        if isinstance(raw, str):
            for m in _PATCH_FILE_RE.finditer(raw):
                add(m.group(1).strip())

    if isinstance(payload.get("tool_input"), str):
        for m in _PATCH_FILE_RE.finditer(payload["tool_input"]):
            add(m.group(1).strip())
    return paths
