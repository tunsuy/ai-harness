"""Tests for ai-harness upgrade / engine path selection."""
from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ai_harness.scaffold_io import PROTECT, is_engine_path, scaffold_dir  # noqa: E402
from ai_harness.upgrade import run_upgrade  # noqa: E402

STITCH_SKILLS = (
    "enhance-prompt",
    "stitch::generate-design",
    "stitch::manage-design-system",
)


def _engine_lock_text() -> str:
    return (scaffold_dir() / "skills-lock.json").read_text(encoding="utf-8")


def _write_subset_lock(dest: Path) -> None:
    """项目锁 = 引擎锁减 Stitch 条目（现实里 upgrade 跟不上引擎新 skill 的实况）。"""
    lock = json.loads(_engine_lock_text())
    for name in STITCH_SKILLS:
        lock["skills"].pop(name, None)
    (dest / "skills-lock.json").write_text(
        json.dumps(lock, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def test_engine_paths():
    assert is_engine_path("scripts/kb_sync.py")
    assert is_engine_path("Makefile.harness.mk")
    assert is_engine_path(".cursor/hooks/policy_lib.py")
    assert is_engine_path("docs/playbooks/define-feature.md")
    assert is_engine_path("docs/features/_TEMPLATE/prototype.md")
    assert is_engine_path("docs/design/references/README.md")
    assert not is_engine_path("docs/harness/handoff.md")
    assert not is_engine_path("docs/harness/domains.yaml")
    assert not is_engine_path("docs/design/DESIGN.md")
    assert not is_engine_path("docs/product-pipeline.md")
    assert not is_engine_path("AGENTS.md")
    assert not is_engine_path("docs/architecture.md")


def test_upgrade_preserves_protect_and_refreshes_engine():
    with tempfile.TemporaryDirectory() as td:
        dest = Path(td)
        (dest / "docs/harness").mkdir(parents=True)
        (dest / "docs/harness/handoff.md").write_text("PROJECT HANDOFF\n", encoding="utf-8")
        (dest / "docs/harness/domains.yaml").write_text("domains: {}\n", encoding="utf-8")
        (dest / "AGENTS.md").write_text("MY AGENTS\n", encoding="utf-8")
        (dest / "scripts").mkdir(parents=True)
        (dest / "scripts/kb_sync.py").write_text("# stale\n", encoding="utf-8")

        rc = run_upgrade(target=str(dest), dry_run=False)
        assert rc == 0
        assert (dest / "docs/harness/handoff.md").read_text(encoding="utf-8") == "PROJECT HANDOFF\n"
        assert (dest / "docs/harness/domains.yaml").read_text(encoding="utf-8") == "domains: {}\n"
        assert (dest / "AGENTS.md").read_text(encoding="utf-8") == "MY AGENTS\n"
        assert (dest / "scripts/kb_sync.py").read_text(encoding="utf-8") != "# stale\n"
        assert (dest / "Makefile.harness.mk").is_file()
        assert (dest / "docs/features/_TEMPLATE/prototype.md").is_file()


def test_upgrade_cli_dry_run():
    with tempfile.TemporaryDirectory() as td:
        dest = Path(td)
        (dest / "docs/harness").mkdir(parents=True)
        (dest / "docs/harness/handoff.md").write_text("x\n", encoding="utf-8")
        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT / "src")
        p = subprocess.run(
            [sys.executable, "-m", "ai_harness", "upgrade", "--target", str(dest), "--dry-run"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )
        assert p.returncode == 0, p.stderr + p.stdout
        assert "dry-run" in p.stdout
        assert not (dest / "Makefile.harness.mk").exists()


def test_protect_set_covers_doc_promise():
    for must in (
        "docs/harness/handoff.md",
        "docs/harness/domains.yaml",
        "docs/harness/invariants.md",
        "skills-lock.json",
    ):
        assert must in PROTECT


def _run_capture(dry_run: bool, dest: Path) -> tuple[int, str]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = run_upgrade(target=str(dest), dry_run=dry_run)
    return rc, buf.getvalue()


def test_upgrade_lock_fast_forward():
    with tempfile.TemporaryDirectory() as td:
        dest = Path(td)
        _write_subset_lock(dest)

        rc, out = _run_capture(dry_run=False, dest=dest)
        assert rc == 0
        got = json.loads((dest / "skills-lock.json").read_text(encoding="utf-8"))
        want = json.loads(_engine_lock_text())
        assert got == want
        assert "fast-forward" in out


def test_upgrade_lock_fast_forward_dry_run():
    with tempfile.TemporaryDirectory() as td:
        dest = Path(td)
        _write_subset_lock(dest)

        rc, out = _run_capture(dry_run=True, dest=dest)
        assert rc == 0
        lock = json.loads((dest / "skills-lock.json").read_text(encoding="utf-8"))
        assert all(name not in lock["skills"] for name in STITCH_SKILLS)
        assert "fast-forward" in out


def test_upgrade_lock_diverged_keeps_project():
    # a) 项目私有条目（业务 skill 只在项目锁）→ 不覆盖
    with tempfile.TemporaryDirectory() as td:
        dest = Path(td)
        lock = json.loads(_engine_lock_text())
        lock["skills"]["my-local"] = dict(lock["skills"]["animate"])
        original = json.dumps(lock, indent=2, ensure_ascii=False) + "\n"
        (dest / "skills-lock.json").write_text(original, encoding="utf-8")

        rc, out = _run_capture(dry_run=False, dest=dest)
        assert rc == 0
        assert (dest / "skills-lock.json").read_text(encoding="utf-8") == original
        assert "protected" in out

    # b) 共有条目 hash 漂移（项目自己 skills update 过）→ 不覆盖
    with tempfile.TemporaryDirectory() as td:
        dest = Path(td)
        lock = json.loads(_engine_lock_text())
        lock["skills"]["animate"]["computedHash"] = "x" + lock["skills"]["animate"]["computedHash"][1:]
        original = json.dumps(lock, indent=2, ensure_ascii=False) + "\n"
        (dest / "skills-lock.json").write_text(original, encoding="utf-8")

        rc, out = _run_capture(dry_run=False, dest=dest)
        assert rc == 0
        assert (dest / "skills-lock.json").read_text(encoding="utf-8") == original
        assert "protected" in out


def test_upgrade_lock_missing_added():
    with tempfile.TemporaryDirectory() as td:
        dest = Path(td)

        rc, out = _run_capture(dry_run=False, dest=dest)
        assert rc == 0
        got = json.loads((dest / "skills-lock.json").read_text(encoding="utf-8"))
        want = json.loads(_engine_lock_text())
        assert got == want
        assert "fast-forward" in out


if __name__ == "__main__":
    test_engine_paths()
    test_upgrade_preserves_protect_and_refreshes_engine()
    test_upgrade_cli_dry_run()
    test_protect_set_covers_doc_promise()
    test_upgrade_lock_fast_forward()
    test_upgrade_lock_fast_forward_dry_run()
    test_upgrade_lock_diverged_keeps_project()
    test_upgrade_lock_missing_added()
    print("ok")
