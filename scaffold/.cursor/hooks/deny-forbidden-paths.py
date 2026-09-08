#!/usr/bin/env python3
"""禁写路径硬拦：读 docs/harness/policy.yaml（可配置）。"""
from __future__ import annotations

import fnmatch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from policy_lib import emit_allow, emit_deny, extract_paths, load_payload  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "docs/harness/policy.yaml"

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore


def load_policy() -> dict:
    if not POLICY.is_file() or yaml is None:
        return {
            "forbidden_write_globs": [".env", ".env.*", "deploy/secrets/**"],
            "readonly_path_prefixes": [],
        }
    data = yaml.safe_load(POLICY.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def normalize_path(path: str) -> str:
    norm = path.replace("\\", "/")
    while norm.startswith("./"):
        norm = norm[2:]
    return norm


def denied(path: str, policy: dict) -> str | None:
    norm = normalize_path(path)
    base = Path(norm).name

    for pref in policy.get("readonly_path_prefixes") or []:
        pref = str(pref).replace("\\", "/").rstrip("/") + "/"
        if norm == pref[:-1] or norm.startswith(pref) or f"/{pref}" in f"/{norm}/":
            return f"只读路径禁止写入: {pref[:-1]}/"

    for g in policy.get("forbidden_write_globs") or []:
        g = str(g)
        if fnmatch.fnmatch(norm, g) or fnmatch.fnmatch(base, g):
            return f"禁止写入匹配 {g} 的文件"
        # ** semantics lite
        if g.endswith("/**") and norm.startswith(g[:-3].rstrip("/")):
            return f"禁止写入匹配 {g} 的文件"

    if base.startswith(".env") or norm == ".env" or "/.env" in f"/{norm}":
        return "禁止写入密钥文件 .env*"
    return None


def main() -> int:
    payload = load_payload()
    policy = load_policy()
    for path in extract_paths(payload):
        reason = denied(path, policy)
        if reason:
            return emit_deny(f"harness deny: {reason} — {path}", payload)
    return emit_allow(payload)


if __name__ == "__main__":
    raise SystemExit(main())
