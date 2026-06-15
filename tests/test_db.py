import sqlite3

from wc2026.db import init_db, get_connection


def test_init_db_creates_tables(tmp_path):
    db_path = tmp_path / "test.db"
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    tables = {row[0] for row in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )}
    assert tables == {"matches_history", "fixtures", "predictions"}


def test_get_connection_returns_sqlite_conn(tmp_path):
    db_path = tmp_path / "test.db"
    init_db(db_path)
    with get_connection(db_path) as conn:
        assert isinstance(conn, sqlite3.Connection)
