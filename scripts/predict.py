"""Compute Elo from history + finished fixtures, then predict every fixture."""
from __future__ import annotations

import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from wc2026.db import get_connection
from wc2026.elo import INITIAL_RATING, update_ratings
from wc2026.poisson import (
    lambda_from_elo,
    most_likely_score,
    outcome_probabilities,
)


def compute_current_elo(db_path: Path) -> dict[str, float]:
    ratings: dict[str, float] = defaultdict(lambda: INITIAL_RATING)
    with get_connection(db_path) as conn:
        history = conn.execute(
            "SELECT date, home_team, away_team, home_score, away_score "
            "FROM matches_history ORDER BY date"
        ).fetchall()
        finished = conn.execute(
            "SELECT utc_kickoff AS date, home_team, away_team, "
            "home_score, away_score FROM fixtures "
            "WHERE status='FINISHED' AND home_score IS NOT NULL "
            "ORDER BY utc_kickoff"
        ).fetchall()
    for row in list(history) + list(finished):
        h, a = ratings[row["home_team"]], ratings[row["away_team"]]
        new_h, new_a = update_ratings(
            h, a,
            home_score=row["home_score"],
            away_score=row["away_score"],
        )
        ratings[row["home_team"]] = new_h
        ratings[row["away_team"]] = new_a
    return dict(ratings)


def predict_all(db_path: Path, ratings: dict[str, float]) -> int:
    now = datetime.now(timezone.utc).isoformat()
    with get_connection(db_path) as conn:
        fixtures = conn.execute(
            "SELECT match_id, home_team, away_team FROM fixtures"
        ).fetchall()
        rows = []
        for f in fixtures:
            # skip placeholders (e.g. knockout slots with team TBD)
            if f["home_team"] in (None, "TBD", "") or f["away_team"] in (None, "TBD", ""):
                continue
            home_elo = ratings.get(f["home_team"], INITIAL_RATING)
            away_elo = ratings.get(f["away_team"], INITIAL_RATING)
            # World Cup: no real home advantage (except for host nations,
            # which we ignore for simplicity)
            lam_h, lam_a = lambda_from_elo(home_elo, away_elo, home_advantage=0.0)
            ph, pd, pa = outcome_probabilities(lam_h, lam_a)
            sh, sa = most_likely_score(lam_h, lam_a)
            rows.append((
                f["match_id"], sh, sa, ph, pd, pa, lam_h, lam_a, now,
            ))
        conn.execute("DELETE FROM predictions")
        conn.executemany(
            "INSERT INTO predictions "
            "(match_id, pred_home_score, pred_away_score, prob_home_win, "
            " prob_draw, prob_away_win, home_xg, away_xg, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            rows,
        )
    return len(rows)


def main() -> int:
    db_path = Path(__file__).parent.parent / "data" / "wc2026.db"
    ratings = compute_current_elo(db_path)
    n = predict_all(db_path, ratings)
    print(f"Predictions written for {n} fixtures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
