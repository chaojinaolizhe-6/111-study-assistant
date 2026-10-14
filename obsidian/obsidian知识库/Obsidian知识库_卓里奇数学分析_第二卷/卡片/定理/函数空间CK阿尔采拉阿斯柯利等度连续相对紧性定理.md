---
tags: [定理卡]
aliases:
  - 阿尔采拉-阿斯柯利定理
  - 阿尔采拉-阿斯科利定理
  - Arzelà-Ascoli 定理
  - Arzelà–Ascoli theorem
  - Arzelà-Ascoli compactness theorem
created: 2026-09-18
updated: 2026-09-18
---

<!-- unit:u16_04_arzela_ascoli -->

# 定理1（阿尔采拉－阿斯柯利定理）

> [!summary] 核心论断
> 设 $K$ 是度量紧集，$Y$ 是完备度量空间。连续函数族 $\mathfrak{F}\subset C(K,Y)$ 相对列紧，即 $\mathfrak{F}$ 中任意序列都含有一个在 $K$ 上一致收敛的子序列，其充要条件是：$\mathfrak{F}$ 完全有界且等度连续。

## 完整表述与条件

先复述教材引入的三个基本概念。

**定义1（一致有界函数族）**  
设 $f:X\to Y$ 是定义在集合 $X$ 上、取值于度量空间 $Y$ 的函数。若函数值的集合

$$
V=\left\{ y\in Y\mid \exists f\in\mathfrak{F},\ \exists x\in X,\ y=f(x) \right\}
$$

在 $Y$ 中有界，则称函数族 $\mathfrak{F}$ 在 $X$ 上一致有界。对于数值函数或 $f:X\to\mathbb{R}^n$ 的情形，这等价于：存在常数 $M\in\mathbb{R}$，使得对任意 $x\in X$ 与任意 $f\in\mathfrak{F}$，都有 $|f(x)|\le M$。

**定义1′（完全有界函数族）**  
如果函数族 $\mathfrak{F}$ 中所有函数值的集合 $V\subset Y$ 完全有界，即对任意 $\varepsilon>0$，在 $Y$ 中存在 $V$ 的有限 $\varepsilon$-网，则称函数族 $\mathfrak{F}$ 完全有界。

当 $Y=\mathbb{R},\mathbb{C},\mathbb{R}^n,\mathbb{C}^m$ 或一般局部紧空间时，有界集与完全有界集概念一致，因此此时“一致有界”与“完全有界”也一致。

**定义2（等度连续函数族）**  
设 $X,Y$ 是度量空间。函数族 $\mathfrak{F}$ 称为在 $X$ 上等度连续，如果对任意 $\varepsilon>0$，存在 $\delta>0$，使得只要 $x_1,x_2\in X$ 且 $d_X(x_1,x_2)<\delta$，则对一切 $f\in\mathfrak{F}$ 都有

$$
d_Y(f(x_1),f(x_2))<\varepsilon.
$$

> [!theorem] 阿尔采拉－阿斯柯利定理
> 设 $K$ 是度量紧集，$Y$ 是完备度量空间，$\mathfrak{F}$ 是由连续函数 $f:K\to Y$ 构成的函数族。则以下两个命题等价：
>
> 1. $\mathfrak{F}$ 中任意序列 $\{f_n\in\mathfrak{F}:n\in\mathbb{N}\}$ 都包含一个在 $K$ 上一致收敛的子序列；
> 2. $\mathfrak{F}$ 完全有界且等度连续。

原书此定理置于第十六章 §4“连续函数空间的紧子集和稠密子集”之内，定理编号为定理1。

## 证明思路与关键步骤

### 引理1：一致收敛序列的必要条件

设 $K,Y$ 是度量空间，$K$ 是紧集。若连续函数列 $\{f_n:K\to Y\}$ 在 $K$ 上一致收敛到 $f$，则 $\{f_n:n\in\mathbb{N}\}$ 完全有界且等度连续。

由 §3 定理2，一致极限 $f\in C(K,Y)$。因为 $f$ 在紧集 $K$ 上一致连续，对任意 $\varepsilon>0$，存在 $\delta>0$，使得当 $d_K(x_1,x_2)<\delta$ 时，

$$
d_Y(f(x_1),f(x_2))<\varepsilon.
$$

