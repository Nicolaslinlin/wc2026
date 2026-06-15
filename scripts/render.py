"""Render fixtures + predictions into public/index.html."""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from jinja2 import Environment, FileSystemLoader, select_autoescape

from wc2026.db import get_connection
from wc2026.team_names_cn import to_chinese

FLAGS = {
    "Germany": "🇩🇪", "Curaçao": "🇨🇼", "Brazil": "🇧🇷", "Argentina": "🇦🇷",
    "France": "🇫🇷", "Spain": "🇪🇸", "England": "🏴", "Portugal": "🇵🇹",
    "Netherlands": "🇳🇱", "Italy": "🇮🇹", "Belgium": "🇧🇪", "Croatia": "🇭🇷",
    "Mexico": "🇲🇽", "United States": "🇺🇸", "Canada": "🇨🇦", "Japan": "🇯🇵",
    "South Korea": "🇰🇷", "Australia": "🇦🇺", "Morocco": "🇲🇦", "Senegal": "🇸🇳",
    "Côte d'Ivoire": "🇨🇮", "Ecuador": "🇪🇨", "Uruguay": "🇺🇾", "Colombia": "🇨🇴",
    "Switzerland": "🇨🇭", "Denmark": "🇩🇰", "Poland": "🇵🇱", "Iran": "🇮🇷",
    "Saudi Arabia": "🇸🇦", "Qatar": "🇶🇦", "Tunisia": "🇹🇳", "Ghana": "🇬🇭",
    "Cameroon": "🇨🇲", "Egypt": "🇪🇬", "Nigeria": "🇳🇬", "Algeria": "🇩🇿",
    "Wales": "🏴", "Scotland": "🏴", "Serbia": "🇷🇸",
    "Cape Verde": "🇨🇻", "Norway": "🇳🇴", "Austria": "🇦🇹",
    "Czech Republic": "🇨🇿", "Sweden": "🇸🇪", "Romania": "🇷🇴",
    "Turkey": "🇹🇷", "Greece": "🇬🇷", "Ukraine": "🇺🇦", "Russia": "🇷🇺",
    "New Zealand": "🇳🇿", "Costa Rica": "🇨🇷", "Panama": "🇵🇦",
    "Honduras": "🇭🇳", "Jamaica": "🇯🇲", "Paraguay": "🇵🇾", "Peru": "🇵🇪",
    "Chile": "🇨🇱", "Venezuela": "🇻🇪", "Bolivia": "🇧🇴",
    "South Africa": "🇿🇦", "Mali": "🇲🇱", "Burkina Faso": "🇧🇫",
    "DR Congo": "🇨🇩", "Zambia": "🇿🇲", "Uzbekistan": "🇺🇿",
    "Jordan": "🇯🇴", "Iraq": "🇮🇶",
    "Bosnia and Herzegovina": "🇧🇦",
    "Republic of the Congo": "🇨🇬",
    "Haiti": "🇭🇹",
    "Slovakia": "🇸🇰",
    "New Caledonia": "🇳🇨",
}

STAGE_LABELS = {
    "GROUP_STAGE": "小组赛",
    "LAST_16": "1/8 决赛",
    "ROUND_OF_16": "1/8 决赛",
    "QUARTER_FINALS": "1/4 决赛",
    "SEMI_FINALS": "半决赛",
    "THIRD_PLACE": "三四名",
    "FINAL": "决赛",
}


def _outcome(home: int, away: int) -> str:
    if home > away:
        return "H"
    if home < away:
        return "A"
    return "D"


