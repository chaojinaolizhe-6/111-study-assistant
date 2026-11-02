"""研究面板：把原始表拼成「每行 = 某只股票某一天」的宽表。

设计要点
--------
1. **复权**：库里只存不复权价与累计复权因子，面板里现算后复权价。
   任何收益率都必须用复权价计算，否则分红送股会被误判成暴跌。
2. **PIT 财务**：用 `notice_date`（公告日）而不是 `report_date` 做 as-of 连接。
   用报告期会把"还没公布的财报"喂给模型，这是最隐蔽的前视偏差。
3. **TTM**：财报是累计口径，直接比较一季报和年报的净利润毫无意义。
   这里由累计值还原单季再滚动成 TTM。
4. **ST 历史**：简称历史里带 ST 的时点即 ST，不能用"当前简称"回头筛历史。
5. **股本与换手**：月度快照前向填充流通股本，换手率 = 成交量 / 流通股本。
6. **可成交性**：涨跌停、停牌、ST、上市天数、流动性都变成显式布尔列，
   后续任何回测都必须先看这些列，而不是"假设都能成交"。
"""
from __future__ import annotations

from aq.labels import forward_open_return

import sqlite3
from typing import Iterable

import numpy as np
import pandas as pd

from . import config

BAR_COLS = ["code", "date", "open", "high", "low", "close", "pre_close",
            "volume", "amount", "turnover", "pct_chg", "adj_factor",
            "is_st", "trade_status"]

FIN_RAW = ["eps", "bps", "roe", "revenue", "net_profit", "ocf_ps",
           "gross_margin", "div_yield", "rev_yoy", "np_yoy"]
TTM_COLS = ["eps", "revenue", "net_profit", "ocf_ps"]


# --------------------------------------------------------------------------
# 基础读取
# --------------------------------------------------------------------------
def load_bars(conn: sqlite3.Connection, start: str, end: str) -> pd.DataFrame:
    q = f"""SELECT {','.join(BAR_COLS)} FROM bar
            WHERE date >= ? AND date <= ? ORDER BY code, date"""
    df = pd.read_sql_query(q, conn, params=(start, end))
    if df.empty:
        return df
    df["date"] = pd.to_datetime(df["date"])
    for c in BAR_COLS:
        if c not in ("code", "date"):
            df[c] = pd.to_numeric(df[c], errors="coerce").astype("float32")
    return df


def add_ttm(fin: pd.DataFrame) -> pd.DataFrame:
    """由累计值还原 TTM：TTM = 本期累计 + 上年年报 - 上年同期累计。"""
    f = fin.copy()
    f["y"] = f["report_date"].dt.year
    f["q"] = f["report_date"].dt.month
    ann = f[f["q"] == 12][["code", "y"] + TTM_COLS].copy()
    ann["y"] = ann["y"] + 1
    ann = ann.rename(columns={c: f"{c}_ann" for c in TTM_COLS})
    prev = f[["code", "y", "q"] + TTM_COLS].copy()
    prev["y"] = prev["y"] + 1
    prev = prev.rename(columns={c: f"{c}_prev" for c in TTM_COLS})
    f = f.merge(ann, on=["code", "y"], how="left").merge(prev, on=["code", "y", "q"], how="left")
    for c in TTM_COLS:
        ttm = np.where(f["q"] == 12, f[c], f[c] + f[f"{c}_ann"] - f[f"{c}_prev"])
        f[f"{c}_ttm"] = ttm
    return f.drop(columns=[f"{c}_{s}" for c in TTM_COLS for s in ("ann", "prev")] + ["y", "q"])


def load_fin(conn: sqlite3.Connection) -> pd.DataFrame:
    q = f"""SELECT code, report_date, notice_date, name, {','.join(FIN_RAW)}
            FROM fin WHERE notice_date IS NOT NULL AND notice_date <> ''"""
    df = pd.read_sql_query(q, conn)
    if df.empty:
        return df
    df["notice_date"] = pd.to_datetime(df["notice_date"], errors="coerce")
    df["report_date"] = pd.to_datetime(df["report_date"], errors="coerce")
    df = df.dropna(subset=["notice_date", "report_date"])
    for c in FIN_RAW:
        df[c] = pd.to_numeric(df[c], errors="coerce").astype("float32")
    df = add_ttm(df)
    df["is_st_flag"] = df["name"].astype(str).str.contains("ST", na=False).astype("int8")
    return df.sort_values(["code", "notice_date"])


