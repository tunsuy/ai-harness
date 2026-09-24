"""Shared scaffold path helpers for init / upgrade."""
from __future__ import annotations

import json
import re
from pathlib import Path

# Project fill — never overwrite on init --force or upgrade
PROTECT = frozenset(
    {
        "docs/harness/handoff.md",
        "docs/harness/domains.yaml",
        "docs/harness/invariants.md",
        "docs/harness/policy.yaml",
        "docs/harness/tasks.yaml",
        "docs/design/DESIGN.md",
        "docs/design/references.md",  # 按仓定制「取什么/不取什么」
        "docs/product-pipeline.md",
        "docs/architecture.md",
        "docs/glossary.md",
        "skills-lock.json",  # init --force 不覆盖；upgrade 时无本地漂移可快进（见 lock_is_fast_forward）
        "AGENTS.md",
        "GEMINI.md",
    }
)

# Exact engine files (not under a prefix below)
ENGINE_EXACT = frozenset(
    {
        "Makefile.harness.mk",
        "docs/harness/README.md",
        "docs/harness/handoff.template.md",
        "docs/features/README.md",
        "docs/features/_accept-checklist.md",
        "docs/design/README.md",
        "docs/decisions/README.md",
    }
)

# Prefixes: everything under these is engine (unless PROTECT)
ENGINE_PREFIXES = (
    "scripts/",
    ".cursor/",
    ".agents/",
    ".claude/",
    ".codex/",
    "docs/features/_TEMPLATE/",
    "docs/design/references/",
    "docs/playbooks/",
)

SKIP_NAMES = {".DS_Store", "__pycache__"}

TEXT_SUFFIXES = {
    ".md",
    ".mdc",
    ".yaml",
    ".yml",
    ".json",
    ".py",
    ".sh",
    ".mk",
    ".txt",
    ".js",
    "",
}
TEXT_NAMES = {"Makefile.harness.mk", "GEMINI.md", "AGENTS.md"}


def package_root() -> Path:
    here = Path(__file__).resolve().parent
    # src layout (repo / editable install): src/ai_harness/scaffold
    cand = here / "scaffold"
    if cand.is_dir():
        return here
    # legacy repo layout: scaffold/ next to src/
    cand2 = here.parents[1] / "scaffold"
    if cand2.is_dir():
        return here.parents[1]
    raise FileNotFoundError(
        "Cannot find scaffold/. Install from the ai-harness repo (pip install -e .)"
    )


def scaffold_dir() -> Path:
    root = package_root()
    s = root / "scaffold"
    if not s.is_dir():
        raise FileNotFoundError(f"missing {s}")
    return s


def is_engine_path(rel: str) -> bool:
    if rel in PROTECT:
        return False
    if rel in ENGINE_EXACT:
        return True
    return any(rel == p.rstrip("/") or rel.startswith(p) for p in ENGINE_PREFIXES)


def lock_is_fast_forward(project_lock: Path, engine_lock: Path) -> bool:
    """skills-lock.json 可否在 upgrade 时安全快进到引擎锁。

    项目锁是引擎锁的「无漂移子集」才快进：version 一致，且每个条目在
    引擎锁中同名整条相等（含 computedHash / source / skillPath）。项目
    锁缺失视为空子集（可直接写入引擎锁）。任一 JSON 解析失败 / version
    不同 / 项目有引擎没有的条目 / 共有条目不同 → False（按 PROTECT 提示手动合并）。
    """
    try:
        engine = json.loads(engine_lock.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    if not isinstance(engine, dict):
        return False

    if not project_lock.is_file():
        project = {"version": engine.get("version"), "skills": {}}
    else:
        try:
            project = json.loads(project_lock.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return False
        if not isinstance(project, dict):
            return False

    if project.get("version") != engine.get("version"):
        return False

    eng_skills = engine.get("skills") or {}
    prj_skills = project.get("skills") or {}
    if not isinstance(eng_skills, dict) or not isinstance(prj_skills, dict):
        return False

    return all(eng_skills.get(name) == entry for name, entry in prj_skills.items())


def substitute(text: str, mapping: dict[str, str]) -> str:
    for k, v in mapping.items():
        text = text.replace("{{" + k + "}}", v)
    return text


def iter_scaffold_files(src: Path):
    for path in sorted(src.rglob("*")):
        if path.name in SKIP_NAMES or any(p in SKIP_NAMES for p in path.parts):
            continue
        if path.is_dir():
            continue
        yield path, path.relative_to(src).as_posix()


def write_scaffold_file(
    path: Path,
    out: Path,
    *,
    mapping: dict[str, str] | None = None,
) -> None:
    """Copy one scaffold file to out, applying {{PLACEHOLDER}} substitution for text."""
    mapping = mapping or {}
    out.parent.mkdir(parents=True, exist_ok=True)
    raw = path.read_bytes()
    if path.suffix in TEXT_SUFFIXES or path.name in TEXT_NAMES:
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            out.write_bytes(raw)
        else:
            out.write_text(substitute(text, mapping), encoding="utf-8")
    else:
        out.write_bytes(raw)

    if path.suffix == ".sh" or path.name.endswith(".sh"):
        out.chmod(out.stat().st_mode | 0o111)
    if path.suffix == ".py" and "hooks" in path.parts:
        out.chmod(out.stat().st_mode | 0o111)


def ensure_makefile_include(dest: Path, project: str) -> str | None:
    """Ensure Makefile includes Makefile.harness.mk. Returns relative note or None."""
    include_line = "include Makefile.harness.mk"
    mk = dest / "Makefile"
    if mk.is_file():
        body = mk.read_text(encoding="utf-8")
        if include_line not in body and "handoff:" not in body:
            mk.write_text(
                body.rstrip() + "\n\n# ai-harness\n" + include_line + "\n",
                encoding="utf-8",
            )
            return "Makefile (appended include)"
        return None
    mk.write_text(f"# {project}\n\ninclude Makefile.harness.mk\n", encoding="utf-8")
    return "Makefile"


def detect_project_name(dest: Path) -> str:
    """Detect the project's name for {{PROJECT_NAME}} substitution on upgrade.

    Reads the first heading of AGENTS.md (``# AGENTS.md — <Name> …`` or
    ``# <Name> …``); falls back to the directory name. init-time substitution
    uses the --name flag; upgrade has no flag, so it recovers the name from
    existing project fill.
    """
    agents = dest / "AGENTS.md"
    if agents.is_file():
        try:
            lines = agents.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            lines = []
        for line in lines:
            s = line.strip()
            if not s.startswith("# "):
                continue
            body = s[2:].strip()
            m = re.match(r"^AGENTS\.md\s*[—–-]\s*(\S+)", body, re.IGNORECASE)
            if m:
                return m.group(1).rstrip("：:（(")
            if body:
                return body.split()[0].rstrip("：:—-（(")
            break
    return dest.name
