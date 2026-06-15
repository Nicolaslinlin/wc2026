import sqlite3
from contextlib import contextmanager
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS matches_history (
    date TEXT NOT NULL,
    home_team TEXT NOT NULL,
    away_team TEXT NOT NULL,
    home_score INTEGER NOT NULL,
    away_score INTEGER NOT NULL,
    tournament TEXT,
    PRIMARY KEY (date, home_team, away_team)
);

CREATE TABLE IF NOT EXISTS fixtures (
    match_id INTEGER PRIMARY KEY,
    utc_kickoff TEXT NOT NULL,
    stage TEXT NOT NULL,
    group_code TEXT,
    venue TEXT,
    home_team TEXT NOT NULL,
    away_team TEXT NOT NULL,
    status TEXT NOT NULL,
    home_score INTEGER,
    away_score INTEGER
);

CREATE TABLE IF NOT EXISTS predictions (
    match_id INTEGER PRIMARY KEY,
    pred_home_score INTEGER NOT NULL,
    pred_away_score INTEGER NOT NULL,
    prob_home_win REAL NOT NULL,
    prob_draw REAL NOT NULL,
    prob_away_win REAL NOT NULL,
    home_xg REAL NOT NULL,
    away_xg REAL NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (match_id) REFERENCES fixtures(match_id)
);

CREATE TABLE IF NOT EXISTS market_predictions (
    match_id INTEGER PRIMARY KEY,
    mkt_home_score INTEGER NOT NULL,
    mkt_away_score INTEGER NOT NULL,
    mkt_prob_home_win REAL NOT NULL,
    mkt_prob_draw REAL NOT NULL,
    mkt_prob_away_win REAL NOT NULL,
    mkt_home_xg REAL NOT NULL,
    mkt_away_xg REAL NOT NULL,
    spread_home REAL,
    total_goals REAL,
    bookmaker TEXT,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (match_id) REFERENCES fixtures(match_id)
);
"""


def init_db(path: Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.executescript(SCHEMA)


@contextmanager
def get_connection(path: Path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()
