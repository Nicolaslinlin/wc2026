"""Translation dictionaries for UI strings and country names (en/ja).

The default rendered language is Chinese. JavaScript on the page swaps
data-i18n elements and country names using these dictionaries.
"""

# UI string translations keyed by data-i18n="<key>"
UI_STRINGS = {
    # Header
    "title": {"zh": "2026 世界杯预测", "en": "2026 World Cup Predictor", "ja": "2026 ワールドカップ予測"},
    "tag_model": {"zh": "模型", "en": "MODEL", "ja": "モデル"},
    "tag_score": {"zh": "比分", "en": "SCORES", "ja": "結果"},
    "tag_odds": {"zh": "盘口", "en": "ODDS", "ja": "オッズ"},
    "model_name": {"zh": "Elo + 泊松 + Dixon-Coles", "en": "Elo + Poisson + Dixon-Coles", "ja": "Elo + ポアソン + Dixon-Coles"},
    "score_refresh": {"zh": "每 20 分钟 刷新一次", "en": "Refreshed every 20 min", "ja": "20 分ごとに更新"},
    "odds_tiered": {
        "zh": "临赛 3h 内 <strong>20 分钟</strong> · 24h 内 <strong>3 小时</strong> · 其他 <strong>8 小时</strong>",
        "en": "&lt;3h to KO: <strong>20 min</strong> · &lt;24h: <strong>3 hours</strong> · else: <strong>8 hours</strong>",
        "ja": "試合 3h 前: <strong>20 分</strong> · 24h 内: <strong>3 時間</strong> · その他: <strong>8 時間</strong>",
    },
    "updated": {"zh": "最后更新", "en": "Last update", "ja": "最終更新"},

    # Dashboard
    "dashboard_title": {"zh": "📊 累计命中率", "en": "📊 Cumulative Hit Rate", "ja": "📊 累計的中率"},
    "finished_count": {"zh": "已结束 {n} 场", "en": "{n} matches finished", "ja": "終了 {n} 試合"},
    "model_outcome": {"zh": "模型 · 胜负", "en": "Model · Outcome", "ja": "モデル · 勝敗"},
    "model_score": {"zh": "模型 · 比分", "en": "Model · Score", "ja": "モデル · スコア"},
    "market_outcome": {"zh": "市场 · 胜负", "en": "Market · Outcome", "ja": "市場 · 勝敗"},
    "market_score": {"zh": "市场 · 比分", "en": "Market · Score", "ja": "市場 · スコア"},
    "stat_sample": {"zh": "/ {n} 场", "en": "/ {n} matches", "ja": "/ {n} 試合"},
    "dashboard_empty": {
        "zh": "还没有已结束的比赛 · 等比赛开始就有数据了 ⚽",
        "en": "No finished matches yet · Data will arrive as games end ⚽",
        "ja": "まだ終了した試合はありません · 試合終了後にデータが入ります ⚽",
    },
    "legend_model": {"zh": "模型胜负命中率", "en": "Model outcome accuracy", "ja": "モデル勝敗的中率"},
    "legend_market": {"zh": "市场胜负命中率", "en": "Market outcome accuracy", "ja": "市場勝敗的中率"},

    # Divergences
    "div_title": {"zh": "🎯 模型 vs 市场 · 分歧最大", "en": "🎯 Model vs Market · Top Divergences", "ja": "🎯 モデル vs 市場 · 乖離の大きい試合"},
    "div_subtitle": {"zh": "点击跳转到完整卡片", "en": "Click to jump to match card", "ja": "クリックで試合カードへ"},
    "div_badge_label": {"zh": "分歧", "en": "Δ", "ja": "乖離"},

    # Filters
    "filter_all": {"zh": "全部", "en": "All", "ja": "全て"},
    "filter_group": {"zh": "小组赛", "en": "Group", "ja": "グループ"},
    "filter_knockout": {"zh": "淘汰赛", "en": "Knockout", "ja": "決勝T"},
    "filter_finished": {"zh": "已结束", "en": "Finished", "ja": "終了"},
    "filter_upcoming": {"zh": "未开始", "en": "Upcoming", "ja": "未開始"},

    # Match card
    "model_pred": {"zh": "模型预测", "en": "Model", "ja": "モデル予測"},
    "market_pred": {"zh": "市场预测", "en": "Market", "ja": "市場予測"},
    "odds_unavailable": {"zh": "盘口未挂出", "en": "No odds yet", "ja": "オッズ未開示"},
    "home_win": {"zh": "主胜", "en": "H", "ja": "ホーム"},
    "draw": {"zh": "平", "en": "D", "ja": "分"},
    "away_win": {"zh": "客胜", "en": "A", "ja": "アウェイ"},
    "outcome_hit": {"zh": "✓ 胜负", "en": "✓ Outcome", "ja": "✓ 勝敗"},
    "outcome_miss": {"zh": "✗ 胜负", "en": "✗ Outcome", "ja": "✗ 勝敗"},
    "score_hit": {"zh": "✓ 比分", "en": "✓ Score", "ja": "✓ スコア"},
    "score_miss": {"zh": "✗ 比分", "en": "✗ Score", "ja": "✗ スコア"},
    "no_odds": {"zh": "无盘口", "en": "no odds", "ja": "オッズなし"},
    "upcoming_label": {"zh": "⏳ 未开始", "en": "⏳ Upcoming", "ja": "⏳ 未開始"},

    # Stage labels (used in meta line)
    "stage_GROUP_STAGE": {"zh": "小组赛", "en": "Group", "ja": "グループ"},
    "stage_LAST_16": {"zh": "1/8 决赛", "en": "Round of 16", "ja": "ラウンド 16"},
    "stage_ROUND_OF_16": {"zh": "1/8 决赛", "en": "Round of 16", "ja": "ラウンド 16"},
    "stage_QUARTER_FINALS": {"zh": "1/4 决赛", "en": "Quarter-final", "ja": "準々決勝"},
    "stage_SEMI_FINALS": {"zh": "半决赛", "en": "Semi-final", "ja": "準決勝"},
    "stage_THIRD_PLACE": {"zh": "三四名", "en": "Third place", "ja": "3 位決定戦"},
    "stage_FINAL": {"zh": "决赛", "en": "Final", "ja": "決勝"},

    # Footer
    "footer_data": {"zh": "数据", "en": "Data", "ja": "データ"},
    "footer_history": {"zh": "历史", "en": "History", "ja": "履歴"},
    "footer_model": {"zh": "模型", "en": "Model", "ja": "モデル"},
    "footer_disclaimer": {
        "zh": "这是一个学习项目，预测仅供娱乐",
        "en": "Learning project · entertainment only",
        "ja": "学習プロジェクト · 娯楽のみ",
    },
    "footer_source": {"zh": "源码", "en": "Source", "ja": "ソース"},
}


