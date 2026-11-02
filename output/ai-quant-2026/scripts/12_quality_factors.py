"""Step 12 — 质量因子族：用 121 个财务指标里真正有信息的那 20 个。

为什么重做
----------
本地库只有 9 个财务字段（EPS/BPS/ROE/毛利率/营收/净利/经营现金流…），
由此构造的质量因子在 2010--2026 全样本上 ICIR 全部小于 1（见第~\ref{ch:result} 章），
这些年度汇总不足以判断全样本显著性。

外部快照带来 121 个指标，其中本地**确实拿不到**的包括：
研发费用、商誉、无形资产、有息负债、营运资本、费用明细、扣非利润、投资收益。
这些正是质量因子真正的原料。

但"字段更多"不等于"因子更好"。本脚本对每个因子同时输出三组数：
  1. 原始 IC / ICIR / Newey-West t
  2. **增量 IC**：对「对数市值 + turn_20 + vol_20 + rev_5」截面回归取残差后重算
  3. 与对数市值的截面相关（检查它是不是又一个规模因子的换皮）

只有增量 IC 仍然显著的，才算真的提供了新信息。

注意：快照股票池只有全市场的 76%--83%（见附录 F），
且区间只有 2020-01 至 2026-08，因此本节的结论**不能外推到更早的样本**。
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aq import config, metrics
from aq.labels import forward_open_return
from aq.db import connect, now_cn

warnings.filterwarnings("ignore")

SRC = Path(r"D:\aaa_D_usual\DSH\项目\量化\数据_原始parquet")
H = 5
YEARS = range(2020, 2027)

FUND_COLS = [
    "stock_code", "trade_date",
    "TotalAssets", "TotalLiability", "SEWithoutMI", "TotalCurrentAssets",
    "TotalCurrentLiability", "GoodWill", "IntangibleAssets",
    "ShortTermLoan", "LongtermLoan", "InvestIncome_ttm",
    "TotalOperatingRevenue_ttm", "TotalOperatingCost_ttm", "OperatingProfit_ttm",
    "NPParentCompanyOwners_ttm", "NetProfitCut_ttm",
    "GrossIncomeRatio", "OperatingProfitMargin", "ROE", "WROE", "ROA",
    "FinancialExpense_ttm", "TotalAdminExpense_ttm", "OperatingExpense_ttm",
    "RAndD_ttm", "NetOperateCashFlow_ttm", "SubtotalOperateCashInflow_ttm",
    "CurrentRatio", "QuickRatio", "TotalShares",
]


def safe_div(a, b, eps=1e-9):
    return a / b.where(b.abs() > eps)


def build_factors(f: pd.DataFrame) -> dict[str, pd.Series]:
    """20 个因子，统一方向：数值越大越好。"""
    ta = f["TotalAssets"]
    se = f["SEWithoutMI"]
    rev = f["TotalOperatingRevenue_ttm"]
    nparent = f["NPParentCompanyOwners_ttm"]
    cfo = f["NetOperateCashFlow_ttm"]
    out = {
        # ---- 盈利能力 ----
        "q_wroe": f["WROE"],
        "q_roe": f["ROE"],
        "q_roa": f["ROA"],
        "q_gm": f["GrossIncomeRatio"],
        "q_opm": f["OperatingProfitMargin"],
        # ---- 现金含量 / 应计 ----
        "q_cfo_ni": safe_div(cfo, nparent.abs()),
        "q_accrual": -safe_div(nparent - cfo, ta),
        "q_cash_rev": safe_div(f["SubtotalOperateCashInflow_ttm"], rev),
        # ---- 研发 ----
        "q_rd": safe_div(f["RAndD_ttm"], rev),
        # ---- 商誉与无形资产 ----
        "q_gw": -safe_div(f["GoodWill"], se.abs()),
        "q_intang": -safe_div(f["GoodWill"] + f["IntangibleAssets"], ta),
        # ---- 杠杆与偿债 ----
        "q_lev": -safe_div(f["TotalLiability"], ta),
        "q_debt": -safe_div(f["ShortTermLoan"] + f["LongtermLoan"], ta),
        "q_current": f["CurrentRatio"],
        "q_quick": f["QuickRatio"],
        # ---- 营运效率 ----
        "q_wc": safe_div(f["TotalCurrentAssets"] - f["TotalCurrentLiability"], ta),
        "q_at": safe_div(rev, ta),
        # ---- 费用率 ----
        "q_exp": -safe_div(f["TotalAdminExpense_ttm"] + f["OperatingExpense_ttm"]
                           + f["FinancialExpense_ttm"], rev),
        # ---- 利润含金量 ----
        "q_cut": safe_div(f["NetProfitCut_ttm"], nparent.abs()),
        "q_invinc": -safe_div(f["InvestIncome_ttm"], nparent.abs()),
    }
    return out


def wide(s: pd.Series, df, dates, codes):
    w = pd.DataFrame({"d": df["date"].to_numpy(), "c": df["code"].to_numpy(),
                      "v": s.to_numpy()}).pivot(index="d", columns="c", values="v")
    return w.reindex(index=dates, columns=codes).astype("float32")


def main() -> int:
    conn = connect()
    bar = pd.read_sql_query(
        """SELECT code, date, adj_open, adj_close, turnover, float_mv
           FROM shm_bar WHERE date >= '2020-01-01'""", conn)
    conn.close()
    bar["date"] = pd.to_datetime(bar["date"])
    bar = bar.sort_values(["code", "date"]).reset_index(drop=True)
    print(f"[quality] bar {len(bar):,} codes={bar.code.nunique()}", flush=True)

    g = bar.groupby("code", observed=True)
    bar["fwd"] = forward_open_return(bar["adj_open"], H, bar["code"])
    bar["ret1"] = g["adj_close"].pct_change()
    bar["turn20"] = bar.groupby("code", observed=True)["turnover"].transform(
        lambda s: s.rolling(20, min_periods=12).mean())
    bar["vol20"] = bar.groupby("code", observed=True)["ret1"].transform(
        lambda s: s.rolling(20, min_periods=12).std())
    bar["rev5"] = -bar.groupby("code", observed=True)["adj_close"].transform(
        lambda s: s / s.shift(5) - 1)
    bar["ln_mv"] = np.log(bar["float_mv"].clip(lower=1e6))
    bar = bar[["code", "date", "fwd", "turn20", "vol20", "rev5", "ln_mv"]]
    bar = bar[bar["fwd"].notna()].reset_index(drop=True)

    all_rows, ic_store, inc_store = [], {}, {}
    for y in YEARS:
        d0, d1 = f"{y}-01-01", f"{y}-12-31"
        tbl = pq.read_table(SRC / "fundamental_daily_a_share.parquet",
                            columns=FUND_COLS,
                            filters=[("trade_date", ">=", pd.Timestamp(d0)),
                                     ("trade_date", "<=", pd.Timestamp(d1))])
        f = tbl.to_pandas()
        if f.empty:
            continue
        f["trade_date"] = pd.to_datetime(f["trade_date"])
        f = f.rename(columns={"stock_code": "code", "trade_date": "date"})
        for c in FUND_COLS:
            if c not in ("stock_code", "trade_date"):
                f[c] = pd.to_numeric(f[c], errors="coerce").astype("float64")

        df = f.merge(bar, on=["code", "date"], how="inner")
        if df.empty:
            continue
        dates = pd.Index(np.sort(df["date"].unique()))
        codes = pd.Index(np.sort(df["code"].unique()))
        y_fwd = wide(df["fwd"], df, dates, codes)
        lab = y_fwd.rank(axis=1, pct=True) - 0.5

        ctrl = {k: wide(df[k], df, dates, codes).to_numpy(dtype="float64")
                for k in ("ln_mv", "turn20", "vol20", "rev5")}

        F = build_factors(df)
        for name, s in F.items():
            s = s.replace([np.inf, -np.inf], np.nan)
            W = wide(s, df, dates, codes)
            if not np.isfinite(W.to_numpy()).any():
                continue
            ic = metrics.rank_ic(W, y_fwd)
            sm = metrics.ic_summary(ic, 252)
            q = metrics.quantile_returns(W, y_fwd, 5)
            qm = q.mean()
            mono = (np.corrcoef(range(1, 6), qm.to_numpy())[0, 1]
                    if np.isfinite(qm).all() else np.nan)
            to = metrics.turnover(W, 0.2, True)

            # 增量 IC：逐日对四个控制变量回归取残差
            M = W.to_numpy(dtype="float64")
            resid = np.full_like(M, np.nan)
            for i in range(len(dates)):
                yv = M[i]
                m = np.isfinite(yv) & np.isfinite(ctrl["ln_mv"][i])
                if m.sum() < 200:
                    continue
                X = np.column_stack([np.ones(m.sum())] +
                                    [ctrl[k][i][m] for k in ctrl])
                X = np.nan_to_num(X)
                beta, *_ = np.linalg.lstsq(X, yv[m], rcond=None)
                r = np.full(M.shape[1], np.nan)
                r[m] = yv[m] - X @ beta
                resid[i] = r
            RW = pd.DataFrame(resid, index=dates, columns=codes)
            ic_inc = metrics.rank_ic(RW, y_fwd)
            smi = metrics.ic_summary(ic_inc, 252)

            # 与规模的截面相关
            cs = []
            for i in range(0, len(dates), 5):
                a, b = M[i], ctrl["ln_mv"][i]
                m = np.isfinite(a) & np.isfinite(b)
                if m.sum() > 200:
                    c0 = np.corrcoef(pd.Series(a[m]).rank(), pd.Series(b[m]).rank())[0, 1]
                    if np.isfinite(c0):
                        cs.append(c0)

            all_rows.append({
                "factor": name, "year": y,
                "ic_mean": sm["ic_mean"], "icir_ann": sm["ic_ir_ann"],
                "t_nw": sm["t_nw"],
                "ic_inc": smi["ic_mean"], "icir_inc": smi["ic_ir_ann"],
                "t_inc": smi["t_nw"],
                "monotonic": float(mono) if np.isfinite(mono) else np.nan,
                "turnover": float(np.nanmean(to)),
                "corr_size": float(np.mean(cs)) if cs else np.nan,
            })
            ic_store.setdefault(name, []).append(ic)
            inc_store.setdefault(name, []).append(ic_inc)
        print(f"  [{y}] merged={len(df):,} dates={len(dates)} codes={len(codes)}", flush=True)

    ev = pd.DataFrame(all_rows)
    ev.to_csv(config.REPORTS / "quality_factor_by_year.csv", index=False,
              encoding="utf-8-sig")
    agg = (ev.groupby("factor")
           .agg(years=("year", "nunique"),
                ic_mean=("ic_mean", "mean"), icir_ann=("icir_ann", "mean"),
                t_nw=("t_nw", "mean"),
                ic_inc=("ic_inc", "mean"), icir_inc=("icir_inc", "mean"),
                t_inc=("t_inc", "mean"),
                monotonic=("monotonic", "mean"), turnover=("turnover", "mean"),
                corr_size=("corr_size", "mean"))
           .reset_index().sort_values("ic_inc", ascending=False))
    raw_ic = pd.DataFrame({k: pd.concat(v).sort_index() for k, v in ic_store.items()})
    inc_ic = pd.DataFrame({k: pd.concat(v).sort_index() for k, v in inc_store.items()})
    raw_ic.to_parquet(config.DATA / "quality_ic.parquet", compression="zstd")
    inc_ic.to_parquet(config.DATA / "quality_ic_inc.parquet", compression="zstd")
    agg = metrics.pooled_factor_summary(agg, raw_ic, inc_ic)
    agg.to_csv(config.REPORTS / "quality_factor_eval.csv", index=False,
               encoding="utf-8-sig")
    print("\n== 质量因子族（按增量 IC 排序）==")
    print(agg.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    print(f"\n[quality] DONE {now_cn()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