又由一致收敛性，对这个 $\varepsilon$，存在 $N\in\mathbb{N}$，使当 $n>N$ 时对一切 $x\in K$ 有

$$
d_Y(f(x),f_n(x))<\varepsilon.
$$

利用三角形不等式，当 $n>N$ 且 $d_K(x_1,x_2)<\delta$ 时，

$$
\begin{aligned}
d_Y(f_n(x_1),f_n(x_2))
&\le d_Y(f_n(x_1),f(x_1))
 + d_Y(f(x_1),f(x_2))
 + d_Y(f(x_2),f_n(x_2))\\
&<3\varepsilon.
\end{aligned}
$$

所以函数族 $\{f_n:n>N\}$ 等度连续。再把有限个在紧集 $K$ 上连续的函数 $f_1,\ldots,f_N$ 补入，仍得到等度连续族，故整个 $\{f_n:n\in\mathbb{N}\}$ 等度连续。

完全有界性来自：当 $n>N$ 时，$f_n(K)$ 中的每个值都在 $f(K)$ 的 $\varepsilon$-邻域内；而 $f(K)$ 与 $\bigcup_{n=1}^{N}f_n(K)$ 都是 $Y$ 中的紧集，因而完全有界。于是整个函数值集合也完全有界。

### 定理必要性

假定函数族 $\mathfrak{F}$ 不满足条件2。

若 $\mathfrak{F}$ 不完全有界，则可从 $\mathfrak{F}$ 中取出一个不完全有界的函数序列 $\{f_n\}$。由引理1，该序列不可能选出一致收敛子序列。

