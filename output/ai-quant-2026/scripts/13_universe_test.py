"""Step 13 — 两条来自文献的严格化检验。

背景
----
外部讲义（AI量化交易成熟技术讲义）第 5 章引了两条对本项目有直接冲击的文献结论：

  ① Harvey, Liu & Zhu (2016)：数百个已发表因子之后，t > 2.0 的门槛已不够，
     新因子应要求 t > 3.0。
  ② Liu, Stambaugh & Yuan (2019)：A 股的小市值效应被"壳价值"污染，
     建议剔除最小 30% 市值后再检验。

本脚本把这两条变成可执行的检验：

  A. 用 t > 3 重新判定本项目 39 个因子的显著性，看有多少"幸存"。
  B. 在「全样本」与「剔除最小 30% 流通市值」两个股票池上重算核心因子的 IC，
     看结论是否依赖微盘股。

为什么要做 B：本项目的多空组合若主要靠微盘股，那么它在容量上是不可执行的，
而且外部快照（只覆盖较大的 76%--83%）与本地库的结论会系统性不一致。
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aq import config, metrics
from aq.db import now_cn

warnings.filterwarnings("ignore")

YEARS = range(2013, 2027)
FACTORS = ["rev_1", "rev_5", "rev_10", "mom_20", "mom_120", "vol_20", "ivol_60",
           "turn_20", "ln_amount_20", "amihud_20", "pv_corr_20", "bp", "size",
           "max_ret_20", "skew_20"]
EXCLUDE_Q = 0.30


def _ic(fr: np.ndarray, rr: np.ndarray) -> np.ndarray:
    m = np.isfinite(fr) & np.isfinite(rr)
    a = np.where(m, fr, np.nan)
    b = np.where(m, rr, np.nan)
    n = m.sum(axis=1)
    a = a - np.nanmean(a, axis=1)[:, None]
    b = b - np.nanmean(b, axis=1)[:, None]
    num = np.nansum(a * b, axis=1)
    den = np.sqrt(np.nansum(a * a, axis=1) * np.nansum(b * b, axis=1))
    with np.errstate(invalid="ignore", divide="ignore"):
        ic = num / den
    ic[n < 50] = np.nan
    return ic


def main() -> int:
    rows = []
    for y in YEARS:
        p = config.DATA / "factors" / f"{y}.parquet"
        if not p.exists():
            continue
        import pyarrow.parquet as pq
        avail = set(pq.ParquetFile(p).schema.names)
        cols = ["date", "code", "fwd_ret_5", "ln_mktcap", "is_tradable"] + \
               [f for f in FACTORS if f in avail]
        df = pd.read_parquet(p, columns=[c for c in cols if c in avail])
        df = df[df["is_tradable"].fillna(False) & df["fwd_ret_5"].notna()]
        if df.empty:
            continue
        dates = pd.Index(np.sort(df["date"].unique()))
        codes = pd.Index(np.sort(df["code"].unique()))

        def W(col):
            w = df.pivot(index="date", columns="code", values=col).reindex(
                index=dates, columns=codes)
            return w.astype("float32").to_numpy()

        ret = W("fwd_ret_5")
        mcap = W("ln_mktcap")
        r_rank_all = pd.DataFrame(ret).rank(axis=1, pct=True).to_numpy()
        # 剔除最小 30%：按当日对数市值分位
        thr = np.nanquantile(mcap, EXCLUDE_Q, axis=1, keepdims=True)
        big_mask = mcap > thr

        for f in FACTORS:
            if f not in df.columns:
                continue
            M = W(f)
            fr_all = pd.DataFrame(M).rank(axis=1, pct=True).to_numpy()
            ic_all = _ic(fr_all, r_rank_all)
            # 小池：把被剔除的样本置为 NaN
            M2 = np.where(big_mask, M, np.nan)
            fr_big = pd.DataFrame(M2).rank(axis=1, pct=True).to_numpy()
            ic_big = _ic(fr_big, r_rank_all)
            rows.append({"factor": f, "year": y,
                         "ic_all": np.nanmean(ic_all), "ic_big": np.nanmean(ic_big),
                         "n_all": int(np.isfinite(ic_all).sum()),
                         "n_big": int(np.isfinite(ic_big).sum()),
                         "_ica": ic_all, "_icb": ic_big})
        print(f"  [{y}] dates={len(dates)} codes={len(codes)}", flush=True)

    if not rows:
        print("[universe] 无数据")
        return 1
    df = pd.DataFrame(rows)

    out = []
    for f, g in df.groupby("factor"):
        ica = np.concatenate([x for x in g["_ica"]])
        icb = np.concatenate([x for x in g["_icb"]])
        sa = metrics.ic_summary(pd.Series(ica).dropna(), 252)
        sb = metrics.ic_summary(pd.Series(icb).dropna(), 252)
        out.append({
            "factor": f,
            "IC_全样本": sa["ic_mean"], "ICIR_全样本": sa["ic_ir_ann"],
            "t_全样本": sa["t_nw"],
            "IC_剔除小30%": sb["ic_mean"], "ICIR_剔除小30%": sb["ic_ir_ann"],
            "t_剔除小30%": sb["t_nw"],
            "IC变化%": (sb["ic_mean"] / sa["ic_mean"] - 1) * 100
            if sa["ic_mean"] not in (0, np.nan) and np.isfinite(sa["ic_mean"]) else np.nan,
        })
    res = pd.DataFrame(out).sort_values("t_全样本", key=lambda s: -s.abs())
    res.to_csv(config.REPORTS / "universe_test.csv", index=False, encoding="utf-8-sig")
    print("\n== A. 全样本 vs 剔除最小 30%（h=5，2013-2026）==")
    print(res.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    # B. t>3 门槛重判
    ev = pd.read_csv(config.REPORTS / "factor_eval.csv")
    ev["t_abs"] = ev["t_nw"].abs()
    n2 = int((ev["t_abs"] > 2).sum())
    n3 = int((ev["t_abs"] > 3).sum())
    print(f"\n== B. 显著性门槛 ==")
    print(f"39 个因子中：t>2 的 {n2} 个；t>3 的 {n3} 个（HLZ 2016 建议门槛）")
    ev["门槛"] = np.where(ev["t_abs"] > 3, "t>3 通过",
                          np.where(ev["t_abs"] > 2, "仅 t>2 通过", "不显著"))
    ev[["factor", "family", "ic_mean", "ic_mean_neu", "icir_ann", "t_nw", "门槛"]] \
        .sort_values("t_nw", key=lambda s: -s.abs()) \
        .to_csv(config.REPORTS / "factor_significance_t3.csv", index=False,
                encoding="utf-8-sig")
    print(ev["门槛"].value_counts().to_string())
    print(f"\n[universe] DONE {now_cn()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
