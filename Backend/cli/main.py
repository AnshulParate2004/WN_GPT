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

import cli._path  # noqa: F401 — bootstrap sys.path before app imports

from cli.session import run_session


def main() -> None:
    parser = argparse.ArgumentParser(description="WellnessGPT streaming CLI")
    parser.add_argument("--patient", "-p", default="P001", help="Patient ID (default: P001)")
    args = parser.parse_args()
    asyncio.run(run_session(args.patient))


if __name__ == "__main__":
    main()
