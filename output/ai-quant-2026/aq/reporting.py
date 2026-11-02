"""Tables shared by report and lecture: no manually copied empirical numbers."""
from __future__ import annotations

import pandas as pd


def esc(value):
    return str(value).replace("_", r"\_").replace("%", r"\%").replace("&", r"\&")


def table(headers, rows, align, long=False):
    env = "longtable" if long else "tabular"
    body = [rf"\begin{{{env}}}{{@{{}}{align}@{{}}}}", r"\toprule",
            " & ".join(headers) + r" \\", r"\midrule"]
    if long:
        body += [r"\endhead"]
    body += [" & ".join(str(c) for c in row) + r" \\" for row in rows]
    body += [r"\bottomrule", rf"\end{{{env}}}"]
    return "\n".join(body)


def factor_table(frame, supplemental=False, limit=None, long=False):
    sort = "ic_inc" if supplemental else "ic_mean_neu"
    d = frame.sort_values(sort, ascending=False)
    if limit:
        d = d.head(limit)
    rows = []
    for r in d.itertuples():
        adjusted = r.ic_inc if supplemental else r.ic_mean_neu
        t_adj = r.t_inc if supplemental else r.t_nw_neu
        rows.append([esc(r.factor), f"{r.ic_mean:.4f}", f"{adjusted:.4f}",
                     f"{r.t_nw:.2f}", f"{t_adj:.2f}", f"{r.n:.0f}", f"{r.n_eff:.0f}"])
    return table(["因子", "原始 IC", "调整后 IC", r"原始 $t$", r"调整后 $t$",
                  r"$n$", r"$n_{\rm eff}$"], rows, "lrrrrrr", long)


def dsr_table(frame):
    values = frame.pivot(index="n_trials_assumed", columns="sigma_source", values="dsr")
    rows = [[str(n), f"{r.observed_candidates:.4f}", f"{r.iid_null_floor_scenario:.4f}"]
            for n, r in values.iterrows()]
    return table([r"假定独立试验数 $N$", "五候选离散度", "零假设标准差下限情景"], rows, "rrr")


def inference_note():
    return r"""原始 IC 与调整后 IC 均由完整日频 IC 序列汇总；$h=5$ 的日频标签重叠，
均值检验使用 Bartlett Newey--West 协方差，滞后阶数为
$L=\max(4,\lfloor4(n/100)^{2/9}\rfloor)$。$n$ 是有值的 IC 日期数，
$n_{\rm eff}=n\gamma_0/\widehat\Omega$ 是原始 IC 均值方差等价的样本量，
不是独立财报次数，也不是未经假设可确定的真实样本数。
完整表另含调整后有效样本量；不同带宽及每五日采样的敏感性见配套 CSV。
本表不再平均各年的 $t$ 值。"""
