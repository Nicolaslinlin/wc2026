import math

from wc2026.poisson import (
    score_matrix,
    outcome_probabilities,
    most_likely_score,
    lambda_from_elo,
)


def test_score_matrix_sums_to_one():
    m = score_matrix(1.5, 1.0, max_goals=10)
    total = sum(sum(row) for row in m)
    assert math.isclose(total, 1.0, abs_tol=1e-3)


def test_score_matrix_shape():
    m = score_matrix(1.5, 1.0, max_goals=5)
    assert len(m) == 6
    assert all(len(row) == 6 for row in m)


def test_outcome_probabilities_sum_to_one():
    home_p, draw_p, away_p = outcome_probabilities(1.5, 1.0)
    assert math.isclose(home_p + draw_p + away_p, 1.0, abs_tol=1e-3)


def test_outcome_probabilities_favors_stronger():
    home_p, _, away_p = outcome_probabilities(2.5, 0.5)
    assert home_p > away_p


def test_most_likely_score_returns_tuple():
    score = most_likely_score(1.5, 1.0)
    assert isinstance(score, tuple)
    assert len(score) == 2
    assert all(isinstance(s, int) for s in score)


def test_most_likely_score_mismatch():
    h, a = most_likely_score(3.0, 0.3)
    assert h > a


def test_lambda_from_elo_equal_returns_baseline():
    lam_h, lam_a = lambda_from_elo(1500, 1500, home_advantage=0.0)
    assert math.isclose(lam_h, lam_a, abs_tol=1e-6)


def test_lambda_from_elo_higher_rating_gets_more_goals():
    lam_h, lam_a = lambda_from_elo(1700, 1500, home_advantage=0.0)
    assert lam_h > lam_a