若 $\mathfrak{F}$ 不等度连续，则存在 $\varepsilon_0>0$、函数列 $\{f_n\in\mathfrak{F}\}$ 以及点对序列 $(x_n',x_n'')$，使得点 $x_n',x_n''$ 均收敛到某个 $x_0\in K$，但

$$
d_Y(f_n(x_n'),f_n(x_n''))\ge \varepsilon_0>0.
$$

如果 $\{f_n\}$ 存在一致收敛子序列，按引理1该子序列应等度连续，这与上述构造矛盾。因此不可能选出一致收敛子序列。

所以条件1蕴含条件2。

### 定理充分性：对角线法则

设 $\{f_n:n\in\mathbb{N}\}$ 是 $\mathfrak{F}$ 的任意函数列。若 $K$ 为有限集，结论显然，故可设 $K$ 为无限集。

在 $K$ 中取一个处处稠密的可数子集 $E=\{x_1,x_2,\ldots\}$。这样的 $E$ 可由 $K$ 的关于 $\varepsilon=1,\frac12,\ldots,\frac1n,\ldots$ 的有限 $\varepsilon$-网的并集得到。

考察这些函数在 $x_1$ 处的值序列 $\{f_n(x_1)\}$。由 $\mathfrak{F}$ 完全有界，该值序列完全有界；又因 $Y$ 完备，可从中选出收敛子序列，记对应的函数子序列为 $\{f_n^1:n\in\mathbb{N}\}$。

再从 $\{f_n^1\}$ 中选出子序列 $\{f_n^2\}$，使 $\{f_n^2(x_2)\}$ 也收敛。继续此过程，得到一串逐次提取的子序列

$$
\{f_n^k:n\in\mathbb{N}\},\qquad k=1,2,\ldots,
$$

其中第 $k$ 个子序列在点 $x_1,\ldots,x_k$ 处均收敛。

取对角线序列

$$
g_n=f_n^n,\qquad n\in\mathbb{N}.
$$

对任意固定的 $x_i\in E$，当 $n\ge i$ 时，$g_n=f_n^n$ 是已使 $x_i$ 处收敛的子序列的尾巴，因此 $g_n(x_i)$ 收敛。于是对角线序列在稠密子集 $E$ 的每一点都收敛。

下面证明 $\{g_n\}$ 在 $K$ 上一致收敛。任给 $\varepsilon>0$，由 $\mathfrak{F}$ 的等度连续性取 $\delta>0$。设 $E_0=\{\xi_1,\ldots,\xi_r\}\subset E$ 是 $K$ 的有限 $\delta$-网。因为每个 $\{g_n(\xi_i)\}$ 都收敛，存在 $N\in\mathbb{N}$，使当 $m,n>N$ 时，

$$
d_Y(g_m(\xi_i),g_n(\xi_i))<\varepsilon,\qquad i=1,\ldots,r.
$$

对任意 $x\in K$，取 $\xi_j\in E_0$ 使 $d_K(x,\xi_j)<\delta$。由等度连续性，对每个 $n$ 有

$$
d_Y(g_n(x),g_n(\xi_j))<\varepsilon,
$$

同样对 $g_m$ 也成立。于是

$$
\begin{aligned}
d_Y(g_m(x),g_n(x))
&\le d_Y(g_n(x),g_n(\xi_j))
 + d_Y(g_m(\xi_j),g_n(\xi_j))
 + d_Y(g_m(x),g_m(\xi_j))\\
&<\varepsilon+\varepsilon+\varepsilon=3\varepsilon.
\end{aligned}
$$

由于 $x\in K$ 任意，按柯西准则，$\{g_n\}$ 在 $K$ 上一致收敛。因此 $\mathfrak{F}$ 中任意序列都含一致收敛子序列。

## 推论、使用方式与边界

在紧集 $K$ 上连续且取值于 $Y$ 的函数空间 $C(K,Y)$ 上，教材引入一致收敛性度量

$$
d(f,g)=\max_{x\in K}d_Y(f(x),g(x)).
$$

由于 $K$ 紧，最大值存在。又因为

$$
d(f_n,f)\to 0 \Longleftrightarrow f_n \text{ 在 } K \text{ 上一致收敛于 } f,
$$

由 §3 定理2与一致收敛柯西准则可知，$C(K,Y)$ 在该度量下是完备的。

在度量空间中，相对列紧子集是指从其任意序列中能选出柯西列；若原空间完备，则该柯西列收敛。因此阿尔采拉－阿斯柯利定理给出了 $C(K,Y)$ 中相对列紧子集的完整描述：连续函数族 $\mathfrak{F}\subset C(K,Y)$ 相对列紧，当且仅当它完全有界且等度连续。

教材中的边界示例：

- 函数族 $\{x^n:n\in\mathbb{N}\}$ 在 $[0,1]$ 上不等度连续，但在任何 $[0,q]$，$0<q<1$，上等度连续。
- 函数族 $\{\sin nx:n\in\mathbb{N}\}$ 在任何非退化区间 $[a,b]\subset\mathbb{R}$ 上都不等度连续。
- 若函数族 $\{f_\alpha:[a,b]\to\mathbb{R}\}$ 的导函数族 $\{f_\alpha'\}$ 一致有界，则由有限增量公式得

$$
|f_\alpha(x_2)-f_\alpha(x_1)|\le M|x_2-x_1|,
$$

所以 $\{f_\alpha\}$ 等度连续。

> [!caution] 条件与反例
> 所给文本的定理句中未重复“连续”一词，但必要性证明引用的是关于连续函数序列的引理1，且本节对象是连续函数空间 $C(K,Y)$，因此定理应在连续函数族中理解。若按任意函数族逐字理解，则单个有界但不连续的函数组成的函数族即可使必要性失效；此为补充观察，非教材原文给出的反例。
>
> 任务大纲中提到的“常微分方程 Peano 存在定理中的应用”未出现在本次提供的教材原文中，因此本卡片不展开该应用。所给材料亦未包含与本定理直接配套的自测题。

教材坐标：Zorich《数学分析 II》第4版，第十六章 §4，定理1；卡片槽位 `[卡片-ZORICH-THM-16-05]`。

<!-- textbook-provenance:start -->
## 教材出处与纸质笔记坐标

- 教材：V. A. Zorich, 《Mathematical Analysis II》 (卓里奇《数学分析》第二卷，第4版)；第十六章 一致收敛性，函数项级数与函数族的基本分析运算 / §4. 连续函数空间的紧子集和稠密子集
- PDF第360页；印刷页码：未核实 <!-- source:pdf:360 -->
- PDF第361页；印刷页码：未核实 <!-- source:pdf:361 -->
- PDF第362页；印刷页码：未核实 <!-- source:pdf:362 -->
- PDF第363页；印刷页码：未核实 <!-- source:pdf:363 -->
- 纸质活页：`[卡片-ZORICH-THM-16-05]`
- 教材导航：[[00_教材索引]]
<!-- textbook-provenance:end -->