# Country names: English → Japanese (Katakana for most; established Kanji for select ones)
# Default behavior: en uses the English key as-is; ja uses this dict.
JAPANESE_NAMES = {
    "Germany": "ドイツ", "Curaçao": "キュラソー", "Brazil": "ブラジル", "Argentina": "アルゼンチン",
    "France": "フランス", "Spain": "スペイン", "England": "イングランド", "Portugal": "ポルトガル",
    "Netherlands": "オランダ", "Italy": "イタリア", "Belgium": "ベルギー", "Croatia": "クロアチア",
    "Mexico": "メキシコ", "United States": "アメリカ", "Canada": "カナダ", "Japan": "日本",
    "South Korea": "韓国", "Australia": "オーストラリア", "Morocco": "モロッコ", "Senegal": "セネガル",
    "Côte d'Ivoire": "コートジボワール", "Ecuador": "エクアドル", "Uruguay": "ウルグアイ", "Colombia": "コロンビア",
    "Switzerland": "スイス", "Denmark": "デンマーク", "Poland": "ポーランド", "Iran": "イラン",
    "Saudi Arabia": "サウジアラビア", "Qatar": "カタール", "Tunisia": "チュニジア", "Ghana": "ガーナ",
    "Cameroon": "カメルーン", "Egypt": "エジプト", "Nigeria": "ナイジェリア", "Algeria": "アルジェリア",
    "Wales": "ウェールズ", "Scotland": "スコットランド", "Serbia": "セルビア",
    "Cape Verde": "カーボベルデ", "Norway": "ノルウェー", "Austria": "オーストリア",
    "Czech Republic": "チェコ", "Sweden": "スウェーデン", "Romania": "ルーマニア",
    "Turkey": "トルコ", "Greece": "ギリシャ", "Ukraine": "ウクライナ", "Russia": "ロシア",
    "New Zealand": "ニュージーランド", "Costa Rica": "コスタリカ", "Panama": "パナマ",
    "Honduras": "ホンジュラス", "Jamaica": "ジャマイカ", "Paraguay": "パラグアイ", "Peru": "ペルー",
    "Chile": "チリ", "Venezuela": "ベネズエラ", "Bolivia": "ボリビア",
    "South Africa": "南アフリカ", "Mali": "マリ", "Burkina Faso": "ブルキナファソ",
    "DR Congo": "コンゴ民主共和国", "Zambia": "ザンビア", "Uzbekistan": "ウズベキスタン",
    "Jordan": "ヨルダン", "Iraq": "イラク",
    "Bosnia and Herzegovina": "ボスニア・ヘルツェゴビナ",
    "Republic of the Congo": "コンゴ共和国",
    "Haiti": "ハイチ", "Slovakia": "スロバキア",
    "New Caledonia": "ニューカレドニア",
}
