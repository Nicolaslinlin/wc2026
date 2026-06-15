"""Refresh fixtures table with latest scores and statuses."""
from __future__ import annotations

import sys
from pathlib import Path

from scripts.load_fixtures import upsert_fixtures
from wc2026.api import get_matches


def main() -> int:
    db_path = Path(__file__).parent.parent / "data" / "wc2026.db"
    matches = get_matches()
    n = upsert_fixtures(matches, db_path)
    print(f"Refreshed {n} fixtures (statuses/scores)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
