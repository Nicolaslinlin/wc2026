"""Thin wrapper around football-data.org v4 API."""
from __future__ import annotations

import os
from typing import Any

import requests

BASE = "https://api.football-data.org/v4"
COMPETITION_CODE = "WC"  # FIFA World Cup


class APIError(RuntimeError):
    pass


def _headers() -> dict[str, str]:
    token = os.environ.get("FOOTBALL_DATA_TOKEN")
    if not token:
        raise APIError("FOOTBALL_DATA_TOKEN env var not set")
    return {"X-Auth-Token": token}


def get_matches() -> list[dict[str, Any]]:
    """Return all matches in the current World Cup competition."""
    resp = requests.get(
        f"{BASE}/competitions/{COMPETITION_CODE}/matches",
        headers=_headers(),
        timeout=30,
    )
    if resp.status_code != 200:
        raise APIError(f"API returned {resp.status_code}: {resp.text}")
    return resp.json().get("matches", [])
