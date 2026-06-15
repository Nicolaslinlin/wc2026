from pathlib import Path

from scripts.render import build_match_view, render


def _row(home_score, away_score, pred_h, pred_a, status="FINISHED"):
    return {
        "match_id": 1,
        "utc_kickoff": "2026-06-14T19:00:00Z",
        "stage": "GROUP_STAGE",
        "group_code": "E",
        "venue": "Houston",
        "home_team": "Germany",
        "away_team": "Curaçao",
        "status": status,
        "home_score": home_score,
        "away_score": away_score,
        "pred_home_score": pred_h,
        "pred_away_score": pred_a,
        "prob_home_win": 0.92,
        "prob_draw": 0.05,
        "prob_away_win": 0.03,
        "home_xg": 3.0,
        "away_xg": 0.3,
    }


def test_build_match_view_finished_score_hit():
    v = build_match_view(_row(3, 0, 3, 0))
    assert v["outcome_hit"] is True
    assert v["score_hit"] is True
    assert v["prob_home_pct"] == 92


def test_build_match_view_outcome_hit_score_miss():
    v = build_match_view(_row(4, 0, 3, 0))
    assert v["outcome_hit"] is True
    assert v["score_hit"] is False


def test_build_match_view_outcome_miss():
    v = build_match_view(_row(0, 1, 3, 0))
    assert v["outcome_hit"] is False
    assert v["score_hit"] is False


def test_build_match_view_upcoming():
    v = build_match_view(_row(None, None, 3, 0, status="TIMED"))
    assert v["outcome_hit"] is False
    assert v["score_hit"] is False


def test_render_writes_html(tmp_path):
    out = tmp_path / "index.html"
    project_root = Path(__file__).parent.parent
    render(
        matches=[],
        updated_at="2026-06-14 18:00",
        out_path=out,
        template_dir=project_root / "templates",
    )
    text = out.read_text(encoding="utf-8")
    assert "2026 世界杯预测" in text
    assert "2026-06-14 18:00" in text
