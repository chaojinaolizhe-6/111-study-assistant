"""过拟合诊断：夏普比率的显著性、多重检验惩罚、回测过拟合概率。

这一模块回答三个不同的问题，很多人把它们混为一谈：

1. **PSR / DSR**：我这条净值曲线，扣除"运气"之后还显著吗？
   - PSR 只考虑单次检验。
   - DSR 额外惩罚"我一共试了多少次"——试得越多，需要越高的夏普才能算数。
2. **PBO（回测过拟合概率）**：我在样本内挑出的"最优参数"，
   到了样本外还有多大概率仍然靠前？这是对**选择过程**的体检，不是对策略的体检。
3. **Bootstrap / 分块重抽样**：净值曲线本身的置信区间，不依赖正态假设。

公式来源
--------
* Bailey & López de Prado (2014), The Deflated Sharpe Ratio.
* Bailey, Borwein, López de Prado & Zhu (2017), The Probability of Backtest Overfitting.
* Lo (2002) 关于年化与自相关对夏普比率的影响。

约定：所有夏普比率在函数内部用**未年化**的样本夏普，年化只在展示层做。
"""
from __future__ import annotations

import itertools
from math import comb, e, log, sqrt

import numpy as np
import pandas as pd
from scipy import stats as st

EULER = 0.5772156649015329


# ---------------------------------------------------------------- 基础指标
def sharpe(returns: np.ndarray | pd.Series, periods: int = 252) -> float:
    r = np.asarray(returns, dtype=float)
    r = r[np.isfinite(r)]
    if len(r) < 2 or r.std(ddof=1) == 0:
        return np.nan
    return float(r.mean() / r.std(ddof=1) * sqrt(periods))


def ann_return(returns: np.ndarray | pd.Series, periods: int = 252) -> float:
    r = np.asarray(returns, dtype=float)
    r = r[np.isfinite(r)]
    if len(r) == 0:
        return np.nan
    return float((1 + r).prod() ** (periods / len(r)) - 1)


def max_drawdown(returns: np.ndarray | pd.Series) -> float:
    r = np.asarray(returns, dtype=float)
    r = np.where(np.isfinite(r), r, 0.0)
    nav = np.cumprod(1 + r)
    peak = np.maximum.accumulate(nav)
    return float((nav / peak - 1).min())


def summary_stats(returns: np.ndarray | pd.Series, periods: int = 252) -> dict:
    r = np.asarray(returns, dtype=float)
    r = r[np.isfinite(r)]
    if len(r) < 2:
        return {}
    sr = r.mean() / r.std(ddof=1) if r.std(ddof=1) > 0 else np.nan
    return {
        "n": len(r),
        "ann_return": ann_return(r, periods),
        "ann_vol": float(r.std(ddof=1) * sqrt(periods)),
        "sharpe": float(sr * sqrt(periods)),
        "max_dd": max_drawdown(r),
        "win_rate": float((r > 0).mean()),
        "skew": float(st.skew(r)),
        "kurt": float(st.kurtosis(r, fisher=False)),
    }


# ---------------------------------------------------------------- PSR / DSR
def probabilistic_sharpe(returns, sr_benchmark: float = 0.0) -> float:
    """PSR：真实夏普大于 sr_benchmark 的概率（考虑偏度与峰度）。"""
    r = np.asarray(returns, dtype=float)
    r = r[np.isfinite(r)]
    T = len(r)
    if T < 10:
        return np.nan
    sd = r.std(ddof=1)
    if sd == 0:
        return np.nan
    sr = r.mean() / sd
    g3 = st.skew(r)
    g4 = st.kurtosis(r, fisher=False)
    denom = 1 - g3 * sr + (g4 - 1) / 4 * sr ** 2
    if denom <= 0:
        return np.nan
    z = (sr - sr_benchmark) * sqrt(T - 1) / sqrt(denom)
    return float(st.norm.cdf(z))


def expected_max_sharpe(n_trials: float, sigma_sr: float) -> float:
    """N 次独立试验下，样本夏普最大值的期望（Gumbel 极值近似）。

    E[max SR] ≈ σ_SR [ (1-γ) Φ⁻¹(1 - 1/N) + γ Φ⁻¹(1 - 1/(N e)) ]
    """
    if n_trials is None or n_trials <= 1:
        return 0.0
    if sigma_sr <= 0 or not np.isfinite(sigma_sr):
        return 0.0
    a = st.norm.ppf(1 - 1.0 / n_trials)
    b = st.norm.ppf(1 - 1.0 / (n_trials * e))
    return float(sigma_sr * ((1 - EULER) * a + EULER * b))


