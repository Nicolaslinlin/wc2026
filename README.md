# 2026 World Cup Predictor

一个轻量级静态站，展示 2026 世界杯全部 104 场比赛的赛程、实际比分和 Elo + 泊松模型预测。

**线上访问：** https://nicolaslinlin.github.io/wc2026/

**📲 装到手机/桌面**：[INSTALL.md](./INSTALL.md)（iPhone / Android / Windows / Mac 全平台说明）

## 工作原理

1. 历史国际比赛数据来自 [martj42/international_results](https://github.com/martj42/international_results)（开源 CSV）
2. 2026 世界杯赛程和实时比分来自 [football-data.org](https://www.football-data.org/)
3. Elo 评分在历史数据上回放计算，泊松分布把 Elo 差转换成期望进球（xG）和最可能比分
4. GitHub Actions 每 30 分钟刷新一次，重新渲染 `public/index.html` 并发布到 `gh-pages` 分支

## 本地开发

```bash
uv sync
$env:FOOTBALL_DATA_TOKEN = "<你的token>"  # PowerShell
uv run python -m scripts.init_db
uv run python -m scripts.load_history
uv run python -m scripts.load_fixtures
uv run python -m scripts.predict
uv run python -m scripts.render
start public/index.html
```

## 测试

```bash
uv run pytest
```

## 免责声明

这是一个学习项目。预测仅供娱乐，**不是博彩建议**。模型有意保持简单（Elo + 独立泊松，不做 Dixon-Coles 修正），经常会和博彩公司盘口不一致。
