"""全局配置：路径、时间范围、股票池口径。"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DB_PATH = DATA / "quant.db"
PARQUET = DATA / "parquet"
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"

for _p in (DATA, PARQUET, REPORTS, FIGURES):
    _p.mkdir(parents=True, exist_ok=True)

# 数据起点。2010 之后 A 股经历了注册制扩容与量化资金入场，
# 是检验"什么信号已衰减"最有信息量的样本。
START_DATE = "2010-01-01"
END_DATE = "2050-12-31"

# 财报期起点（含）
FIN_START_YEAR = 2009

# 股票池：上市满 N 个自然日后才可进入可交易池
MIN_LIST_DAYS = 250
# 剔除 ST / *ST（按当日证券简称判断）
EXCLUDE_ST = True
# 剔除当日停牌
EXCLUDE_SUSPENDED = True
# 剔除当日涨跌停（不可成交）
EXCLUDE_LIMIT = True
# 最低价格过滤（避免极低价仙股与退市整理股）
MIN_PRICE = 1.0
# 最低日均成交额（元），流动性门槛
MIN_AMOUNT_20D = 2e7

INDEXES = {
    "000300": ("1.000300", "沪深300"),
    "000905": ("1.000905", "中证500"),
    "000852": ("1.000852", "中证1000"),
    "000016": ("1.000016", "上证50"),
    "000985": ("1.000985", "中证全指"),
    "399006": ("0.399006", "创业板指"),
    "000001": ("1.000001", "上证指数"),
}
