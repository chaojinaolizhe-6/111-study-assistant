# -*- coding: utf-8 -*-
"""图 2 改为单幅：实线=有反馈，虚线=被短接的 R_E2。"""
import io

p = r"D:\aaa_D_usual\DSH\111学习助手\subjects\06-电工电子技术\实验\实验5-单管放大电路-实验讲义-20261104.tex"
s = io.open(p, encoding="utf-8").read()

fig2 = r"""\begin{center}
\begin{circuitikz}[american, scale=1.15, transform shape]
\draw (0.6,3.6) to[V=$U_s$] (0.6,2.0) to[R=$R_s$] (0.6,0.4);
\draw (0.6,3.6) -- (2.2,3.6);
\node[circ] at (2.2,3.6) {};
\node[above] at (2.2,3.66) {\small B};
\draw (2.2,3.6) to[R, l={\small $R_B$}] (2.2,0.4);
\draw (2.2,3.6) -- (3.6,3.6);
\node[circ] at (3.6,3.6) {};
\draw (3.6,3.6) to[R, l={\small $r_{be}$}] (3.6,1.6);
\node[circ] at (3.6,1.6) {};
\node[below left] at (3.55,1.55) {\small E};
\draw (3.6,1.6) to[R, l={$R_{E2}$}] (3.6,0.4);
\draw[dashed, thick] (2.1,1.0) -- (2.1,0.4) -- (3.5,0.4);
\node[left] at (2.05,0.7) {\small 短接};
\draw (3.6,3.6) -- (5.2,3.6);
\node[circ] at (5.2,3.6) {};
\node[above] at (5.2,3.66) {\small C};
\draw (5.2,3.6) to[I, l={$\beta i_b$}] (5.2,1.6);
\draw (5.2,1.6) -- (3.6,1.6);
\draw (5.2,3.6) -- (6.4,3.6);
\draw (6.4,3.6) to[R, l_={\small $R_C$}] (6.4,0.4);
\draw (0.6,0.4) -- (6.4,0.4);
\node[ground] at (1.4,0.4) {};
\end{circuitikz}

{\small 图 2\quad 小信号等效电路（\textbf{重绘}）：实线为 $S_1$ 断开（$R_{E2}$ 接入，电流串联负反馈）；虚线表示 $S_1$ 闭合时 $R_{E2}$ 被短接。受控源 $\beta i_b$ 按惯例画成恒流源符号；$r_{be}$ 与 $R_{E2}$ 串联后接地，所以有反馈时所有式子里的 $r_{be}$ 都要换成 $r_{be}+(1+\beta)R_{E2}$。}
\end{center}
"""

start = s.index("\\begin{center}\n\\begin{circuitikz}[american, scale=1.0, transform shape]")
end = s.index("%=============================================================\n\\hdr{§3}")
s = s[:start] + fig2 + "\n" + s[end:]
s = s.replace("断开设就是开路", "断开就是开路")
io.open(p, "w", encoding="utf-8").write(s)
print("ok", len(s))
