"""Step 7 — 多模型、多验证协议的重复测试。

核心问题
--------
"我的模型样本外 Rank IC 是 0.05"这句话本身没有意义，除非同时说清：
样本外怎么切的？试了多少组配置？这个数字在 15 次不同切法下的波动有多大？
扣掉交易成本、扣掉多重检验惩罚之后还剩什么？

本脚本把这些"必须一起说"的数字一次性算出来：

  A. 5 折 Purged K-Fold        -> 5 段互不重叠的样本外
  B. 组合 Purged CV (CPCV)     -> C(6,2)=15 次切分，评估"切法"本身的不确定性
  C. 扩展窗口 Walk-Forward     -> 模拟"每季度重训一次"的真实流程
  D. 5 个随机种子的 LightGBM   -> 模型自身的随机稳定性
  E. 等权合成 / Ridge / LightGBM 三条基线

最后给出条件性的 DSR 敏感性与仅覆盖当前候选的 PBO；研究搜索史不完整，不能统一裁决。
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aq import config, cv, metrics, stats
from aq.audit import search_diagnostics, refresh_ic_inference
from aq.factors import FACTORS

warnings.filterwarnings("ignore")

H = 5
STEP = 5
COST_BP = 30.0
TOP_Q = 0.2


def load_dataset(years: range, step: int = STEP) -> tuple[pd.DataFrame, list[str]]:
    """两遍读取：先只读日期列确定采样日，再按需读因子列。

    直接 concat 14 年全量会占用 3 GB 以上内存；先过滤再拼接，
    峰值降到 600 MB 左右，这是"在 16 GB 机器上做严肃研究"的必要工程。
    """
    from aq.factors import FACTORS as _F

    paths = [config.DATA / "factors" / f"{y}.parquet" for y in years]
    paths = [p for p in paths if p.exists()]
    if not paths:
        raise SystemExit("没有因子文件，先跑 06_factors.py")

    # 各年文件列数不同：换手类因子要等 2018 年估值快照才有值，
    # 因此必须取所有年份的列并集，否则模型会静默丢掉 6 个因子。
    import pyarrow.parquet as pq
    all_cols = set()
    for p in paths:
        all_cols |= set(pq.ParquetFile(p).schema.names)
    cols_needed = [c for c in _F if c in all_cols]

    udates = sorted(set().union(*[
        set(pd.read_parquet(p, columns=["date"])["date"].unique()) for p in paths]))
    udates = np.array(udates)
    keep = set(udates[::step])

    frames = []
    for p in paths:
        df = pd.read_parquet(p)
        for c in cols_needed:
            if c not in df.columns:
                df[c] = np.nan
        m = df["is_tradable"].fillna(False) & df["fwd_ret_5"].notna() & df["date"].isin(keep)
        sub = df.loc[m, ["date", "code", "fwd_ret_5", "can_buy_next"] + cols_needed]
        frames.append(sub)
        del df

    out = pd.concat(frames, ignore_index=True)
    out["date"] = pd.to_datetime(out["date"])
    out = out.sort_values(["date", "code"]).reset_index(drop=True)
    return out, cols_needed


def make_label(df: pd.DataFrame, method: str = "rank") -> pd.Series:
    g = df.groupby("date", observed=True)["fwd_ret_5"]
    if method == "rank":
        return g.rank(pct=True) - 0.5
    if method == "cls":
        return (g.rank(pct=True) > 0.7).astype(float)
    r = df["fwd_ret_5"]
    return r.clip(r.quantile(0.005), r.quantile(0.995))


def portfolio_returns(df: pd.DataFrame, score: np.ndarray, q: float = TOP_Q):
    d = df[["date", "code", "fwd_ret_5", "can_buy_next"]].copy()
    d["s"] = score
    d = d[d["s"].notna() & d["can_buy_next"]]
    rets, turns, prev = {}, {}, set()
    for dt, g in d.groupby("date", observed=True):
        if len(g) < 100:
            continue
        rk = g["s"].rank(pct=True)
        top = set(g.loc[rk > 1 - q, "code"])
        rets[dt] = (g.loc[rk > 1 - q, "fwd_ret_5"].mean()
                    - g.loc[rk <= q, "fwd_ret_5"].mean())
        if prev:
            turns[dt] = 1 - len(top & prev) / max(len(top), 1)
        prev = top
    r = pd.Series(rets).sort_index()
    t = pd.Series(turns).reindex(r.index).fillna(0.0)
    return r, t


def evaluate(df: pd.DataFrame, score: np.ndarray, label: str = "") -> dict:
    d = df.assign(s=score)
    ics = [g["s"].corr(g["fwd_ret_5"], method="spearman")
           for _, g in d.groupby("date", observed=True) if len(g) >= 100]
    ic = pd.Series(ics).dropna()
    gross, turn = portfolio_returns(d, d["s"].to_numpy())
    net = gross - turn * 2 * COST_BP / 1e4
    s = stats.summary_stats(net, periods=252 / STEP)
    n_per = max(len(gross), 1)
    return {
        "label": label, "n_dates": int(len(ic)),
        "ic_mean": float(ic.mean()), "ic_std": float(ic.std()),
        "icir_ann": float(ic.mean() / ic.std() * np.sqrt(252 / STEP)) if ic.std() > 0 else np.nan,
        "t_nw": metrics.newey_west_t(ic, lags=H),
        "ic_pos": float((ic > 0).mean()),
        "ls_ann_gross": float((1 + gross).prod() ** (252 / STEP / n_per) - 1) if len(gross) else np.nan,
        "ls_ann_net": s.get("ann_return"),
        "sharpe_net": s.get("sharpe"),
        "mdd_net": s.get("max_dd"),
        "turnover": float(turn.mean()),
        "net": net, "gross": gross, "turn_s": turn,
    }


def fit_composite(X_tr, y_tr, X_te, feats):
    signs = []
    for c in feats:
        a = np.nan_to_num(X_tr[c].to_numpy(dtype="float64"))
        b = np.nan_to_num(y_tr.to_numpy(dtype="float64"))
        if a.std() < 1e-12:
            signs.append(1.0)
            continue
        ic = np.corrcoef(a, b)[0, 1]
        signs.append(1.0 if (not np.isfinite(ic) or ic >= 0) else -1.0)
    w = np.array(signs)
    a = np.nan_to_num(X_te[feats].to_numpy(dtype="float32")) * w
    return a.sum(axis=1)


def fit_ridge(X_tr, y_tr, X_te, feats):
    from sklearn.linear_model import Ridge
    a = np.nan_to_num(X_tr[feats].to_numpy(dtype="float32"))
    b = np.nan_to_num(X_te[feats].to_numpy(dtype="float32"))
    m = Ridge(alpha=10.0)
    m.fit(a, y_tr.to_numpy())
    return m.predict(b)


def fit_lgbm(X_tr, y_tr, X_te, feats, seed: int = 0):
    import lightgbm as lgb
    a = np.nan_to_num(X_tr[feats].to_numpy(dtype="float32"))
    b = np.nan_to_num(X_te[feats].to_numpy(dtype="float32"))
    m = lgb.LGBMRegressor(
        objective="regression", n_estimators=300, learning_rate=0.03,
        num_leaves=15, max_depth=4, min_child_samples=200,
        subsample=0.8, subsample_freq=1, colsample_bytree=0.8,
        reg_lambda=5.0, random_state=seed, verbose=-1, n_jobs=8)
    m.fit(a, y_tr.to_numpy())
    return m.predict(b)


CANDIDATES = {
    "composite": lambda tr, te, f: fit_composite(tr[f], tr["y"], te[f], f),
    "ridge": lambda tr, te, f: fit_ridge(tr[f], tr["y"], te[f], f),
    "lgbm_s0": lambda tr, te, f: fit_lgbm(tr[f], tr["y"], te[f], f, 0),
    "lgbm_s1": lambda tr, te, f: fit_lgbm(tr[f], tr["y"], te[f], f, 1),
    "lgbm_s2": lambda tr, te, f: fit_lgbm(tr[f], tr["y"], te[f], f, 2),
}


def protocol_test(df, feats, n):
    rows = []
    protocols = {
        "purged_kfold": cv.purged_kfold(n, k=5, embargo=H, horizon=H),
        "cpcv": cv.cpcv(n, n_groups=6, k_test=2, embargo=H, horizon=H),
        "walk_forward": cv.expanding_walk_forward(n, min_train=int(n * 0.35),
                                                  test_size=60, step=60,
                                                  embargo=H, horizon=H),
    }
    for pname, splits in protocols.items():
        for mname in ("composite", "ridge", "lgbm_s0"):
            fn = CANDIDATES[mname]
            for sp in splits:
                tr = df[df["_t"].isin(sp.train)]
                te = df[df["_t"].isin(sp.test)]
                if len(tr) < 5000 or len(te) < 800:
                    continue
                sc = fn(tr, te, feats)
                r = evaluate(te, sc, label=mname)
                r.pop("net"); r.pop("gross")
                r.update({"protocol": pname, "model": mname, "fold": sp.name})
                rows.append(r)
    return pd.DataFrame(rows)


def walk_forward_matrix(df, feats, n):
    splits = cv.expanding_walk_forward(n, min_train=int(n * 0.3), test_size=60,
                                       step=60, embargo=H, horizon=H)
    preds = []
    for sp in splits:
        tr = df[df["_t"].isin(sp.train)]
        te = df[df["_t"].isin(sp.test)]
        if len(tr) < 5000 or len(te) < 500:
            continue
        block = te[["date", "code", "fwd_ret_5", "can_buy_next"]].copy()
        for name, fn in CANDIDATES.items():
            block[name] = fn(tr, te, feats)
        preds.append(block)
    return pd.concat(preds, ignore_index=True) if preds else pd.DataFrame()


def refresh_diagnostics_from_cache():
    """Rebuild candidate observations from saved predictions, without refitting."""
    wf = pd.read_parquet(config.DATA / "wf_predictions.parquet")
    old = json.loads((config.REPORTS / "diagnostics.json").read_text(encoding="utf-8"))
    rows, returns = [], {}
    for name in CANDIDATES:
        r = evaluate(wf, wf[name].to_numpy(), label=name)
        returns[name] = r.pop("net")
        r.pop("gross"); r.pop("turn_s")
        rows.append(r)
    cand = pd.DataFrame(rows).sort_values("ic_mean", ascending=False)
    cand.to_csv(config.REPORTS / "candidates_oos.csv", index=False, encoding="utf-8-sig")
    R = pd.DataFrame(returns).sort_index()
    R.to_csv(config.REPORTS / "candidate_returns.csv", encoding="utf-8-sig")
    best = cand.iloc[0]["label"]
    old.update(search_diagnostics(R, best, periods=252 / STEP))
    old["best_candidate"] = best
    old["candidates"] = cand.to_dict(orient="records")
    old["candidate_missing_periods"] = R.isna().sum().to_dict()
    (config.REPORTS / "diagnostics.json").write_text(
        json.dumps(old, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    refresh_ic_inference()
    print("[audit] cached predictions: refreshed DSR/PBO/IC; no models refitted")
    print("[audit] DSR stress scenario:", old["dsr"])
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, default=2013)
    ap.add_argument("--end", type=int, default=2026)
    ap.add_argument("--label", default="rank", choices=["rank", "ret", "cls"])
    ap.add_argument("--diagnostics-only", action="store_true", help="recompute inference from saved predictions/IC")
    args = ap.parse_args()
    if args.diagnostics_only:
        return refresh_diagnostics_from_cache()

    t0 = time.time()
    df, feats = load_dataset(range(args.start, args.end + 1))
    df["y"] = make_label(df, args.label)
    df = df[df["y"].notna()].reset_index(drop=True)
    dates = np.sort(df["date"].unique())
    pos = pd.Series(np.arange(len(dates)), index=pd.DatetimeIndex(dates))
    df["_t"] = df["date"].map(pos)
    n = len(dates)
    print(f"[model] rows={len(df):,} dates={len(dates)} feats={len(feats)} "
          f"{pd.Timestamp(dates[0]).date()}~{pd.Timestamp(dates[-1]).date()}", flush=True)

    res = protocol_test(df, feats, n)
    res.to_csv(config.REPORTS / "model_tests.csv", index=False, encoding="utf-8-sig")
    agg = (res.groupby(["protocol", "model"])
           .agg(n=("ic_mean", "size"), ic_mean=("ic_mean", "mean"),
                ic_std=("ic_mean", "std"), icir_ann=("icir_ann", "mean"),
                t_nw=("t_nw", "mean"), sharpe_net=("sharpe_net", "mean"),
                ls_ann_net=("ls_ann_net", "mean"))
           .reset_index())
    print("\n== 协议 x 模型 ==")
    print(agg.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    wf = walk_forward_matrix(df, feats, n)
    if wf.empty:
        print("[model] walk-forward 无可用切分")
        return 1
    wf.to_parquet(config.DATA / "wf_predictions.parquet", index=False, compression="zstd")

    cand_rows, ret_mat, turn_mat = [], {}, {}
    for name in CANDIDATES:
        r = evaluate(wf, wf[name].to_numpy(), label=name)
        ret_mat[name] = r["net"]
        turn_mat[name] = r["turn_s"]
        r.pop("net"); r.pop("gross"); r.pop("turn_s")
        cand_rows.append(r)
    cand = pd.DataFrame(cand_rows).sort_values("ic_mean", ascending=False)
    cand.to_csv(config.REPORTS / "candidates_oos.csv", index=False, encoding="utf-8-sig")
    print("\n== Walk-forward 全样本外 ==")
    print(cand[["label", "n_dates", "ic_mean", "icir_ann", "t_nw",
                "ls_ann_net", "sharpe_net", "mdd_net", "turnover"]]
          .to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    # ---- 成本敏感性：用毛收益与逐期换手重算 ----
    cost_curve = []
    for bp in (0, 10, 20, 30, 40, 50, 60, 80):
        sharpes = []
        for name in ret_mat:
            g = ret_mat[name] + turn_mat[name] * 2 * COST_BP / 1e4  # 还原毛收益
            net = g - turn_mat[name] * 2 * bp / 1e4
            sd = net.std(ddof=1)
            sharpes.append(net.mean() / sd * np.sqrt(252 / STEP) if sd > 0 else np.nan)
        cost_curve.append({"cost_bp": bp, "sharpe_mean": float(np.nanmean(sharpes)),
                           "sharpe_best": float(np.nanmax(sharpes))})
    pd.DataFrame(cost_curve).to_csv(config.REPORTS / "cost_sensitivity.csv",
                                    index=False, encoding="utf-8-sig")

    # 种子稳定性
    seed_rows = []
    splits = cv.expanding_walk_forward(n, min_train=int(n * 0.3), test_size=60,
                                       step=60, embargo=H, horizon=H)
    if splits:
        sp = splits[len(splits) // 2]
        tr = df[df["_t"].isin(sp.train)]
        te = df[df["_t"].isin(sp.test)]
        for s in range(5):
            sc = fit_lgbm(tr[feats], tr["y"], te[feats], feats, seed=s)
            r = evaluate(te, sc, label=f"seed{s}")
            r.pop("net"); r.pop("gross")
            seed_rows.append(r)
    seeds = pd.DataFrame(seed_rows)
    seeds.to_csv(config.REPORTS / "seed_stability.csv", index=False, encoding="utf-8-sig")

    R = pd.DataFrame(ret_mat).dropna(how="all")
    best = cand.iloc[0]["label"]
    audit = search_diagnostics(R, best, periods=252 / STEP)
    dsr, boot = audit["dsr"], audit["bootstrap"]


    diag = {
        "rows": int(len(df)), "dates": int(n), "features": int(len(feats)),
        "start": str(pd.Timestamp(dates[0]).date()),
        "end": str(pd.Timestamp(dates[-1]).date()),
        "wf_periods": int(len(R)), "best_candidate": best,
        "best_ic": float(cand.iloc[0]["ic_mean"]),
        "ic_range": [float(cand["ic_mean"].min()), float(cand["ic_mean"].max())],
        "ic_mean_across": float(cand["ic_mean"].mean()),
        "ic_std_across": float(cand["ic_mean"].std()),
        **audit,
        "cost_curve": cost_curve,
        "seed_ic_std": float(seeds["ic_mean"].std()) if not seeds.empty else None,
        "protocol_table": agg.to_dict(orient="records"),
        "candidates": cand[["label", "ic_mean", "icir_ann", "t_nw",
                            "ls_ann_net", "sharpe_net", "mdd_net", "turnover"]]
                      .to_dict(orient="records"),
    }
    with open(config.REPORTS / "diagnostics.json", "w", encoding="utf-8") as f:
        json.dump(diag, f, ensure_ascii=False, indent=2, default=float)

    print("\n== 过拟合诊断 ==")
    print(f"  PBO = {diag['pbo']:.3f} (组合数 {diag['pbo_combos']})")
    print(f"  Reality Check p = {diag['rc_p']:.3f}")
    print(f"  DSR = {dsr['dsr']:.3f}  SR_ann={dsr['sr_ann']:.2f}  SR0_ann={dsr['sr0_ann']:.2f}"
          f"  N_assumed={dsr['n_eff']:.1f}")
    print(f"  bootstrap 95%CI = [{boot.get('p025', float('nan')):.2f}, "
          f"{boot.get('p975', float('nan')):.2f}]")
    R.to_csv(config.REPORTS / "candidate_returns.csv", encoding="utf-8-sig")
    print(f"\n[model] DONE {time.time() - t0:.0f}s", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
