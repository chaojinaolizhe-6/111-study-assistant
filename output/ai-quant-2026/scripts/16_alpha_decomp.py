"""Step 16 — alpha 到底在多头端还是空头端？

背景
----
第 11.5 节发现：把多空信号放进指数增强（long-only）框架后，超额是负的。
一种解释是"alpha 全在空头端"。本节直接把这个说法量化：

  价差 = (多头端 − 全样本均值) + (全样本均值 − 空头端)
         \______ 多头贡献 ______/   \______ 空头贡献 ______/

并对两端分别做 Newey-West 检验。同时按市值三分组，看多头端是否只在某一档有效。

三种基准口径：
  * 等权全样本（EW）：不受市值结构影响，衡量"纯排序能力"
  * 市值加权（CW）：即第 11.5 节的基准，衡量"能不能赚到钱"
两者之差，正好是"多头端偏向小盘"带来的影响。
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

Q = 0.2
PERIODS = 252 / 5


def ann(s: pd.Series) -> float:
    s = s.dropna()
    if len(s) == 0:
        return np.nan
    return float((1 + s).prod() ** (PERIODS / len(s)) - 1)


def nw(s: pd.Series) -> float:
    return metrics.newey_west_t(s.dropna(), lags=4)


def main() -> int:
    wf = pd.read_parquet(config.DATA / "wf_predictions.parquet")
    wf["date"] = pd.to_datetime(wf["date"])

    frames = []
    for y in range(2013, 2027):
        p = config.DATA / "factors" / f"{y}.parquet"
        if p.exists():
            frames.append(pd.read_parquet(p, columns=["date", "code", "ln_mktcap"]))
    mc = pd.concat(frames, ignore_index=True)
    mc["date"] = pd.to_datetime(mc["date"])
    df = wf.merge(mc, on=["date", "code"], how="left")
    df["mktcap"] = np.exp(df["ln_mktcap"])

    cand = "lgbm_s0"
    recs = []
    for d, g in df.groupby("date", observed=True):
        g = g[g["can_buy_next"].fillna(False) & g[cand].notna() & g["fwd_ret_5"].notna()]
        if len(g) < 200:
            continue
        rk = g[cand].rank(pct=True)
        top = g[rk > 1 - Q]["fwd_ret_5"].mean()
        bot = g[rk <= Q]["fwd_ret_5"].mean()
        ew = g["fwd_ret_5"].mean()
        gm = g[np.isfinite(g["mktcap"]) & (g["mktcap"] > 0)]
        cw = (float((gm["mktcap"] / gm["mktcap"].sum() * gm["fwd_ret_5"]).sum())
              if len(gm) > 200 else np.nan)
        recs.append({"date": d, "top": top, "bot": bot, "ew": ew, "cw": cw,
                     "spread": top - bot,
                     "long_ex_ew": top - ew, "short_ex_ew": ew - bot,
                     "long_ex_cw": top - cw, "short_ex_cw": cw - bot})
    r = pd.DataFrame(recs).set_index("date").sort_index()
    print(f"[decomp] 期数 {len(r)}  {r.index[0].date()} ~ {r.index[-1].date()}", flush=True)

    rows = []
    for col, label in [("spread", "多空价差"),
                       ("long_ex_ew", "多头端超额(等权)"),
                       ("short_ex_ew", "空头端超额(等权)"),
                       ("long_ex_cw", "多头端超额(市值加权)"),
                       ("short_ex_cw", "空头端超额(市值加权)")]:
        s = r[col].dropna()
        rows.append({"项目": label, "期数": len(s),
                     "年化": ann(s), "NW_t": nw(s),
                     "胜率": float((s > 0).mean())})
    tab = pd.DataFrame(rows)
    tab.to_csv(config.REPORTS / "alpha_decomposition.csv", index=False, encoding="utf-8-sig")
    print("\n== alpha 的两端分解（2013-2026，h=5，每 5 日）==")
    print(tab.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    # 按市值三分组
    tri = []
    for d, g in df.groupby("date", observed=True):
        g = g[g["can_buy_next"].fillna(False) & g[cand].notna() & g["fwd_ret_5"].notna()
              & np.isfinite(g["mktcap"]) & (g["mktcap"] > 0)]
        if len(g) < 300:
            continue
        g = g.assign(tercile=pd.qcut(g["mktcap"].rank(method="first"), 3,
                                     labels=["小", "中", "大"]))
        for t in ("小", "中", "大"):
            gg = g[g["tercile"] == t]
            if len(gg) < 60:
                continue
            rk = gg[cand].rank(pct=True)
            tri.append({"date": d, "组": t,
                        "多头超额": gg[rk > 1 - Q]["fwd_ret_5"].mean() - gg["fwd_ret_5"].mean(),
                        "价差": (gg[rk > 1 - Q]["fwd_ret_5"].mean()
                                 - gg[rk <= Q]["fwd_ret_5"].mean())})
    t3 = pd.DataFrame(tri)
    if not t3.empty:
        out = []
        for t in ("小", "中", "大"):
            s = t3[t3["组"] == t].set_index("date")
            out.append({"市值组": t, "多头端超额": ann(s["多头超额"]),
                        "多头端NW_t": nw(s["多头超额"]),
                        "组内价差": ann(s["价差"]), "价差NW_t": nw(s["价差"])})
        o = pd.DataFrame(out)
        o.to_csv(config.REPORTS / "alpha_by_size.csv", index=False, encoding="utf-8-sig")
        print("\n== 按市值三分组 ==")
        print(o.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    print(f"\n[decomp] DONE {now_cn()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
