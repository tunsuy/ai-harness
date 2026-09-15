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
    # 只匹配 push 目标 ref，避免 HEREDOC/PR title 里的 “on main” 误伤
    (
        r"\bgit\s+push\b(?:\s+(?:-[a-zA-Z0-9]|--[a-zA-Z0-9-]+(?:=\S+)?))*\s+(?:origin\s+)?(?:HEAD:)?(?:refs/heads/)?(main|master)\b",
        "禁止直推 main/master",
    ),
    (r"\bgit\s+reset\s+--hard\b", "禁止 git reset --hard"),
    # rm 强删根路径：flag 含 f（任意顺序/分离/--force）；/ 后为 glob、或跨空白后是操作符/行尾
    (
        r"\brm\s+(-[a-zA-Z]*f[a-zA-Z]*|--force).*/\b"
        r"|\brm\s+(?:-{1,2}[a-zA-Z][a-zA-Z-]*\s+)*(?:-[a-zA-Z]*f[a-zA-Z]*|--force)"
        r"(?:\s+-{1,2}[a-zA-Z][a-zA-Z-]*)*\s+/(?:[*?$]|(?=\s*(?:$|&&|\|\||[;|&)<])))",
        "禁止危险 rm -rf /",
    ),
    (r"curl[^\n]*\|\s*(ba)?sh\b|wget[^\n]*\|\s*(ba)?sh\b", "禁止 curl|sh / wget|sh"),
    (r"\bsudo\s+rm\b|\bchmod\s+-R\s+777\b", "禁止高危权限操作"),
    # 收工合入必须等 CI：走 scripts/pr-merge.sh / make pr-merge
    # 仅匹配「作为命令调用」的 gh pr merge，避免 commit message / 文档误伤
    (
        r"(?:^|&&|\|\||;|\n)\s*(?:[A-Za-z_][A-Za-z0-9_]*=\S*\s+)*gh\s+pr\s+merge\b",
        "禁止裸 gh pr merge；用 make pr-merge PR=<n>（等 CI 绿再合）",
    ),
    # 破坏性 git 命令：防止误删未追踪文件或丢弃工作区
    (r"\bgit\s+clean\b.*-[a-zA-Z]*f", "禁止 git clean -f（防止未追踪文件丢失）"),
    (r"\bgit\s+checkout\b.*-(?:f\b|-force\b)", "禁止强制检出 git checkout -f（防止工作区丢失）"),
    # 禁止通过 shell 重定向/拷贝写入敏感文件（.env* / deploy/secrets/）
    (
        r"(?:>|>>|\btee\s+(?:-[a-zA-Z]+\s+)*)\s*(?:[^\s;]+\/)?(?:\.env(?:\.[a-zA-Z0-9_-]+)?|deploy\/secrets\/[^\s;|&]+)\b",
        "禁止通过 shell 写入密钥文件（.env* / deploy/secrets/）",
    ),
    (
        r"\b(?:cp|mv)\s+.*?\s+(?:[^\s;]+\/)?(?:\.env(?:\.[a-zA-Z0-9_-]+)?|deploy\/secrets\/[^\s;|&]+)\b",
        "禁止拷贝/移动至密钥文件（.env* / deploy/secrets/）",
    ),
]


def main() -> int:
    payload = load_payload()
    cmd = extract_command(payload)
    for pat, reason in DENY_PATTERNS:
        if re.search(pat, cmd, re.I):
            return emit_deny(f"harness deny: {reason} — {cmd[:120]}", payload)
    return emit_allow(payload)


if __name__ == "__main__":
    raise SystemExit(main())
