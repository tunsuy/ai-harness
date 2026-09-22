"""Shared scaffold path helpers for init / upgrade."""
from __future__ import annotations

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
        "docs/product-pipeline.md",
        "docs/architecture.md",
        "docs/glossary.md",
        "AGENTS.md",
        "GEMINI.md",
    }
)

# Exact engine files (not under a prefix below)
ENGINE_EXACT = frozenset(
    {
        "Makefile.harness.mk",
        "skills-lock.json",
        "docs/harness/README.md",
        "docs/harness/handoff.template.md",
        "docs/features/README.md",
        "docs/features/_accept-checklist.md",
        "docs/design/README.md",
        "docs/design/references.md",
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
