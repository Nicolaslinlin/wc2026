import math

from wc2026.market import xg_from_spread_total, implied_probability


def test_xg_solves_spread_and_total():
    # 市场说：让球 -2（home 净胜 2 球），总进球 3.5
    # 解方程：xh - xa = 2, xh + xa = 3.5  → xh=2.75, xa=0.75
    xh, xa = xg_from_spread_total(spread_home=-2.0, total=3.5)
    assert math.isclose(xh, 2.75, abs_tol=1e-6)
    assert math.isclose(xa, 0.75, abs_tol=1e-6)


def test_xg_underdog_home():
    # home 是弱队：让球 +1.5（market 觉得 home 会净输 1.5）
    xh, xa = xg_from_spread_total(spread_home=1.5, total=2.5)
    # xh - xa = -1.5; xh + xa = 2.5 → xh=0.5, xa=2.0
    assert math.isclose(xh, 0.5, abs_tol=1e-6)
    assert math.isclose(xa, 2.0, abs_tol=1e-6)


def test_xg_floors_at_zero():
    # 极端情况：让球绝对值大于总进球 → 数学上会算出负 xG，要 floor 到 0
    xh, xa = xg_from_spread_total(spread_home=-5.0, total=3.0)
    assert xh >= 0
    assert xa >= 0


def test_implied_probability_h2h_normalizes():
    # 德 1.02 / 平 19 / 客 100 (decimal odds)
    # 原始隐含 1/1.02 + 1/19 + 1/100 ≈ 0.98 + 0.053 + 0.01 = 1.04（含 vig）
    # 归一化后概率和应该 = 1
    home, draw, away = implied_probability(1.02, 19.0, 100.0)
    assert math.isclose(home + draw + away, 1.0, abs_tol=1e-6)
    assert home > 0.9  # 强主队
    assert away < 0.05


def test_implied_probability_balanced_match():
    # 三个等概率赔率
    home, draw, away = implied_probability(3.0, 3.0, 3.0)
    assert math.isclose(home, draw, abs_tol=1e-6)
    assert math.isclose(home, away, abs_tol=1e-6)
