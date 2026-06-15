# Task Plan: 2026 世界杯比赛预测网站

## Goal
搭建一个 GitHub Pages 静态站，展示 2026 世界杯全部比赛的赛程、实际比分和 Elo+泊松模型预测，每 30 分钟由 GitHub Actions 自动更新；URL: https://nicolaslinlin.github.io/wc2026/

## Current Phase
Phase 7（模型 vs 市场对比）

✅ Phase 1-6 已完成（2026-06-15 上线）— https://nicolaslinlin.github.io/wc2026/

## Phases

### Phase 1: 项目脚手架与基础设施
- [ ] uv init 项目（pyproject.toml + 依赖）
- [ ] 创建目录结构（wc2026/, scripts/, tests/, templates/, data/, public/）
- [ ] git 初始化
- [ ] SQLite schema + db helper（wc2026/db.py + tests）
- [ ] scripts/init_db.py 跑通
- **Status:** in_progress
- **参考：** 计划 Task 1-2

### Phase 2: 核心模型
- [ ] Elo 评分模型（wc2026/elo.py + 7 个 TDD 测试）
- [ ] 泊松比分模型（wc2026/poisson.py + 8 个 TDD 测试）
- **Status:** pending
- **参考：** 计划 Task 3-4

### Phase 3: 数据接入
- [ ] 下载并导入历史 CSV（scripts/load_history.py）
- [ ] football-data.org API 封装（wc2026/api.py）
- [ ] 队名映射（wc2026/team_mapping.py + tests）
- [ ] 关键 smoke test：API 能拿到 WC 数据吗？不行触发备选方案 A
- [ ] 加载 2026 赛程（scripts/load_fixtures.py）
- [ ] 周期性更新（scripts/update_results.py）
- **Status:** pending
- **参考：** 计划 Task 5-9

### Phase 4: 预测与渲染
- [ ] 预测脚本（scripts/predict.py）
- [ ] Jinja2 模板（templates/index.html.j2）
- [ ] 渲染器（scripts/render.py + tests）
- [ ] 本地浏览器看页面效果
- **Status:** pending
- **参考：** 计划 Task 10-12

### Phase 5: 部署
- [ ] README
- [ ] GitHub Actions 工作流（.github/workflows/update.yml）
- [ ] 用户：在 GitHub 网站建仓库、加 secret、开 Pages
- [ ] 本地推 main，触发首次 Actions
- [ ] 验证线上 URL 可访问
- **Status:** pending
- **参考：** 计划 Task 13-15

### Phase 7: 模型 vs 市场盘口对比
- [ ] 注册 The Odds API 拿 key（用户）
- [ ] DB 加 `market_predictions` 表
- [ ] `wc2026/market.py`：从让球(spread) + 大小球(total) 反推 home_xg / away_xg + TDD
- [ ] `wc2026/odds_api.py`：The Odds API 封装
- [ ] `scripts/fetch_odds.py`：拉盘口 → 反推 xG → 跑泊松 → 写表
- [ ] `render.py` 增加"市场预测"一行
- [ ] 模板 UI 更新
- [ ] 用户在 GitHub Secret 加 `ODDS_API_TOKEN`
- [ ] `update.yml` workflow 加 fetch_odds 步骤
- [ ] 部署 + 验证
- **Status:** in_progress
- **设计要点：** spread = home_xg - away_xg；total/2 = (home_xg+away_xg)/2；二元一次方程求解；再丢入现成的 poisson 函数

### Phase 6: 端到端验证
- [ ] 全测试套件通过（uv run pytest）
- [ ] 本地端到端跑一遍
- [ ] 线上访问与本地一致
- [ ] 等待第一场比赛结束，验证「真实比分 + 命中标记」显示正确
- **Status:** pending

## Key Questions
1. football-data.org 免费版能拿到 WC 数据吗？（Phase 3 smoke test 验证；不行走备选方案 A 手动 CSV）
2. martj42 历史 CSV 的队名与 API 队名一致性如何？（Phase 3 team_mapping.py 覆盖）
3. Elo + 独立泊松对世界杯的精度可接受吗？（接受 — MVP 目标是跑通链路，不追求超越盘口）

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| 静态站 + GitHub Pages | 免费、零运维、URL 可分享、不需实时 |
| Elo + 独立泊松（不上 Dixon-Coles 低分相关性修正）| YAGNI；首版求跑通 |
| SQLite 文件提交到仓库 | 数据量小（~100KB），便于版本回溯 |
| 国旗用 emoji | 避免引入图片资源 |
| 仅中文、不做盘口对比 | MVP 范围控制 |
| 项目根 `C:\Users\linna\Documents\cloude Projects\wc2026\` | 用户指定，与 `学习/` 平级 |
| 不放球员级别预测、不做用户竞猜 | 排除项，留 V2 |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
|       | 1       |            |

## Notes
- 完整实现细节在 `学习/docs/superpowers/plans/2026-06-14-worldcup-predictor.md`（15 个 Task，每步含代码）
- 完整设计在 `学习/docs/superpowers/specs/2026-06-14-worldcup-predictor-design.md`
- API token 不写入任何文件 → 仅放 GitHub Secrets
- 用户已贴过一次 token，已建议（但不强制）regenerate
