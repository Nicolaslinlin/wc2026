"""Thin wrapper around The Odds API v4 for FIFA World Cup soccer odds.

Token is read from ODDS_API_TOKEN env var. Free plan: 500 requests/month.
"""
from __future__ import annotations

import os
from typing import Any

import requests

BASE = "https://api.the-odds-api.com/v4"
SPORT = "soccer_fifa_world_cup"
MARKETS = "h2h_3_way,spreads,totals"
REGIONS = "uk,eu"


class OddsAPIError(RuntimeError):
    pass


def _params(extra: dict[str, Any] | None = None) -> dict[str, Any]:
    token = os.environ.get("ODDS_API_TOKEN")
    if not token:
        raise OddsAPIError("ODDS_API_TOKEN env var not set")
    base = {"apiKey": token}
    if extra:
        base.update(extra)
    return base


def get_odds() -> list[dict[str, Any]]:
    """Return all current World Cup matches with bookmaker odds."""
    resp = requests.get(
        f"{BASE}/sports/{SPORT}/odds",
        params=_params({
            "regions": REGIONS,
            "markets": MARKETS,
            "oddsFormat": "decimal",
        }),
        timeout=30,
    )
    if resp.status_code != 200:
        raise OddsAPIError(f"API returned {resp.status_code}: {resp.text}")
    return resp.json()
