---
tags: [概念卡]
aliases: [多重线性斜对称形式与Grassmann外代数公理体系, Multilinear Alternating Forms and Grassmann Exterior Algebra, 外代数公理体系, 斜对称形式代数]
created: 2026-09-18
updated: 2026-09-18
---

# 多重线性斜对称形式与Grassmann外代数公理体系

> [!summary] 核心认知先验
> 在定义流形上微分形式的积分之前，需要先把线性空间上的多重线性形式与斜对称形式的结构梳理清楚。本节引入形式代数 $\mathfrak{F}=\bigoplus_k\mathfrak{F}^k$ 及由斜对称形式构成的子代数 $\Omega=\bigoplus_k\Omega^k$，后者正是 Grassmann 外代数。斜对称形式对应于“有向体积”的代数模型，外积则编码了行列式的反对称乘法。

## 定义、条件与直观

<!-- unit:u15_01_forms_algebra -->
### 形式代数：多重线性形式与张量积

设 $X$ 是实数域上的线性空间，$F^k: X^k \to \mathbb{R}$ 称为 $X$ 上的一个 **$k$-形式**（或多重线性形式），如果它对每个变量都是线性的。教材中不要求连续性，只有代数线性。

给定基底 $e_1,\dots,e_n$，任取 $x_1,\dots,x_k\in X$，其坐标分解为 $x_\alpha = x^{i_\alpha} e_{i_\alpha}$，则多重线性性给出坐标表示
$$F^k(x_1,\dots,x_k)=F^k(e_{i_1},\dots,e_{i_k})\,x^{i_1}\cdots x^{i_k}=a_{i_1\cdots i_k}x^{i_1}\cdots x^{i_k}, \tag{1}$$
其中系数 $a_{i_1\cdots i_k}=F^k(e_{i_1},\dots,e_{i_k})$。因此，在固定基底下，$k$-形式与一组数 $a_{i_1\cdots i_k}$ 一一对应。

若另一基底为 $\widetilde e_j=c_j^{i}e_i$，则同一形式对应的系数满足张量分量变换律
$$\widetilde a_{j_1\cdots j_k}=a_{i_1\cdots i_k} c_{j_1}^{i_1}\cdots c_{j_k}^{i_k}. \tag{2}$$

所有 $k$-形式构成线性空间 $\mathfrak{F}^k$，其加法与数乘由
$$(F_1^k+F_2^k)(x)=F_1^k(x)+F_2^k(x),\qquad (\lambda F^k)(x)=\lambda F^k(x) \tag{3,4}$$
定义。对 $k$-形式 $F^k$ 与 $l$-形式 $F^l$，定义张量积
$$(F^k\otimes F^l)(x_1,\dots,x_{k+l}):=F^k(x_1,\dots,x_k)\,F^l(x_{k+1},\dots,x_{k+l}), \tag{5}$$
它是 $k+l$-形式。张量积满足线性性与结合律：
$$(\lambda F^k)\otimes F^l=\lambda(F^k\otimes F^l), \qquad (F_1^k+F_2^k)\otimes F^l=F_1^k\otimes F^l+F_2^k\otimes F^l, \tag{6,7}$$
$$F^k\otimes(F_1^l+F_2^l)=F^k\otimes F_1^l+F^k\otimes F_2^l, \qquad (F^k\otimes F^l)\otimes F^m=F^k\otimes(F^l\otimes F^m). \tag{8,9}$$
于是全体形式之集 $\mathfrak{F}=\bigoplus_{k\ge 0}\mathfrak{F}^k$ 成为分次代数，其中 $\mathfrak{F}^0=\mathbb{R}$（约定 0-形式为数）。

**教材例 1（对偶基展开）**：设 $X^*$ 为 $X$ 的对偶空间，$e^1,\dots,e^n$ 是与 $e_1,\dots,e_n$ 对偶的基，即 $e^i(e_j)=\delta_j^i$。则 $e^i(x)=x^i$。利用(1)和(9)，任意 $k$-形式可唯一写为
$$F^k=a_{i_1\cdots i_k}\,e^{i_1}\otimes\cdots\otimes e^{i_k}. \tag{10}$$

<!-- unit:u15_01_skew_forms_wedge -->
### 斜对称形式代数与 Grassmann 外代数

