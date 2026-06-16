"""Tests for model-vs-market divergence ranking."""
from __future__ import annotations

from scripts.render import find_top_divergences, total_variation_distance


def _row(mid, status, model_h, model_d, model_a,
         mkt_h=None, mkt_d=None, mkt_a=None):
    has_market = mkt_h is not None
    return {
        "match_id": mid,
        "status": status,
        "utc_kickoff": "2026-06-20T19:00:00Z",
        "home_team": "X", "away_team": "Y",
        "pred_home_score": 1, "pred_away_score": 1,
        "prob_home_win": model_h, "prob_draw": model_d, "prob_away_win": model_a,
        "mkt_home_score": 1 if has_market else None,
        "mkt_away_score": 1 if has_market else None,
        "mkt_prob_home_win": mkt_h,
        "mkt_prob_draw": mkt_d,
        "mkt_prob_away_win": mkt_a,
    }


def test_tvd_equal_distributions_is_zero():
    d = total_variation_distance((0.5, 0.3, 0.2), (0.5, 0.3, 0.2))
    assert d == 0


def test_tvd_opposite_distributions_is_one():
    d = total_variation_distance((1.0, 0.0, 0.0), (0.0, 0.0, 1.0))
    assert d == 1.0


def test_tvd_typical_case():
    # |0.8 - 0.5| + |0.15 - 0.25| + |0.05 - 0.25| → 0.3+0.1+0.2 = 0.6, /2 = 0.3
    d = total_variation_distance((0.8, 0.15, 0.05), (0.5, 0.25, 0.25))
    assert abs(d - 0.3) < 1e-9


def test_find_divergences_excludes_finished():
    rows = [
        _row(1, "FINISHED", 0.6, 0.2, 0.2, 0.3, 0.3, 0.4),
        _row(2, "TIMED",    0.6, 0.2, 0.2, 0.3, 0.3, 0.4),
    ]
    top = find_top_divergences(rows, n=5)
    assert len(top) == 1
    assert top[0]["match_id"] == 2


def test_find_divergences_excludes_no_market():
    rows = [
        _row(1, "TIMED", 0.6, 0.2, 0.2),  # no market
        _row(2, "TIMED", 0.6, 0.2, 0.2, 0.3, 0.3, 0.4),
    ]
    top = find_top_divergences(rows, n=5)
    assert len(top) == 1
    assert top[0]["match_id"] == 2


def test_find_divergences_sorted_descending():
    rows = [
        _row(1, "TIMED", 0.6, 0.2, 0.2, 0.55, 0.25, 0.20),  # small div
        _row(2, "TIMED", 0.9, 0.05, 0.05, 0.4, 0.3, 0.3),   # big div
        _row(3, "TIMED", 0.5, 0.3, 0.2, 0.45, 0.30, 0.25),  # smallest
    ]
    top = find_top_divergences(rows, n=5)
    assert [r["match_id"] for r in top] == [2, 1, 3]


def test_find_divergences_caps_at_n():
    rows = [_row(i, "TIMED", 0.5, 0.3, 0.2, 0.3, 0.3, 0.4) for i in range(10)]
    top = find_top_divergences(rows, n=3)
    assert len(top) == 3


def test_find_divergences_pct_field_added():
    rows = [_row(1, "TIMED", 0.8, 0.15, 0.05, 0.5, 0.25, 0.25)]
    top = find_top_divergences(rows, n=5)
    assert top[0]["divergence_pct"] == 30
