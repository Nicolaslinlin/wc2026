from __future__ import annotations

INITIAL_RATING = 1500
K_FACTOR = 30


def expected_score(rating_a: float, rating_b: float) -> float:
    return 1.0 / (1.0 + 10 ** ((rating_b - rating_a) / 400))


def _goal_diff_multiplier(home_score: int, away_score: int) -> float:
    diff = abs(home_score - away_score)
    if diff <= 1:
        return 1.0
    if diff == 2:
        return 1.5
    return (11 + diff) / 8.0


def update_ratings(
    home_rating: float,
    away_rating: float,
    *,
    home_score: int,
    away_score: int,
    k: float = K_FACTOR,
) -> tuple[float, float]:
    expected_home = expected_score(home_rating, away_rating)
    if home_score > away_score:
        actual_home = 1.0
    elif home_score < away_score:
        actual_home = 0.0
    else:
        actual_home = 0.5
    multiplier = _goal_diff_multiplier(home_score, away_score)
    delta = k * multiplier * (actual_home - expected_home)
    return home_rating + delta, away_rating - delta
