"""Step 14 — 把严格化检验的结果生成 LaTeX 表格。

产出的 generated_strictness.tex / generated_t3_summary.tex / generated_t3_only2.tex
由 appendix_strictness.tex 引用，保证讲义里的数字与 CSV 永远一致。
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aq import config

LEC = config.ROOT / "lectures"


def esc(s) -> str:
    return str(s).replace("_", r"\_")


def main() -> int:
    rep = config.REPORTS
    u = pd.read_csv(rep / "universe_test.csv")
    t3 = pd.read_csv(rep / "factor_significance_t3.csv")

    u = u.assign(_abs=u["t_全样本"].abs()).sort_values("_abs", ascending=False)

    head = [r"\begin{tabular}{@{}lrrrrrr@{}}", r"\toprule",
            r"因子 & IC 全样本 & IC 剔除小30\% & IC 变化 & $t$ 全样本 & $t$ 剔除后 & 判定 \\",
            r"\midrule"]
    body = []
    for _, r in u.iterrows():
        chg = r["IC变化%"]
        if r["factor"] == "size":
            verdict = r"\textbf{翻负，不可用}"
        elif abs(chg) < 20:
            verdict = "稳健"
        elif abs(chg) < 40:
            verdict = "减弱"
        else:
            verdict = "依赖微盘"
        body.append(
            f"{esc(r['factor'])} & {r['IC_全样本']:+.4f} & {r['IC_剔除小30%']:+.4f} & "
            f"{chg:+.1f}\\% & {r['t_全样本']:+.2f} & {r['t_剔除小30%']:+.2f} & {verdict} \\\\")
    tail = [r"\bottomrule", r"\end{tabular}"]
    (LEC / "generated_strictness.tex").write_text(
        "\n".join(head + body + tail) + "\n", encoding="utf-8")

    n3 = int((t3["门槛"] == "t>3 通过").sum())
    n2 = int((t3["门槛"] == "仅 t>2 通过").sum())
    n0 = int((t3["门槛"] == "不显著").sum())
    summ = "\n".join([
        r"\begin{tabular}{@{}lr@{}}", r"\toprule",
        r"判定 & 因子数 \\", r"\midrule",
        f"$|t|>3$（HLZ 建议门槛） & \\textbf{{{n3}}} \\\\",
        f"仅 $2<|t|\\le 3$ & {n2} \\\\",
        f"$|t|\\le 2$ & {n0} \\\\",
        r"\bottomrule", r"\end{tabular}"])
    (LEC / "generated_t3_summary.tex").write_text(summ + "\n", encoding="utf-8")

    only2 = t3[t3["门槛"] == "仅 t>2 通过"].copy()
    only2 = only2.assign(_abs=only2["t_nw"].abs()).sort_values("_abs", ascending=False)
    rows = [f"{esc(r['factor'])} & {r['family']} & {r['ic_mean']:+.4f} & "
            f"{r['t_nw']:+.2f} \\\\" for _, r in only2.iterrows()]
    (LEC / "generated_t3_only2.tex").write_text(
        "\n".join([r"\begin{tabular}{@{}llrr@{}}", r"\toprule",
                   r"因子 & 家族 & IC & $t$ \\", r"\midrule"] + rows +
                  [r"\bottomrule", r"\end{tabular}"]) + "\n", encoding="utf-8")

    print(f"[strictness] t>3={n3}  only2={n2}  none={n0}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
