"""Step 11 — 资金流因子族：新增 8 个因子 + 与已知因子的换皮检验。

为什么单独做
------------
本地库完全没有资金流数据。外加快照提供了超大单/大单/中单/小单四档的
流入、流出、成交量与笔数，可以构造一个全新的因子族。

但先要回答一个问题：**资金流因子是不是"当日涨跌幅"或"换手率"的换皮？**
A 股的主力净流入与当日涨跌高度同向，而涨跌幅本身已经是反转因子的原料。
所以本脚本除了算 IC，还强制输出三个东西：
  1. 与 rev_5 / turn_20 / vol_20 的截面相关性
  2. 中性化（对涨跌幅与换手）之后的增量 IC
  3. 分层单调性

只有增量 IC 仍然显著，这个因子族才算"新信息"。

口径
----
所有资金流都除以当日成交额，变成无量纲的"净流入强度"，
否则大市值股票会天然占优（金额绝对值不可比）。
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aq import config, metrics
from aq.labels import forward_open_return
from aq.db import connect, now_cn

warnings.filterwarnings("ignore")

H = 5
START, END = "2020-01-01", "2026-08-31"


def wide(df, col, dates, codes):
    w = df.pivot(index="date", columns="code", values=col).reindex(
        index=dates, columns=codes)
    return w.astype("float32")


def load() -> tuple[pd.DataFrame, pd.DataFrame]:
    conn = connect()
    bar = pd.read_sql_query(
        """SELECT code, date, close, amount, turnover, adj_close, adj_open
           FROM shm_bar WHERE date BETWEEN ? AND ?""", conn, params=(START, END))
    flow = pd.read_sql_query(
        """SELECT code, date, super_in_amt, super_out_amt, big_in_amt, big_out_amt,
                  mid_in_amt, mid_out_amt, small_in_amt, small_out_amt, main_net_amt
           FROM shm_moneyflow WHERE date BETWEEN ? AND ?""", conn, params=(START, END))
    conn.close()
    for d in (bar, flow):
        d["date"] = pd.to_datetime(d["date"])
    return bar, flow


def main() -> int:
    bar, flow = load()
    print(f"[flow] bar {len(bar):,}  flow {len(flow):,}", flush=True)
    df = bar.merge(flow, on=["code", "date"], how="left").sort_values(["code", "date"])
    df = df.reset_index(drop=True)

    dates = pd.Index(np.sort(df["date"].unique()))
    codes = pd.Index(np.sort(df["code"].unique()))
    print(f"[flow] dates={len(dates)} codes={len(codes)}", flush=True)

    c = wide(df, "adj_close", dates, codes)
    ret = c / c.shift(1) - 1
    amt = wide(df, "amount", dates, codes)
    turn = wide(df, "turnover", dates, codes)

    def net(i, o):
        return wide(df, i, dates, codes) - wide(df, o, dates, codes)

    super_net = net("super_in_amt", "super_out_amt")
    big_net = net("big_in_amt", "big_out_amt")
    main_net = wide(df, "main_net_amt", dates, codes)
    small_net = net("small_in_amt", "small_out_amt")

    def ratio(x, w=1):
        a = amt if w == 1 else amt.rolling(w, min_periods=int(w * 0.6)).sum()
        b = x if w == 1 else x.rolling(w, min_periods=int(w * 0.6)).sum()
        return b / a.where(a > 0)

    # ---------------- 因子定义 ----------------
    F: dict[str, pd.DataFrame] = {}
    F["mfr"] = ratio(main_net)                       # 主力净流入强度(日)
    F["sfr"] = ratio(super_net)                      # 超大单净流入强度(日)
    F["bfr"] = ratio(big_net)                        # 大单净流入强度(日)
    F["lfr"] = -ratio(small_net)                     # 散户(小单)反向
    F["mfr_20"] = ratio(main_net, 20)                # 20日主力净流入强度
    F["mfr_pos_20"] = (ratio(main_net) > 0).rolling(
        20, min_periods=12).mean()                   # 主力连续流入天数占比
    mr = ratio(main_net)
    F["mfr_stab_20"] = (mr.rolling(20, min_periods=12).mean()
                        / mr.rolling(20, min_periods=12).std()).replace(
                            [np.inf, -np.inf], np.nan)   # 资金流的稳定性(夏普式)
    F["mfr_chg"] = (mr.rolling(5, min_periods=3).mean()
                    - mr.rolling(20, min_periods=12).mean())  # 资金流加速

    # 与主面板、质量因子共用次日开盘到第 h+1 日开盘标签。
    df["fwd"] = forward_open_return(df["adj_open"], H, df["code"])
    fwd = wide(df, "fwd", dates, codes)

    # 用于换皮检验的已知因子
    known = {
        "rev_5": -(c / c.shift(5) - 1),
        "turn_20": -turn.rolling(20, min_periods=12).mean(),
        "vol_20": -ret.rolling(20, min_periods=12).std(),
    }

    rows, ic_rows, inc_rows = [], {}, {}
    for name, f in F.items():
        f = f.replace([np.inf, -np.inf], np.nan)
        ic = metrics.rank_ic(f, fwd)
        s = metrics.ic_summary(ic, 252, lags=max(H - 1, int(4 * (ic.count() / 100) ** (2 / 9))))
        q = metrics.quantile_returns(f, fwd, 5)
        spread = q[5] - q[1]
        qm = q.mean()
        mono = (np.corrcoef(range(1, 6), qm.to_numpy())[0, 1]
                if np.isfinite(qm).all() else np.nan)
        to = metrics.turnover(f, 0.2, top=True)

        # 与已知因子的截面相关（时间平均）
        corrs = {}
        for kname, kf in known.items():
            cs = []
            for dt in dates[::20]:
                if dt not in f.index or dt not in kf.index:
                    continue
                a, b = f.loc[dt], kf.loc[dt]
                m = a.notna() & b.notna()
                if m.sum() > 100:
                    cc = np.corrcoef(a[m].rank(), b[m].rank())[0, 1]
                    if np.isfinite(cc):
                        cs.append(cc)
            corrs[kname] = float(np.mean(cs)) if cs else np.nan

        # 增量 IC：对 rev_5 与 turn_20 做截面回归取残差后再算 IC
        def resid_against(x, refs):
            out = pd.DataFrame(np.nan, index=x.index, columns=x.columns)
            for dt in x.index:
                y = x.loc[dt]
                cols = [r.loc[dt] if dt in r.index else pd.Series(index=y.index)
                        for r in refs]
                X = np.column_stack([np.ones(len(y))] +
                                    [np.nan_to_num(c_.reindex(y.index).to_numpy())
                                     for c_ in cols])
                m = y.notna()
                if m.sum() < 200:
                    continue
                yy = np.nan_to_num(y[m].to_numpy())
                Xm = X[m.to_numpy()]
                beta, *_ = np.linalg.lstsq(Xm, yy, rcond=None)
                r = np.full(len(y), np.nan)
                r[m.to_numpy()] = yy - Xm @ beta
                out.loc[dt] = r
            return out

        inc = resid_against(f, [known["rev_5"], known["turn_20"]])
        ic_inc = metrics.rank_ic(inc, fwd)
        s_inc = metrics.ic_summary(ic_inc, 252)

        rows.append({
            "factor": name,
            "ic_mean": s["ic_mean"], "icir_ann": s["ic_ir_ann"], "t_nw": s["t_nw"],
            "ic_inc": s_inc["ic_mean"], "icir_inc": s_inc["ic_ir_ann"],
            "t_inc": s_inc["t_nw"],
            "monotonic": float(mono) if np.isfinite(mono) else np.nan,
            "q_spread": float(np.nanmean(spread)),
            "turnover": float(np.nanmean(to)),
            "corr_rev5": corrs["rev_5"], "corr_turn20": corrs["turn_20"],
            "corr_vol20": corrs["vol_20"],
        })
        ic_rows[name] = ic
        inc_rows[name] = ic_inc
        print(f"  {name:12s} IC {s['ic_mean']:+.4f}  ICIR {s['ic_ir_ann']:6.2f}  "
              f"增量IC {s_inc['ic_mean']:+.4f}  与rev5相关 {corrs['rev_5']:+.2f}  "
              f"与换手相关 {corrs['turn_20']:+.2f}", flush=True)

    ev = pd.DataFrame(rows).sort_values("ic_inc", ascending=False)
    ev = metrics.pooled_factor_summary(ev, pd.DataFrame(ic_rows), pd.DataFrame(inc_rows))
    ev.to_csv(config.REPORTS / "flow_factor_eval.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(inc_rows).to_parquet(config.DATA / "flow_ic_inc.parquet", compression="zstd")
    pd.DataFrame(ic_rows).to_parquet(config.DATA / "flow_ic.parquet",
                                     compression="zstd")
    print("\n== 资金流因子评价（按增量 IC 排序）==")
    print(ev.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    print(f"[flow] DONE {now_cn()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
