from __future__ import annotations

import math

BASE_LAMBDA = 1.35
ELO_BETA = 0.0035
# Dixon-Coles low-score correlation (1997). Empirical value for soccer
# is slightly negative — increases P(0-0) and P(1-1), decreases P(0-1) and P(1-0).
DC_RHO = -0.13


def lambda_from_elo(
    home_elo: float,
    away_elo: float,
    *,
    home_advantage: float = 0.15,
) -> tuple[float, float]:
    diff = home_elo - away_elo
    lam_h = BASE_LAMBDA * math.exp(ELO_BETA * diff + home_advantage)
    lam_a = BASE_LAMBDA * math.exp(-ELO_BETA * diff)
    return lam_h, lam_a


def _poisson_pmf(k: int, lam: float) -> float:
    return math.exp(-lam) * lam**k / math.factorial(k)


def _dc_tau(i: int, j: int, lam_h: float, lam_a: float, rho: float) -> float:
    """Dixon-Coles low-score multiplier. Returns 1 outside {0,1} x {0,1}."""
    if i == 0 and j == 0:
        return 1.0 - lam_h * lam_a * rho
    if i == 0 and j == 1:
        return 1.0 + lam_h * rho
    if i == 1 and j == 0:
        return 1.0 + lam_a * rho
    if i == 1 and j == 1:
        return 1.0 - rho
    return 1.0


def score_matrix(
    home_xg: float,
    away_xg: float,
    max_goals: int = 8,
    rho: float = 0.0,
) -> list[list[float]]:
    """matrix[i][j] = P(home=i, away=j). rho=0 → independent Poisson."""
    home_pmf = [_poisson_pmf(i, home_xg) for i in range(max_goals + 1)]
    away_pmf = [_poisson_pmf(j, away_xg) for j in range(max_goals + 1)]
    matrix = [[h * a for a in away_pmf] for h in home_pmf]
    if rho != 0.0:
        cap = min(2, max_goals + 1)
        for i in range(cap):
            for j in range(cap):
                matrix[i][j] *= _dc_tau(i, j, home_xg, away_xg, rho)
    return matrix


def outcome_probabilities(
    home_xg: float, away_xg: float, rho: float = 0.0
) -> tuple[float, float, float]:
    m = score_matrix(home_xg, away_xg, rho=rho)
    n = len(m)
    home_win = sum(m[i][j] for i in range(n) for j in range(i))
    draw = sum(m[i][i] for i in range(n))
    away_win = sum(m[i][j] for i in range(n) for j in range(i + 1, n))
    return home_win, draw, away_win


def most_likely_score(
    home_xg: float, away_xg: float, rho: float = 0.0
) -> tuple[int, int]:
    m = score_matrix(home_xg, away_xg, rho=rho)
    best_i, best_j, best_p = 0, 0, -1.0
    for i, row in enumerate(m):
        for j, p in enumerate(row):
            if p > best_p:
                best_i, best_j, best_p = i, j, p
    return best_i, best_j