def load_float_shares(conn: sqlite3.Connection) -> pd.DataFrame:
    """月度股本快照 -> 流通股本序列。"""
    q = """SELECT code, date, free_shares, float_mv, close FROM valuation"""
    try:
        df = pd.read_sql_query(q, conn)
    except Exception:
        return pd.DataFrame(columns=["code", "date", "fshare"])
    if df.empty:
        return pd.DataFrame(columns=["code", "date", "fshare"])
    df["date"] = pd.to_datetime(df["date"])
    df["fshare"] = pd.to_numeric(df["free_shares"], errors="coerce")
    m = df["fshare"].isna() | (df["fshare"] <= 0)
    if m.any():
        cl = pd.to_numeric(df["close"], errors="coerce")
        mv = pd.to_numeric(df["float_mv"], errors="coerce")
        df.loc[m, "fshare"] = mv[m] / cl[m].where(cl[m] > 0)
    df = df.dropna(subset=["fshare"])
    return df[df["fshare"] > 0].sort_values(["code", "date"])


# --------------------------------------------------------------------------
# 涨跌停判定
# --------------------------------------------------------------------------
def limit_pct(code: pd.Series, is_st: pd.Series, date: pd.Series) -> np.ndarray:
    """按板块与 ST 状态给出涨跌停幅度。

    * 主板 10%，ST 5%
    * 创业板(300/301) 20%（2020-08-24 注册制起），此前 10%
    * 科创板(688/689) 20%
    * 北交所(4/8/92 开头) 30%
    """
    c = code.astype(str)
    chinext = c.str.startswith(("300", "301")).to_numpy()
    star = c.str.startswith(("688", "689")).to_numpy()
    bse = c.str.startswith(("4", "8", "92")).to_numpy()
    st = is_st.astype(bool).to_numpy()
    pct = np.full(len(c), 0.10)
    pct = np.where(chinext | star, 0.20, pct)
    pct = np.where(bse, 0.30, pct)
    pct = np.where(st & ~(chinext | star | bse), 0.05, pct)
    early = (date < pd.Timestamp("2020-08-24")).to_numpy() & chinext
    pct = np.where(early, np.where(st, 0.05, 0.10), pct)
    return pct


def add_limit_flags(df: pd.DataFrame, tol: float = 0.011) -> pd.DataFrame:
    pct = limit_pct(df["code"], df["is_st"], df["date"])
    pre = df["pre_close"].astype("float64")
    up = np.round(pre * (1 + pct), 2)
    dn = np.round(pre * (1 - pct), 2)
    close = df["close"].astype("float64")
    high = df["high"].astype("float64")
    low = df["low"].astype("float64")
    df["limit_up"] = ((close >= up - tol) | (high >= up - tol)).astype("int8")
    df["limit_down"] = ((close <= dn + tol) | (low <= dn + tol)).astype("int8")
    df["one_word"] = ((high - low).abs() < 1e-6).astype("int8")
    return df


