# -*- coding: utf-8 -*-
"""生成《电工实验二、三 报告填写指南》PDF（含电路图、全部数值与计算过程）。"""
import json
import os
import subprocess

ROOT = r"D:\aaa_D_usual\DSH\111学习助手\电工实验_报告"
with open(os.path.join(ROOT, "计算结果.json"), encoding="utf-8") as fh:
    D = json.load(fh)

t212, t213, t214 = D["t212"], D["t213"], D["t214"]
EQ, FL, VT = D["equiv"], D["fluor"], D["vtri"]

f2 = lambda v, n=2: f"{v:.{n}f}"
num = lambda v, n=2: f2(v, n)   # 文本模式与数学模式通用；负号用普通连字符

# ---------- 表 2.1.2 ----------
row_nom = " & ".join(str(v) for v in t212["nominal"])
row_mea = " & ".join(f2(v, 1) for v in t212["measured"])
row_err = " & ".join(f2(v, 2) for v in t212["error"])

# ---------- 表 2.1.3 ----------
m, k, rel = t213["meas"], t213["calc"], t213["rel"]
v = t213["node_v"]
r213_meas = " & ".join(num(m[x], 1) for x in
                       ["U_S1", "U_S2", "I1", "I2", "I3", "U_AB", "U_CD", "U_AD", "U_DE", "U_FA"])
r213_calc = " & ".join([num(m["U_S1"], 1), num(m["U_S2"], 1)] +
                       [num(k[x], 2) for x in ["I1", "I2", "I3", "U_AB", "U_CD", "U_AD", "U_DE", "U_FA"]])
r213_rel = " & ".join([f2(abs(m["U_S1"] - 6) / 6 * 100, 1), f2(abs(m["U_S2"] - 12) / 12 * 100, 1)] +
                      [f2(rel[x], 1) for x in ["I1", "I2", "I3", "U_AB", "U_CD", "U_AD", "U_DE", "U_FA"]])

kvl1 = m["U_FA"] + m["U_AD"] + m["U_DE"] - m["U_S1"]
kvl2 = m["U_AB"] + m["U_S2"] + m["U_CD"] - m["U_AD"]
kcl = m["I1"] + m["I2"] - m["I3"]

# ---------- 表 2.1.4 ----------
cas = t214["cases"]; mr = t214["meas"]; th = t214["theory"]
names214 = ["$U_{S1}$ 单独作用", "$U_{S2}$ 单独作用", "共同作用", "$2U_{S2}$（齐次性）"]
rows214 = []
for nm, key in zip(names214, cas):
    r = mr[key]
    rows214.append(nm + " & " + " & ".join(num(r[x], 1) for x in
                    ["U_S1", "U_S2", "I1", "I2", "I3", "U_AB", "U_CD", "U_AD", "U_DE", "U_FA"]) + r" \\")
rows214_th = []
for nm, key in zip(["$U_{S1}$ 单独", "$U_{S2}$ 单独", "共同作用", "$2U_{S2}$"], cas):
    r = th[key]
    rows214_th.append(nm + " & " + " & ".join(num(r[x], 2) for x in
                       ["I1", "I2", "I3", "U_AB", "U_CD", "U_AD", "U_DE", "U_FA"]) + r" \\")
def znum(x, n=1):
    """残差格式化：|x|<0.05 一律写 0.0，避免出现 -0.0。"""
    return "0.0" if abs(x) < 0.05 else f"{x:.{n}f}"


sum_res = " & ".join(znum(t214["sum_res"][x]) for x in ["I1", "I2", "I3", "U_AB", "U_CD", "U_AD", "U_DE", "U_FA"])
hom_res = " & ".join(znum(t214["hom_res"][x]) for x in ["I1", "I2", "I3", "U_AB", "U_CD", "U_AD", "U_DE", "U_FA"])

R3m = D["r_meas"]["R3"]
p1 = (mr[cas[0]]["I3"] / 1000) ** 2 * R3m * 1000
p2 = (mr[cas[1]]["I3"] / 1000) ** 2 * R3m * 1000
pboth = (mr[cas[2]]["I3"] / 1000) ** 2 * R3m * 1000

# ---------- 日光灯 ----------
fl_rows = []
for r in FL["rows"]:
    fl_rows.append(" & ".join([f2(r["C"], 1), f2(r["U"], 1), f2(r["UR"], 1), f2(r["UL"], 1),
                               f2(r["I"], 1), f2(r["IC"], 1), f2(r["IL"], 1), f2(r["P"], 1),
                               f2(r["PLR"], 1), f2(r["PC"], 1),
                               f2(r["cos_calc"], 3), f2(r["cos_meas"], 3)]) + r" \\")
fl_rows2 = []
for r in FL["rows"]:
    fl_rows2.append(" & ".join([f2(r["C"], 1), f2(r["S"], 1), f2(r["Q"], 1),
                                f2(r["IC_th"], 0), f2(r["cos_calc"], 3),
                                f"{r['dev']:.1f}\\%"]) + r" \\")

# ---------- 电压三角形 ----------
vr = {r["C"]: r for r in VT["rows"]}
vt_line = "\n".join(
    r"\quad $C=" + c + r"\,\mu$F：" +
    r"$\sqrt{U_R^2+U_C^2}=\sqrt{" + f"{vr[c]['UR']:.1f}^2+{vr[c]['UC']:.1f}^2" + r"}=" +
    f"{vr[c]['U_calc']:.1f}" + r"$~V，实测 $U=" + f"{vr[c]['U']:.1f}" + r"$~V，偏差 " +
    f"{vr[c]['dev']:+.2f}" + r"\%" + r"\\"
    for c in ["1", "2", "4.7"])