def effective_n_trials(returns_matrix: np.ndarray | pd.DataFrame) -> float:
    """用相关矩阵的有效秩估计"独立试验次数"，避免把 100 个高度相关的参数当 100 次。

    两种口径都给：
      N1 = 1 + (M-1)(1 - ρ̄)   平均相关系数近似
      N2 = (Σλ)² / Σλ²          特征值有效秩
    返回两者较小的一个（惩罚较弱，不能代表未记录的研究搜索）。
    """
    X = np.asarray(returns_matrix, dtype=float)
    X = X[np.isfinite(X).all(axis=1)]
    if X.ndim != 2 or X.shape[1] < 2 or X.shape[0] < 5:
        return 1.0
    with np.errstate(invalid="ignore", divide="ignore"):
        C = np.corrcoef(X, rowvar=False)
    C = np.nan_to_num(C, nan=0.0)
    np.fill_diagonal(C, 1.0)
    M = C.shape[0]
    off = C[~np.eye(M, dtype=bool)]
    rho = off.mean() if off.size else 0.0
    n1 = 1 + (M - 1) * (1 - rho)
    lam = np.linalg.eigvalsh(C)
    lam = np.clip(lam, 1e-12, None)
    n2 = lam.sum() ** 2 / (lam ** 2).sum()
    return float(max(1.0, min(n1, n2)))


def deflated_sharpe(returns, n_trials: float | None = None,
                    sigma_sr: float | None = None,
                    trial_matrix: np.ndarray | pd.DataFrame | None = None,
                    periods: int = 252) -> dict:
    """DSR = PSR 的"多重检验"版本。

    参数
    ----
    returns     : 待检验策略的收益序列
    n_trials    : 假定的独立试验数；显式给出时优先于矩阵估计
    sigma_sr    : 各次试验夏普的横截面标准差；缺失时用 1/sqrt(T-1) 的理论值
    trial_matrix: T x M 的候选策略收益矩阵，用来自动估计 N 与 σ_SR

    返回 dict：sr（未年化）、sr_ann、sr0（基准）、dsr、n_eff、sigma_sr
    """
    r = np.asarray(returns, dtype=float)
    r = r[np.isfinite(r)]
    T = len(r)
    if T < 20:
        return {"error": "样本太短"}
    sd = r.std(ddof=1)
    sr = r.mean() / sd if sd > 0 else np.nan

    if trial_matrix is not None:
        X = np.asarray(trial_matrix, dtype=float)
        if n_trials is None:
            n_trials = effective_n_trials(X)
        if sigma_sr is None:
            mu = np.nanmean(X, axis=0)
            sdd = np.nanstd(X, axis=0, ddof=1)
            with np.errstate(invalid="ignore", divide="ignore"):
                srs = mu / sdd
            srs = srs[np.isfinite(srs)]
            sigma_sr = float(np.std(srs, ddof=1)) if len(srs) > 1 else None
    if sigma_sr is None:
        sigma_sr = 1.0 / sqrt(max(T - 1, 1))
    if n_trials is None:
        n_trials = 1.0

    sr0 = expected_max_sharpe(float(max(1, n_trials)), sigma_sr)
    g3 = st.skew(r)
    g4 = st.kurtosis(r, fisher=False)
    denom = 1 - g3 * sr + (g4 - 1) / 4 * sr ** 2
    z = (sr - sr0) * sqrt(T - 1) / sqrt(denom) if denom > 0 else np.nan
    return {
        "T": T,
        "sr": float(sr),
        "sr_ann": float(sr * sqrt(periods)),
        "n_eff": float(n_trials),
        "sigma_sr": float(sigma_sr),
        "sr0": float(sr0),
        "sr0_ann": float(sr0 * sqrt(periods)),
        "dsr": float(st.norm.cdf(z)) if np.isfinite(z) else np.nan,
        "psr": probabilistic_sharpe(r),
        "skew": float(g3),
        "kurt": float(g4),
    }


def min_track_record_length(returns, target_sr: float = 0.0,
                            confidence: float = 0.95) -> float:
    """达到给定置信度所需的最短样本长度（交易日）。

    回答"我这段 8 个月的漂亮净值，够不够说明问题"。
    """
    r = np.asarray(returns, dtype=float)
    r = r[np.isfinite(r)]
    if len(r) < 10:
        return np.nan
    sd = r.std(ddof=1)
    sr = r.mean() / sd
    g3 = st.skew(r)
    g4 = st.kurtosis(r, fisher=False)
    z = st.norm.ppf(confidence)
    num = 1 - g3 * sr + (g4 - 1) / 4 * sr ** 2
    den = (sr - target_sr) ** 2
    if den <= 0:
        return np.inf
    return float(1 + num / den * z ** 2)


