import sqlite3
from typing import Generator
from app.core.config import get_settings

def get_db() -> sqlite3.Connection:
    """
    Returns a connected sqlite3.Connection.
    We return rows as dictionaries for easy migration from Supabase.
    """
    settings = get_settings()
    # It's recommended to set check_same_thread=False for FastAPI / Starlette,
    # because they might run dependencies in different threads of a threadpool.
    # We rely on transactions and short-lived connections anyway, or the caller
    # making sure it doesn't leak. Still, we will open a new connection per call
    # since sqlite3 is extremely fast to connect.
    conn = sqlite3.connect(settings.sqlite_db_path, check_same_thread=False)
    
    # Factory to act like a dictionary
    def dict_factory(cursor, row):
        return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
        
    conn.row_factory = dict_factory
    return conn
