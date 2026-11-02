"""样本外验证：Purged K-Fold、Embargo、组合 Purged CV（CPCV）、Walk-Forward。

为什么普通 K-Fold 一定错
------------------------
金融样本是**重叠**的：若用 t 日的特征预测 t+1..t+5 的收益，那么 t 日与 t+4 日
的标签共享未来信息。随机切分训练/测试集时，测试集的未来会漏进训练集，
于是样本外表现被系统性高估。这类泄漏不会报错，只会让你以为找到了 alpha。

三个层次的对策
--------------
1. **Purge（清洗）**：把训练集中标签区间与测试集标签区间重叠的样本删掉。
2. **Embargo（禁运）**：在测试集之后额外留一段空档，切断"特征回看窗"造成的
   反向泄漏（训练集的特征窗口若伸进测试期，等于用了测试期的信息）。
3. **CPCV**：把时间切成 N 块、每次留 2 块做测试，穷举所有组合，
   得到 C(N,2) 条完整的样本外回测路径，用来估计"策略表现的分布"而不是一个点。
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class Split:
    train: np.ndarray
    test: np.ndarray
    name: str = ""


def purged_kfold(n: int, k: int = 5, embargo: int = 5, horizon: int = 5) -> list[Split]:
    """按时间顺序切 k 折，并对每一折做 purge + embargo。

    参数
    ----
    n        : 样本（交易日）个数
    k        : 折数
    embargo  : 测试段之后额外禁运的交易日数，通常 >= horizon
    horizon  : 标签持有期（交易日），决定向前 purging 的长度

    返回的 train/test 都是 **位置索引** 数组。
    """
    idx = np.arange(n)
    folds = np.array_split(idx, k)
    out: list[Split] = []
    for i, test in enumerate(folds):
        t0, t1 = test[0], test[-1]
        drop = np.zeros(n, dtype=bool)
        # purge：训练样本的标签窗口 [pos, pos+horizon] 与测试段 [t0, t1] 相交则剔除
        drop[max(0, t0 - horizon): t1 + 1] = True
        # embargo：测试段之后一段也剔除，防止特征窗口伸进测试期
        drop[t1 + 1: min(n, t1 + 1 + embargo)] = True
        train = idx[~drop]
        out.append(Split(train=train, test=test, name=f"fold{i}"))
    return out


def cpcv(n: int, n_groups: int = 6, k_test: int = 2, embargo: int = 5,
         horizon: int = 5) -> list[Split]:
    """组合 purged 交叉验证。

    切 N 组，每次取 k 组做测试，其余做训练（训练集内部同样 purge）。
    路径数 = C(N, k) * k / N，即每个策略评估会得到 C(N,k)*k/N 条独立回测。
    """
    groups = np.array_split(np.arange(n), n_groups)
    out: list[Split] = []
    for combo in itertools.combinations(range(n_groups), k_test):
        test = np.concatenate([groups[g] for g in combo])
        drop = np.zeros(n, dtype=bool)
        # 标记整个测试区段（可能不连续）
        for g in combo:
            seg = groups[g]
            drop[max(0, seg[0] - horizon): seg[-1] + 1] = True
        # embargo 针对每个测试段的尾部
        for g in combo:
            seg = groups[g]
            drop[seg[-1] + 1: min(n, seg[-1] + 1 + embargo)] = True
        train = np.arange(n)[~drop]
        out.append(Split(train=np.sort(train), test=np.sort(test),
                         name="cpcv_" + "-".join(map(str, combo))))
    return out


def n_paths(n_groups: int, k_test: int = 2) -> int:
    """CPCV 能产生的独立回测路径数：C(N,k)*k/N。"""
    from math import comb
    return comb(n_groups, k_test) * k_test // n_groups


def walk_forward(n: int, train_size: int, test_size: int, step: int | None = None,
                 embargo: int = 5, horizon: int = 5) -> list[Split]:
    """滚动的样本外回测：训练窗口固定长度向前推进，每次预测紧随其后的一段。"""
    step = step or test_size
    out: list[Split] = []
    start = 0
    while start + train_size + test_size <= n:
        tr = np.arange(start, start + train_size)
        te = np.arange(start + train_size + embargo, start + train_size + embargo + test_size)
        te = te[te < n]
        if len(te) < test_size // 2:
            break
        # 训练集尾部 purge
        tr = tr[tr < te[0] - horizon]
        out.append(Split(train=tr, test=te, name=f"wf{start}"))
        start += step
    return out


def expanding_walk_forward(n: int, min_train: int, test_size: int,
                           step: int | None = None, embargo: int = 5,
                           horizon: int = 5) -> list[Split]:
    """扩展窗口版本：训练集从起点开始不断变长，更贴近"越做越久"的真实研究。"""
    step = step or test_size
    out: list[Split] = []
    t = min_train
    while t + embargo + test_size <= n:
        te = np.arange(t + embargo, min(n, t + embargo + test_size))
        tr = np.arange(0, t)
        tr = tr[tr < te[0] - horizon]
        out.append(Split(train=tr, test=te, name=f"ewf{t}"))
        t += step
    return out


def describe_splits(splits: list[Split], dates: pd.Index) -> pd.DataFrame:
    rows = []
    for s in splits:
        rows.append({
            "name": s.name,
            "train_n": len(s.train),
            "test_n": len(s.test),
            "train_start": dates[s.train[0]] if len(s.train) else None,
            "train_end": dates[s.train[-1]] if len(s.train) else None,
            "test_start": dates[s.test[0]] if len(s.test) else None,
            "test_end": dates[s.test[-1]] if len(s.test) else None,
        })
    return pd.DataFrame(rows)