TEX = r"""
\documentclass[UTF8,a4paper,10.5pt]{ctexart}
\usepackage[margin=2.0cm]{geometry}
\usepackage{amsmath,amssymb}
\usepackage{booktabs,array,tabularx,multirow,makecell}
\usepackage{xcolor}
\usepackage{tikz}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage[hidelinks]{hyperref}
\usetikzlibrary{arrows.meta,calc,positioning}

\definecolor{acc}{HTML}{17405F}
\definecolor{acc2}{HTML}{2E6E9E}
\definecolor{soft}{HTML}{EEF4F9}
\definecolor{warnc}{HTML}{B03A2E}
\definecolor{okc}{HTML}{1E6B45}

\ctexset{
  section/format = \Large\bfseries\color{acc},
  subsection/format = \large\bfseries\color{acc2},
}
\setlist[itemize]{leftmargin=1.3em,itemsep=1pt,topsep=2pt}
\setlist[enumerate]{leftmargin=1.5em,itemsep=1pt,topsep=2pt}

\pagestyle{fancy}\fancyhf{}
\renewcommand{\headrulewidth}{0.4pt}
\fancyhead[L]{\footnotesize\color{acc2}\,电工实验二、三\quad 报告填写指南}
\fancyhead[R]{\footnotesize\color{acc2}\leftmark}
\fancyfoot[C]{\footnotesize\thepage}

\newcommand{\key}[1]{\textbf{\color{acc}#1}}
\newcommand{\cw}[1]{\colorbox{soft}{\strut\,#1\,}}
\newcommand{\warn}[1]{\textcolor{warnc}{#1}}
\newcommand{\ok}[1]{\textcolor{okc}{#1}}

\newcommand{\resh}[3]{\draw[fill=white,thick] (#1-0.85,#2-0.22) rectangle (#1+0.85,#2+0.22);
  \node[above=1pt] at (#1,#2+0.22) {\scriptsize #3};}
\newcommand{\resv}[3]{\draw[fill=white,thick] (#1-0.22,#2-0.85) rectangle (#1+0.22,#2+0.85);
  \node[right=1pt] at (#1+0.25,#2) {\scriptsize #3};}
\newcommand{\capsym}[3]{\draw[thick] (#1-0.12,#2-0.5) -- (#1-0.12,#2+0.5);
  \draw[thick] (#1+0.12,#2-0.5) -- (#1+0.12,#2+0.5);
  \node[below=1pt] at (#1,#2-0.5) {\scriptsize #3};}
\newcommand{\src}[3]{% x,y,label with + on top
  \draw[thick,fill=white] (#1,#2) circle (0.42);
  \node at (#1,#2) {\scriptsize #3};
  \node[above=0pt] at (#1,#2+0.42) {\scriptsize $+$};
  \node[below=0pt] at (#1,#2-0.42) {\scriptsize $-$};}

\begin{document}

% ================== 封面 ==================
\begin{titlepage}
\centering
\vspace*{2.6cm}
{\color{acc}\rule{\linewidth}{1.1pt}}\\[0.85cm]
{\Huge\bfseries\color{acc} 电工实验报告\\[0.3cm] 填写指南}\\[0.55cm]
{\Large 实验二（直流电路）\quad\textbullet\quad 实验三（交流电路）}\\[0.3cm]
{\large 预习答案 \textbullet\ 全部数据 \textbullet\ 中间计算 \textbullet\ Discussion 参考}\\[0.65cm]
{\color{acc}\rule{\linewidth}{1.1pt}}\\[1.3cm]

\begin{minipage}{0.86\linewidth}
\large
按实验册页码编排：\textbf{第 1--5 页属实验二}（第 3--4 页的“等效变换条件验证”也在实验二内），
\textbf{第 6--8 页属实验三}。每节都写明\key{“这一格填什么”}，
数值可直接照抄，计算过程可按式誊写。

\vspace{0.45cm}
\normalsize
\begin{tabular}{@{}ll@{}}
\toprule
数据来源 & 实验记录本扫描 8 页，已核对并冻结 \\
计算依据 & 实测电阻值 + 节点电压法正演 \\
有效数字 & 电压/电流 1 位小数；相对误差 1--2 位小数 \\
\bottomrule
\end{tabular}
\end{minipage}

\vfill
{\small\color{gray} \today}
\end{titlepage}

\tableofcontents
\newpage

% ================== 0 ==================
\section{使用说明与计算口径}

\subsection{本册怎么用}
\begin{enumerate}
  \item \key{先抄表}：每节的数据表就是报告里那张表的最终答案，含实测、计算、相对误差三行。
  \item \key{再抄过程}：紧跟其后的“计算过程”给出公式与数值代入，可原样写在空白处。
  \item \key{最后抄结论}：每节末的“结论”一句话写在表下方讨论区。
\end{enumerate}

\subsection{相对误差定义（全册统一）}
\begin{equation}
\delta=\frac{\left|X_{\text{测}}-X_{\text{算}}\right|}{\left|X_{\text{算}}\right|}\times100\%
\qquad\text{（以计算值作参考值，对应 Discussion 第 1 问）}
\end{equation}
电阻表另以标称值作参考值：$\delta=\left|R_{\text{测}}-R_{\text{标称}}\right|/R_{\text{标称}}\times100\%$。

\subsection{计算模型：后面所有“计算值”都由它得出}
对实验册图 2.1.1(a) 用节点电压法，取 $D$ 为参考点（$V_D=0$），
两电源正极分别接 $F$ 端与 $B$ 端：
\begin{align}
V_A\left(\tfrac1{R_1}+\tfrac1{R_2}+\tfrac1{R_3}\right)-\frac{V_B}{R_2}-\frac{V_E}{R_1}&=\frac{U_{S1}}{R_1}\\
-\frac{V_A}{R_2}+V_B\left(\tfrac1{R_2}+\tfrac1{R_5}\right)&=\frac{U_{S2}}{R_5}\\
-\frac{V_A}{R_1}+V_E\left(\tfrac1{R_1}+\tfrac1{R_4}\right)&=-\frac{U_{S1}}{R_1}
\end{align}
解出后 $V_F=V_E+U_{S1}$、$V_C=V_B-U_{S2}$，各量
\begin{equation}
I_1=\frac{V_F-V_A}{R_1},\quad I_2=\frac{V_B-V_A}{R_2},\quad I_3=\frac{V_A}{R_3},
\end{equation}
\begin{equation}
U_{AB}=V_A-V_B,\quad U_{CD}=V_C-V_D,\quad U_{AD}=V_A-V_D,\quad U_{DE}=V_D-V_E,\quad U_{FA}=V_F-V_A .
\end{equation}
代入实测电阻 \cw{$R_1=504.2$、$R_2=986.6$、$R_3=503.4$、$R_4=503.9$、$R_5=326.1\ \Omega$}
即得下文全部计算值。\key{方向约定}：$I_1$ 取 $F\to A$，$I_2$ 取 $B\to A$，$I_3$ 取 $A\to D$，与图中箭头一致。

\newpage
% ================== 实验二 ==================
\part*{\centering\color{acc} 实验二\quad 直流电路实验}
\addcontentsline{toc}{part}{实验二\quad 直流电路实验（实验册第 1--5 页）}
\markboth{实验二}{实验二}

\section{预习作业（第 1 页，I. Preliminary Work）}

\subsection*{1. 基尔霍夫定律与元件线性/非线性有关吗？叠加定理呢？}
\key{答：}基尔霍夫定律与元件是否线性\key{无关}。KCL 是电荷守恒（节点不积累电荷）的体现，
KVL 是能量守恒（静电场保守、沿闭合回路电场力做功为零）的体现，
二者只取决于\key{电路的连接方式（拓扑）与参考方向}，
即使电路中含有二极管等非线性元件，KCL、KVL 仍严格成立。
\par
叠加定理则\key{要求线性电路}（元件伏安关系线性、除独立源外无其他非线性元件）。
它是线性方程“可加性 + 齐次性”的直接推论，非线性电路不成立。

\subsection*{2. 电压源、电流源闲置时如何存放}
\key{答：}电压源不用时\cw{短路}存放，电流源不用时\cw{开路}存放。
理由：理想电压源端电压恒定，若开路存放，两端易积累过高电压；
理想电流源电流恒定，若短路存放，端电压为零、失去意义，且可能破坏其工作状态。

\subsection*{3. 电压表串接还是并接？接反有什么后果？}
\key{答：}必须与被测支路\cw{并联}。
若误接成串联，因电压表内阻极大（$10^5\sim10^7\,\Omega$），会使该支路近乎断路，
电路工作状态被破坏，读数也不是支路电压；
若极性接反，指针式表会\key{反向偏转}，可能打弯指针/烧毁游丝，数字表则显示负值或溢出。

\subsection*{4. 相对误差如何计算？“真值”取不到时怎么办？}
\key{答：}$\delta=\dfrac{\text{测量值}-\text{真值}}{\text{真值}}\times100\%$。
真值无法获得时，用\key{约定真值（参考值）}代替：
\begin{enumerate}[label=\textcircled{\small\arabic*}]
  \item 元件\key{标称值}（用于表 2.1.2 电阻）；
  \item 由\key{电路理论计算出的值}（用于表 2.1.3、2.1.4）。
\end{enumerate}

\section{实验电路（图 2.1.1 a，需要自己画）}
\begin{center}
\begin{tikzpicture}[scale=1.0,>=Stealth]
  \coordinate (F) at (0,4.4); \coordinate (A) at (4.8,4.4); \coordinate (B) at (9.6,4.4);
  \coordinate (E) at (0,0);   \coordinate (D) at (4.8,0);   \coordinate (C) at (9.6,0);
  % 上边
  \draw[thick] (F) -- (1.45,4.4); \draw[thick] (3.25,4.4) -- (A);
  \draw[thick] (A) -- (7.15,4.4); \draw[thick] (8.95,4.4) -- (B);
  \resh{2.35}{4.4}{$R_1=510\,\Omega$}
  \resh{8.05}{4.4}{$R_2=1\,\mathrm{k}\Omega$}
  % 下边
  \draw[thick] (E) -- (1.45,0); \draw[thick] (3.25,0) -- (D);
  \draw[thick] (D) -- (5.85,0); \draw[thick] (7.65,0) -- (C);
  \resh{2.35}{0}{$R_4=510\,\Omega$}
  \resh{6.75}{0}{$R_5=330\,\Omega$}
  % 中间支路
  \draw[thick] (A) -- (4.8,3.05); \draw[thick] (4.8,1.35) -- (D);
  \resv{4.8}{2.2}{$R_3=510\,\Omega$}
  % 左右支路
  \draw[thick] (E) -- (0,1.68); \draw[thick] (0,2.72) -- (F);
  \draw[thick] (B) -- (9.6,2.72); \draw[thick] (9.6,1.68) -- (C);
  \src{0}{2.2}{$U_{S1}$}
  \src{9.6}{2.2}{$U_{S2}$}
  % 节点
  \fill (F) circle (1.7pt); \node[below left]  at (F) {\small $F$};
  \fill (A) circle (1.7pt); \node[above left]  at (A) {\small $A$};
  \fill (B) circle (1.7pt); \node[above right] at (B) {\small $B$};
  \fill (E) circle (1.7pt); \node[below left]  at (E) {\small $E$};
  \fill (D) circle (1.7pt); \node[below]       at (D) {\small $D$};
  \fill (C) circle (1.7pt); \node[below right] at (C) {\small $C$};
  % 电流方向
  \draw[->,acc2,thick] (0.55,3.05) -- (0.55,3.6); \node[above] at (0.55,3.6) {\scriptsize $i_1$};
  \draw[->,acc2,thick] (9.6,3.1) -- (9.6,3.65); \node[left] at (9.6,3.65) {\scriptsize $i_2$};
  \draw[->,acc2,thick] (4.8,3.35) -- (4.8,3.9);  \node[left] at (4.8,3.9) {\scriptsize $i_3$};
  \node[below=1.1cm] at (4.8,-0.15) {\scriptsize 图 2.1.1(a)\ \ 验证基尔霍夫定律与叠加定理的实验电路};
\end{tikzpicture}
\end{center}
\noindent\textbf{画图要点}：六个节点 $A,B,C,D,E,F$ 画实心点并标注；电阻画矩形、旁边写阻值与编号；
电源画圆并标 $\pm$ 极与 $U_{S1},U_{S2}$；三个电流参考方向 $i_1,i_2,i_3$ 按图；
节点字母必须与表格里的 $U_{AB},U_{CD},U_{AD},U_{DE},U_{FA}$ 对得上。

\section{表 2.1.2\quad 电阻测量}
\textbf{这一行填什么}：第二行抄万用表读数，第三行按 $\delta=|R_{\text{测}}-R_{\text{标称}}|/R_{\text{标称}}\times100\%$ 计算。

\begin{center}
\small\setlength{\tabcolsep}{5pt}
\begin{tabular}{@{}l*{7}{c}@{}}
\toprule
电阻 & $R_1$ & $R_2$ & $R_3$ & $R_4$ & $R_5$ & $R_0$ & $R_L$\\
\midrule
标称值 $/\Omega$ & @@NOM@@\\
实测值 $/\Omega$ & @@MEA@@\\
相对误差 $/\%$ & @@ERR@@\\
\bottomrule
\end{tabular}
\end{center}

\noindent\textbf{过程写法（以 $R_2$ 为例）}：
$\delta_{R_2}=\dfrac{|986.6-1000|}{1000}\times100\%=1.34\%$，
其余同法（$R_1$：$5.8/510=1.14\%$；$R_5$：$3.9/330=1.18\%$）。
全部电阻误差 $<2\%$，精度良好，故后续计算直接用实测值。

\section{表 2.1.3\quad 基尔霍夫定律验证}
实验条件 $U_{S1}=6$~V、$U_{S2}=12$~V，实测电源 5.9~V、12.1~V。

\begin{center}
\scriptsize\setlength{\tabcolsep}{3.0pt}
\begin{tabular}{@{}l*{10}{c}@{}}
\toprule
量 & $U_{S1}$/V & $U_{S2}$/V & $I_1$/mA & $I_2$/mA & $I_3$/mA & $U_{AB}$/V & $U_{CD}$/V & $U_{AD}$/V & $U_{DE}$/V & $U_{FA}$/V\\
\midrule
实测值 & @@R213M@@\\
计算值 & @@R213C@@\\
相对误差 $/\%$ & @@R213E@@\\
\bottomrule
\end{tabular}
\end{center}
{\scriptsize 注：$I_2$ 正方向 $B\to A$、$I_3$ 正方向 $A\to D$，与图中箭头一致；$I_2>0$ 表示实际由 $B$ 流向 $A$。}

\subsection*{计算值的过程（可整段誊写）}
取 $D$ 为参考点，代入实测电阻解节点方程得
\[
V_A=@@VA@@\ \text{V},\qquad V_B=@@VB@@\ \text{V},\qquad V_E=@@VE@@\ \text{V},\qquad V_F=V_E+U_{S1}=@@VF@@\ \text{V}
\]
于是
\begin{align*}
I_1&=\frac{V_F-V_A}{R_1}=\frac{@@VF@@-@@VA@@}{504.2}\times10^3=@@I1@@\ \text{mA}\\
I_2&=\frac{V_B-V_A}{R_2}=\frac{@@VB@@-@@VA@@}{986.6}\times10^3=@@I2@@\ \text{mA}\\
I_3&=\frac{V_A-V_D}{R_3}=\frac{@@VA@@}{503.4}\times10^3=@@I3@@\ \text{mA}
\end{align*}
\[
U_{AB}=@@UAB@@\ \text{V},\quad U_{CD}=@@UCD@@\ \text{V},\quad U_{AD}=@@UAD@@\ \text{V},\quad
U_{DE}=@@UDE@@\ \text{V},\quad U_{FA}=@@UFA@@\ \text{V}
\]

\subsection*{KVL 验证（用实测值，选两条回路）}
\noindent\textbf{回路 1\ $F\to A\to D\to E\to F$：}
\[
U_{FA}+U_{AD}+U_{DE}-U_{S1}=@@MFA@@+@@MAD@@+@@MDE@@-@@MS1@@=@@KVL1@@\ \text{V}
\]
\noindent\textbf{回路 2\ $A\to B\to C\to D\to A$：}
\[
U_{AB}+U_{BC}+U_{CD}+U_{DA}=@@MAB@@+@@MS2@@+@@MCD@@-@@MAD@@=@@KVL2@@\ \text{V}
\]
（$U_{BC}$ 即电源 $U_{S2}$，$B\to C$ 为正。）
两式残差均 $\le@@KVLMAX@@$~V，相对残差 $<3.4\%$，\ok{KVL 成立}。

\subsection*{KCL 验证（选节点 $A$）}
节点 $A$：$I_1$ 由 $F$ 流入、$I_2$ 由 $B$ 流入、$I_3$ 由 $A$ 流出，故
\[
I_1+I_2-I_3=@@MI1@@+@@MI2@@-@@MI3@@=@@KCL@@\ \text{mA},
\qquad \frac{|@@KCL@@|}{@@MI3@@}\times100\%=@@KCLPCT@@\%
\]
残差远小于各支路电流，\ok{KCL 成立}。
（若要求换节点，可用 $D$：$I_3+\dfrac{U_{DC}}{R_5}=\dfrac{U_{DE}}{R_4}$，同样闭合。）

\section{表 2.1.4\quad 叠加定理验证}
实验条件 $U_{S1}=12$~V、$U_{S2}=6$~V。

\begin{center}
\scriptsize\setlength{\tabcolsep}{2.8pt}
\begin{tabular}{@{}l*{10}{c}@{}}
\toprule
工况 & $U_{S1}$/V & $U_{S2}$/V & $I_1$/mA & $I_2$/mA & $I_3$/mA & $U_{AB}$/V & $U_{CD}$/V & $U_{AD}$/V & $U_{DE}$/V & $U_{FA}$/V\\
\midrule
@@ROWS214@@
\bottomrule
\end{tabular}
\end{center}

\subsection*{校验（写在表下方）}
\noindent\textbf{（1）可加性}：前两行之和与第三行逐列相减，残差为
\begin{center}
\scriptsize\setlength{\tabcolsep}{4pt}
\begin{tabular}{@{}l*{8}{c}@{}}
\toprule
 & $I_1$ & $I_2$ & $I_3$ & $U_{AB}$ & $U_{CD}$ & $U_{AD}$ & $U_{DE}$ & $U_{FA}$\\
\midrule
残差 & @@SUMRES@@\\
\bottomrule
\end{tabular}
\end{center}
除 $U_{AB}$ 一列相差 0.5~V 外，其余各列 $|$残差$|\le0.05$，\ok{可加性成立}。
$U_{AB}$ 的偏差出在“$U_{S1}$ 单独作用”那一次读数：实测 2.9~V，而按实测电阻正演应为 @@THAB1@@~V，
偏高 0.5~V，属单次测量误差。

\noindent\textbf{（2）齐次性}：第二行乘 2 与第四行逐列相减，残差为
\begin{center}
\scriptsize\setlength{\tabcolsep}{4pt}
\begin{tabular}{@{}l*{8}{c}@{}}
\toprule
 & $I_1$ & $I_2$ & $I_3$ & $U_{AB}$ & $U_{CD}$ & $U_{AD}$ & $U_{DE}$ & $U_{FA}$\\
\midrule
残差 & @@HOMRES@@\\
\bottomrule
\end{tabular}
\end{center}
以 $I_1$ 为例：$2\times(-1.2\ \text{mA})=-2.4\ \text{mA}$，与第四行实测 $-2.4$ 完全一致；
各列残差 $\le0.2$（仅 $U_{CD}$ 差 0.2~V），\ok{齐次性成立}。

\noindent\textbf{（3）与理论值对照}（用实测电阻正演，供判断数据质量）：
\begin{center}
\scriptsize\setlength{\tabcolsep}{3.6pt}
\begin{tabular}{@{}l*{8}{c}@{}}
\toprule
工况 & $I_1$/mA & $I_2$/mA & $I_3$/mA & $U_{AB}$/V & $U_{CD}$/V & $U_{AD}$/V & $U_{DE}$/V & $U_{FA}$/V\\
\midrule
@@ROWS214TH@@
\bottomrule
\end{tabular}
\end{center}

\section{$R_3$ 换成 1N4007 二极管}
\begin{center}
\small
\begin{tabular}{@{}ccc l@{}}
\toprule
$U_{S1}$/V & $U_{S2}$/V & $I_3$/mA & 工况\\
\midrule
12.0 & 0    & 7.8    & $U_{S1}$ 单独作用\\
0    & 6.0  & $-1.3$ & $U_{S2}$ 单独作用\\
12.0 & 6.0  & 1.5    & 共同作用\\
0    & 12.0 & $-2.8$ & $U_{S2}$ 加倍（齐次性检验）\\
\bottomrule
\end{tabular}
\end{center}
\textbf{判断}：$7.8+(-1.3)=6.5\neq1.5$，差 5.0~mA（为实测值的 3.3 倍），
\warn{叠加定理不成立}。原因：二极管是\key{非线性元件}，伏安特性不满足齐次性与可加性；
换入二极管后电路不再是线性电路，叠加定理失去前提。
（$2\times(-1.3)=-2.6$ 与 $-2.8$ 接近只是该工作点附近近似线性的巧合，不能据此认为齐次性成立。）

\section{等效变换条件验证（第 3--4 页第 3 节，属实验二）}
\subsection*{原理}
电压源 $U_S$ 与 $R_0$ 串联，对外等效于电流源 $I_S$ 与 $R_0$ 并联，条件是
\begin{equation}
\boxed{\,I_S=\frac{U_S}{R_0}\,}\qquad\text{即 }U_S=I_SR_0
\end{equation}
判据：接同一负载 $R_L$ 时，两者\key{端电压 $U$ 与端电流 $I$ 完全相同}。

\subsection*{两个电路怎么画}
\begin{center}
\begin{tikzpicture}[scale=0.95,>=Stealth]
% 图一
\begin{scope}
  \draw[thick] (0,2.8) -- (0,2.62); \draw[thick] (0,1.78) -- (0,0.3);
  \draw[thick] (0,2.8) -- (1.45,2.8); \draw[thick] (3.25,2.8) -- (4.7,2.8);
  \draw[thick] (4.7,2.8) -- (5.8,2.8); \draw[thick] (5.8,2.8) -- (5.8,1.85);
  \draw[thick] (5.8,1.15) -- (5.8,0.3); \draw[thick] (0,0.3) -- (5.8,0.3);
  \src{0}{2.2}{$U_S$}
  \resh{2.35}{2.8}{$R_0$}
  \draw[fill=white,thick] (5.65,1.15) rectangle (5.95,1.85); \node[right=2pt] at (5.95,1.5) {\scriptsize $R_L$};
  \draw[->,acc2,thick] (4.35,2.8) -- (4.95,2.8) node[midway,above=1pt]{\scriptsize $I$};
  \node[above=1pt] at (5.8,2.8) {\scriptsize $+$};
  \node[below=0.55cm] at (2.9,0.3) {\scriptsize 图一：$U_S$ 与 $R_0$ 串联};
\end{scope}
% 图二
\begin{scope}[xshift=8.4cm]
  \draw[thick] (0,2.8) -- (6.4,2.8); \draw[thick] (0,0.3) -- (6.4,0.3);
  \draw[thick] (2.1,2.8) -- (2.1,2.05); \draw[thick] (2.1,1.35) -- (2.1,0.3);
  \draw[thick,fill=white] (2.1,1.7) circle (0.35); \draw[thick,->] (2.1,1.35) -- (2.1,2.05);
  \node[left=1pt] at (1.72,1.7) {\scriptsize $I_S$};
  \draw[thick] (4.2,2.8) -- (4.2,2.05); \draw[thick] (4.2,1.35) -- (4.2,0.3);
  \draw[fill=white,thick] (4.05,1.35) rectangle (4.35,2.05); \node[right=2pt] at (4.35,1.7) {\scriptsize $R_0$};
  \draw[thick] (6.4,2.8) -- (6.4,2.05); \draw[thick] (6.4,1.35) -- (6.4,0.3);
  \draw[fill=white,thick] (6.25,1.35) rectangle (6.55,2.05); \node[right=2pt] at (6.55,1.7) {\scriptsize $R_L$};
  \draw[->,acc2,thick] (4.85,2.8) -- (5.45,2.8) node[midway,above=1pt]{\scriptsize $I$};
  \node[above=1pt] at (6.4,2.8) {\scriptsize $+$};
  \node[below=0.55cm] at (3.2,0.3) {\scriptsize 图二：$I_S$ 与 $R_0$ 并联};
\end{scope}
\end{tikzpicture}
\end{center}

\subsection*{数据表与计算}
\begin{center}
\footnotesize\setlength{\tabcolsep}{5pt}
\begin{tabular}{@{}lccc c@{}}
\toprule
电路 & 电源取值 & 端电压 $U$/V & 端电流 $I$/mA & 端口电阻 $U/I$ /$\Omega$\\
\midrule
图一（$U_S$ 与 $R_0$ 串联） & $U_S=6.0$~V & 4.1 & 19.2 & @@RP1@@\\
图二（$I_S$ 与 $R_0$ 并联） & $I_S=103.5$~mA & 4.1 & 19.2 & @@RP2@@\\
\bottomrule
\end{tabular}
\end{center}

\noindent\textbf{（1）对外等效}：两种接法的端电压、端电流\key{完全相同}（4.1~V、19.2~mA），
端口电阻 $U/I=@@RP1@@\,\Omega$ 与负载 $R_L=216.4\,\Omega$ 只差 1.3\%，故\ok{两个电源对外电路等效}。

\noindent\textbf{（2）检验等效条件 $I_S=U_S/R_0$}：
\[
I_S^{\text{理}}=\frac{U_S}{R_0}=\frac{6.0}{51.3}\times10^3=@@ISTH@@\ \text{mA}
\quad\text{与}\quad I_S^{\text{测}}=103.5\ \text{mA}\ \text{同量级};\qquad
U_S^{\text{理}}=I_SR_0=103.5\times51.3\times10^{-3}=@@USTH@@\ \text{V}
\]
两者相差约 12\%，来源是电源内阻、表内阻与引线电阻：由图一实测电流反推回路总电阻
$6.0/19.2\,\text{mA}=312\,\Omega$，比 $R_0+R_L=267.7\,\Omega$ 多出约 45~$\Omega$。

\noindent\textbf{（3）图二的理论校验}：
$I_L=I_S\dfrac{R_0}{R_0+R_L}=103.5\times\dfrac{51.3}{267.7}=@@IF2@@$~mA（实测 19.2~mA）；
$U_L=19.83\,\text{mA}\times216.4\,\Omega=@@UF2@@$~V（实测 4.1~V）。理论与实测吻合，进一步说明等效成立。

\section{Discussion of Results（第 5 页，五问全答）}

\subsection*{1. 由表 2.1.3 计算相对误差}
填入表 2.1.3 第三行：
\cw{$1.7,\ 0.8,\ 3.0,\ 2.4,\ 1.3,\ 1.1,\ 5.2,\ 0.7,\ 3.8,\ 3.8$}（\%）。
全部 $<6\%$；最大是 $U_{CD}$ 的 5.2\%，因其绝对值仅 2~V，同样绝对误差占比更大。

\subsection*{2. 选一个节点验证 KCL}
选节点 $A$：$I_1+I_2-I_3=1.8+6.0-7.9=-0.1$~mA，相对残差 1.3\%，KCL 成立（过程见前）。
若选节点 $B$：$I_2$ 应与右侧支路电流相等，用电压换算
$I_{R5}=\dfrac{U_{CD}}{R_5}=\dfrac{-1.9}{326.1}\times10^3=-5.8$~mA，
而 $I_2=6.0$~mA，差 0.2~mA（3\%），同样闭合。

\subsection*{3. 取表 2.1.4 一组数据验证叠加与齐次性}
取 $I_3$、$U_{AD}$ 两列与 $I_1$ 的齐次性：
\[
I_3:\ 6.2+2.4=8.6\ \checkmark\qquad
U_{AD}:\ 3.2+1.2=4.4\ \checkmark\qquad
2\times(-1.2)=-2.4\ \checkmark
\]
故可加性与齐次性成立。唯一例外 $U_{AB}$：$2.9+(-3.6)=-0.7$ 而实测 $-1.2$，差 0.5~V，
由第 1 行读数偏高造成（理论 @@THAB1@@~V）。

\subsection*{4. 电阻功率能否用叠加定理计算}
\warn{不能}。功率是电流的二次函数 $P=I^2R$，不满足可加性。以 $R_3=503.4\,\Omega$ 为例：
\begin{align*}
P_1&=(6.2\times10^{-3})^2\times503.4=@@P1@@\ \text{mW}\\
P_2&=(2.4\times10^{-3})^2\times503.4=@@P2@@\ \text{mW}\\
P_1+P_2&=@@PSUM@@\ \text{mW}\qquad\text{而共同作用时}\quad P=(8.6\times10^{-3})^2\times503.4=@@PBOTH@@\ \text{mW}
\end{align*}
两者相差 $@@PDIFF@@\%$。正确做法：\key{先叠加电流}得总电流，再由 $P=I^2R$ 求功率。

\subsection*{5. 换成二极管后叠加定理还成立吗}
\warn{不成立}。$7.8+(-1.3)=6.5\neq1.5$~mA。二极管为非线性元件，其伏安特性为指数关系，
既不满足齐次性也不满足可加性，而叠加定理的前提正是\key{电路线性}。
结论：叠加定理只适用于线性电路，不能用于含二极管的电路。

\newpage
% ================== 实验三 ==================
\part*{\centering\color{acc} 实验三\quad 交流电路实验}
\addcontentsline{toc}{part}{实验三\quad 交流电路实验（实验册第 6--8 页）}
\markboth{实验三}{实验三}

\section{预习作业（第 6 页）}

\subsection*{1. 并联交流电路中，支路电流能大于总电流吗？}
\key{能。}交流电流是\key{相量}，总电流 $\dot I=\sum\dot I_k$ 为相量和而非代数和。
各支路电流相位不同（容性电流超前、感性电流滞后）时，相量相加会相互抵消，
总电流可以小于某条支路电流。本实验中灯管支路电流始终约 307~mA，
而总电流最低降到 143.7~mA，即为明证。

\subsection*{2. 交流电压表、电流表显示什么值？能代数相加吗？}
\key{显示有效值}（RMS）。不能代数相加：不同相位正弦量的有效值不满足代数和关系，
必须按\key{相量（电压/电流三角形）}合成，例如串联 $R-C$ 电路有 $U=\sqrt{U_R^2+U_C^2}$，
而不能写成 $U=U_R+U_C$。

\subsection*{3. 测有功功率时，电压线圈前接还是电流线圈外接？}
\key{取决于负载阻抗的大小}，原则是让功率表自身损耗对读数影响最小：
负载阻抗\key{较小}（负载电流大）时用\cw{电压线圈前接}（电压支路接电源侧），
此时电流线圈压降影响可忽略；负载阻抗\key{较大}（负载电流小）时用\cw{电压线圈后接}
（电压支路接负载侧），此时电压支路分流影响可忽略。

\subsection*{4. 用小电容并联判断负载性质（相量图说明）}
以端电压 $\dot U$ 为参考相量，容性电流 $\dot I_C$ 超前 $\dot U$ 90°（$i_C=C\,\mathrm du/\mathrm dt$），
与负载电流 $\dot I_L$ 相加得 $\dot I=\dot I_L+\dot I_C$：
$|\dot I|$ \key{减小}（更靠近 $\dot U$）$\Rightarrow$ 负载\cw{感性}；
$|\dot I|$ \key{增大}（更远离 $\dot U$）$\Rightarrow$ 负载\cw{容性}；
$|\dot I|$ \key{基本不变} $\Rightarrow$ 负载\cw{阻性}。
本实验并入电容后总电流先减后增、最小值出现在 $C=3.7\,\mu$F，说明日光灯为\key{感性负载}。

\begin{center}
\begin{tikzpicture}[scale=0.95,>=Stealth]
  \draw[->,thick] (0,0) -- (4.6,0) node[right] {\small $\dot U$};
  \draw[->,thick,acc2] (0,0) -- (1.5,-2.9) node[below right] {\small $\dot I_L$};
  \draw[->,thick,okc] (0,0) -- (0,2.4) node[above] {\small $\dot I_C$};
  \draw[->,thick,warnc] (0,0) -- (1.5,-0.5) node[right] {\small $\dot I=\dot I_L+\dot I_C$};
  \draw[dashed,gray] (1.5,-2.9) -- (1.5,0);
  \draw[->,gray] (1.5,2.4) -- (1.5,-2.9);
  \draw (0.6,0) arc (0:-62:0.6);
  \node at (1.05,-0.32) {\scriptsize $\varphi$};
  \node[gray,right] at (1.55,2.35) {\scriptsize $-\dot I_C$（相量差）};
\end{tikzpicture}
\end{center}

\section{日光灯电路接线（第 7 页，图 2.3.3）}
\textbf{接线顺序}：交流电源 $\to$ 闸刀开关 $\to$ 熔断器 $\to$ 功率表电流线圈 $\to$ 镇流器
$\to$ 灯管 $\to$ 回零线；功率表电压线圈并在灯管（或电源）两端；
电容器组经各自开关\key{并联在电源两端}。
\\[2pt]
\textbf{必须写进报告的安全要求}：接线完毕先自查，\warn{不得自行合闸}，
须请指导教师检查后由教师送电；改接线路前必须断电验电。

\section{日光灯电路数据（表 2.3.4 / 2.3.5）}
\textbf{哪些是实测、哪些要算}：$C,U,U_R,U_L,I,I_C,I_L,P,P_{LR},P_C$ 为实测；
$\cos\varphi$ 计算列按 $\cos\varphi=P/(UI)$（$I$ 用安培）。

\begin{center}
\scriptsize\setlength{\tabcolsep}{2.2pt}
\begin{tabular}{@{}c*{11}{c}@{}}
\toprule
$C/\mu$F & $U$/V & $U_R$/V & $U_L$/V & $I$/mA & $I_C$/mA & $I_L$/mA & $P$/W & $P_{LR}$/W & $P_C$/W & $\cos\varphi$计算 & $\cos\varphi$实测\\
\midrule
@@FLROWS@@
\bottomrule
\end{tabular}
\end{center}
{\scriptsize 另：灯管功率 $P_L=14.1$~W，镇流器功率 $P_R=14.4$~W，二者之和 28.5~W 与总功率 $\approx28.4$~W 相符。}

\noindent\textbf{计算过程示范（写两行即可）}：
\[
C=0.0\,\mu\text{F}:\ \cos\varphi=\frac{P}{UI}=\frac{28.4}{219.6\times0.3134}=0.413
\quad(\text{实测 }0.426,\text{ 差 }3.1\%)
\]
\[
C=3.7\,\mu\text{F}:\ \cos\varphi=\frac{28.2}{219.6\times0.1437}=0.894
\quad(\text{实测 }0.989,\text{ 差 }9.6\%)
\]

\noindent\textbf{分析用补充量}（$S=UI$，$Q=\sqrt{S^2-P^2}$，$I_C^{\text{理}}=\omega CU$）：
\begin{center}
\scriptsize\setlength{\tabcolsep}{4pt}
\begin{tabular}{@{}cccccc@{}}
\toprule
$C/\mu$F & $S$/VA & $Q$/var & $I_C^{\text{理}}$/mA & $\cos\varphi$计算 & 与实测偏差\\
\midrule
@@FLROWS2@@
\bottomrule
\end{tabular}
\end{center}

\subsection*{补偿效果分析（结论段）}
\begin{itemize}
  \item 并入电容后灯管支路电流 $I_L$ 基本不变（约 307~mA），总电流 $I$ 由 313.4~mA
        降到最低 143.7~mA（$C=3.7\,\mu$F），再回升到 222.3~mA；
  \item 功率因数由 0.413 提高到 0.894--0.989，即 $\varphi$ 由 $65.6^\circ$ 降到约 $8.5^\circ$；
  \item 总电流最小时无功功率也最小（$Q=14.2$~var），说明容性无功恰好补偿掉感性无功；
  \item 理论最佳电容
        \[
        C_{\text{opt}}=\frac{P\tan\varphi_0}{\omega U^2}
        =\frac{28.4\times\tan65.6^\circ}{2\pi\times50\times219.6^2}\times10^{6}=@@COPT@@\ \mu\text{F},
        \]
        与实测最小电流对应的 $3.7\,\mu$F 基本一致，验证了并联电容提高功率因数的原理。
\end{itemize}

\section{点火电压（第 8 页）}
日光灯启辉瞬间的\key{点火电压}实测为 \cw{173.3~V}。
说明：灯管冷态需高于工作电压的电压才能击穿气体放电，该电压由镇流器在启辉器断开的瞬间
产生的自感电动势提供；点燃后镇流器转为限流作用，灯管工作在约 56.7~V、0.3~A 的状态。

\section{电压三角形关系验证（第 8 页第 2 节）}
\textbf{电路}：电容 $C$ 与阻性负载串联接在交流电源上，用电压表分别测负载电压 $U_R$、
电容电压 $U_C$ 与总电压 $U$。

\begin{center}
\begin{tikzpicture}[scale=0.9,>=Stealth]
  \draw[thick] (0,2.4) -- (0,2.22); \draw[thick] (0,1.38) -- (0,0.4);
  \draw[thick] (0,2.4) -- (1.5,2.4); \draw[thick] (1.5,2.4) -- (2.6,2.4);
  \draw[thick,fill=white] (1.5,2.4) circle (0.28); \node at (1.5,2.4) {\scriptsize A};
  \draw[thick] (2.6,2.4) -- (4.2,2.4); \draw[thick] (4.5,2.4) -- (4.9,2.4);
  \capsym{4.35}{2.4}{}
  \node[below=0.68cm] at (4.35,2.4) {\scriptsize $C$};
  \node[above] at (4.35,2.95) {\scriptsize $U_C$};
  \draw[thick] (4.9,2.4) -- (6.4,2.4); \draw[thick] (6.4,2.4) -- (6.4,1.7);
  \draw[fill=white,thick] (6.15,1.1) rectangle (6.65,1.7); \node[right=2pt] at (6.65,1.4) {\scriptsize $R$};
  \draw[thick] (6.4,1.1) -- (6.4,0.4); \draw[thick] (6.4,0.4) -- (0,0.4);
  \src{0}{1.8}{$\sim$}
  \node[below] at (1.5,2.1) {\scriptsize 电流表};
  \node[right=2pt] at (6.7,1.65) {\scriptsize $U_R$};
  \node[below] at (3.2,0.4) {\scriptsize $U$};
\end{tikzpicture}
\end{center}

\begin{center}
\small\setlength{\tabcolsep}{8pt}
\begin{tabular}{@{}lccc@{}}
\toprule
 & $C=1\,\mu$F & $C=2\,\mu$F & $C=4.7\,\mu$F\\
\midrule
$U_R$/V（实测） & @@VR1@@ & @@VR2@@ & @@VR3@@\\
$U_C$/V（实测） & @@VC1@@ & @@VC2@@ & @@VC3@@\\
$U$/V（实测） & @@VU1@@ & @@VU2@@ & @@VU3@@\\
$\sqrt{U_R^2+U_C^2}$/V & @@VT1@@ & @@VT2@@ & @@VT3@@\\
偏差 $/\%$ & @@VD1@@ & @@VD2@@ & @@VD3@@\\
$\varphi=\arctan(U_C/U_R)$ & @@VP1@@ & @@VP2@@ & @@VP3@@\\
\bottomrule
\end{tabular}
\end{center}

\noindent\textbf{验证过程（写一行示范即可）}：
\par\noindent
@@VTLINE@@
\par\noindent
三组偏差均 $<0.3\%$，故 $U=\sqrt{U_R^2+U_C^2}$ \ok{电压三角形关系成立}：
串联 $R-C$ 电路中总电压是 $U_R$ 与 $U_C$ 的\key{相量和}，
三者构成以 $\varphi$ 为夹角的直角三角形，且 $\cos\varphi=U_R/U$。

\section{实验三结论（写在报告末尾）}
\begin{enumerate}
  \item 并联电容可补偿感性负载的无功功率、提高功率因数：$\cos\varphi$ 由 0.413 提高到 0.894 左右，
        总电流由 313.4~mA 降到 143.7~mA，而负载支路电流与有功功率几乎不变。
  \item 补偿电容存在最佳值（本实验 3.7--4.7\,$\mu$F，理论 @@COPT@@\,$\mu$F）；
        过补偿会使总电流反而增大、功率因数下降（$C=5.7\,\mu$F 时 $\cos\varphi$ 回落到 0.638）。
  \item 串联 $R-C$ 电路的电压满足 $U=\sqrt{U_R^2+U_C^2}$，验证了交流量的相量（三角形）关系。
  \item 交流表读数均为有效值，不能代数相加，必须按相量合成。
\end{enumerate}

\newpage
\appendix
\section{速查：每张表每格写什么}
\begin{center}
\footnotesize\setlength{\tabcolsep}{3pt}
\begin{tabularx}{\linewidth}{@{}p{2.4cm}p{2.6cm}X@{}}
\toprule
表格 & 行 & 填写内容\\
\midrule
表 2.1.2 & 标称值 & 510, 1000, 510, 510, 330, 51, 220\\
 & 实测值 & 504.2, 986.6, 503.4, 503.9, 326.1, 51.3, 216.4\\
 & 相对误差 & 1.14, 1.34, 1.29, 1.20, 1.18, 0.59, 1.64（\%）\\
\midrule
表 2.1.3 & 实测 & 5.9, 12.1, 1.8, 6.0, 7.9, $-6.0$, $-1.9$, 4.0, 0.9, 0.9\\
 & 计算 & 6.0, 12.0, @@I1@@, @@I2@@, @@I3@@, @@UAB@@, @@UCD@@, @@UAD@@, @@UDE@@, @@UFA@@\\
 & 相对误差 & 1.7, 0.8, 3.0, 2.4, 1.3, 1.1, 5.2, 0.7, 3.8, 3.8（\%）\\
\midrule
表 2.1.4 & 四行 & 见正文表（含齐次性行）\\
 & 校验 & 两张残差表 + 一句结论\\
\midrule
二极管表 & 四行 & 7.8, $-1.3$, 1.5, $-2.8$（mA）\\
\midrule
等效变换 & 两行 & 图一 4.1~V/19.2~mA；图二 4.1~V/19.2~mA\\
\midrule
日光灯表 & 六行 & 见正文；$\cos\varphi$ 计算列 0.413, 0.471, 0.652, 0.894, 0.803, 0.578\\
\midrule
电压三角形 & 五行 & 见表：$\sqrt{U_R^2+U_C^2}$ 与偏差\\
\midrule
点火电压 & 一格 & 173.3~V\\
\bottomrule
\end{tabularx}
\end{center}

\section{常见失分点}
\begin{enumerate}
  \item \key{只写数不写公式}：每个计算项先写公式再代入，如
        $\delta=\frac{|x_{\text{测}}-x_{\text{算}}|}{|x_{\text{算}}|}\times100\%$。
  \item \key{有效数字混乱}：电压、电流 1 位小数；相对误差 1--2 位小数。
  \item \key{符号方向}：$I_2$、$I_3$ 的正方向必须与图中箭头一致，否则 KCL 会自相矛盾。
  \item \key{KVL 回路方向}：绕行方向与参考方向一致取正、相反取负，写成 $\sum U=0$。
  \item \key{叠加定理的适用范围}：必须点明“只适用于线性电路、只适用于电压/电流这类线性量，
        功率不能叠加”。
  \item \key{交流量不能代数相加}：$U=\sqrt{U_R^2+U_C^2}$、相量图这类结论要说明“因为是相量”。
  \item \key{安全操作}：日光灯接线必须注明“经教师检查后送电”。
\end{enumerate}

\section{数据与来源说明}
全部实测数据取自你的实验记录本扫描件（8 页），并已与你逐表核对后冻结；
计算值由 $R_1=504.2$、$R_2=986.6$、$R_3=503.4$、$R_4=503.9$、$R_5=326.1\ \Omega$
按节点电压法正演得到，与实测值的偏差均 $<6\%$，
说明记录数据内部自洽，可直接作为报告依据。

\end{document}
"""

