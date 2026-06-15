"""Map football-data.org team names to martj42 international_results names."""

ALIAS = {
    "Korea Republic": "South Korea",
    "Korea DPR": "North Korea",
    "USA": "United States",
    "Czechia": "Czech Republic",
    "Ivory Coast": "Côte d'Ivoire",
    "Cabo Verde": "Cape Verde",
    "Türkiye": "Turkey",
}


def normalize_team_name(name: str) -> str:
    return ALIAS.get(name, name)
