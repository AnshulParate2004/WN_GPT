"""
WellnessGPT — Streaming CLI
───────────────────────────
Run from Backend/:
  uv run python -m cli
  uv run python -m cli --patient P002
  uv run wellnessgpt
"""
from __future__ import annotations

import argparse
import asyncio
import sys

import cli._path  # noqa: F401

from cli.branding import ensure_utf8_stdio
from cli.session import run_session
from cli.theme import VERSION, make_console


def main() -> int:
    ensure_utf8_stdio()
    parser = argparse.ArgumentParser(
        prog="wellnessgpt",
        description="WellnessGPT — 15-agent healthcare AI (streaming CLI)",
    )
    parser.add_argument("--patient", "-p", default="P001", help="Patient ID (default: P001)")
    parser.add_argument("--version", "-V", action="version", version=f"WellnessGPT CLI {VERSION}")
    args = parser.parse_args()

    try:
        return asyncio.run(run_session(args.patient))
    except KeyboardInterrupt:
        console = make_console()
        console.print("\n[dim]Interrupted. Goodbye.[/dim]")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