# --------------------------------------------------------------------------
# 面板构建
# --------------------------------------------------------------------------
def build_panel(conn: sqlite3.Connection, start: str, end: str, *,
                with_labels: bool = True, horizons: Iterable[int] = (1, 5, 10, 20),
                load_before: int = 420, load_after: int = 45,
                fin: pd.DataFrame | None = None,
                shares: pd.DataFrame | None = None) -> pd.DataFrame:
    """构建 [start, end] 区间的面板（前后各留缓冲）。

    load_before: 长窗口因子（mom_12_1 需要 240 日）的回看缓冲（自然日）
    load_after : 标签需要的未来数据缓冲（自然日）
    fin/shares : 预先加载好的财务与股本表，循环建板时传入可省去重复读库
    """
    rs = (pd.Timestamp(start) - pd.Timedelta(days=load_before)).strftime("%Y-%m-%d")
    re_ = (pd.Timestamp(end) + pd.Timedelta(days=load_after)).strftime("%Y-%m-%d")
    df = load_bars(conn, rs, re_)
    if df.empty:
        return df
    # merge_asof(by=...) 要求按 [on 键, by 键] 排序
    df = df.sort_values(["date", "code"]).reset_index(drop=True)

    # ---- 复权价 ----
    fac = df["adj_factor"].astype("float64").fillna(1.0)
    for c in ("open", "high", "low", "close", "pre_close"):
        df[f"adj_{c}"] = (df[c].astype("float64") * fac).astype("float32")

    # ---- PIT 财务 + ST 历史 ----
    fin = load_fin(conn) if fin is None else fin
    if not fin.empty:
        df = df.drop(columns=["is_st"], errors="ignore")
        df = pd.merge_asof(
            df, fin[["code", "notice_date", "is_st_flag"] + FIN_RAW
                    + [f"{c}_ttm" for c in TTM_COLS]]
            .rename(columns={"notice_date": "_nd", "is_st_flag": "is_st"})
            .sort_values(["_nd", "code"]),
            left_on="date", right_on="_nd", by="code", direction="backward",
        ).drop(columns=["_nd"])
        df["is_st"] = df["is_st"].fillna(0).astype("int8")
    else:
        df["is_st"] = 0

    # ---- 流通股本 / 市值 / 换手 ----
    shares = load_float_shares(conn) if shares is None else shares
    if not shares.empty:
        df = pd.merge_asof(df, shares[["code", "date", "fshare"]].sort_values(["date", "code"]),
                           on="date", by="code", direction="backward")
        df["turnover"] = (df["volume"].astype("float64") /
                          df["fshare"].where(df["fshare"] > 0) * 100)
    else:
        df["fshare"] = np.nan
    df["float_share"] = df["fshare"].astype("float32")
    df["mktcap"] = (df["close"].astype("float64") * df["fshare"]).astype("float32")
    df["ln_mktcap"] = np.log(df["mktcap"].clip(lower=1e6)).astype("float32")
    df["turnover"] = df["turnover"].replace([np.inf, -np.inf], np.nan).astype("float32")

    # ---- 涨跌停 / 可成交 ----
    df = add_limit_flags(df)

    # ---- 上市天数 ----
    first = df.groupby("code", observed=True)["date"].transform("min")
    df["list_date"] = first
    df["listed_days"] = (df["date"] - first).dt.days.astype("float32")

    # ---- 流动性 ----
    g = df.groupby("code", observed=True)
    df["amount_ma20"] = g["amount"].transform(
        lambda s: s.rolling(20, min_periods=10).mean()).astype("float32")
    df["turn_ma20"] = g["turnover"].transform(
        lambda s: s.rolling(20, min_periods=10).mean()).astype("float32")

    # ---- 标签 ----
    if with_labels:
        g = df.groupby("code", observed=True)
        next_open = g["adj_open"].shift(-1).astype("float64")
        for h in horizons:
            df[f"fwd_ret_{h}"] = forward_open_return(df["adj_open"], h, df["code"]).astype("float32")
            exit_close = g["adj_close"].shift(-(1 + h)).astype("float64")
            df[f"fwd_close_ret_{h}"] = (exit_close / next_open - 1).astype("float32")
        df["next_ret"] = (next_open / df["adj_open"].astype("float64") - 1).astype("float32")
        df["next_open"] = next_open.astype("float32")

    # ---- 股票池标记 ----
    df["is_tradable"] = (
        (df["volume"].fillna(0) > 0)
        & (df["is_st"] == 0)
        & (df["listed_days"] >= config.MIN_LIST_DAYS)
        & (df["close"] >= config.MIN_PRICE)
        & (df["amount_ma20"] >= config.MIN_AMOUNT_20D)
    )
    df["can_buy_next"] = df["is_tradable"] & (df["limit_up"] == 0) & (df["one_word"] == 0)
    df["can_sell_next"] = df["is_tradable"] & (df["limit_down"] == 0) & (df["one_word"] == 0)

    out = df[(df["date"] >= pd.Timestamp(start)) & (df["date"] <= pd.Timestamp(end))]
    return out.reset_index(drop=True)


def panel_summary(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d["year"] = d["date"].dt.year
    g = d.groupby("year", observed=True)
    return pd.DataFrame({
        "rows": g.size(),
        "stocks": g["code"].nunique(),
        "tradable": g["is_tradable"].sum(),
        "tradable%": (g["is_tradable"].mean() * 100).round(1),
        "limit_up": g["limit_up"].sum(),
        "st_days": (g["is_st"] == 1).sum(),
        "turn_cov%": (g["turnover"].apply(lambda s: s.notna().mean()) * 100).round(1),
    })
