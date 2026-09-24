"""Upgrade engine files in an existing project from the current scaffold."""
from __future__ import annotations

import filecmp
from pathlib import Path

from ai_harness.scaffold_io import (
    PROTECT,
    detect_project_name,
    ensure_makefile_include,
    is_engine_path,
    iter_scaffold_files,
    lock_is_fast_forward,
    scaffold_dir,
    write_scaffold_file,
)


def run_upgrade(*, target: str, dry_run: bool = False) -> int:
    dest = Path(target).resolve()
    if not dest.is_dir():
        print(f"upgrade: target is not a directory: {dest}")
        return 2

    src = scaffold_dir()
    # Engine files carry {{PROJECT_*}} placeholders; upgrade recovers the
    # project's name from existing fill (AGENTS.md heading / dir name) so
    # substitution matches what init produced, never regressing it to the
    # literal placeholder.
    project = detect_project_name(dest)
    mapping = {"PROJECT_NAME": project}

    updated: list[str] = []
    added: list[str] = []
    unchanged: list[str] = []
    lock_ff: list[str] = []
    protected_hint: list[str] = []

    for path, rel in iter_scaffold_files(src):
        if rel in PROTECT:
            out = dest / rel
            if rel == "skills-lock.json":
                # 升级特例：无本地漂移的项目锁可快进到引擎锁（见 lock_is_fast_forward）
                if out.is_file() and path.is_file() and filecmp.cmp(path, out, shallow=False):
                    unchanged.append(rel)
                elif lock_is_fast_forward(out, path):
                    if not dry_run:
                        write_scaffold_file(path, out, mapping=mapping)
                    lock_ff.append(rel)
                elif out.is_file():
                    protected_hint.append(rel)
                continue
            if out.is_file() and path.is_file() and not filecmp.cmp(path, out, shallow=False):
                protected_hint.append(rel)
            continue
        if not is_engine_path(rel):
            continue

        out = dest / rel
        if out.is_file() and filecmp.cmp(path, out, shallow=False):
            unchanged.append(rel)
            continue

        if dry_run:
            (updated if out.exists() else added).append(rel)
            continue

        existed = out.exists()
        write_scaffold_file(path, out, mapping=mapping)
        (updated if existed else added).append(rel)

    mk_note: str | None = None
    if not dry_run:
        mk_note = ensure_makefile_include(dest, dest.name)
        if mk_note:
            added.append(mk_note)

    label = "ai-harness upgrade (dry-run)" if dry_run else "ai-harness upgrade"
    print(f"{label} → {dest}")
    print(f"  updated:   {len(updated)}")
    print(f"  added:     {len(added)}")
    print(f"  unchanged: {len(unchanged)}")
    print(f"  lock ff:   {len(lock_ff)}")
    for title, items in (("updated", updated), ("added", added)):
        if not items:
            continue
        print(f"  — {title}:")
        for s in items[:20]:
            print(f"    - {s}")
        if len(items) > 20:
            print(f"    … +{len(items) - 20} more")

    if lock_ff:
        print("  — fast-forwarded (engine skills merged in; no local lock edits detected):")
        for s in lock_ff:
            print(f"    - {s}")

    if protected_hint:
        print()
        print(
            "  protected (not overwritten; scaffold differs — merge manually if needed):"
        )
        for s in protected_hint[:12]:
            print(f"    - {s}")
        if len(protected_hint) > 12:
            print(f"    … +{len(protected_hint) - 12} more")

    print()
    print("Engine only. Never touches: domains.yaml / invariants.md / handoff.md /")
    print("  policy.yaml / tasks.yaml / DESIGN.md / product-pipeline.md / AGENTS.md …")
    print("skills-lock.json: fast-forwarded only if it is an unmodified subset of the")
    print("  engine lock; a locally updated lock (npx skills update) is kept + hinted.")
    if dry_run:
        print("Re-run without --dry-run to apply.")
    else:
        print("Next: make check-harness")
    return 0
