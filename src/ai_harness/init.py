"""Copy scaffold/ into a target project with light templating."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from ai_harness.scaffold_io import (
    PROTECT,
    ensure_makefile_include,
    iter_scaffold_files,
    scaffold_dir,
    write_scaffold_file,
)


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
    if len(now) >= 5 and now[-5] in "+-" and now[-3] != ":":
        now = now[:-2] + ":" + now[-2:]

    mapping = {
        "PROJECT_NAME": project,
        "PROJECT_ONE_LINER": blurb,
        "HANDOFF_UPDATED": now,
    }

    written: list[str] = []
    skipped: list[str] = []

    for path, rel in iter_scaffold_files(src):
        out = dest / rel
        if out.exists() and not force:
            skipped.append(rel)
            continue
        if out.exists() and force and rel in PROTECT:
            skipped.append(f"{rel} (protected)")
            continue

        write_scaffold_file(path, out, mapping=mapping)
        written.append(rel)

    mk_note = ensure_makefile_include(dest, project)
    if mk_note:
        written.append(mk_note)

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
    print()
    print("Later: ai-harness upgrade  # refresh engine files only")
    return 0
