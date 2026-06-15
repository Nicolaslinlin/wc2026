"""Download international match results CSV and load into matches_history.

Source: https://github.com/martj42/international_results (public CSV, no auth).
"""
from __future__ import annotations

import sys
from io import StringIO
from pathlib import Path

import pandas as pd
import requests

from wc2026.db import get_connection

CSV_URL = (
    "https://raw.githubusercontent.com/martj42/international_results/master/"
    "results.csv"
)


def fetch_csv(url: str = CSV_URL) -> pd.DataFrame:
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    return pd.read_csv(StringIO(resp.text))


def load_into_db(df: pd.DataFrame, db_path: Path) -> int:
    df = df[["date", "home_team", "away_team", "home_score", "away_score", "tournament"]]
    df = df.dropna(subset=["home_score", "away_score"])
    df = df.copy()
    df["home_score"] = df["home_score"].astype(int)
    df["away_score"] = df["away_score"].astype(int)

    # keep last 3 years for training relevance
    cutoff = pd.Timestamp.now("UTC").tz_localize(None) - pd.Timedelta(days=3 * 365)
    df["date_ts"] = pd.to_datetime(df["date"])
    df = df[df["date_ts"] >= cutoff].drop(columns=["date_ts"])

    rows = df.to_records(index=False).tolist()
    with get_connection(db_path) as conn:
        conn.execute("DELETE FROM matches_history")
        conn.executemany(
            "INSERT OR REPLACE INTO matches_history "
            "(date, home_team, away_team, home_score, away_score, tournament) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            rows,
        )
    return len(rows)


def main() -> int:
    db_path = Path(__file__).parent.parent / "data" / "wc2026.db"
    print(f"Downloading {CSV_URL}...")
    df = fetch_csv()
    print(f"Loaded {len(df)} rows from CSV, filtering and writing to DB...")
    n = load_into_db(df, db_path)
    print(f"Inserted {n} historical matches into {db_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
