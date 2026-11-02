"""因子预处理：去极值、标准化、行业 + 市值中性化。

为什么必须做
------------
* 去极值：A 股有大量"净资产为负→BP 爆炸""净利润接近 0→EP 爆炸"的样本，
  一个 500 倍 PE 的股票会直接把线性回归的系数带偏。
* 标准化：让不同量纲的因子可以相加、可以喂给树模型（树模型不需要，但便于解释）。
* 中性化：如果不剥离行业与市值，你所谓的"新因子"很可能只是"小盘股因子"或
  "医药行业因子"的换皮。中性化后剩下的残差才是增量信息。

实现选择
--------
截面回归残差，而不是分组 demean：
  分组 demean 只能处理离散分组（行业），无法同时控制连续的 log 市值；
  回归可以一次剥离行业哑变量 + log 市值，且残差与解释变量严格正交。

所有函数都在 **宽表** 上操作（行=日期，列=股票）。
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def winsorize_mad(x: pd.DataFrame, n: float = 5.0) -> pd.DataFrame:
    """按日中位数绝对偏差（MAD）缩尾，比 3σ 更抗厚尾。"""
    med = x.median(axis=1)
    mad = (x.sub(med, axis=0)).abs().median(axis=1)
    scale = 1.4826 * mad  # 使 MAD 与正态 σ 可比
    lo = med - n * scale
    hi = med + n * scale
    return x.clip(lower=lo, upper=hi, axis=0)


def winsorize_pct(x: pd.DataFrame, lo: float = 0.01, hi: float = 0.99) -> pd.DataFrame:
    q = x.quantile([lo, hi], axis=1).T
    return x.clip(lower=q[lo], upper=q[hi], axis=0)


def cross_zscore(x: pd.DataFrame) -> pd.DataFrame:
    """截面标准化；剔除样本过少的日期。"""
    mu = x.mean(axis=1)
    sd = x.std(axis=1)
    z = x.sub(mu, axis=0).div(sd.replace(0, np.nan), axis=0)
    return z


def cross_rank(x: pd.DataFrame) -> pd.DataFrame:
    """截面百分位排名，映射到 [-0.5, 0.5]，天然抗极值。"""
    return x.rank(axis=1, pct=True) - 0.5


def preprocess(x: pd.DataFrame, method: str = "mad", n: float = 5.0) -> pd.DataFrame:
    """去极值 + 标准化（因子评价前的标准动作）。"""
    if method == "mad":
        x = winsorize_mad(x, n)
    elif method == "pct":
        x = winsorize_pct(x)
    return cross_zscore(x)


def _design_matrix(industry: pd.DataFrame, size: pd.DataFrame) -> pd.DataFrame:
    """构造 行业哑变量 + log 市值 的设计矩阵（行=股票，列=特征）。"""
    ind = industry.astype("string").fillna("UNKNOWN")
    dummies = pd.get_dummies(ind, prefix="ind", drop_first=True, dtype=float)
    d = pd.concat([dummies, size.rename("ln_mktcap")], axis=1)
    d.insert(0, "const", 1.0)
    return d


def neutralize(x: pd.DataFrame, industry: pd.DataFrame, size: pd.DataFrame,
               n_jobs: int = 1) -> pd.DataFrame:
    """逐日截面回归取残差： x = α + Σβ·行业哑变量 + γ·ln(市值) + ε，返回 ε。

    参数
    ----
    x        : 因子宽表（index=日期, columns=股票）
    industry : 行业宽表，同形状（字符串）
    size     : log 市值宽表，同形状

    注意：同一天的所有因子共用同一个设计矩阵，因此对 X 做一次 QR 分解，
    再用 Q 把整块因子矩阵投影掉，比逐因子回归快一个数量级。
    """
    out = pd.DataFrame(np.nan, index=x.index, columns=x.columns)
    common_dates = x.index.intersection(industry.index).intersection(size.index)
    for dt in common_dates:
        y_row = x.loc[dt]
        mask = y_row.notna() & size.loc[dt].notna() & industry.loc[dt].notna()
        if mask.sum() < 30:
            continue
        sub = y_row[mask]
        ind_sub = industry.loc[dt][mask]
        # 行业类别过少（<2）时退化为仅市值中性
        if ind_sub.nunique() < 2:
            continue
        X = _design_matrix(ind_sub, size.loc[dt][mask]).to_numpy(dtype=float)
        # 去掉全零列，避免奇异
        keep = X.std(axis=0) > 1e-12
        keep[0] = True
        X = X[:, keep]
        y = sub.to_numpy(dtype=float)
        # 最小二乘残差（lstsq 内部已做 QR，2000×32 规模下足够快）
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        resid = y - X @ beta
        out.loc[dt, sub.index] = resid
    return out


def neutralize_panel(x: pd.DataFrame, industry: pd.DataFrame, size: pd.DataFrame,
                     **kw) -> pd.DataFrame:
    """neutralize 的别名，保持接口语义清晰。"""
    return neutralize(x, industry, size, **kw)


# 语义更明确的别名：行业 + 市值 中性化
neutral_industry_size_wide = neutralize
