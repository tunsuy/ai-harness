"""CLI entry: ai-harness / python -m ai_harness."""
from __future__ import annotations

import argparse
import sys

from ai_harness import __version__
from ai_harness.init import run_init


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="ai-harness",
        description="AI-native project harness: init scaffold into a repo",
    )
    ap.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="Copy harness scaffold into a project")
    p_init.add_argument(
        "--target",
        default=".",
        help="Project root (default: cwd)",
    )
    p_init.add_argument("--name", default="", help="Project display name")
    p_init.add_argument(
        "--one-liner",
        default="",
        help="One-line product definition for AGENTS.md",
    )
    p_init.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing scaffold files (never handoff.md)",
    )

    p_up = sub.add_parser(
        "upgrade",
        help="Update engine files from a newer ai-harness (planned)",
    )
    p_up.add_argument("--target", default=".")

    args = ap.parse_args(argv)
    if args.cmd == "init":
        return run_init(
            target=args.target,
            name=args.name,
            one_liner=args.one_liner,
            force=args.force,
        )
    if args.cmd == "upgrade":
        print(
            "upgrade: not implemented yet. "
            "Re-run init --force on engine paths only, or sync from scaffold/ manually.",
            file=sys.stderr,
        )
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
