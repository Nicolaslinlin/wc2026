import math

from wc2026.poisson import (
    DC_RHO,
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


# --- Dixon-Coles low-score correction ---

def test_dc_rho_default_negative():
    """Empirically rho is slightly negative for soccer."""
    assert -0.2 < DC_RHO < 0.0


def test_dc_default_rho_zero_matches_independent_poisson():
    """Without rho (default 0), score_matrix is unchanged."""
    m_indep = score_matrix(1.5, 1.0)
    m_default = score_matrix(1.5, 1.0, rho=0.0)
    for i in range(len(m_indep)):
        for j in range(len(m_indep[0])):
            assert math.isclose(m_indep[i][j], m_default[i][j], abs_tol=1e-12)


def test_dc_increases_one_one_probability():
    """rho=-0.13 should make 1-1 more likely than independent Poisson."""
    indep = score_matrix(1.4, 1.2)[1][1]
    dc = score_matrix(1.4, 1.2, rho=-0.13)[1][1]
    assert dc > indep
    # 1-1 multiplier is (1 - rho), so increase factor is 1.13
    assert math.isclose(dc / indep, 1.13, rel_tol=1e-6)


def test_dc_score_matrix_still_sums_to_one():
    """DC adjustment preserves total probability (key mathematical property)."""
    m = score_matrix(1.5, 1.0, rho=-0.13, max_goals=10)
    total = sum(sum(row) for row in m)
    assert math.isclose(total, 1.0, abs_tol=1e-3)


def test_dc_outcome_probabilities_accepts_rho():
    h, d, a = outcome_probabilities(1.5, 1.0, rho=-0.13)
    assert math.isclose(h + d + a, 1.0, abs_tol=1e-3)
    # DC raises draw probability vs independent Poisson
    _, d_indep, _ = outcome_probabilities(1.5, 1.0, rho=0.0)
    assert d > d_indep


def test_dc_most_likely_score_accepts_rho():
    s = most_likely_score(1.4, 1.2, rho=-0.13)
    assert isinstance(s, tuple) and len(s) == 2
