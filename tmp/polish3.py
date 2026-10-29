p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
s = open(p, encoding="utf-8").read()

# (a) §0 末尾补「读的顺序」，填满首页
anchor_a = "本讲义一律用 $h$ 表示片厚，就是为了让这两件事在纸上分得开。}\n"
add_a = anchor_a + (
r"""
\subhdr{0.3 读的顺序（一条主线）}

\begin{enumerate}
\item \textbf{先把换算写死}：$\delta=\frac{2\pi}{\lambda}\Delta L$（\S2）。所有干涉题都从这一条出发，包括你作业里那步 $\delta_P=16\pi$。
\item \textbf{再用几何换成装置参数}：双缝 $\Delta L\approx yd/D$（\S3）；双镜、双棱镜、洛埃镜各自换成等效双缝间距 $d_{\mathrm{eq}}$（\S8）。
\item \textbf{遇到“插片、移动、盖缝”只用一句}：零级 $\Leftrightarrow$ $\Delta L=0$（\S5）。片厚 $h$ 的作用只是在某束光的 $\Delta L$ 上加 $(n-1)h$。
\item \textbf{遇到“看不看得清”}：用对比度与空间相干（\S6--\S7）。
\end{enumerate}
""")
print("anchor a:", s.count(anchor_a))
s = s.replace(anchor_a, add_a, 1)

# (b) 免得“8.2 三个装置对照”标题孤零零落在页底
anchor_b = "\\subhdr{8.2 三个装置对照}"
print("anchor b:", s.count(anchor_b))
s = s.replace(anchor_b, "\\needspace{0.45\\textheight}\n" + anchor_b, 1)

open(p, "w", encoding="utf-8", newline="\n").write(s)
print("ok")