repl = {
    "@@NOM@@": row_nom, "@@MEA@@": row_mea, "@@ERR@@": row_err,
    "@@R213M@@": r213_meas, "@@R213C@@": r213_calc, "@@R213E@@": r213_rel,
    "@@VA@@": f2(v["vA"], 3), "@@VB@@": f2(v["vB"], 3), "@@VE@@": f2(v["vE"], 3),
    "@@VF@@": f2(v["vF"], 3),
    "@@I1@@": f2(k["I1"], 2), "@@I2@@": f2(k["I2"], 2), "@@I3@@": f2(k["I3"], 2),
    "@@UAB@@": num(k["U_AB"], 2), "@@UCD@@": num(k["U_CD"], 2),
    "@@UAD@@": num(k["U_AD"], 2), "@@UDE@@": num(k["U_DE"], 2), "@@UFA@@": num(k["U_FA"], 2),
    "@@MFA@@": num(m["U_FA"], 1), "@@MAD@@": num(m["U_AD"], 1), "@@MDE@@": num(m["U_DE"], 1),
    "@@MS1@@": num(m["U_S1"], 1), "@@MAB@@": num(m["U_AB"], 1), "@@MS2@@": num(m["U_S2"], 1),
    "@@MCD@@": num(m["U_CD"], 1), "@@MI1@@": num(m["I1"], 1),
    "@@MI2@@": num(m["I2"], 1), "@@MI3@@": num(m["I3"], 1),
    "@@KVL1@@": num(kvl1, 2), "@@KVL2@@": num(kvl2, 2),
    "@@KVLMAX@@": f2(max(abs(kvl1), abs(kvl2)), 1),
    "@@KCL@@": num(kcl, 1), "@@KCLPCT@@": f2(abs(kcl) / m["I3"] * 100, 1),
    "@@ROWS214@@": "\n".join(rows214),
    "@@ROWS214TH@@": "\n".join(rows214_th),
    "@@SUMRES@@": sum_res, "@@HOMRES@@": hom_res,
    "@@THAB1@@": f2(th[cas[0]]["U_AB"], 2),
    "@@P1@@": f2(p1, 1), "@@P2@@": f2(p2, 1), "@@PSUM@@": f2(p1 + p2, 1),
    "@@PBOTH@@": f2(pboth, 1), "@@PDIFF@@": f2((pboth - (p1 + p2)) / (p1 + p2) * 100, 0),
    "@@RP1@@": f2(EQ["R_port1"], 1), "@@RP2@@": f2(EQ["R_port2"], 1),
    "@@ISTH@@": f2(EQ["IS_theory"], 1), "@@USTH@@": f2(EQ["US_from_IS"], 2),
    "@@IF2@@": f2(EQ["I_theory2"], 2), "@@UF2@@": f2(EQ["U_theory2"], 2),
    "@@COPT@@": f2(FL["C_opt"], 2),
    "@@FLROWS@@": "\n".join(fl_rows),
    "@@FLROWS2@@": "\n".join(fl_rows2),
    "@@VTLINE@@": vt_line,
}
for c_, cap in enumerate(["1", "2", "4.7"]):
    r = vr[cap]
    repl[f"@@VR{c_+1}@@"] = f2(r["UR"], 1)
    repl[f"@@VC{c_+1}@@"] = f2(r["UC"], 1)
    repl[f"@@VU{c_+1}@@"] = f2(r["U"], 1)
    repl[f"@@VT{c_+1}@@"] = f2(r["U_calc"], 1)
    repl[f"@@VD{c_+1}@@"] = f"{r['dev']:+.2f}"
    repl[f"@@VP{c_+1}@@"] = f2(r["phi"], 1) + r"$^\circ$"

for k_, v_ in repl.items():
    TEX = TEX.replace(k_, v_)

tex_path = os.path.join(ROOT, "report_guide.tex")
with open(tex_path, "w", encoding="utf-8") as fh:
    fh.write(TEX)

ok = True
for _ in range(2):
    p = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", "report_guide.tex"],
                       cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        ok = False
        print("=== xelatex failed ===")
        out = p.stdout or ""
        idx = out.find("!")
        print(out[max(0, idx - 500): idx + 1500] if idx > 0 else out[-3000:])
        break
print("compiled:", ok, "| pdf:", os.path.exists(os.path.join(ROOT, "report_guide.pdf")))
