from wc2026.team_mapping import normalize_team_name


def test_normalize_known_alias():
    assert normalize_team_name("Korea Republic") == "South Korea"
    assert normalize_team_name("USA") == "United States"


def test_normalize_unknown_returns_input():
    assert normalize_team_name("Germany") == "Germany"
    assert normalize_team_name("Brazil") == "Brazil"