称 $k$-形式 $\omega\in\mathfrak{F}^k$ 为 **斜对称形式**，若对任意两个不同指标 $i,j$ 交换两个变量后变号：
$$\omega(x_1,\dots,x_i,\dots,x_j,\dots,x_k)=-\omega(x_1,\dots,x_j,\dots,x_i,\dots,x_k).$$
全体斜对称 $k$-形式记为 $\Omega^k$，它是 $\mathfrak{F}^k$ 的线性子空间。

定义 **斜对称化算子** $A:\mathfrak{F}^k\to\Omega^k$ 为
$$A F^k(x_1,\dots,x_k):=\frac{1}{k!} F^k(x_{i_1},\dots,x_{i_k})\,\delta_{1\cdots k}^{i_1\cdots i_k}, \tag{11}$$
其中广义 Kronecker 符号 $\delta_{1\cdots k}^{i_1\cdots i_k}$ 在 $(i_1,\dots,i_k)$ 为 $(1,\dots,k)$ 的偶排列时取 $1$，奇排列时取 $-1$，其余情况取 $0$。

显然，若 $F^k$ 本身斜对称，则 $A F^k=F^k$，且 $A(A F^k)=A F^k$，所以 $A$ 是幂等线性算子，并把 $\mathfrak{F}^k$ 映满 $\Omega^k$。

对斜对称形式 $\omega^k\in\Omega^k$、$\omega^l\in\Omega^l$，定义 **外积（楔积）** 为
$$\omega^k\wedge\omega^l:=\frac{(k+l)!}{k!\,l!}\,A(\omega^k\otimes\omega^l), \tag{15}$$
它仍是 $k+l$-次斜对称形式。

## 性质与教材例子

### 形式代数的性质与例子

张量积的线性性与结合律已由(6)–(9)给出，证明是直接按定义逐点验证。这些性质使 $\mathfrak{F}$ 成为分次代数。

教材在例1中展示了对偶基 $e^i$ 的重要性：$e^i$ 可以看作坐标函数，因而 $e^{i_1}\otimes\cdots\otimes e^{i_k}$ 构成 $\mathfrak{F}^k$ 的基，任意 $F^k$ 有坐标表示(10)。

### 斜对称形式与外代数的性质及证明

1. **斜对称化算子的线性性**：由定义直接得
$$A(F_1^k+F_2^k)=A F_1^k+A F_2^k,\qquad A(\lambda F^k)=\lambda A F^k. \tag{12,13}$$

2. **例2：斜对称化对偶基张量积得到行列式**。
由(10)和(12),(13)，
$$A F^k=a_{i_1\cdots i_k}\,A(e^{i_1}\otimes\cdots\otimes e^{i_k}).$$
而由(11)，并注意 $e^i(x)=x^i$，可得
$$A(e^{j_1}\otimes\cdots\otimes e^{j_k})(x_1,\dots,x_k)=\frac{1}{k!} \begin{vmatrix} x_1^{j_1} & \cdots & x_1^{j_k}\\ \vdots & & \vdots\\ x_k^{j_1} & \cdots & x_k^{j_k}\end{vmatrix}. \tag{14}$$
因此 $A(e^{j_1}\otimes\cdots\otimes e^{j_k})$ 就是这组 1-形式对应的行列式除以 $k!$。

3. **例3：两个 1-形式的外积**。由(15)和(14)，
$$e^{i_1}\wedge e^{i_2}(x_1,x_2)=\frac{2!}{1!\,1!}A(e^{i_1}\otimes e^{i_2})(x_1,x_2)=\begin{vmatrix} x_1^{i_1} & x_1^{i_2}\\ x_2^{i_1} & x_2^{i_2}\end{vmatrix}. \tag{16}$$

4. **结合律**。教材通过直接计算证明了对三个 1-形式有
$$e^{i_1}\wedge(e^{i_2}\wedge e^{i_3})=(e^{i_1}\wedge e^{i_2})\wedge e^{i_3}. \tag{17}$$
将行列式按行展开并归纳，得到对任意 $k$ 个 1-形式，
$$e^{i_1}\wedge\cdots\wedge e^{i_k}(x_1,\dots,x_k)=\det\!\bigl(e^{i_\alpha}(x_\beta)\bigr)_{\alpha,\beta=1}^k. \tag{18}$$
且该公式对任意 1-形式（不必是对偶基）都成立。