def build_match_view(row: dict[str, Any]) -> dict[str, Any]:
    kickoff_utc = datetime.fromisoformat(row["utc_kickoff"].replace("Z", "+00:00"))
    kickoff_local = kickoff_utc.astimezone(ZoneInfo("Asia/Tokyo"))
    is_finished = row["status"] == "FINISHED" and row.get("home_score") is not None
    outcome_hit = score_hit = False
    if is_finished:
        actual = _outcome(row["home_score"], row["away_score"])
        predicted = _outcome(row["pred_home_score"], row["pred_away_score"])
        outcome_hit = actual == predicted
        score_hit = (
            row["home_score"] == row["pred_home_score"]
            and row["away_score"] == row["pred_away_score"]
        )
    weekday_zh = "日一二三四五六"[kickoff_local.weekday()]  # mon=0
    # weekday() returns 0=mon..6=sun; rearrange so 日 is sun
    weekday_zh = ["一", "二", "三", "四", "五", "六", "日"][kickoff_local.weekday()]
    has_market = row.get("mkt_home_score") is not None
    market_outcome_hit = market_score_hit = False
    if is_finished and has_market:
        actual = _outcome(row["home_score"], row["away_score"])
        mkt = _outcome(row["mkt_home_score"], row["mkt_away_score"])
        market_outcome_hit = actual == mkt
        market_score_hit = (
            row["home_score"] == row["mkt_home_score"]
            and row["away_score"] == row["mkt_away_score"]
        )
    return {
        "match_id": row["match_id"],
        "kickoff_local": kickoff_local.strftime(f"%m/%d ({weekday_zh}) %H:%M JST"),
        "stage": row["stage"],
        "stage_label": STAGE_LABELS.get(row["stage"], row["stage"]),
        "group_code": row["group_code"],
        "venue": row["venue"],
        "home_team": to_chinese(row["home_team"]),
        "away_team": to_chinese(row["away_team"]),
        "home_flag": FLAGS.get(row["home_team"], "🏳"),
        "away_flag": FLAGS.get(row["away_team"], "🏳"),
        "status": row["status"] if is_finished else "UPCOMING",
        "home_score": row.get("home_score"),
        "away_score": row.get("away_score"),
        "pred_home": row["pred_home_score"],
        "pred_away": row["pred_away_score"],
        "prob_home_pct": round(row["prob_home_win"] * 100),
        "prob_draw_pct": round(row["prob_draw"] * 100),
        "prob_away_pct": round(row["prob_away_win"] * 100),
        "outcome_hit": outcome_hit,
        "score_hit": score_hit,
        "has_market": has_market,
        "mkt_home": row.get("mkt_home_score"),
        "mkt_away": row.get("mkt_away_score"),
        "mkt_prob_home_pct": round(row["mkt_prob_home_win"] * 100) if has_market else None,
        "mkt_prob_draw_pct": round(row["mkt_prob_draw"] * 100) if has_market else None,
        "mkt_prob_away_pct": round(row["mkt_prob_away_win"] * 100) if has_market else None,
        "market_outcome_hit": market_outcome_hit,
        "market_score_hit": market_score_hit,
    }


def render(matches: list[dict], updated_at: str, out_path: Path,
           template_dir: Path) -> None:
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html"]),
    )
    template = env.get_template("index.html.j2")
    html = template.render(matches=matches, updated_at=updated_at)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")


def main() -> int:
    project_root = Path(__file__).parent.parent
    db_path = project_root / "data" / "wc2026.db"
    out_path = project_root / "public" / "index.html"
    template_dir = project_root / "templates"

    with get_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT f.match_id, f.utc_kickoff, f.stage, f.group_code, f.venue,
                   f.home_team, f.away_team, f.status, f.home_score, f.away_score,
                   p.pred_home_score, p.pred_away_score,
                   p.prob_home_win, p.prob_draw, p.prob_away_win,
                   p.home_xg, p.away_xg,
                   m.mkt_home_score, m.mkt_away_score,
                   m.mkt_prob_home_win, m.mkt_prob_draw, m.mkt_prob_away_win
            FROM fixtures f
            LEFT JOIN predictions p USING (match_id)
            LEFT JOIN market_predictions m USING (match_id)
            ORDER BY f.utc_kickoff
            """
        ).fetchall()

    matches = [build_match_view(dict(r)) for r in rows
               if r["pred_home_score"] is not None]
    updated = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M JST")
    render(matches, updated, out_path, template_dir)
    print(f"Rendered {len(matches)} matches to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
