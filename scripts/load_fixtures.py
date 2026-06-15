"""Fetch 2026 World Cup fixtures from football-data.org and upsert into DB."""
from __future__ import annotations

import sys
from pathlib import Path

from wc2026.api import get_matches
from wc2026.db import get_connection
from wc2026.team_mapping import normalize_team_name


def upsert_fixtures(matches: list[dict], db_path: Path) -> int:
    rows = []
    for m in matches:
        home = normalize_team_name(m["homeTeam"]["name"] or "TBD")
        away = normalize_team_name(m["awayTeam"]["name"] or "TBD")
        score = m.get("score", {}).get("fullTime", {})
        rows.append((
            m["id"],
            m["utcDate"],
            m.get("stage", "UNKNOWN"),
            m.get("group"),
            (m.get("venue") or ""),
            home,
            away,
            m.get("status", "SCHEDULED"),
            score.get("home"),
            score.get("away"),
        ))

    with get_connection(db_path) as conn:
        conn.executemany(
            "INSERT OR REPLACE INTO fixtures "
            "(match_id, utc_kickoff, stage, group_code, venue, home_team, "
            " away_team, status, home_score, away_score) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            rows,
        )
    return len(rows)


def main() -> int:
    db_path = Path(__file__).parent.parent / "data" / "wc2026.db"
    matches = get_matches()
    n = upsert_fixtures(matches, db_path)
    print(f"Upserted {n} fixtures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
