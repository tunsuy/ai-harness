"""Copy scaffold/ into a target project with light templating."""
from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path

# Never overwrite these on --force (project state / secrets of progress)
PROTECT = {
    "docs/harness/handoff.md",
    "docs/harness/domains.yaml",
    "docs/harness/invariants.md",
    "docs/harness/policy.yaml",
}

SKIP_NAMES = {".DS_Store", "__pycache__"}


def package_root() -> Path:
    # src/ai_harness/init.py → repo root (dev) or site-packages parent
    here = Path(__file__).resolve().parent
    # editable / source tree: .../ai-harness/src/ai_harness
    cand = here.parents[1] / "scaffold"
    if cand.is_dir():
        return here.parents[1]
    # installed: look for package data sibling (we keep scaffold next to package via path)
    cand2 = here / "scaffold"
    if cand2.is_dir():
        return here
    raise FileNotFoundError(
        "Cannot find scaffold/. Install from the ai-harness repo (pip install -e .)"
    )


def scaffold_dir() -> Path:
    root = package_root()
    s = root / "scaffold"
    if not s.is_dir():
        raise FileNotFoundError(f"missing {s}")
    return s


def substitute(text: str, mapping: dict[str, str]) -> str:
    for k, v in mapping.items():
        text = text.replace("{{" + k + "}}", v)
    return text


def run_init(
    *,
    target: str,
    name: str,
    one_liner: str,
    force: bool,
) -> int:
    dest = Path(target).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    src = scaffold_dir()

    project = name.strip() or dest.name
    blurb = one_liner.strip() or f"{project}（请改为一句话产品定义）"
    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
    # +0800 style: insert colon in offset if missing
    if len(now) >= 5 and now[-5] in "+-" and now[-3] != ":":
        now = now[:-2] + ":" + now[-2:]

    mapping = {
        "PROJECT_NAME": project,
        "PROJECT_ONE_LINER": blurb,
        "HANDOFF_UPDATED": now,
    }

    written: list[str] = []
    skipped: list[str] = []

    for path in sorted(src.rglob("*")):
        if path.name in SKIP_NAMES or any(p in SKIP_NAMES for p in path.parts):
            continue
        if path.is_dir():
            continue
        rel = path.relative_to(src).as_posix()
        out = dest / rel
        if out.exists() and not force:
            skipped.append(rel)
            continue
        if out.exists() and force and rel in PROTECT:
            skipped.append(f"{rel} (protected)")
            continue

        out.parent.mkdir(parents=True, exist_ok=True)
        raw = path.read_bytes()
        # text templates
        if path.suffix in {
            ".md",
            ".mdc",
            ".yaml",
            ".yml",
            ".json",
            ".py",
            ".sh",
            ".mk",
            ".txt",
            "",
        } or path.name in {"Makefile.harness.mk", "GEMINI.md", "AGENTS.md"}:
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

        written.append(rel)

    # Makefile include hint
    mk = dest / "Makefile"
    include_line = "include Makefile.harness.mk"
    if mk.is_file():
        body = mk.read_text(encoding="utf-8")
        if include_line not in body and "handoff:" not in body:
            mk.write_text(body.rstrip() + "\n\n# ai-harness\n" + include_line + "\n", encoding="utf-8")
            written.append("Makefile (appended include)")
    else:
        mk.write_text(
            f"# {project}\n\ninclude Makefile.harness.mk\n",
            encoding="utf-8",
        )
        written.append("Makefile")

    print(f"ai-harness init → {dest}")
    print(f"  project: {project}")
    print(f"  wrote:   {len(written)} files")
    if skipped:
        print(f"  skipped: {len(skipped)} (use --force to overwrite engine files)")
        for s in skipped[:12]:
            print(f"    - {s}")
        if len(skipped) > 12:
            print(f"    … +{len(skipped) - 12} more")
    print()
    print("Next:")
    print("  1. Edit docs/harness/invariants.md, domains.yaml, policy.yaml")
    print("  2. pip3 install -r scripts/requirements-kb.txt")
    print("  3. make kb-gen && make check-harness")
    print("  4. 有 UI：填 docs/design/DESIGN.md（tokens + lint: 块）→ make design-lint")
    print("  5. Open AGENTS.md — cold start from handoff")
    return 0
