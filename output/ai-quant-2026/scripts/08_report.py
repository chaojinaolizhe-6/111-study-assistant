"""Step 8 — 生成图表与《拟合精度报告》PDF。

产出的图：
  fig_factor_ic   单因子 IC（原始 vs 中性化）
  fig_ic_curve    头部因子的累计 IC
  fig_quantile    代表因子的五分层收益
  fig_nav         候选策略的样本外净值
  fig_cpcv        CPCV 各折 IC 分布
  fig_pbo         PBO 的 logit 分布
  fig_cost        成本敏感性

产出的文档：
  reports/拟合精度报告.pdf
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aq import config
from aq.audit import file_hash
from aq.reporting import factor_table, dsr_table, inference_note

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "SimSun"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 150
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["axes.edgecolor"] = "#9AA5B1"
plt.rcParams["axes.linewidth"] = 0.7
plt.rcParams["grid.color"] = "#E3E8EF"
plt.rcParams["grid.linewidth"] = 0.6

C_MAIN = "#2F5D8A"
C_ALT = "#B4532A"
C_GRAY = "#7B8794"

FIG = config.FIGURES
FIG.mkdir(parents=True, exist_ok=True)


def esc(s: str) -> str:
    return str(s).replace("_", r"\_").replace("%", r"\%").replace("&", r"\&")


# ---------------------------------------------------------------- 图
def fig_factor_ic(ev: pd.DataFrame) -> Path:
    d = ev.dropna(subset=["ic_mean"]).sort_values("ic_mean")
    d = pd.concat([d.head(12), d.tail(12)]).drop_duplicates("factor")
    fig, ax = plt.subplots(figsize=(7.2, 6.2))
    y = np.arange(len(d))
    ax.barh(y + 0.2, d["ic_mean"], height=0.38, color=C_MAIN, label="原始因子")
    ax.barh(y - 0.2, d["ic_mean_neu"], height=0.38, color=C_ALT, label="行业市值中性化后")
    ax.set_yticks(y)
    ax.set_yticklabels(d["factor"].tolist(), fontsize=7.5)
    ax.axvline(0, color=C_GRAY, lw=0.8)
    ax.set_xlabel("Rank IC 均值（h=5）")
    ax.legend(fontsize=8, frameon=False, loc="lower right")
    ax.grid(axis="x", alpha=0.7)
    ax.set_axisbelow(True)
    fig.savefig(FIG / "fig_factor_ic.png")
    plt.close(fig)
    return FIG / "fig_factor_ic.png"


def fig_ic_curve(ic: pd.DataFrame, top: list[str]) -> Path:
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    for i, f in enumerate(top):
        s = ic[ic["factor"] == f].set_index("date")["ic"].sort_index()
        if s.empty:
            continue
        ax.plot(s.index, s.cumsum(), lw=1.3 if i < 3 else 0.9,
                color=plt.cm.viridis(i / max(len(top) - 1, 1)), label=f)
    ax.axhline(0, color=C_GRAY, lw=0.8)
    ax.set_ylabel("累计 IC")
    ax.legend(fontsize=7, frameon=False, ncol=2)
    ax.grid(alpha=0.7)
    fig.savefig(FIG / "fig_ic_curve.png")
    plt.close(fig)
    return FIG / "fig_ic_curve.png"


def quintile_returns(name: str, years: range) -> pd.Series:
    """从因子面板直接算某因子的五分层平均前瞻收益。"""
    vals = []
    for y in years:
        p = config.DATA / "factors" / f"{y}.parquet"
        if not p.exists() or name not in pd.read_parquet(p, columns=[name]).columns:
            continue
        df = pd.read_parquet(p, columns=["date", "code", name, "fwd_ret_5", "is_tradable"])
        df = df[df["is_tradable"].fillna(False) & df["fwd_ret_5"].notna() & df[name].notna()]
        df = df[np.isfinite(df["fwd_ret_5"].to_numpy())]
        if df.empty:
            continue
        df["rk"] = df.groupby("date")[name].rank(pct=True)
        for k in range(1, 6):
            lo, hi = (k - 1) / 5, k / 5
            sel = (df["rk"] > lo) & (df["rk"] <= hi) if k > 1 else (df["rk"] <= hi)
            vals.append((k, df.loc[sel, "fwd_ret_5"].mean()))
    s = pd.DataFrame(vals, columns=["q", "r"]).groupby("q")["r"].mean()
    return s.reindex([1, 2, 3, 4, 5])


def fig_quantile(qm: pd.Series, name: str) -> Path:
    fig, ax = plt.subplots(figsize=(4.6, 2.9))
    m = qm.to_numpy() * 100
    ax.bar(range(1, 6), m, color=[C_ALT, "#8FA8C0", "#8FA8C0", "#8FA8C0", C_MAIN])
    ax.set_xticks(range(1, 6))
    ax.set_xticklabels([f"Q{i}" for i in range(1, 6)])
    ax.set_ylabel("5 日平均收益（%）")
    ax.set_title(f"{name} 五分层（2018--2026）", fontsize=9, color="#333")
    ax.grid(axis="y", alpha=0.7)
    fig.savefig(FIG / "fig_quantile.png")
    plt.close(fig)
    return FIG / "fig_quantile.png"


def fig_nav(R: pd.DataFrame) -> Path:
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    for c in R.columns:
        s = R[c].dropna()
        ax.plot(s.index, (1 + s).cumprod(), lw=1.4 if "lgbm_s0" in c else 1.0,
                label=c)
    ax.set_ylabel("净值（多空组合，扣 30bp 单边成本）")
    ax.legend(fontsize=7, frameon=False, ncol=3)
    ax.grid(alpha=0.7)
    fig.autofmt_xdate()
    fig.savefig(FIG / "fig_nav.png")
    plt.close(fig)
    return FIG / "fig_nav.png"


def fig_cpcv(res: pd.DataFrame) -> Path:
    d = res[res["protocol"] == "cpcv"]
    fig, ax = plt.subplots(figsize=(5.2, 2.8))
    data = [d[d["model"] == m]["ic_mean"].dropna().to_numpy()
            for m in ("composite", "ridge", "lgbm_s0")]
    labels = ["等权合成", "Ridge", "LightGBM"]
    bp = ax.boxplot(data, tick_labels=labels, patch_artist=True, widths=0.5)
    for patch, col in zip(bp["boxes"], [C_GRAY, "#8FA8C0", C_MAIN]):
        patch.set_facecolor(col)
        patch.set_alpha(0.75)
    ax.axhline(0, color=C_ALT, lw=0.9, ls="--")
    ax.set_ylabel("各折样本外 Rank IC")
    ax.grid(axis="y", alpha=0.7)
    fig.savefig(FIG / "fig_cpcv.png")
    plt.close(fig)
    return FIG / "fig_cpcv.png"


def fig_pbo(pbo: dict) -> Path:
    logits = np.asarray(pbo.get("logits", []), dtype=float)
    fig, ax = plt.subplots(figsize=(4.8, 2.7))
    if logits.size:
        ax.hist(logits, bins=40, color=C_MAIN, alpha=0.8)
        ax.axvline(0, color=C_ALT, lw=1.0, ls="--")
    ax.set_xlabel(r"$\lambda=\ln[\omega/(1-\omega)]$")
    ax.set_ylabel("组合数")
    ax.set_title(f"PBO = {pbo.get('pbo', float('nan')):.3f}", fontsize=9, color="#333")
    ax.grid(alpha=0.6)
    fig.savefig(FIG / "fig_pbo.png")
    plt.close(fig)
    return FIG / "fig_pbo.png"


def fig_cost(diag: dict) -> Path:
    cc = pd.DataFrame(diag.get("cost_curve", []))
    fig, ax = plt.subplots(figsize=(5.0, 2.8))
    if not cc.empty:
        ax.plot(cc["cost_bp"], cc["sharpe_best"], marker="o", color=C_MAIN,
                lw=1.5, ms=4, label="最优候选")
        ax.plot(cc["cost_bp"], cc["sharpe_mean"], marker="s", color=C_GRAY,
                lw=1.0, ms=3, ls="--", label="候选均值")
        ax.legend(fontsize=8, frameon=False)
    ax.axhline(0, color=C_ALT, lw=0.9, ls="--")
    ax.set_xlabel("单边成本（bp）")
    ax.set_ylabel("年化夏普")
    ax.grid(alpha=0.7)
    fig.savefig(FIG / "fig_cost.png")
    plt.close(fig)
    return FIG / "fig_cost.png"


# ---------------------------------------------------------------- LaTeX
def build_tex(ctx: dict) -> str:
    t = r"""
