"""Step 15 — 指数增强回测：A 股唯一可执行的形态。

为什么必须做这一步
------------------
第 11 章的所有收益都是\textbf{多空}口径（做多前 20%、做空后 20%）。
但 A 股个股融券基本不可行（2023--2024 监管收紧、暂停转融券），
负向信号只能"低配"，不能"做空"。所以可实现的形态是\textbf{指数增强}：
组合 = 基准权重 + 主动偏离，收益 = 基准 + 超额，风险 = 跟踪误差。

本脚本把 Walk-Forward 的样本外预测（由 07_model.py 落盘）套进指数增强框架：

  1. 基准：可交易全市场的\textbf{流通市值加权}组合。
     不用官方指数，因为本地只有单期成分快照，用当期成分回测历史
     会重新引入第 2 章批判过的成分股幸存者偏差。
  2. 主动偏离：行业内标准化打分后，按 w_i = W_g · ω_i·e^{κ z_i} / Σ 构造，
     其中 ω_i 是行业内基准权重，W_g 是行业基准权重。
     这个形式保证\textbf{行业权重与基准完全一致}，且权重恒为正（天然满足 long-only）。
  3. κ 扫描：κ 越大偏离越激进，跟踪误差越大。画出一条
     "跟踪误差 -- 信息比率" 的有效前沿。
  4. 成本：与多空版一致，单边 30 bp，按实际换手扣。

局限（写进讲义，不掩饰）：
  * 行业用当前行业分类，非历史 PIT；
  * 基准是可交易全市场加权，不是沪深 300 / 中证 500；
  * 未模拟整手、资金约束、涨跌停的路径依赖（只按 can_buy_next 剔除样本）。
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aq import config
from aq.db import connect, now_cn

warnings.filterwarnings("ignore")

KAPPAS = [0.0, 0.2, 0.5, 1.0, 2.0, 3.0, 5.0]
COST_BP = 30.0
PERIODS = 252 / 5


def load() -> pd.DataFrame:
    wf = pd.read_parquet(config.DATA / "wf_predictions.parquet")
    wf["date"] = pd.to_datetime(wf["date"])

    frames = []
    for y in range(2013, 2027):
        p = config.DATA / "factors" / f"{y}.parquet"
        if not p.exists():
            continue
        d = pd.read_parquet(p, columns=["date", "code", "ln_mktcap", "turnover"])
        frames.append(d)
    mcap = pd.concat(frames, ignore_index=True)
    mcap["date"] = pd.to_datetime(mcap["date"])

    conn = connect()
    ind = pd.read_sql_query("SELECT code, board FROM stock", conn).rename(
        columns={"board": "industry"})
    conn.close()

    df = wf.merge(mcap, on=["date", "code"], how="left")
    df = df.merge(ind, on="code", how="left")
    df["industry"] = df["industry"].fillna("UNKNOWN")
    df["mktcap"] = np.exp(df["ln_mktcap"])
    return df


def build_weights(g: pd.DataFrame, score: np.ndarray, kappa: float) -> pd.Series:
    """行业内基准权重 * exp(kappa*z) 归一，保证行业权重 = 基准行业权重。"""
    d = g.assign(s=score)
    d = d[np.isfinite(d["s"]) & np.isfinite(d["mktcap"]) & (d["mktcap"] > 0)]
    if len(d) < 100:
        return pd.Series(dtype=float)
    total = d["mktcap"].sum()
    wb = d["mktcap"] / total
    d = d.assign(wb=wb)

    # 行业内标准化
    def zs(x):
        sd = x.std()
        return (x - x.mean()) / sd if sd and sd > 0 else x * 0.0

    d["z"] = d.groupby("industry", observed=True)["s"].transform(zs).fillna(0.0)
    # 行业内：omega_i * exp(kappa z_i) 归一
    d["omega"] = d["wb"] / d.groupby("industry", observed=True)["wb"].transform("sum")
    d["num"] = d["omega"] * np.exp(np.clip(kappa * d["z"], -5, 5))
    d["v"] = d["num"] / d.groupby("industry", observed=True)["num"].transform("sum")
    Wg = d.groupby("industry", observed=True)["wb"].transform("sum")
    w = (Wg * d["v"]).fillna(0.0)
    return pd.Series(w.to_numpy(), index=d["code"].to_numpy()).groupby(level=0).sum()


def main() -> int:
    df = load()
    dates = np.sort(df["date"].unique())
    # 只用市值可得的日期（估值快照 2018 起）
    cover = df.groupby("date")["mktcap"].apply(lambda s: s.notna().mean())
    ok_dates = [d for d in dates if cover.get(d, 0) > 0.8]
    print(f"[ie] 全部 {len(dates)} 期，市值覆盖达标 {len(ok_dates)} 期 "
          f"({pd.Timestamp(ok_dates[0]).date()} ~ {pd.Timestamp(ok_dates[-1]).date()})", flush=True)

    cands = [c for c in df.columns if c in ("composite", "lgbm_s0")]
    rows = []
    for name in cands:
        for kappa in KAPPAS:
            prev = pd.Series(dtype=float)
            recs = []
            for d in ok_dates:
                g = df[df["date"] == d]
                g = g[g["can_buy_next"].fillna(False)]
                if len(g) < 200:
                    continue
                w = build_weights(g, g[name].to_numpy(), kappa)
                if w.empty:
                    continue
                # 基准
                gg = g[np.isfinite(g["mktcap"]) & (g["mktcap"] > 0)]
                wb = gg["mktcap"] / gg["mktcap"].sum()
                bench = float((wb * gg["fwd_ret_5"]).sum())
                # 组合
                ww = w.reindex(g["code"]).fillna(0.0)
                port_gross = float((ww * g.set_index("code")["fwd_ret_5"]).sum())
                # 换手与成本
                idx = ww.index
                pv = prev.reindex(idx).fillna(0.0)
                to = float((ww - pv).abs().sum()) / 2.0
                cost = to * 2 * COST_BP / 1e4
                recs.append({"date": d, "port": port_gross - cost,
                             "bench": bench, "turnover": to,
                             "n": int((ww > 0).sum())})
                prev = ww[ww > 0]
            if not recs:
                continue
            r = pd.DataFrame(recs).set_index("date")
            ex = r["port"] - r["bench"]
            te = float(ex.std(ddof=1) * np.sqrt(PERIODS))
            ir = float(ex.mean() / ex.std(ddof=1) * np.sqrt(PERIODS)) if ex.std() > 0 else np.nan
            n = len(r)
            ann_p = float((1 + r["port"]).prod() ** (PERIODS / n) - 1)
            ann_b = float((1 + r["bench"]).prod() ** (PERIODS / n) - 1)
            cum = (1 + ex).cumprod()
            mdd = float((cum / cum.cummax() - 1).min())
            rows.append({
                "candidate": name, "kappa": kappa, "periods": n,
                "ann_port": ann_p, "ann_bench": ann_b,
                "ann_excess": ann_p - ann_b,
                "tracking_error": te, "IR": ir,
                "excess_mdd": mdd,
                "turnover": float(r["turnover"].mean()),
                "avg_holdings": float(r["n"].mean()),
            })
        print(f"  [{name}] done", flush=True)

    res = pd.DataFrame(rows)
    res.to_csv(config.REPORTS / "index_enhance_ext.csv", index=False, encoding="utf-8-sig")
    print("\n== 指数增强（long-only，行业中性，扣单边 30bp）==")
    print(res.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    best = res.loc[res.groupby("candidate")["IR"].idxmax()] if len(res) else None
    if best is not None:
        print("\n== 每个候选的最优 kappa ==")
        print(best.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    print(f"\n[ie] DONE {now_cn()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
