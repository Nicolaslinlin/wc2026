"""Tests for the tiered refresh logic in fetch_odds."""
from datetime import datetime, timedelta, timezone

from scripts.fetch_odds import (
    COLD_INTERVAL,
    HOT_INTERVAL,
    WARM_INTERVAL,
    required_interval,
)
from wc2026.db import get_connection, init_db


def _insert_fixture(db_path, match_id, kickoff_dt, status="TIMED"):
    with get_connection(db_path) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO fixtures "
            "(match_id, utc_kickoff, stage, group_code, venue, home_team, "
            " away_team, status, home_score, away_score) "
            "VALUES (?, ?, 'GROUP_STAGE', 'A', '', 'A', 'B', ?, NULL, NULL)",
            (match_id, kickoff_dt.isoformat().replace("+00:00", "Z"), status),
        )


def test_required_interval_no_upcoming_matches_is_cold(tmp_path):
    db = tmp_path / "test.db"
    init_db(db)
    interval, tier = required_interval(db)
    assert tier == "cold"
    assert interval == COLD_INTERVAL


def test_required_interval_match_within_3h_is_hot(tmp_path):
    db = tmp_path / "test.db"
    init_db(db)
    _insert_fixture(db, 1, datetime.now(timezone.utc) + timedelta(hours=2))
    interval, tier = required_interval(db)
    assert tier == "hot"
    assert interval == HOT_INTERVAL


def test_required_interval_match_within_24h_is_warm(tmp_path):
    db = tmp_path / "test.db"
    init_db(db)
    _insert_fixture(db, 1, datetime.now(timezone.utc) + timedelta(hours=10))
    interval, tier = required_interval(db)
    assert tier == "warm"
    assert interval == WARM_INTERVAL


def test_required_interval_match_far_future_is_cold(tmp_path):
    db = tmp_path / "test.db"
    init_db(db)
    _insert_fixture(db, 1, datetime.now(timezone.utc) + timedelta(days=2))
    interval, tier = required_interval(db)
    assert tier == "cold"
    assert interval == COLD_INTERVAL


def test_required_interval_picks_earliest_upcoming(tmp_path):
    """When there are multiple matches, the earliest non-finished kickoff wins."""
    db = tmp_path / "test.db"
    init_db(db)
    _insert_fixture(db, 1, datetime.now(timezone.utc) + timedelta(days=3))
    _insert_fixture(db, 2, datetime.now(timezone.utc) + timedelta(hours=1))
    _insert_fixture(db, 3, datetime.now(timezone.utc) + timedelta(days=5))
    interval, tier = required_interval(db)
    assert tier == "hot"


def test_required_interval_ignores_finished_matches(tmp_path):
    """Finished matches in the past shouldn't trigger hot mode."""
    db = tmp_path / "test.db"
    init_db(db)
    _insert_fixture(
        db, 1, datetime.now(timezone.utc) + timedelta(hours=1), status="FINISHED"
    )
    _insert_fixture(db, 2, datetime.now(timezone.utc) + timedelta(days=2))
    interval, tier = required_interval(db)
    assert tier == "cold"


def test_required_interval_ignores_past_matches(tmp_path):
    """A scheduled match in the past (data lag) should not be considered upcoming."""
    db = tmp_path / "test.db"
    init_db(db)
    _insert_fixture(db, 1, datetime.now(timezone.utc) - timedelta(hours=5))
    _insert_fixture(db, 2, datetime.now(timezone.utc) + timedelta(days=2))
    interval, tier = required_interval(db)
    assert tier == "cold"
