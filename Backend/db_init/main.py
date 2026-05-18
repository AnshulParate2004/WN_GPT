"""
WellnessGPT — Database initialization
────────────────────────────────────
Run from Backend/:
  uv run python -m db_init
  uv run wellness-db-init
"""
from __future__ import annotations

import argparse

import db_init._path  # noqa: F401

from db_init.initializer import init_db


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize WellnessGPT SQLite database")
    parser.add_argument(
        "--keep",
        action="store_true",
        help="Keep existing database file (append/update without deleting)",
    )
    args = parser.parse_args()
    init_db(reset=not args.keep)


if __name__ == "__main__":
    main()