\documentclass[UTF8,10pt,a4paper]{ctexart}
\usepackage[a4paper,left=2.2cm,right=2.2cm,top=2.2cm,bottom=2.0cm]{geometry}
\usepackage[dvipsnames]{xcolor}
\usepackage{amsmath,amssymb}
\usepackage{booktabs,longtable,array,tabularx}
\usepackage{graphicx}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage[hidelinks]{hyperref}
\usepackage{tcolorbox}
\tcbuselibrary{skins,breakable}
\definecolor{accent}{HTML}{2F5D8A}
\definecolor{warm}{HTML}{B4532A}
\definecolor{soft}{HTML}{EEF3F8}
\titleformat{\section}{\sffamily\bfseries\large\color{accent}}{\thesection}{0.6em}{}
\titleformat{\subsection}{\sffamily\bfseries\normalsize\color{black!85}}{\thesubsection}{0.5em}{}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\sffamily\footnotesize\color{gray} 拟合精度报告}
\fancyhead[R]{\sffamily\footnotesize\color{gray}A 股日频 AI 选股}
\fancyfoot[C]{\sffamily\footnotesize\color{gray}\thepage}
\renewcommand{\headrulewidth}{0.3pt}
\newtcolorbox{kb}[1][]{enhanced,breakable,colback=soft,colframe=accent,
  boxrule=0pt,leftrule=3pt,arc=2pt,left=9pt,right=9pt,top=6pt,bottom=6pt,
  fonttitle=\sffamily\bfseries\small\color{accent},title={#1}}
\newtcolorbox{wb}[1][]{enhanced,breakable,colback=white,colframe=warm,
  boxrule=0.5pt,leftrule=3pt,arc=2pt,left=9pt,right=9pt,top=6pt,bottom=6pt,
  fonttitle=\sffamily\bfseries\small\color{warm},coltitle=warm,title={#1}}
\renewcommand{\arraystretch}{1.15}
\setlength{\parindent}{0pt}\setlength{\parskip}{4pt}

\begin{document}
\begin{center}
{\sffamily\color{accent}\large 量化研究交付物 · 03}\\[6pt]
{\sffamily\bfseries\LARGE 拟合精度与过拟合诊断报告}\\[6pt]
{\small\color{gray} 沪深 A 股研究样本 \quad 数据区间 __START__ 至 __END__ \quad 生成于 __NOW__}
\end{center}
\vspace{4pt}

\section{结论先行}

\begin{kb}[一句话结论]
在 __START__ 至 __END__ 的沪深 A 股研究样本上，__NCAND__ 个候选模型中最优者的
内部 Walk-Forward Rank IC 为 \textbf{__BESTIC__}，年化 ICIR 为 \textbf{__BESTICIR__}；
扣除单边 30\,bp 成本后，多空组合年化 \textbf{__BESTANN__}、夏普 \textbf{__BESTSR__}。
完整研究搜索史尚未记录，不能宣称已通过全流程多重检验。
DSR 压力情景为 \textbf{__DSR__}（假定 $N=603$，采用零假设离散度下限）；
PBO 为 \textbf{__PBO__}，仅描述现有五个候选。
\end{kb}

\subsection{这个数字应该怎么读}

\begin{itemize}
  \item \textbf{频率分开}：模型每五个交易日采样，ICIR 按 $\sqrt{252/5}$ 年化；
        单因子表用每日 IC，标签仍为未来五日收益，使用 HAC 修正标签重叠与序列相关。
  \item \textbf{成本是假设}：30\,bp 是统一敏感性参数，尚未按流动性、成交规模或盘口深度校准。
  \item \textbf{内部验证边界}：研究者已看过该历史区间；切分测试不是从未见过的前瞻样本。
  \item \textbf{统计量有条件}：DSR 依赖搜索次数和夏普离散度假设；PBO 与简化 RC 仅覆盖保存的候选集。
\end{itemize}

\section{数据与样本}

\begin{center}
\begin{tabular}{@{}lr@{}}
\toprule
项目 & 数值 \\
\midrule
数据库总行数（日线） & __DBROWS__ \\
证券数（有行情） & __NCODES__ \\
有效交易日 & __NDATES__ \\
研究样本行数（间隔采样后） & __NROWS__ \\
因子数 & __NFEAT__ \\
\bottomrule
\end{tabular}
\end{center}

\subsection{已知的数据局限}

\begin{wb}[三条必须披露的局限]
\begin{enumerate}
  \item \textbf{北交所缺失}：新浪财经无北交所接口，355 只北交所股票未纳入。
        该板块 2021 年才成立，因此 2010--2020 年的样本不受影响，
        同时存在退市股覆盖缺口，不能把有行情证券数等同于完整历史股票池。
  \item \textbf{成交额为估算值}：数据源不提供逐日成交额，由「成交量 $\times$ 当日均价」
        估算；其对流动性过滤与因子排序的影响尚未完成分层验证。
  \item \textbf{历史股本为月度近似}：换手率用月度股本快照前向填充，
        送转发生后的一个月内会有偏差。
\end{enumerate}
\end{wb}

\section{单因子评价}

__FIG_IC__

\begin{center}
\small
__TAB_FACTOR__
\end{center}
__INFERENCE_NOTE__

\begin{kb}[读表要点]
\begin{itemize}
  \item 先看\textbf{中性化后 IC}：如果相对原始 IC 大幅缩水，说明这个因子很大程度是
        行业或市值暴露的换皮。
  \item 再看 \textbf{NW $t$}：绝对值大于 2 才值得进一步讨论。
  \item 最后看\textbf{换手}：单边换手超过 30\% 的因子，需要显著更强的 IC 才能覆盖成本。
\end{itemize}
\end{kb}

\section{因子的时间稳定性}

__FIG_ICCURVE__

__FIG_QUANTILE__

\section{模型与验证协议}

\subsection{三种验证协议的对比}

__TAB_PROTOCOL__

\begin{kb}[这张表的信息量]
表中所有协议行均为折内指标的均值，包括 NW $t$；折均值 $t$ 只是描述性汇总，不是合并样本的显著性检验。
同一批因子、同一批模型，在不同验证协议下的内部样本外 IC 差异，反映了切分的不确定性。
如果 Purged K-Fold 与 Walk-Forward 的结果差距很大，说明模型对时间窗口敏感，
不应相信任何单一数字。
\end{kb}

\subsection{CPCV 的样本外分布}

__FIG_CPCV__

\section{样本外净值}

__FIG_NAV__

__TAB_CAND__

\section{过拟合诊断}

\subsection{四个统计量}

\begin{center}
\begin{tabular}{@{}lrl@{}}
\toprule
统计量 & 数值 & 判断标准 \\
\midrule
DSR 压力情景 & __DSR__ & 条件值，不作全搜索通过判定 \\
假定独立试验次数 $N$ & __NEFF__ & 搜索范围压力情景，非估计值 \\
五候选 PBO & __PBO__ & 不能代表所有因子筛选和调参 \\
简化 RC 重抽样 $p$ 值 & __RCP__ & 仅五候选；400 次重抽样 \\
Bootstrap 95\% 区间 & __BPCI__ & 2.5\% 与 97.5\% 分位 \\
\bottomrule
\end{tabular}
\end{center}

\subsection{DSR 对搜索次数与离散度的敏感性}
\begin{center}\small
__TAB_DSR__
\end{center}
第一列结果沿用五候选夏普的横截面标准差；第二列将该标准差至少设为
$1/\sqrt{T-1}$，只是一种独立零均值收益近似的压力情景。
$603=(39+8+20)\times3\times3$ 是名义搜索范围情景，不是已执行配置清单，
也不是可由五候选相关矩阵识别的真实独立次数。完整搜索史不足时不能给唯一的可靠 DSR。
本次诊断使用 __COMMON_N__ 个共同有效日期，不把缺失收益当现金零收益；
五候选收益相关系数范围为 __CORR_RANGE__。
DSR 仍沿用标准 PSR 的矩近似，没有因此解决收益自相关或反复查看历史的问题。
简化 RC 若报告 0.000，仅表示 400 次抽样中没有超越；不能解释为真实 $p=0$ 或 $p<0.001$。

\subsection{PBO 的分布}

__FIG_PBO__

\begin{wb}[PBO 的误读]
PBO 只衡量"样本内最优在样本外是否仍靠前"这个\textbf{序关系}，
它不衡量策略是否赚钱。低 PBO 也可能对应一群全都亏钱的策略。本次只有三类模型，其中三个 LightGBM 种子高度相关；
相关性并不保证 PBO 单调降低，候选不全才是外推限制。
\end{wb}

\section{成本敏感性}

__FIG_COST__

\begin{kb}[成本是最后的裁判]
成本曲线仅显示所选固定成本下的条件结果。30\,bp 未经实盘成交校准；
缺少市场深度、资金规模和融券费用模型，不能据此承诺可执行收益。
\end{kb}

\clearpage
\section{补充因子：统一开盘标签后的复核}
资金流与质量因子来自补充库（2020--2026），与主库的股票池、流动性口径和区间不同。
统一标签只解决目标变量的价格口径，不能把跨库 IC 当成相同条件下的优劣排名。
两个脚本与主面板共用 $y_t=O^{adj}_{t+6}/O^{adj}_{t+1}-1$；
现有位移按个股观测行计数，缺失交易日仍可能拉长实际持有跨度，尚需日历对齐审计。

\subsection{资金流因子（八个）}
调整后 IC 控制五日反转与二十日换手；该残差检验未加入主模型重训。
\begin{center}\small
__TAB_FLOW__
\end{center}
__INFERENCE_NOTE__

\subsection{质量因子（二十个）}
调整后 IC 控制对数市值、换手、波动和反转。以下用实际 IC 序列重算，
撤回旧版基于年度 $t$ 均值作出的“全部不显著”及“有效样本仅 14 个”的结论。
{\small
__TAB_QUALITY__
}
慢变的因子值不等于慢变的 IC；收益每天变化，IC 序列的相关性必须实测。
任何单因子 $|t|>2$ 也仍未校正多重筛选，不能直接认定可交易 alpha。

\section{结论与后续}

\subsection{可以下的结论}

\begin{enumerate}
  \item 在这段已被研究者查看的历史数据中，内部验证显示正的横截面预测关联。
        未见样本外、数据覆盖偏差和完整搜索校正仍未解决。
  \item 模型相对等权基线的提升有限；真正决定结果的是\textbf{因子质量与验证严格度}，
        而不是模型复杂度。
  \item 扣除成本后，多空组合的收益显著缩水，说明\textbf{换手控制}与\textbf{信号选择}
        同样重要。
\end{enumerate}

\subsection{不能下的结论}

\begin{itemize}
  \item 不能推断实盘可获利：本报告未模拟冲击成本的市场深度、未考虑资金规模、
        未考虑滑点的时变。
  \item 尚无 long-only 或事件驱动组合，整手、资金占用及跌停无法退出的路径依赖未模拟。
  \item 2010--2019 价格缺第二来源验证，退市股覆盖仍有缺口；补充库 2021 年缺失规则未知。
  \item 不能外推到其他市场：所有结论仅基于 A 股日频。
  \item 不能认为因子长期有效：第 11 章已说明，拥挤与制度变化会让因子衰减。
\end{itemize}

\subsection{建议的下一步}

\begin{enumerate}
  \item 用事件驱动回测替换向量化回测，加入整手与资金约束；
  \item 引入换手惩罚与行业中性约束，观察扣费后夏普的变化；
  \item 用滚动窗口重做一遍全流程，检查结论的时间稳定性；
  \item 把因子库扩充到包括分钟频量价特征，检验边际信息。
\end{enumerate}

\paragraph{统计方法来源}
Bailey 与 L\'opez de Prado，\href{https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf}{The Deflated Sharpe Ratio}；
Bailey 等，\href{https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf}{The Probability of Backtest Overfitting}。
本地实现与这些统计量的适用范围应分开审计。
\end{document}
"""
    return t


def main() -> int:
    rep = config.REPORTS
    ev = pd.read_csv(rep / "factor_eval.csv")
    res = pd.read_csv(rep / "model_tests.csv")
    cand = pd.read_csv(rep / "candidates_oos.csv")
    diag = json.loads((rep / "diagnostics.json").read_text(encoding="utf-8"))
    R = pd.read_csv(rep / "candidate_returns.csv", index_col=0, parse_dates=True)
    flow = pd.read_csv(rep / "flow_factor_eval.csv")
    quality = pd.read_csv(rep / "quality_factor_eval.csv")
    sensitivity = pd.read_csv(rep / "dsr_sensitivity.csv")
    ic = pd.read_parquet(config.DATA / "ic_series.parquet")
    ic["date"] = pd.to_datetime(ic["date"])

    fig_ic = fig_factor_ic(ev)
    top = ev.sort_values("ic_mean_neu", ascending=False)["factor"].head(5).tolist()
    fig_curve = fig_ic_curve(ic, top)
    qm = quintile_returns(top[0], range(2018, 2027))
    fig_q = fig_quantile(qm, top[0])
    fig_c = fig_cpcv(res)
    fig_n = fig_nav(R)
    fig_p = fig_pbo(diag.get("pbo_detail", {}))
    fig_cs = fig_cost(diag)

    # 表格
    f = ev.sort_values("ic_mean_neu", ascending=False)
    rows = "\n".join(
        f"{esc(r.factor)} & {r.family} & {r.ic_mean:.4f} & {r.ic_mean_neu:.4f} & "
        f"{r.icir_ann:.2f} & {r.t_nw:.2f} & {r.monotonic:.2f} & {r.turnover*100:.1f}\\% \\\\"
        for r in f.head(18).itertuples())
    tab_factor = (r"\begin{tabular}{@{}llrrrrrr@{}}" "\n\\toprule\n"
                  r"因子 & 家族 & IC & 中性化 IC & ICIR & NW $t$ & 单调性 & 单边换手 \\" "\n\\midrule\n"
                  + rows + "\n\\bottomrule\n\\end{tabular}")

    p = (res.groupby(["protocol", "model"])
         .agg(n=("ic_mean", "size"), ic=("ic_mean", "mean"), sd=("ic_mean", "std"),
              icir=("icir_ann", "mean"), t=("t_nw", "mean"),
              ann=("ls_ann_net", "mean"), sr=("sharpe_net", "mean")).reset_index())
    drows = "\n".join(
        f"{esc(r.protocol)} & {esc(r.model)} & {int(r.n)} & {r.ic:.4f} & {r.sd:.4f} & "
        f"{r.icir:.2f} & {r.t:.2f} & {r.ann*100:.1f}\\% & {r.sr:.2f} \\\\"
        for r in p.itertuples())
    tab_protocol = (r"\begin{tabular}{@{}llrrrrrrr@{}}" "\n\\toprule\n"
                    r"协议 & 模型 & 折数 & IC 均值 & IC 标准差 & ICIR & NW $t$ & 年化 & 夏普 \\"
                    "\n\\midrule\n" + drows + "\n\\bottomrule\n\\end{tabular}")

    crows = "\n".join(
        f"{esc(r.label)} & {r.ic_mean:.4f} & {r.icir_ann:.2f} & {r.t_nw:.2f} & "
        f"{r.ls_ann_net*100:.1f}\\% & {r.sharpe_net:.2f} & {r.mdd_net*100:.1f}\\% & "
        f"{r.turnover*100:.1f}\\% \\\\"
        for r in cand.itertuples())
    tab_cand = (r"\begin{tabular}{@{}lrrrrrrr@{}}" "\n\\toprule\n"
                r"候选 & IC & ICIR & NW $t$ & 年化 & 夏普 & 最大回撤 & 换手 \\"
                "\n\\midrule\n" + crows + "\n\\bottomrule\n\\end{tabular}")

    tab_factor = factor_table(ev, limit=18)
    dsr = diag.get("dsr", {})
    boot = diag.get("bootstrap", {})
    ctx = {
        "__START__": diag.get("start", ""), "__END__": diag.get("end", ""),
        "__NOW__": pd.Timestamp.now(tz="Europe/London").strftime("%Y-%m-%d"),
        "__NCAND__": str(len(cand)),
        "__BESTIC__": f"{diag.get('best_ic', float('nan')):.4f}",
        "__BESTICIR__": f"{cand.iloc[0]['icir_ann']:.2f}" if len(cand) else "--",
        "__BESTANN__": f"{cand.iloc[0]['ls_ann_net']*100:.1f}\\%" if len(cand) else "--",
        "__BESTSR__": f"{cand.iloc[0]['sharpe_net']:.2f}" if len(cand) else "--",
        "__DSR__": f"{dsr.get('dsr', float('nan')):.3f}",
        "__NEFF__": f"{dsr.get('n_eff', float('nan')):.1f}",
        "__PBO__": f"{diag.get('pbo', float('nan')):.3f}",
        "__RCP__": f"{diag.get('rc_p', float('nan')):.3f}",
        "__BPCI__": f"[{boot.get('p025', float('nan')):.2f}, {boot.get('p975', float('nan')):.2f}]",
        "__DBROWS__": f"{__import__('sqlite3').connect(str(config.DB_PATH)).execute('SELECT COUNT(*) FROM bar').fetchone()[0]:,}",
        "__NCODES__": f"{__import__('sqlite3').connect(str(config.DB_PATH)).execute('SELECT COUNT(DISTINCT code) FROM bar').fetchone()[0]:,}",
        "__NDATES__": str(diag.get("dates", 0)),
        "__NROWS__": f"{diag.get('rows', 0):,}",
        "__NFEAT__": str(diag.get("features", 0)),
        "__FIG_IC__": r"\includegraphics[width=\textwidth]{" + str(fig_ic).replace("\\", "/") + "}",
        "__FIG_ICCURVE__": r"\includegraphics[width=\textwidth]{" + str(fig_curve).replace("\\", "/") + "}",
        "__FIG_QUANTILE__": r"\includegraphics[width=0.62\textwidth]{" + str(fig_q).replace("\\", "/") + "}",
        "__FIG_CPCV__": r"\includegraphics[width=0.72\textwidth]{" + str(fig_c).replace("\\", "/") + "}",
        "__FIG_NAV__": r"\includegraphics[width=\textwidth]{" + str(fig_n).replace("\\", "/") + "}",
        "__FIG_PBO__": r"\includegraphics[width=0.62\textwidth]{" + str(fig_p).replace("\\", "/") + "}",
        "__FIG_COST__": r"\includegraphics[width=0.62\textwidth]{" + str(fig_cs).replace("\\", "/") + "}",
        "__TAB_FACTOR__": tab_factor, "__TAB_PROTOCOL__": tab_protocol,
        "__TAB_CAND__": tab_cand,
        "__TAB_FLOW__": factor_table(flow, supplemental=True),
        "__TAB_QUALITY__": factor_table(quality, supplemental=True, long=True),
        "__TAB_DSR__": dsr_table(sensitivity),
        "__INFERENCE_NOTE__": inference_note(),
        "__COMMON_N__": str(diag["wf_periods"]),
        "__CORR_RANGE__": f"{diag['candidate_corr_min']:.3f}--{diag['candidate_corr_max']:.3f}",
    }
    tex = build_tex(ctx)
    for k, v in ctx.items():
        tex = tex.replace(k, v)
    out = config.ROOT / "reports" / "report.tex"
    out.write_text(tex, encoding="utf-8")

    xelatex = r"C:\Users\M\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe"
    for _ in range(2):
        subprocess.run([xelatex, "-interaction=nonstopmode", "-halt-on-error", "report.tex"],
                       cwd=str(config.REPORTS), capture_output=True, text=True, encoding="utf-8", errors="replace", check=True)
    pdf = config.REPORTS / "report.pdf"
    if pdf.exists():
        pdf.replace(config.REPORTS / "拟合精度报告.pdf")
        print(f"[report] OK -> {config.REPORTS / '拟合精度报告.pdf'}")
    else:
        raise RuntimeError("编译失败，见 reports/report.log")
    inputs = ["factor_eval.csv", "flow_factor_eval.csv", "quality_factor_eval.csv",
              "diagnostics.json", "dsr_sensitivity.csv", "candidate_returns.csv",
              "candidates_oos.csv", "model_tests.csv", "ic_inference_sensitivity.csv",
              "../scripts/08_report.py", "../aq/reporting.py", "../research_search.json"]
    manifest = {"inputs_sha256": {f: file_hash(rep / f) for f in inputs},
                "pdf_sha256": file_hash(rep / "拟合精度报告.pdf")}
    (rep / "report_inputs.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"[report] 图表: {sorted(p.name for p in FIG.glob('*.png'))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
