"""Forward returns shared by the main and supplementary research pipelines."""
from __future__ import annotations


def forward_open_return(adj_open, horizon: int, groups=None):
    """Signal at t; entry at t+1 open; exit at t+1+h open.

    Input must be sorted by date within security. Shifts count observed bars,
    as in the original panel; missing sessions are a separate data limitation.
    Never substitute close prices or forward-fill missing prices here.
    """
    if not isinstance(horizon, int) or horizon < 1:
        raise ValueError("horizon must be a positive integer")
    prices = adj_open.astype("float64")
    source = prices if groups is None else prices.groupby(groups, observed=True)
    entry = source.shift(-1)
    return source.shift(-(1 + horizon)) / entry.where(entry > 0) - 1
