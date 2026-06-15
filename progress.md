# Progress Log: 2026 世界杯预测网站

## Session 2026-06-14 → 2026-06-15 — 设计 + 实现 + 部署

### ✅ 全部完成（6 个 Phase）

**Phase 1: 项目脚手架 + DB schema**
- `uv init`, 目录结构, git init
- SQLite schema（3 张表：matches_history / fixtures / predictions）
- `wc2026/db.py` + `scripts/init_db.py` + 2 tests

**Phase 2: Elo + 泊松模型（TDD）**
- `wc2026/elo.py`（含 FIFA 风格进球差倍数）+ 7 tests
- `wc2026/poisson.py`（lambda_from_elo / score_matrix / outcome_probabilities / most_likely_score）+ 8 tests

**Phase 3: 数据接入**
- `scripts/load_history.py`（martj42 CSV → 3317 条历史）
- `wc2026/api.py`（football-data.org 封装）
- `wc2026/team_mapping.py` + 2 tests
- `scripts/load_fixtures.py`（API → 104 场赛程）
- `scripts/update_results.py`（周期性刷新）
- ✅ smoke test 通过（用户用真 token 跑 `Upserted 104 fixtures`）

**Phase 4: 预测 + 渲染**
- `scripts/predict.py`（Elo 重放 + 72 场预测，跳过 TBD 淘汰赛位）
- `templates/index.html.j2`（深色主题 + Twemoji + 中文化）
- `scripts/render.py` + 5 tests
- `wc2026/team_names_cn.py`（60+ 国家中文名）
- ⚠️ 修复：取消世界杯主场加成（home_advantage=0），否则厄瓜多尔被错误加权

**Phase 5: GitHub Actions + Pages 部署**
- `README.md`
- `.github/workflows/update.yml`（cron `*/30 * * * *` + push 触发）
- 用户在 GitHub 上：建仓库、加 secret `FOOTBALL_DATA_TOKEN`、push、开 Pages
- ✅ 上线 https://nicolaslinlin.github.io/wc2026/

**Phase 6: 端到端验证**
- 全部 24 个测试通过
- 线上页面显示正确：德国 7-1 库拉索（胜负命中、比分未中）、科特迪瓦 1-0 厄瓜多尔（胜负未中，模型走眼）
- GitHub Pages CDN ~10 分钟缓存延迟，用户用 Ctrl+F5 强刷确认

### 关键决策与坑

1. **取消世界杯主场加成** — 否则非主办国的"home team"会被错误加权
2. **Twemoji** — Windows 不渲染 emoji 国旗，必须用图片化方案
3. **`uv run python -m scripts.xxx`** — 直接 `python scripts/xxx.py` 找不到包，需用 module 方式
4. **GitHub Pages 顺序** — 必须先 push 让 Actions 跑出 `gh-pages` 分支，才能在 Settings 里选它
5. **Pages CDN 缓存** — 部署后 ~10 分钟才更新，需要强刷

### 错误与解决

| 错误 | 解决 |
|---|---|
| `ModuleNotFoundError: wc2026` 跑 script 时 | 改用 `python -m scripts.xxx` |
| `Timestamp.utcnow is deprecated` | 改用 `Timestamp.now("UTC").tz_localize(None)` |
| `UnicodeEncodeError cp932` 控制台输出 | `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')` |
| 用户首次 `$env:` 设置时把 `<...>` 占位符也复制了 | 去掉尖括号 |
| 厄瓜多尔被预测为 50% 胜率（vs 德国客场） | 取消世界杯主场加成 |
| 测试断言"最后更新："文案过时 | 改用更宽松的时间字符串断言 |

### 后续可玩（V2 备忘录）

- 博彩盘口对比列
- 朋友竞猜功能（输入预测、自动算分）
- 球员级别特征（伤病、首发阵容）
- Dixon-Coles 低比分相关性修正
- 历史届世界杯回顾对比
