from pathlib import Path

from wc2026.db import init_db

if __name__ == "__main__":
    db_path = Path(__file__).parent.parent / "data" / "wc2026.db"
    init_db(db_path)
    print(f"Initialized DB at {db_path}")
