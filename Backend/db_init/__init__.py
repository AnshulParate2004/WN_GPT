"""WellnessGPT database initialization."""
import db_init._path  # noqa: F401

from db_init.initializer import init_db

__all__ = ["init_db"]
