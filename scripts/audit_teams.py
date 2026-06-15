"""Audit current fixtures for team-name coverage in Chinese names and flag maps.

Prints any team name in the DB that is missing a Chinese display name or
a flag emoji. Run after `load_fixtures` / `update_results` to catch
unmapped countries before they hit the live page.

Usage:
    uv run python -m scripts.audit_teams
"""
from __future__ import annotations

import sys
from pathlib import Path

from scripts.render import FLAGS
from wc2026.db import get_connection
from wc2026.team_names_cn import CHINESE_NAMES

# Acceptable placeholders that we intentionally don't translate
IGNORED = {"TBD", "", None}


def main() -> int:
    db_path = Path(__file__).parent.parent / "data" / "wc2026.db"
    with get_connection(db_path) as conn:
        teams = {
            r[0]
            for r in conn.execute(
                "SELECT DISTINCT home_team FROM fixtures "
                "UNION SELECT DISTINCT away_team FROM fixtures"
            )
            if r[0] not in IGNORED
        }

    missing_cn = sorted(t for t in teams if t not in CHINESE_NAMES)
    missing_flag = sorted(t for t in teams if t not in FLAGS)

    if not missing_cn and not missing_flag:
        print(f"✓ All {len(teams)} team names have Chinese name + flag.")
        return 0

    if missing_cn:
        print(f"Missing Chinese name ({len(missing_cn)}):")
        for t in missing_cn:
            print(f"  - {t!r}")

    if missing_flag:
        print(f"Missing flag emoji ({len(missing_flag)}):")
        for t in missing_flag:
            print(f"  - {t!r}")

    # exit non-zero so CI can fail-fast if we ever add this to the workflow
    return 1


if __name__ == "__main__":
    sys.exit(main())
