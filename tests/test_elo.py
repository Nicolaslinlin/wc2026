from wc2026.elo import expected_score, update_ratings, INITIAL_RATING


def test_initial_rating_is_1500():
    assert INITIAL_RATING == 1500


def test_expected_score_equal_ratings_is_half():
    assert expected_score(1500, 1500) == 0.5


def test_expected_score_higher_rating_favored():
    assert expected_score(1700, 1500) > 0.5
    assert expected_score(1500, 1700) < 0.5


def test_update_ratings_winner_gains():
    new_home, new_away = update_ratings(1500, 1500, home_score=2, away_score=0)
    assert new_home > 1500
    assert new_away < 1500


def test_update_ratings_draw_balances():
    new_home, new_away = update_ratings(1500, 1500, home_score=1, away_score=1)
    assert new_home == 1500
    assert new_away == 1500


def test_update_ratings_zero_sum():
    new_home, new_away = update_ratings(1600, 1400, home_score=1, away_score=2)
    assert abs((new_home - 1600) + (new_away - 1400)) < 1e-9


def test_goal_difference_amplifies_change():
    big_win = update_ratings(1500, 1500, home_score=5, away_score=0)
    small_win = update_ratings(1500, 1500, home_score=1, away_score=0)
    assert big_win[0] - 1500 > small_win[0] - 1500
