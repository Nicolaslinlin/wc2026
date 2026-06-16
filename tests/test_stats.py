"""Tests for cumulative model vs market accuracy stats."""
from __future__ import annotations

from scripts.render import compute_stats, build_timeline


def _finished(home, away, ph, pa, mh=None, ma=None, kickoff="2026-06-14T19:00:00Z"):
    return {
        "status": "FINISHED",
        "utc_kickoff": kickoff,
        "home_score": home, "away_score": away,
        "pred_home_score": ph, "pred_away_score": pa,
        "mkt_home_score": mh, "mkt_away_score": ma,
    }


def _upcoming():
    return {
        "status": "TIMED",
        "utc_kickoff": "2026-06-20T19:00:00Z",
        "home_score": None, "away_score": None,
        "pred_home_score": 1, "pred_away_score": 1,
        "mkt_home_score": 1, "mkt_away_score": 0,
    }


def test_stats_zero_finished_returns_zero_counts():
    s = compute_stats([_upcoming()])
    assert s["finished_total"] == 0
    assert s["model_outcome_hit_pct"] == 0
    assert s["market_outcome_hit_pct"] == 0


def test_stats_model_outcome_hit():
    # actual 2-0, model 3-0 → outcome (H) hit, score miss
    rows = [_finished(2, 0, 3, 0)]
    s = compute_stats(rows)
    assert s["finished_total"] == 1
    assert s["model_outcome_hit_pct"] == 100
    assert s["model_score_hit_pct"] == 0


def test_stats_market_outcome_separately_counted():
    # one match with model hit + market miss
    rows = [_finished(1, 0, 1, 0, mh=0, ma=1)]
    s = compute_stats(rows)
    assert s["model_outcome_hit_pct"] == 100
    assert s["market_outcome_hit_pct"] == 0
    assert s["market_total"] == 1


def test_stats_market_total_excludes_unmarketed_matches():
    rows = [
        _finished(1, 0, 1, 0),                 # no market data
        _finished(2, 1, 2, 1, mh=2, ma=1),     # has market, hit
    ]
    s = compute_stats(rows)
    assert s["finished_total"] == 2
    assert s["market_total"] == 1
    assert s["market_score_hit_pct"] == 100


def test_timeline_orders_chronologically_and_accumulates():
    rows = [
        _finished(0, 1, 1, 0, kickoff="2026-06-15T00:00:00Z"),  # model miss
        _finished(2, 0, 2, 0, kickoff="2026-06-14T00:00:00Z"),  # model hit (earlier)
    ]
    t = build_timeline(rows)
    assert len(t) == 2
    assert t[0]["model_rate"] == 1.0   # earliest first match: hit
    assert t[1]["model_rate"] == 0.5   # one hit out of two


def test_timeline_skips_unfinished():
    rows = [_finished(1, 0, 1, 0), _upcoming()]
    t = build_timeline(rows)
    assert len(t) == 1
