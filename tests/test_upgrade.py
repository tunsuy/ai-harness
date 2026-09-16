"""Tests for ai-harness upgrade / engine path selection."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ai_harness.scaffold_io import PROTECT, is_engine_path  # noqa: E402
from ai_harness.upgrade import run_upgrade  # noqa: E402


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
    ):
        assert must in PROTECT


if __name__ == "__main__":
    test_engine_paths()
    test_upgrade_preserves_protect_and_refreshes_engine()
    test_upgrade_cli_dry_run()
    test_protect_set_covers_doc_promise()
    print("ok")
