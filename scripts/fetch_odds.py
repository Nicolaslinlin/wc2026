"""Pull bookmaker odds, reverse-engineer xG, write market_predictions table.

Matches odds events to fixtures rows by (home_team, away_team) name pair.
Uses median spread/total/h2h across bookmakers to reduce single-book noise.
"""
from __future__ import annotations

import statistics
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from wc2026.db import get_connection
from wc2026.market import xg_from_spread_total
from wc2026.odds_api import get_odds
from wc2026.poisson import DC_RHO, most_likely_score, outcome_probabilities
from wc2026.team_mapping import normalize_team_name

# Tiered refresh intervals based on time-to-kickoff of the next match.
# The Odds API free quota is 500/month; the tiered design keeps us well under
# that while reacting fast when bookmakers are actively moving lines.
HOT_INTERVAL = timedelta(minutes=20)   # match within HOT_HORIZON → lines moving fast
WARM_INTERVAL = timedelta(hours=3)     # match within WARM_HORIZON
COLD_INTERVAL = timedelta(hours=8)     # nothing imminent

HOT_HORIZON = timedelta(hours=3)
WARM_HORIZON = timedelta(hours=24)

# The Odds API uses slightly different team names; map them to martj42 style
# (same canonical form our fixtures table uses).
ODDS_API_ALIASES = {
    "United States of America": "United States",
    "South Korea": "South Korea",
    "Korea Republic": "South Korea",
    "Ivory Coast": "Côte d'Ivoire",
}


def _canon(name: str) -> str:
    name = ODDS_API_ALIASES.get(name, name)
    return normalize_team_name(name)


def _aggregate_market(event: dict) -> dict | None:
    """Aggregate spread + total across bookmakers; xG and probs come from Poisson."""
    spreads = []
    totals = []
    book_names = []

    home_name = _canon(event["home_team"])

    for book in event.get("bookmakers", []):
        book_names.append(book["title"])
        for market in book.get("markets", []):
            key = market["key"]
            outcomes = market.get("outcomes", [])
            if key == "spreads":
                for o in outcomes:
                    if _canon(o["name"]) == home_name and "point" in o:
                        spreads.append(o["point"])
                        break
            elif key == "totals":
                for o in outcomes:
                    if o["name"] == "Over" and "point" in o:
                        totals.append(o["point"])
                        break

    if not spreads or not totals:
        return None

    return {
        "spread_home": statistics.median(spreads),
        "total_goals": statistics.median(totals),
        "bookmaker": f"median of {len(book_names)} books",
    }


def _next_kickoff(db_path: Path) -> "datetime | None":
    """Earliest kickoff among matches not yet finished."""
    now = datetime.now(timezone.utc)
    with get_connection(db_path) as conn:
        rows = conn.execute(
            "SELECT utc_kickoff FROM fixtures "
            "WHERE status != 'FINISHED' "
            "ORDER BY utc_kickoff"
        ).fetchall()
    for r in rows:
        kickoff = datetime.fromisoformat(r["utc_kickoff"].replace("Z", "+00:00"))
        if kickoff >= now:
            return kickoff
    return None


def required_interval(db_path: Path) -> tuple[timedelta, str]:
    """Return (interval, tier name) based on time-to-next-kickoff."""
    kickoff = _next_kickoff(db_path)
    if kickoff is None:
        return COLD_INTERVAL, "cold"
    time_to_match = kickoff - datetime.now(timezone.utc)
    if time_to_match <= HOT_HORIZON:
        return HOT_INTERVAL, "hot"
    if time_to_match <= WARM_HORIZON:
        return WARM_INTERVAL, "warm"
    return COLD_INTERVAL, "cold"


def _should_refresh(db_path: Path) -> bool:
    if "--force" in sys.argv:
        return True
    with get_connection(db_path) as conn:
        row = conn.execute(
            "SELECT MAX(updated_at) AS last FROM market_predictions"
        ).fetchone()
    last = row["last"] if row else None
    interval, tier = required_interval(db_path)
    if not last:
        print(f"[odds] no prior fetch; refreshing (tier={tier})")
        return True
    last_dt = datetime.fromisoformat(last)
    if last_dt.tzinfo is None:
        last_dt = last_dt.replace(tzinfo=timezone.utc)
    age = datetime.now(timezone.utc) - last_dt
    if age >= interval:
        print(f"[odds] tier={tier} interval={interval} age={age}; refreshing")
        return True
    print(f"[odds] tier={tier} interval={interval} age={age}; skipping")
    return False


def main() -> int:
    db_path = Path(__file__).parent.parent / "data" / "wc2026.db"
    if not _should_refresh(db_path):
        print("Odds were refreshed recently; skipping to save API quota. Pass --force to override.")
        return 0
    events = get_odds()
    print(f"Fetched {len(events)} events with odds from The Odds API")

    # build lookup: (home, away) -> match_id
    with get_connection(db_path) as conn:
        fixtures = {
            (r["home_team"], r["away_team"]): r["match_id"]
            for r in conn.execute(
                "SELECT match_id, home_team, away_team FROM fixtures"
            )
        }

    rows = []
    matched = 0
    skipped_no_match = 0
    skipped_no_data = 0
    now = datetime.now(timezone.utc).isoformat()

    for ev in events:
        home = _canon(ev["home_team"])
        away = _canon(ev["away_team"])
        match_id = fixtures.get((home, away))
        if match_id is None:
            skipped_no_match += 1
            continue

        agg = _aggregate_market(ev)
        if agg is None:
            skipped_no_data += 1
            continue

        xh, xa = xg_from_spread_total(agg["spread_home"], agg["total_goals"])
        # outcome probabilities + most-likely score from market-derived xG
        # via our existing Poisson + Dixon-Coles correction
        ph, pd, pa = outcome_probabilities(xh, xa, rho=DC_RHO)
        sh, sa = most_likely_score(xh, xa, rho=DC_RHO)

        rows.append((
            match_id, sh, sa, ph, pd, pa, xh, xa,
            agg["spread_home"], agg["total_goals"], agg["bookmaker"], now,
        ))
        matched += 1

    with get_connection(db_path) as conn:
        # don't wipe rows we couldn't refresh — only upsert what we have
        conn.executemany(
            "INSERT OR REPLACE INTO market_predictions "
            "(match_id, mkt_home_score, mkt_away_score, mkt_prob_home_win, "
            " mkt_prob_draw, mkt_prob_away_win, mkt_home_xg, mkt_away_xg, "
            " spread_home, total_goals, bookmaker, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            rows,
        )

    print(
        f"Matched {matched} fixtures · skipped {skipped_no_match} (no fixture) "
        f"+ {skipped_no_data} (insufficient market data)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
