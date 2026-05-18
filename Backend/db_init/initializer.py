"""SQLite database initialization from schema + seed SQL."""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path

import db_init._path  # noqa: F401

from app.core.config import get_settings

_SQL_DIR = Path(__file__).resolve().parent / "sql"
_BACKEND_ROOT = Path(__file__).resolve().parents[1]


def _resolve_db_path() -> Path:
    settings = get_settings()
    db_path = Path(settings.sqlite_db_path)
    if not db_path.is_absolute():
        db_path = _BACKEND_ROOT / db_path
    return db_path


def _run_sql_script(cursor: sqlite3.Cursor, script_path: Path) -> None:
    print(f"Running {script_path.name}...")
    sql = script_path.read_text(encoding="utf-8")
    cursor.executescript(sql)


def init_db(*, reset: bool = True) -> Path:
    """
    Create the SQLite database from schema.sql and seed.sql.

    Args:
        reset: If True, delete an existing database file before initializing.

    Returns:
        Absolute path to the created database file.
    """
    db_path = _resolve_db_path()
    schema_path = _SQL_DIR / "schema.sql"
    seed_path = _SQL_DIR / "seed.sql"

    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    if not seed_path.exists():
        raise FileNotFoundError(f"Seed data not found: {seed_path}")

    print(f"Initializing database at: {db_path}")

    if reset and db_path.exists():
        os.remove(db_path)

    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    _run_sql_script(cursor, schema_path)
    _run_sql_script(cursor, seed_path)

    conn.commit()
    conn.close()

    uploads_dir = _BACKEND_ROOT / "uploads"
    uploads_dir.mkdir(exist_ok=True)
    print(f"Created uploads folder at: {uploads_dir}")
    print("Initialization complete.")

    return db_path
