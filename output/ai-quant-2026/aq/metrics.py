"""因子评价：IC / ICIR / 分层 / 换手 / 衰减。

约定
----
* **Rank IC**（Spearman）：截面排名相关，抗极值，是选股因子的标准指标。
* **ICIR** = mean(IC) / std(IC) * sqrt(年化期数)，日频取 252。
* **Newey-West t**：IC 序列存在自相关（尤其用重叠标签时），普通 t 会高估显著性。
* **分层收益**：按因子值分 Q 组，检验单调性——单调性比 IC 均值更能说明不是噪声。
* **换手率**：因子排序的稳定性，直接决定成本。

所有输入都是宽表（index=日期, columns=股票）。
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def _clean_pair(f: pd.DataFrame, r: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    common_d = f.index.intersection(r.index)
    common_c = f.columns.intersection(r.columns)
    return f.loc[common_d, common_c], r.loc[common_d, common_c]


def rank_ic(f: pd.DataFrame, r: pd.DataFrame, min_n: int = 30) -> pd.Series:
    """逐日 Spearman 相关（等价于先排名再算 Pearson）。"""
    f, r = _clean_pair(f, r)
    fr = f.rank(axis=1)
    rr = r.rank(axis=1)
    mask = fr.notna() & rr.notna()
    a = fr.where(mask)
    b = rr.where(mask)
    n = mask.sum(axis=1)
    am = a.sub(a.mean(axis=1), axis=0)
    bm = b.sub(b.mean(axis=1), axis=0)
    num = (am * bm).sum(axis=1, min_count=1)
    den = np.sqrt((am * am).sum(axis=1, min_count=1) * (bm * bm).sum(axis=1, min_count=1))
    ic = num / den.replace(0, np.nan)
    return ic.where(n >= min_n)


def pearson_ic(f: pd.DataFrame, r: pd.DataFrame, min_n: int = 30) -> pd.Series:
    f, r = _clean_pair(f, r)
    mask = f.notna() & r.notna()
    a = f.where(mask)
    b = r.where(mask)
    n = mask.sum(axis=1)
    am = a.sub(a.mean(axis=1), axis=0)
    bm = b.sub(b.mean(axis=1), axis=0)
    num = (am * bm).sum(axis=1, min_count=1)
    den = np.sqrt((am * am).sum(axis=1, min_count=1) * (bm * bm).sum(axis=1, min_count=1))
    return (num / den.replace(0, np.nan)).where(n >= min_n)


def newey_west_t(x: pd.Series, lags: int | None = None) -> float:
    """Bartlett HAC, autocovariances normalized by n (not n-lag)."""
    return mean_inference(x, lags)["t_nw"]


def mean_inference(x: pd.Series, lags: int | None = None) -> dict:
    """Variance-equivalent sample size for the *IC series*, not factor updates.

    n_eff = n * gamma0 / long_run_variance. It is bandwidth dependent and
    can exceed n with negative autocorrelation; it is not an independence count.
    Missing IC dates are dropped; sample spacing must be disclosed by the caller.
    """
    a = np.asarray(x, dtype=float)
    a = a[np.isfinite(a)]
    n = len(a)
    lag = max(4, int(4 * (n / 100) ** (2 / 9))) if lags is None else int(lags)
    if lag < 0:
        raise ValueError("lags must be nonnegative")
    lag = min(lag, max(n - 1, 0))
    out = {"n": n, "nw_lags": lag, "n_eff": np.nan,
           "t_naive": np.nan, "t_nw": np.nan, "ic_acf1": np.nan}
    if n < 10:
        return out
    e = a - a.mean()
    g0 = float(e @ e / n)
    if g0 <= 0:
        return out
    lrv = g0 + 2 * sum((1 - k / (lag + 1)) * (e[k:] @ e[:-k]) / n
                       for k in range(1, lag + 1))
    out.update(t_naive=float(a.mean() / np.sqrt(g0 / n)),
               ic_acf1=float(e[1:] @ e[:-1] / n / g0))
    if lrv > 0:
        out.update(t_nw=float(a.mean() / np.sqrt(lrv / n)),
                   n_eff=float(n * g0 / lrv))
    return out


def pooled_factor_summary(table, raw_ic, adjusted_ic=None, adjusted_suffix="_inc"):
    """Replace averaged yearly inference with estimates from actual pooled ICs."""
    out = table.set_index("factor").copy()
    for name in raw_ic.columns:
        if name not in out.index:
            continue
        s = raw_ic[name].sort_index()
        inf = mean_inference(s)
        sm = ic_summary(s, 252, inf["nw_lags"])
        for k, v in {**inf, "ic_mean": sm["ic_mean"],
                     "icir_ann": sm["ic_ir_ann"]}.items():
            out.loc[name, k] = v
        if adjusted_ic is not None and name in adjusted_ic:
            a = adjusted_ic[name].sort_index()
            ai = mean_inference(a)
            am = ic_summary(a, 252, ai["nw_lags"])
            mean_col = "ic_mean_neu" if adjusted_suffix == "_neu" else "ic_inc"
            ir_col = "icir_ann_neu" if adjusted_suffix == "_neu" else "icir_inc"
            t_col = "t_nw_neu" if adjusted_suffix == "_neu" else "t_inc"
            for k, v in {mean_col: am["ic_mean"], ir_col: am["ic_ir_ann"],
                         t_col: ai["t_nw"], "n_eff" + adjusted_suffix: ai["n_eff"],
                         "n" + adjusted_suffix: ai["n"]}.items():
                out.loc[name, k] = v
    out["summary_method"] = "pooled_daily_ic_h5_bartlett_hac"
    out["label"] = "adj_open_t6_over_t1_minus_1"
    return out.reset_index()


def ic_summary(ic: pd.Series, periods_per_year: int = 252,
               lags: int | None = None) -> dict:
    s = ic.dropna()
    if len(s) < 10:
        return {"n": len(s), "ic_mean": np.nan, "ic_std": np.nan, "icir": np.nan,
                "t_nw": np.nan, "ic_pos_ratio": np.nan, "ic_ir_ann": np.nan}
    mu, sd = s.mean(), s.std()
    return {
        "n": len(s),
        "ic_mean": float(mu),
        "ic_std": float(sd),
        "icir": float(mu / sd) if sd > 0 else np.nan,
        "ic_ir_ann": float(mu / sd * np.sqrt(periods_per_year)) if sd > 0 else np.nan,
        "t_nw": newey_west_t(s, lags),
        "ic_pos_ratio": float((s > 0).mean()),
    }


def quantile_returns(f: pd.DataFrame, r: pd.DataFrame, q: int = 5,
                     min_n: int = 50) -> pd.DataFrame:
    """按日分位分组，返回每组等权平均前瞻收益。"""
    f, r = _clean_pair(f, r)
    mask = f.notna() & r.notna()
    f = f.where(mask)
    r = r.where(mask)
    n = mask.sum(axis=1)
    valid = n >= max(min_n, q * 10)
    fr = f.rank(axis=1, pct=True)
    out = pd.DataFrame(index=f.index, columns=range(1, q + 1), dtype=float)
    for k in range(1, q + 1):
        lo = (k - 1) / q
        hi = k / q
        sel = (fr > lo) & (fr <= hi) if k > 1 else (fr <= hi)
        sel = sel & mask
        cnt = sel.sum(axis=1).replace(0, np.nan)
        out[k] = (r.where(sel).sum(axis=1) / cnt).where(valid)
    return out


def quantile_spread(f: pd.DataFrame, r: pd.DataFrame, q: int = 5,
                    long: str = "top", short: str = "bottom") -> pd.Series:
    qr = quantile_returns(f, r, q)
    if long == "top":
        return qr[q] - qr[1]
    return qr[1] - qr[q]


def turnover(f: pd.DataFrame, q: float = 0.2, top: bool = True) -> pd.Series:
    """高位组合的单边换手率（0~1）。日频调仓时用它估算成本。"""
    fr = f.rank(axis=1, pct=True)
    sel = fr >= (1 - q) if top else fr <= q
    sel = sel.fillna(False)
    prev = sel.shift(1).fillna(False)
    inter = (sel & prev).sum(axis=1)
    n_cur = sel.sum(axis=1).replace(0, np.nan)
    n_prev = prev.sum(axis=1).replace(0, np.nan)
    # 单边换手：卖出一半 + 买入一半，标准定义取 1 - overlap/avg_size
    return (1 - inter / ((n_cur + n_prev) / 2)).clip(0, 1)


def autocorr(f: pd.DataFrame, lag: int = 1) -> pd.Series:
    """因子截面排名的自相关，衡量因子"粘性"。"""
    fr = f.rank(axis=1, pct=True)
    a = fr.iloc[:-lag]
    b = fr.iloc[lag:]
    a = a.sub(a.mean(axis=1), axis=0)
    b = b.sub(b.mean(axis=1), axis=0)
    num = (a.values * b.values)
    den = np.sqrt((a.values ** 2).sum(axis=1) * (b.values ** 2).sum(axis=1))
    return pd.Series(np.nansum(num, axis=1) / den, index=a.index)


def decay(f: pd.DataFrame, returns: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """因子在不同持有期上的 IC，用来判断"这个信号多久失效"。"""
    rows = []
    for h, r in returns.items():
        ic = rank_ic(f, r)
        s = ic.dropna()
        rows.append({
            "horizon": h,
            "ic_mean": s.mean(),
            "icir": s.mean() / s.std() if s.std() > 0 else np.nan,
            "t_nw": newey_west_t(s),
        })
    return pd.DataFrame(rows)


def factor_corr(mats: dict[str, pd.DataFrame], sample_days: int = 250) -> pd.DataFrame:
    """因子之间的平均截面 Spearman 相关。

    这是判断「新因子是不是老因子的换皮」的第一道筛子：
    相关性 > 0.7 的两个因子，几乎没有独立价值。
    """
    names = list(mats)
    if len(names) < 2:
        return pd.DataFrame(index=names, columns=names, dtype=float)
    corr = np.zeros((len(names), len(names)))
    cnt = 0
    dates = None
    for i, a in enumerate(names):
        if dates is None:
            dates = mats[a].index[-sample_days:]
    for dt in dates:
        vals = []
        for n in names:
            v = mats[n].loc[dt] if dt in mats[n].index else None
            vals.append(v.rank() if v is not None else None)
        for i in range(len(names)):
            for j in range(i, len(names)):
                if vals[i] is None or vals[j] is None:
                    continue
                m = vals[i].notna() & vals[j].notna()
                if m.sum() < 30:
                    continue
                c = np.corrcoef(vals[i][m], vals[j][m])[0, 1]
                if np.isfinite(c):
                    corr[i, j] += c
                    corr[j, i] += c if i != j else 0
        cnt += 1
    if cnt:
        corr = corr / cnt
        np.fill_diagonal(corr, 1.0)
    return pd.DataFrame(corr, index=names, columns=names)

