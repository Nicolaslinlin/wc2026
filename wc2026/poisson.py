from __future__ import annotations

import math

BASE_LAMBDA = 1.35
ELO_BETA = 0.0035


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


def score_matrix(home_xg: float, away_xg: float, max_goals: int = 8) -> list[list[float]]:
    home_pmf = [_poisson_pmf(i, home_xg) for i in range(max_goals + 1)]
    away_pmf = [_poisson_pmf(j, away_xg) for j in range(max_goals + 1)]
    return [[h * a for a in away_pmf] for h in home_pmf]


def outcome_probabilities(home_xg: float, away_xg: float) -> tuple[float, float, float]:
    m = score_matrix(home_xg, away_xg)
    n = len(m)
    home_win = sum(m[i][j] for i in range(n) for j in range(i))
    draw = sum(m[i][i] for i in range(n))
    away_win = sum(m[i][j] for i in range(n) for j in range(i + 1, n))
    return home_win, draw, away_win


def most_likely_score(home_xg: float, away_xg: float) -> tuple[int, int]:
    m = score_matrix(home_xg, away_xg)
    best_i, best_j, best_p = 0, 0, -1.0
    for i, row in enumerate(m):
        for j, p in enumerate(row):
            if p > best_p:
                best_i, best_j, best_p = i, j, p
    return best_i, best_j