5. **外积的线性性、反交换律与结合律**。利用张量积性质(6)–(9)和 $A$ 的线性性，推出
$$(\omega_1^k+\omega_2^k)\wedge\omega^l=\omega_1^k\wedge\omega^l+\omega_2^k\wedge\omega^l,\qquad (\lambda\omega^k)\wedge\omega^l=\lambda(\omega^k\wedge\omega^l). \tag{19,20}$$
为了证明
$$\omega^k\wedge\omega^l=(-1)^{kl}\,\omega^l\wedge\omega^k, \tag{21}$$
及
$$(\omega^k\wedge\omega^l)\wedge\omega^m=\omega^k\wedge(\omega^l\wedge\omega^m), \tag{22}$$
教材指出：由(19),(20)，只需对形如 $e^{i_1}\wedge\cdots\wedge e^{i_k}$ 的基形式验证；结合律由(17)的归纳推广得到，反交换律则由行列式交换两列变号的性质并利用(18)得到。

6. **外代数的基与维数**。任意斜对称形式 $\omega\in\Omega^k$ 可写为
$$\omega=A\omega=a_{i_1\cdots i_k}A(e^{i_1}\otimes\cdots\otimes e^{i_k})=\frac{1}{k!}a_{i_1\cdots i_k}\,e^{i_1}\wedge\cdots\wedge e^{i_k}.$$
由于斜对称性，同一组指标的不同排列对应的楔积相等或仅差符号，最终可合并为严格递增指标，故
$$\omega=\sum_{1\leqslant i_1<\cdots<i_k\leqslant n} a_{i_1\cdots i_k}\,e^{i_1}\wedge\cdots\wedge e^{i_k}. \tag{23}$$
因此 $\Omega^k$ 的一组基为
$$\{e^{i_1}\wedge\cdots\wedge e^{i_k}:1\le i_1<\cdots<i_k\le n\},$$
维数为 $\binom{n}{k}=\dim\Omega^k$。

全体斜对称形式集合 $\Omega=\bigoplus_{k=0}^{\dim X}\Omega^k$ 关于线性运算和外积构成分次代数，即 **Grassmann 外代数**。当 $k>\dim X$ 时 $\Omega^k=\{0\}$，因为任意 $k$ 个向量在 $n$ 维空间中线性相关，或者从(23)看出没有严格递增的 $k$ 元组。

> [!warning] 易混概念与适用边界
> - **张量积与外积**：$\mathfrak{F}^k$ 上的张量积把 $k$-形式与 $l$-形式变为 $k+l$-形式，但不保持斜对称性；$\Omega$ 上的外积是斜对称化后的张量积，并带有组合因子 $\frac{(k+l)!}{k!\,l!}$，使得 $e^{i_1}\wedge\cdots\wedge e^{i_k}$ 直接对应行列式，无 $\frac1{k!}$ 瑕疵。
> - **斜对称化算子不是单射**：$A$ 把任意形式投影到斜对称部分，许多非斜对称形式可能被映为零（例如变量重复的结构）。
> - **反交换律中的符号**：$\omega^k\wedge\omega^l=(-1)^{kl}\omega^l\wedge\omega^k$，指数是 $k l$ 而不是 $k+l$ 或别的。
> - **基底表示中系数的重排约定**：教材最终采用严格递增指标求和(23)。若使用所有指标求和，系数需带上广义 Kronecker 符号并除以 $k!$；两者可通过重排等价。
> - **代数范围**：本节中的“形式”是纯代数多重线性函数，未赋予连续性或光滑性；在后面流形上的微分形式中，系数将变为函数，且考虑可微性。

关联本节笔记；可核实的教材坐标和纸质槽位由工具追加。

<!-- textbook-provenance:start -->
## 教材出处与纸质笔记坐标

- 教材：V. A. Zorich, 《Mathematical Analysis II》 (卓里奇《数学分析》第二卷，第4版)；第十五章 流形上微分形式的积分 / §1. 线性代数准备知识
- PDF第288页；印刷页码：未核实 <!-- source:pdf:288 -->
- PDF第289页；印刷页码：未核实 <!-- source:pdf:289 -->
- PDF第290页；印刷页码：未核实 <!-- source:pdf:290 -->
- PDF第291页；印刷页码：未核实 <!-- source:pdf:291 -->
- PDF第292页；印刷页码：未核实 <!-- source:pdf:292 -->
- 纸质活页：`[卡片-ZORICH-CON-15-01]`
- 教材导航：[[00_教材索引]]
<!-- textbook-provenance:end -->
