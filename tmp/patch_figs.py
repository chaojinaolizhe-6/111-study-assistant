# -*- coding: utf-8 -*-
"""把讲义里的图 1 换成教材原图裁剪、图 2 换成加宽版重绘。"""
import io, re, sys

p = r"D:\aaa_D_usual\DSH\111学习助手\subjects\06-电工电子技术\实验\实验5-单管放大电路-实验讲义-20261104.tex"
s = io.open(p, encoding="utf-8").read()

# 1) 导言区加 graphicx
if "\\usepackage{graphicx}" not in s:
    s = s.replace("\\usepackage[american]{circuitikz}",
                  "\\usepackage[american]{circuitikz}\n\\usepackage{graphicx}", 1)

fig1_new = r"""\begin{center}
\includegraphics[width=0.90\linewidth]{图-实验5-教材图524-裁剪.png}

{\small 图 1\quad 共射极单管放大电路（\textbf{裁剪}自教材图 5.2.4，书 p.151）。$S_1$ 与 $R_{E2}$ 并联（闭合即短接 $R_{E2}$）；$S_2$ 串在负载支路里，断开设就是开路；a、b1/b2、d1/d2、c 是实验箱面上的接线柱，跳线方式见 §4.3。}
\end{center}
"""

start = s.index(r"\subhdr{4.2 电路")
end = s.index(r"\subhdr{4.3 端子与开关")
s = s[:start] + r"\subhdr{4.2 电路（教材图 5.2.4 原图）}" + "\n\n" + fig1_new + "\n" + s[end:]

fig2_new = r"""\begin{center}
\begin{circuitikz}[american, scale=1.0, transform shape]
% ---- (a) S1 closed ----
\node at (2.7,3.9) {\small (a) $S_1$ 闭合：$R_{E2}$ 被短接，无负反馈};
\draw (0.4,3.2) to[V=$U_s$] (0.4,1.7) to[R=$R_s$] (0.4,0.2);
\draw (0.4,3.2) -- (1.6,3.2);
\node[circ] at (1.6,3.2) {};
\node[above] at (1.6,3.26) {\small B};
\draw (1.6,3.2) to[R=$R_B$] (1.6,0.2);
\draw (1.6,3.2) -- (2.8,3.2);
\node[circ] at (2.8,3.2) {};
\draw (2.8,3.2) to[R=$r_{be}$] (2.8,0.2);
\draw (2.8,3.2) -- (4.0,3.2);
\node[circ] at (4.0,3.2) {};
\node[above] at (4.0,3.26) {\small C};
\draw (4.0,3.2) to[I, l=$\beta i_b$] (4.0,0.2);
\draw (4.0,3.2) -- (5.2,3.2);
\draw (5.2,3.2) to[R=$R_C$] (5.2,0.2);
\draw (0.4,0.2) -- (5.2,0.2);
\node[ground] at (3.4,0.2) {};
% ---- (b) S1 open ----
\begin{scope}[xshift=8.0cm]
\node at (2.7,3.9) {\small (b) $S_1$ 断开：$R_{E2}$ 串在发射极，有负反馈};
\draw (0.4,3.2) to[V=$U_s$] (0.4,1.7) to[R=$R_s$] (0.4,0.2);
\draw (0.4,3.2) -- (1.6,3.2);
\node[circ] at (1.6,3.2) {};
\node[above] at (1.6,3.26) {\small B};
\draw (1.6,3.2) to[R=$R_B$] (1.6,0.2);
\draw (1.6,3.2) -- (2.8,3.2);
\node[circ] at (2.8,3.2) {};
\draw (2.8,3.2) to[R=$r_{be}$] (2.8,1.4);
\node[circ] at (2.8,1.4) {};
\node[below] at (2.8,1.33) {\small E};
\draw (2.8,1.4) to[R=$R_{E2}$] (2.8,0.2);
\draw (2.8,3.2) -- (4.0,3.2);
\node[circ] at (4.0,3.2) {};
\node[above] at (4.0,3.26) {\small C};
\draw (4.0,3.2) to[I, l=$\beta i_b$] (4.0,1.4);
\draw (4.0,1.4) -- (2.8,1.4);
\draw (4.0,3.2) -- (5.2,3.2);
\draw (5.2,3.2) to[R=$R_C$] (5.2,0.2);
\draw (0.4,0.2) -- (5.2,0.2);
\node[ground] at (3.4,0.2) {};
\end{scope}
\end{circuitikz}

{\small 图 2\quad 交流通路与小信号等效电路（\textbf{重绘}）：三极管用 $r_{be}$ 与受控源 $\beta i_b$ 替换（受控源按惯例画成恒流源符号）。左图为 $S_1$ 闭合，右图为 $S_1$ 断开——$r_{be}$ 与 $R_{E2}$ 串联后接地，所以后面所有式子里的 $r_{be}$ 都要换成 $r_{be}+(1+\beta)R_{E2}$。}
\end{center}
"""

start2 = s.index(r"\subhdr{2.2 小信号模型")
end2 = s.index("模型只有两句话")
s = s[:start2] + r"\subhdr{2.2 小信号模型：$r_{be}$ 是哪来的}" + "\n\n" + fig2_new + "\n" + s[end2:]

io.open(p, "w", encoding="utf-8").write(s)
print("ok", len(s))
