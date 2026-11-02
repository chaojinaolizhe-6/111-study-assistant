r"""Step 6 — 逐因子计算、单因子评价、因子面板落盘。

性能设计（这一段决定了 17 年数据能不能在半小时内跑完）
----------------------------------------------------
朴素写法每天每因子做一次截面排序 + 一次行业市值回归，复杂度是
$O(T \cdot F \cdot (n\log n + nk^2))$，在 $T=250$、$F=40$、$n=4000$、$k=32$ 时约 40 分钟／年。
本脚本做了三件事：

1. **收益率的截面排名只算一次**。四个持有期的收益矩阵先各自 rank 好，因子 IC 直接复用。
2. **因子排名只算一次**。IC、分层、换手共用同一个 rank 矩阵。
3. **设计矩阵只分解一次**。同一天所有因子共用同一个 $X$，先做 QR 得到 $Q$，
   再用 $Y - Q(Q^\top Y)$ 一次性投影掉全部因子。

另外按年切块、前后各留 420/45 天缓冲，把峰值内存压在 1 GB 以内。

产出
----
data/factors/{year}.parquet   当年因子值（去极值+标准化后）+ 标签 + 标记
reports/factor_eval.csv       单因子评价汇总（原始 / 中性化两套）
data/ic_series.parquet        每个因子每日 IC 序列
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aq import config, metrics
from aq.db import connect, init_db
from aq.factors import FACTORS, Wide
from aq.neutralize import _design_matrix, preprocess
from aq.panel import build_panel, load_fin, load_float_shares

PERIODS = 252
HORIZONS = (1, 5, 10, 20)


# --------------------------------------------------------------------------
def industry_map(conn) -> pd.Series:
    cur = pd.read_sql_query("SELECT code, board FROM stock", conn).set_index("code")["board"]
    try:
        val = pd.read_sql_query(
            "SELECT code, date, board FROM valuation WHERE board IS NOT NULL", conn)
    except Exception:
        return cur.fillna("UNKNOWN")
    if not val.empty:
        val["date"] = pd.to_datetime(val["date"])
        last = val.sort_values("date").groupby("code")["board"].last()
        cur = cur.copy()
        cur.update(last)
    return cur.fillna("UNKNOWN")


def build_designs(ind: pd.DataFrame, size: pd.DataFrame, dates: pd.Index) -> dict:
    """逐日预计算正交基 Q 与有效列，供所有因子共用。"""
    out = {}
    for dt in dates:
        s = size.loc[dt]
        g = ind.loc[dt]
        mask = s.notna() & g.notna()
        if mask.sum() < 30 or g[mask].nunique() < 2:
            out[dt] = None
            continue
        X = _design_matrix(g[mask], s[mask]).to_numpy(dtype="float64")
        keep = X.std(axis=0) > 1e-12
        keep[0] = True
        X = X[:, keep]
        try:
            Q, _ = np.linalg.qr(X)
        except np.linalg.LinAlgError:
            out[dt] = None
            continue
        out[dt] = (Q, mask.to_numpy())
    return out


def neutralize_fast(F: np.ndarray, designs: dict, dates: pd.Index) -> np.ndarray:
    """用预计算的正交基一次性残差化整个因子矩阵。"""
    out = np.full_like(F, np.nan, dtype="float64")
    for i, dt in enumerate(dates):
        d = designs.get(dt)
        if d is None:
            continue
        Q, mask = d
        y = F[i, mask]
        ok = np.isfinite(y)
        if ok.sum() < 30:
            continue
        col = np.full(mask.sum(), np.nan)
        col[ok] = y[ok] - Q[ok] @ (Q[ok].T @ y[ok])
        out[i, mask] = col
    return out


def _ic_from_rank(fr: np.ndarray, rr: np.ndarray) -> np.ndarray:
    """由排名矩阵直接算逐日 Pearson（即 Spearman）。"""
    m = np.isfinite(fr) & np.isfinite(rr)
    a = np.where(m, fr, np.nan)
    b = np.where(m, rr, np.nan)
    n = m.sum(axis=1)
    am = np.nanmean(a, axis=1)
    bm = np.nanmean(b, axis=1)
    a = a - am[:, None]
    b = b - bm[:, None]
    num = np.nansum(a * b, axis=1)
    den = np.sqrt(np.nansum(a * a, axis=1) * np.nansum(b * b, axis=1))
    with np.errstate(invalid="ignore", divide="ignore"):
        ic = num / den
    ic[n < 30] = np.nan
    return ic


def metric_from_rank(fr: np.ndarray, rr: np.ndarray, min_n: int = 30) -> np.ndarray:
    return _ic_from_rank(fr, rr)


def quantile_from_rank(fr: np.ndarray, ret: np.ndarray, q: int = 5):
    """按排名分位算各组平均收益（返回 q 列的均值向量与各日矩阵）。"""
    m = np.isfinite(fr) & np.isfinite(ret)
    pct = np.full_like(fr, np.nan)
    cnt = m.sum(axis=1, keepdims=True)
    # 排名已经由调用方算好（0~1），这里直接切分位
    pct = np.where(m, fr, np.nan)
    out = np.full((fr.shape[0], q), np.nan)
    for k in range(1, q + 1):
        lo = (k - 1) / q
        hi = k / q
        sel = m & (pct > lo) & (pct <= hi) if k > 1 else m & (pct <= hi)
        c = sel.sum(axis=1)
        with np.errstate(invalid="ignore", divide="ignore"):
            out[:, k - 1] = np.where(c > 0, np.nansum(np.where(sel, ret, np.nan), axis=1) / c, np.nan)
    out[cnt[:, 0] < 100] = np.nan
    return out


def turnover_from_rank(fr: np.ndarray, q: float = 0.2) -> np.ndarray:
    sel = fr >= (1 - q)
    sel = np.where(np.isfinite(fr), sel, False)
    prev = np.vstack([np.zeros((1, sel.shape[1]), bool), sel[:-1]])
    inter = (sel & prev).sum(axis=1)
    ncur = sel.sum(axis=1)
    nprev = prev.sum(axis=1)
    avg = (ncur + nprev) / 2.0
    with np.errstate(invalid="ignore", divide="ignore"):
        to = 1 - inter / avg
    to[avg < 20] = np.nan
    return to


# --------------------------------------------------------------------------
def run_year(conn, year: int, fin, shares, ind_map, names: list[str],
             save: bool = True):
    t0 = time.time()
    start, end = f"{year}-01-01", f"{year}-12-31"
    panel = build_panel(conn, start, end, fin=fin, shares=shares, horizons=HORIZONS)
    if panel.empty:
        return [], []
    keep = ["date", "code", "fwd_ret_1", "fwd_ret_5", "fwd_ret_10", "fwd_ret_20",
            "is_tradable", "can_buy_next", "is_st", "limit_up", "limit_down",
            "ln_mktcap", "turnover", "amount", "close", "adj_close"]

    w = Wide(panel)
    dates, codes = w.dates, w.codes
    n_d, n_c = len(dates), len(codes)

    ind = pd.DataFrame(
        np.tile(ind_map.reindex(codes).to_numpy(dtype=object), (n_d, 1)),
        index=dates, columns=codes)
    size = w("ln_mktcap")

    # 收益率排名只算一次
    rets = {h: w(f"fwd_ret_{h}").to_numpy(dtype="float32") for h in HORIZONS}
    r_rank = {}
    for h in HORIZONS:
        dfh = pd.DataFrame(rets[h], index=dates, columns=codes)
        r_rank[h] = dfh.rank(axis=1, pct=True).to_numpy(dtype="float32")
    del dfh

    designs = build_designs(ind, size, dates)

    rows, ic_frames, store = [], [], {}
    for n in names:
        try:
            raw = FACTORS[n].func(w)
        except Exception as e:  # noqa: BLE001
            print(f"  [factor] {n} FAILED {type(e).__name__}: {e}", flush=True)
            continue
        arr = raw.to_numpy(dtype="float32")
        if not np.isfinite(arr).any():
            continue
        fr = pd.DataFrame(arr, index=dates, columns=codes).rank(axis=1, pct=True)
        fr = fr.to_numpy(dtype="float32")

        ic_h = {h: _ic_from_rank(fr, r_rank[h]) for h in HORIZONS}
        s5 = metrics.ic_summary(pd.Series(ic_h[5], index=dates), PERIODS)

        qmat = quantile_from_rank(fr, rets[5], 5)
        spread = qmat[:, 4] - qmat[:, 0]
        qmean = np.nanmean(qmat, axis=0)
        mono = np.corrcoef(np.arange(1, 6), qmean)[0, 1] if np.isfinite(qmean).all() else np.nan
        to = turnover_from_rank(fr, 0.2)

        # 中性化：去极值 + 标准化 -> 用预计算正交基残差化
        clean = preprocess(raw, "mad", 5.0)
        neu = neutralize_fast(clean.to_numpy(dtype="float64"), designs, dates)
        neu_df = pd.DataFrame(neu, index=dates, columns=codes)
        nrank = neu_df.rank(axis=1, pct=True)
        ic5n = _ic_from_rank(nrank.to_numpy(dtype="float32"), r_rank[5])
        s5n = metrics.ic_summary(pd.Series(ic5n, index=dates), PERIODS)

        rows.append({
            "factor": n, "year": year, "family": FACTORS[n].category,
            "ic_mean": s5["ic_mean"], "ic_std": s5["ic_std"],
            "icir_ann": s5["ic_ir_ann"], "t_nw": s5["t_nw"],
            "ic_pos_ratio": s5["ic_pos_ratio"], "n_days": s5["n"],
            "ic_mean_neu": s5n["ic_mean"], "icir_ann_neu": s5n["ic_ir_ann"],
            "t_nw_neu": s5n["t_nw"],
            "ic_h1": float(np.nanmean(ic_h[1])), "ic_h10": float(np.nanmean(ic_h[10])),
            "ic_h20": float(np.nanmean(ic_h[20])),
            "q_spread": float(np.nanmean(spread)),
            "monotonic": float(mono) if np.isfinite(mono) else np.nan,
            "turnover": float(np.nanmean(to)),
        })
        ic_frames.append(pd.DataFrame({
            "date": dates, "factor": n, "ic": ic_h[5], "ic_neu": ic5n}))

        # 落盘：风格因子不做中性化（否则 size 对市值中性化等于归零），
        # 其余因子存"中性化 + 重新标准化"后的值，直接可喂模型。
        if n in ("size", "beta_60"):
            keep_df = clean
        else:
            mu = neu_df.mean(axis=1)
            sd = neu_df.std(axis=1).replace(0, np.nan)
            keep_df = neu_df.sub(mu, axis=0).div(sd, axis=0)
        store[n] = keep_df.astype("float32").stack()
        del raw, arr, fr, clean, neu, neu_df, nrank, keep_df

    if not store:
        return rows, ic_frames

    fac = pd.DataFrame(store)
    fac.index.names = ["date", "code"]
    fac = fac.reset_index().replace([np.inf, -np.inf], np.nan)
    out = panel[keep].merge(fac, on=["date", "code"], how="left")
    if save:
        p = config.DATA / "factors"
        p.mkdir(parents=True, exist_ok=True)
        out.to_parquet(p / f"{year}.parquet", index=False, compression="zstd")
    print(f"  [{year}] panel={len(panel):,} codes={n_c} factors={len(store)} "
          f"{time.time() - t0:.0f}s", flush=True)
    return rows, ic_frames


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, default=2010)
    ap.add_argument("--end", type=int, default=2026)
    ap.add_argument("--factors", default="")
    ap.add_argument("--no-save", action="store_true")
    args = ap.parse_args()

    conn = connect()
    init_db(conn)
    fin = load_fin(conn)
    shares = load_float_shares(conn)
    ind_map = industry_map(conn)
    names = ([x.strip() for x in args.factors.split(",") if x.strip()]
             if args.factors else list(FACTORS))
    print(f"[factors] {len(names)} factors, years {args.start}-{args.end}", flush=True)

    all_rows, all_ic = [], []
    for y in range(args.start, args.end + 1):
        rows, ic = run_year(conn, y, fin, shares, ind_map, names,
                            save=not args.no_save)
        all_rows.extend(rows)
        all_ic.extend(ic)

    if all_rows:
        ev = pd.DataFrame(all_rows)
        ev.to_csv(config.REPORTS / "factor_eval_by_year.csv", index=False,
                  encoding="utf-8-sig")
        agg = (ev.groupby("factor")
               .agg(family=("family", "first"), years=("year", "nunique"),
                    ic_mean=("ic_mean", "mean"), icir_ann=("icir_ann", "mean"),
                    t_nw=("t_nw", "mean"),
                    ic_mean_neu=("ic_mean_neu", "mean"),
                    icir_ann_neu=("icir_ann_neu", "mean"),
                    q_spread=("q_spread", "mean"),
                    monotonic=("monotonic", "mean"),
                    turnover=("turnover", "mean"))
               .reset_index().sort_values("icir_ann", ascending=False))
        pooled = pd.concat(all_ic, ignore_index=True)
        raw_ic = pooled.pivot(index="date", columns="factor", values="ic")
        neu_ic = pooled.pivot(index="date", columns="factor", values="ic_neu")
        agg = metrics.pooled_factor_summary(agg, raw_ic, neu_ic, "_neu")
        agg.to_csv(config.REPORTS / "factor_eval.csv", index=False, encoding="utf-8-sig")
        print("\n== 单因子评价（按 ICIR 排序）==")
        print(agg.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    if all_ic:
        pd.concat(all_ic, ignore_index=True).to_parquet(
            config.DATA / "ic_series.parquet", index=False, compression="zstd")
    print("[factors] DONE", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

