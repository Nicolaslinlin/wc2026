"""Reverse-engineer xG and probabilities from bookmaker markets.

Bookmakers price three soccer markets that together imply their goal model:
  - Asian handicap (spread): market expects (home_goals - away_goals) ≈ -spread_home
  - Total goals (O/U): market expects home + away ≈ total
  - Moneyline (h2h_3_way): direct win/draw/away probabilities with vig

We solve the first two as a 2x2 linear system to recover home_xg and away_xg.
We strip vig from h2h by simple normalization.
"""
from __future__ import annotations


def xg_from_spread_total(spread_home: float, total: float) -> tuple[float, float]:
    """Solve {xh - xa = -spread_home, xh + xa = total} for xh, xa.

    spread_home is the Asian handicap on the home team (negative = favored).
    Floor at 0 to avoid nonsensical negative goal expectations from extreme lines.
    """
    expected_diff = -spread_home  # home - away expected
    xh = (total + expected_diff) / 2.0
    xa = (total - expected_diff) / 2.0
    return max(xh, 0.0), max(xa, 0.0)


def implied_probability(
    home_odds: float, draw_odds: float, away_odds: float
) -> tuple[float, float, float]:
    """Convert decimal odds to vig-free probabilities by normalization."""
    raw_h = 1.0 / home_odds
    raw_d = 1.0 / draw_odds
    raw_a = 1.0 / away_odds
    total = raw_h + raw_d + raw_a
    return raw_h / total, raw_d / total, raw_a / total