# ---------------------------------------------------------------- PBO / CSCV
def pbo_cscv(returns_matrix: np.ndarray | pd.DataFrame, n_blocks: int = 16,
             metric: str = "sharpe", seed: int = 0) -> dict:
    """组合对称交叉验证（CSCV）估计回测过拟合概率。

    参数
    ----
    returns_matrix : T x M，M 个候选策略（参数组合）在同一时间轴上的收益
    n_blocks       : 时间分块数 S（必须为偶数）。S=16 时共 C(16,8)=12870 个组合，
                     每块约 T/16 个交易日。块太短会让块内夏普估计噪声过大。

    返回
    ----
    pbo        : P(样本内最优策略在样本外落到后半区)
    logits     : 各组合的 λ
    oos_rank   : 样本外排名分位
    """
    X = np.asarray(returns_matrix, dtype=float)
    X = X[np.isfinite(X).all(axis=1)]
    T, M = X.shape
    if M < 2 or T < n_blocks * 5:
        return {"pbo": np.nan, "error": "样本或策略数不足"}
    if n_blocks % 2:
        n_blocks += 1
    S = n_blocks
    bounds = np.linspace(0, T, S + 1).astype(int)
    blocks = [X[bounds[i]:bounds[i + 1]] for i in range(S)]

    def perf(a: np.ndarray) -> np.ndarray:
        mu = a.mean(axis=0)
        sd = a.std(axis=0, ddof=1)
        with np.errstate(invalid="ignore", divide="ignore"):
            v = mu / sd
        return np.where(np.isfinite(v), v, -np.inf)

    logits, oos_rank = [], []
    combos = list(itertools.combinations(range(S), S // 2))
    for combo in combos:
        is_idx = list(combo)
        oos_idx = [i for i in range(S) if i not in combo]
        IS = np.concatenate([blocks[i] for i in is_idx])
        OOS = np.concatenate([blocks[i] for i in oos_idx])
        r_is = perf(IS)
        r_oos = perf(OOS)
        n_star = int(np.argmax(r_is))
        # 样本外排名（1 = 最差，M = 最好）
        order = st.rankdata(r_oos, method="average")
        rank = order[n_star]
        omega = rank / (M + 1)
        logits.append(log(omega / (1 - omega)))
        oos_rank.append(omega)

    logits = np.array(logits)
    return {
        "pbo": float((logits <= 0).mean()),
        "n_combos": len(combos),
        "logits": logits,
        "oos_rank": np.array(oos_rank),
        "median_logit": float(np.median(logits)),
        "n_blocks": S,
    }


def performance_degradation(is_perf: np.ndarray, oos_perf: np.ndarray) -> dict:
    """样本内 -> 样本外的退化回归：OOS = a + b * IS。

    b < 1 说明样本内表现无法线性外推；b <= 0 说明"越好的参数样本外越差"，
    这是过拟合最强形式的证据。
    """
    x = np.asarray(is_perf, float)
    y = np.asarray(oos_perf, float)
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 3:
        return {}
    b, a = np.polyfit(x[m], y[m], 1)
    r = np.corrcoef(x[m], y[m])[0, 1]
    return {"slope": float(b), "intercept": float(a), "corr": float(r)}


# ---------------------------------------------------------------- Bootstrap
def block_bootstrap_sharpe(returns, n_boot: int = 2000, block: int = 20,
                           periods: int = 252, seed: int = 42) -> dict:
    """分块 bootstrap 给夏普比率一个不依赖正态假设的置信区间。"""
    r = np.asarray(returns, dtype=float)
    r = r[np.isfinite(r)]
    T = len(r)
    if T < 60:
        return {}
    rng = np.random.default_rng(seed)
    n_blocks = int(np.ceil(T / block))
    out = np.empty(n_boot)
    for i in range(n_boot):
        starts = rng.integers(0, T - block + 1, n_blocks)
        samp = np.concatenate([r[s:s + block] for s in starts])[:T]
        sd = samp.std(ddof=1)
        out[i] = samp.mean() / sd * sqrt(periods) if sd > 0 else np.nan
    out = out[np.isfinite(out)]
    return {
        "mean": float(out.mean()),
        "p025": float(np.percentile(out, 2.5)),
        "p975": float(np.percentile(out, 97.5)),
        "p05": float(np.percentile(out, 5)),
        "p50": float(np.percentile(out, 50)),
        "p95": float(np.percentile(out, 95)),
        "prob_positive": float((out > 0).mean()),
    }


def reality_check(returns_matrix: np.ndarray | pd.DataFrame, benchmark=0.0,
                  n_boot: int = 1000, block: int = 20, seed: int = 7) -> dict:
    """White's Reality Check / Hansen SPA 的简化版。

    原假设：N 个策略里最好的那个也不优于基准。用**同一天同一块**重抽样，
    保留策略之间的相关性，得到 max(超额夏普) 的零分布。
    """
    X = np.asarray(returns_matrix, dtype=float)
    X = X[np.isfinite(X).all(axis=1)]
    T, M = X.shape
    if T < 60 or M < 2:
        return {}
    f = X - benchmark
    mu = f.mean(axis=0)
    sd = f.std(axis=0, ddof=1)
    sd[sd == 0] = np.inf
    obs = (mu / sd).max()
    rng = np.random.default_rng(seed)
    n_blocks = int(np.ceil(T / block))
    maxes = np.empty(n_boot)
    for i in range(n_boot):
        starts = rng.integers(0, T - block + 1, n_blocks)
        idx = np.concatenate([np.arange(s, s + block) for s in starts])[:T]
        samp = f[idx]
        m = samp.mean(axis=0) - mu          # 去均值，构造零分布
        s = samp.std(axis=0, ddof=1)
        s[s == 0] = np.inf
        maxes[i] = (m / s).max()
    return {
        "obs_max_sr": float(obs),
        "p_value": float((maxes >= obs).mean()),
        "boot_mean": float(maxes.mean()),
        "boot_p95": float(np.percentile(maxes, 95)),
    }
