"""Step 10 — 导入外部 A 股快照（a_share_20260831）。

数据来源与核验结论（2026-10-31 实测）
------------------------------------
四张 parquet，2020-01-02 ~ 2026-08-31：

  market_daily     5,637,878 行 / 5,257 只 / 24 列
  market_moneyflow 5,637,848 行 / 33 列（超大单~小单 四档资金流）
  valuation_daily  9,553,741 行 / 15 列（PE/PB/PS/PCF/PEG/股息率/资产负债率）
  fundamental_daily 5,637,878 行 / 123 列（121 个财务指标，含单季与 TTM）

三项核验结果：
  ① 与本地库交叉校验 554 万行，收盘价相对误差 > 0.1% 的比例 = 0.000%（完全一致）
  ② 基本面是 **point-in-time**：净利润的变化日精确落在公告日
     （平安银行 2020-02-14 年报 / 04-21 一季报 / 08-28 中报 / 10-22 三季报）
  ③ 覆盖范围只有全市场的约 80%（2026-08-31：4186 只 vs 本地 5202 只），
     且各年比例不同（2021 日均 2818 只最低）。**这是一个已过滤的股票池，
     不是全市场**，不能直接替代本地库做横截面研究。

因此本脚本把它作为**补充层**导入，用于三件事：
  * 真实成交额 / 换手率 / 流通股本（本地是估算值）
  * 四档资金流（本地完全没有，是一个新因子族）
  * 日频估值（本地只有月度快照）
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aq.config import DATA, DB_PATH
from aq.db import connect, now_cn

SRC = Path(r"D:\aaa_D_usual\DSH\项目\量化\数据_原始parquet")

SCHEMA = """
CREATE TABLE IF NOT EXISTS shm_bar (
    code TEXT NOT NULL, date TEXT NOT NULL,
    open REAL, high REAL, low REAL, close REAL, pre_close REAL,
    adj_open REAL, adj_high REAL, adj_low REAL, adj_close REAL, adj_pre_close REAL,
    volume REAL, volume_adj REAL, amount REAL, vwap REAL, twap REAL,
    ret REAL, ret_adj REAL, turnover REAL, float_share REAL, float_mv REAL,
    PRIMARY KEY (code, date)
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS shm_moneyflow (
    code TEXT NOT NULL, date TEXT NOT NULL, market TEXT,
    super_in_amt REAL, super_out_amt REAL,
    big_in_amt REAL, big_out_amt REAL,
    mid_in_amt REAL, mid_out_amt REAL,
    small_in_amt REAL, small_out_amt REAL,
    main_in_amt REAL, main_out_amt REAL, main_net_amt REAL,
    main_in_vol REAL, main_out_vol REAL, main_net_vol REAL,
    PRIMARY KEY (code, date)
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS shm_valuation (
    code TEXT NOT NULL, date TEXT NOT NULL,
    pb REAL, pe REAL, ps REAL, pcf REAL,
    total_mv REAL, float_mv REAL,
    forward_pe REAL, peg REAL, ps_ttm REAL, pcf_ttm REAL,
    div_yield REAL, mv_to_randd REAL, debt_to_asset REAL,
    PRIMARY KEY (code, date)
) WITHOUT ROWID;
"""


def _chunks(n: int, size: int = 200_000):
    for i in range(0, n, size):
        yield i, min(i + size, n)


def ingest(src: Path, table: str, cols_in: list[str], cols_out: list[str],
           date_col: str, code_col: str, conn) -> int:
    t0 = time.time()
    df = pd.read_parquet(src, columns=cols_in)
    df = df.rename(columns=dict(zip(cols_in, cols_out)))
    d_out = cols_out[cols_in.index(date_col)]
    c_out = cols_out[cols_in.index(code_col)]
    df[d_out] = pd.to_datetime(df[d_out]).dt.strftime("%Y-%m-%d")
    df[c_out] = df[c_out].astype(str)
    for c in cols_out:
        if c not in (d_out, c_out):
            df[c] = pd.to_numeric(df[c], errors="coerce").astype("float64")
    df = df[cols_out]

    ph = ",".join("?" * len(cols_out))
    sql = f"INSERT OR REPLACE INTO {table} ({','.join(cols_out)}) VALUES ({ph})"
    n = 0
    # 分块转元组，避免 560 万 x 22 的 object 数组把内存打爆
    for a, b in _chunks(len(df), 100_000):
        sub = df.iloc[a:b]
        conn.executemany(sql, list(sub.itertuples(index=False, name=None)))
        conn.commit()
        n += len(sub)
        if n % 1_000_000 == 0 or n == len(df):
            print(f"    {table} {n:,}/{len(df):,}", flush=True)
    print(f"  [ingest] {table} 完成 {n:,} 行 {time.time() - t0:.0f}s", flush=True)
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-fundamental", action="store_true")
    args = ap.parse_args()

    if not SRC.exists():
        print(f"[ingest] 源目录不存在: {SRC}")
        return 1
    conn = connect(fast=True)
    conn.executescript(SCHEMA)
    conn.commit()
    print(f"[ingest] 开始 {now_cn()}", flush=True)

    # ---- 1. 日行情 ----
    ingest(SRC / "market_daily_a_share.parquet", "shm_bar",
           ["stock_code", "trade_date", "S_DQ_OPEN", "S_DQ_HIGH", "S_DQ_LOW",
            "S_DQ_CLOSE", "S_DQ_PRECLOSE", "S_DQ_OPEN_ADJ", "S_DQ_HIGH_ADJ",
            "S_DQ_LOW_ADJ", "S_DQ_CLOSE_ADJ", "S_DQ_PRECLOSE_ADJ", "S_DQ_VOLUME",
            "S_DQ_VOLUME_ADJ", "S_DQ_AMOUNT", "S_DQ_VWAP", "S_DQ_TWAP",
            "S_DQ_RETURN", "S_DQ_RETURN_ADJ", "S_DQ_TURNOVER_RATE",
            "FloatShare", "S_DQ_NEG_MARKET_VALUE"],
           ["code", "date", "open", "high", "low", "close", "pre_close",
            "adj_open", "adj_high", "adj_low", "adj_close", "adj_pre_close",
            "volume", "volume_adj", "amount", "vwap", "twap",
            "ret", "ret_adj", "turnover", "float_share", "float_mv"],
           "trade_date", "stock_code", conn)

    # ---- 2. 资金流 ----
    ingest(SRC / "market_moneyflow_a_share.parquet", "shm_moneyflow",
           ["stockcode", "trade_date", "market", "superin_amt", "superout_amt",
            "bigin_amt", "bigout_amt", "midin_amt", "midout_amt",
            "smallin_amt", "smallout_amt", "mainin_amt", "mainout_amt",
            "mainnetin_amt", "mainin_vol", "mainout_vol", "mainnetin_vol"],
           ["code", "date", "market", "super_in_amt", "super_out_amt",
            "big_in_amt", "big_out_amt", "mid_in_amt", "mid_out_amt",
            "small_in_amt", "small_out_amt", "main_in_amt", "main_out_amt",
            "main_net_amt", "main_in_vol", "main_out_vol", "main_net_vol"],
           "trade_date", "stockcode", conn)

    # ---- 3. 估值 ----
    ingest(SRC / "valuation_daily_a_share.parquet", "shm_valuation",
           ["stock_code", "TradingDay", "PB", "PE", "PS", "PCF", "TotalASMV",
            "NegotiableMV", "ForwardPEHR", "PEG", "PSTTM", "PCFTTM",
            "DividendRatioTTM", "TotalMVToRANDD", "DebtToAssetValue1"],
           ["code", "date", "pb", "pe", "ps", "pcf", "total_mv", "float_mv",
            "forward_pe", "peg", "ps_ttm", "pcf_ttm", "div_yield",
            "mv_to_randd", "debt_to_asset"],
           "TradingDay", "stock_code", conn)

    # ---- 4. 基本面：121 列不进 SQLite，转成精简 parquet ----
    if not args.skip_fundamental:
        keep = ["stock_code", "trade_date", "TotalAssets", "TotalLiability",
                "SEWithoutMI", "TotalShareholderEquity", "GoodWill",
                "IntangibleAssets", "RAndD", "RAndD_ttm", "NetOperateCashFlow_ttm",
                "NetProfitCut_ttm", "NPParentCompanyOwners_ttm",
                "OperatingRevenue_ttm", "TotalOperatingRevenue_ttm",
                "ROE", "WROE", "ROECut", "GrossIncomeRatio", "CurrentRatio",
                "QuickRatio", "TotalShares", "NAPS", "NetProfitCut"]
        df = pd.read_parquet(SRC / "fundamental_daily_a_share.parquet", columns=keep)
        out = DATA / "shm"
        out.mkdir(parents=True, exist_ok=True)
        df.to_parquet(out / "fundamental_subset.parquet", index=False, compression="zstd")
        print(f"  [ingest] fundamental 子集 {len(df):,} 行 x {len(keep)} 列 "
              f"-> {out / 'fundamental_subset.parquet'}", flush=True)

    conn.execute("ANALYZE")
    conn.commit()
    for t in ("shm_bar", "shm_moneyflow", "shm_valuation"):
        n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"[ingest] {t:16s} {n:,}")
    print(f"[ingest] DONE {now_cn()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
