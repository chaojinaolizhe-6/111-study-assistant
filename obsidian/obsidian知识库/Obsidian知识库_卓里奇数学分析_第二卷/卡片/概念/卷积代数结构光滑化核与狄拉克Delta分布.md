---
tags: [概念卡]
aliases:
  - 卷积
  - 光滑化核
  - 柔化子
  - 狄拉克δ分布
  - Convolution
  - Mollifier
  - Dirac delta distribution
  - Approximate identity
created: 2026-09-18
updated: 2026-09-18
---

# 卷积代数结构、光滑化核与狄拉克δ分布

> [!summary] 核心认知先验
> 教材从“仪器接受输入信号 $f$ 并输出信号 $\tilde f=Af$”这一物理问题出发，证明对线性、保位移的仪器，其作用完全由脉冲响应 $E$ 决定，并且恰好是卷积 $\tilde f=f*E$。这使卷积成为一类线性时不变系统的统一表示。随后教材把“理想单位脉冲”狄拉克 $\delta$ 定义为 $\delta$ 型函数族的极限作用，并用卷积给出光滑化逼近与魏尔斯特拉斯多项式逼近定理。

<!-- unit:u17_04_convolution -->

## 定义、条件与直观

### 物理问题：线性平移不变系统与脉冲响应

设 $A$ 是定义在 $\mathbb R$ 上的实（或复）值函数空间中的线性算子，并在同一空间中取值。用 $T_{t_0}$ 表示位移算子：

$$
(T_{t_0}f)(t):=f(t-t_0).
$$

**定义 1（位移不变算子）**  
如果对算子 $A$ 定义域中的任何函数 $f$，都有

$$
A(T_{t_0}f)=T_{t_0}(Af),
$$

即 $A\circ T_{t_0}=T_{t_0}\circ A$，则称 $A$ 是**位移不变算子**，或**保位移算子**。

若 $t$ 表示时间，则 $A\circ T_{t_0}=T_{t_0}\circ A$ 解释为：仪器 $A$ 的性质不随时间变化，对 $f(t)$ 与 $f(t-t_0)$ 的响应只相差时间位移 $t_0$。

**定义 2（脉冲响应函数）**  
仪器 $A$ 作用在单位脉冲 $\delta$ 上的响应 $E(t)$ 称为**仪器装置函数**（光学）或**脉冲响应函数**（电工学、控制论）。教材中采用较简短的术语“脉冲响应函数”。

教材先用两个图像中画出的阶梯函数 $\delta_\alpha(t)$ 来模拟脉冲，并保持脉冲总能量为 $1$，随着脉冲长度 $\alpha$ 不断减小，模拟越来越精确。也可以利用光滑函数 $f_\alpha$ 模拟脉冲，满足：

$$
f_\alpha\ge 0,\qquad \int_{\mathbb R} f_\alpha(t)\,dt=1,
$$

且对 $t=0$ 的任意邻域 $U(0)$，当 $\alpha\to0$ 时，

$$
\int_{U(0)} f_\alpha(t)\,dt\to1.
$$

图 100 表示阶梯函数模拟脉冲，图 101 表示光滑函数模拟脉冲。二者都以总能量 $1$ 向 $0$ 点集中。

理想脉冲 $\delta$ 下的响应 $E(t)$ 定义为

$$
A\delta:=E=\lim_{n\to\infty} A\Delta_n,
$$

其中 $\Delta_n(t):=\delta_{1/n}(t)$ 是模拟脉冲的阶梯函数序列。

设输入信号为 $f$，用分段常值函数

$$
l_h(t)=\sum_i f(\tau_i)\delta_h(t-\tau_i)h
$$

逼近 $f$。当 $h\to0$ 时有 $l_h\to f$，因此应该也有 $A l_h\to Af=\tilde f$。若 $A$ 线性且保位移，则

$$
\tilde l_h(t)=\sum_i f(\tau_i)E_h(t-\tau_i)h,
$$

其中 $E_h=A\delta_h$。令 $h\to0$，形式上得到

$$
\tilde f(t)=\int_{\mathbb R} f(\tau)E(t-\tau)\,d\tau.
\tag{1}
$$

公式 (1) 完全由输入信号 $f$ 与仪器脉冲响应 $E$ 确定。从数学观点看，仪器 $A$ 和积分 (1) 是同一个对象。

### 卷积的定义

**定义 3（卷积）**  
由关系式

$$
(u*v)(x):=\int_{\mathbb R} u(y)v(x-y)\,dy
\tag{2}
$$

（假定对一切 $x\in\mathbb R$，式中的反常积分存在）确定的函数 $u*v:\mathbb R\to\mathbb C$ 称为函数 $u:\mathbb R\to\mathbb C$ 与 $v:\mathbb R\to\mathbb C$ 的**卷积**。

于是，公式 (1) 断言：保位移线性仪器 $A$ 对输入 $f$ 的响应是

$$
Af = f*E.
$$

### 记号：局部可积、支集、光滑函数类

- **局部可积**：$f:G\to\mathbb C$ 定义在开集 $G\subset\mathbb R$ 上。若每一点 $x\in G$ 都有邻域 $U(x)\subset G$，使 $f|_{U(x)}$ 在 $U(x)$ 中可积，则称 $f$ 在 $G$ 上局部可积。当 $G=\mathbb R$ 时，这等价于对任何区间 $[a,b]$，$f|_{[a,b]}\in\mathcal R[a,b]$。
- **支集**：集合 $\{x\in G\mid f(x)\ne 0\}$ 在 $G$ 中的闭包称为 $f$ 的支集，记作 $\operatorname{supp} f$。
- **紧支集函数**：若 $\operatorname{supp} f$ 是 $G$ 中的紧集，则称 $f$ 在 $G$ 中具有紧支集。
- **光滑函数类**：$C^{(m)}(G)$ 表示在 $G$ 中具有直到 $m$ 阶（$0\le m\le\infty$）连续导数的函数 $f:G\to\mathbb C$ 组成的集合；其中具有紧支集的函数构成的子集记作 $C_0^{(m)}(G)$。当 $G=\mathbb R$ 时，简记作 $C^{(m)}$ 与 $C_0^{(m)}$。

## 性质与教材例子

### 1. 卷积的存在性充分条件

**命题 1**  
以下三个条件中的每一个，都是局部可积函数 $u:\mathbb R\to\mathbb C$ 与 $v:\mathbb R\to\mathbb C$ 的卷积 $u*v$ 存在的充分条件：

1. 函数 $|u|^2$ 与 $|v|^2$ 在 $\mathbb R$ 上可积；
2. 函数 $|u|,|v|$ 之一在 $\mathbb R$ 上可积，而另一个在 $\mathbb R$ 上有界；
3. 函数 $u,v$ 之一具有紧支集。

**证明要点。**

1. 由柯西–布尼雅可夫斯基不等式，

$$
\int_{\mathbb R}|u(y)v(x-y)|\,dy
\le
\left(\int_{\mathbb R}|u|^2(y)\,dy\right)^{1/2}
\left(\int_{\mathbb R}|v|^2(x-y)\,dy\right)^{1/2}.
$$

而

$$
\int_{-\infty}^{\infty}|v|^2(x-y)\,dy
=
\int_{-\infty}^{\infty}|v|^2(y)\,dy,
$$

故积分收敛。

2. 若 $|u|$ 在 $\mathbb R$ 上可积且 $|v|\le M$，则

$$
\int_{\mathbb R}|u(y)v(x-y)|\,dy
\le
M\int_{\mathbb R}|u|(y)\,dy<+\infty.
$$

3. 设 $\operatorname{supp} u\subset[a,b]\subset\mathbb R$，则

$$
\int_{\mathbb R}u(y)v(x-y)\,dy
=
\int_a^b u(y)v(x-y)\,dy.
$$

因为 $u,v$ 局部可积，最后积分对任何 $x\in\mathbb R$ 都存在。当 $v$ 具有紧支集时，利用变量替换 $x-y=z$ 可化为已分析过的情况。

### 2. 对称性（交换律）

**命题 2**  
如果卷积 $u*v$ 存在，那么卷积 $v*u$ 也存在，并且

$$
u*v=v*u.
\tag{3}
$$

证明只需在积分 (2) 中作变量替换 $x-y=z$：

$$
u*v(x):=\int_{-\infty}^{\infty}u(y)v(x-y)\,dy
=\int_{-\infty}^{\infty}v(z)u(x-z)\,dz
=:v*u(x).
$$

> 教材给出的代数运算规律明确包括对称性。截取文本中未列出结合律；因此本文不把结合律当作本节教材定理。

### 3. 保位移性

设 $T_{x_0}$ 是位移算子，即 $(T_{x_0}f)(x)=f(x-x_0)$。

**命题 3**  
如果函数 $u$ 与 $v$ 的卷积 $u*v$ 存在，则

$$
T_{x_0}(u*v)
=
T_{x_0}u*v
=
u*T_{x_0}v.
\tag{4}
$$

第一个等式的正式证明：

$$
\begin{aligned}
(T_{x_0}(u*v))(x)
&=(u*v)(x-x_0)
=\int_{-\infty}^{\infty}u(y)v(x-x_0-y)\,dy\\
&=\int_{-\infty}^{\infty}u(y-x_0)v(x-y)\,dy\\
&=\int_{-\infty}^{\infty}(T_{x_0}u)(y)v(x-y)\,dy
=((T_{x_0}u)*v)(x).
\end{aligned}
$$

第二个等式由卷积对称性得。公式 (4) 表明卷积算子与位移算子交换。

### 4. 卷积的微分法与光滑度提升

卷积是含参变量积分，其微分可按含参变量积分微分法进行。特别地，若 $u$ 连续、$v$ 光滑，且二者之一具紧支集，则卷积满足连续可微条件。一般地：

**命题 4**  
如果 $u$ 是局部可积函数，$v$ 是具紧支集函数类 $C_0^{(m)}$（$0\le m\le+\infty$）中的函数，那么

$$
(u*v)\in C^{(m)},
$$

且

$$
D^k(u*v)=u*(D^k v).
\tag{5}
$$

当 $u$ 连续时，限定参变量在任何有限区间上变化，则积分 (2) 化为在某个不依赖于 $x$ 的有限区间上的积分，可按古典莱布尼茨法则关于参变量微分；一般情形需利用 §1 练习 6 的考察。

**注 1**  
由于卷积可交换（公式 (3)），如果把 $u$ 与 $v$ 的位置交换但保持公式 (5) 左端不变，命题 4 仍有效。公式 (5) 说明卷积与微分算子交换，类似于它与位移算子交换；但与公式 (4) 不同，公式 (5) 右端的 $u$ 与 $v$ 一般不可交换位置，因为 $u$ 可能没有相应导数。因此命题 4 给出的是卷积可微性的充分条件，不是必要条件。

**例 1**  
设 $f$ 是局部可积函数，$\delta_\alpha$ 是图 100 所示的“阶梯函数”。这时

$$
(f*\delta_\alpha)(x)
=
\int_{-\infty}^{\infty}f(y)\delta_\alpha(x-y)\,dy
=
\frac1\alpha\int_{x-\alpha}^{x}f(y)\,dy.
\tag{6}
$$

因此卷积有积分平均作用：即使 $f$ 不光滑，$f*\delta_\alpha$ 也可微。教材由此指出，由卷积的磨光效应会产生新的机会，进而引入 $\delta$ 型函数族。

<!-- unit:u17_04_delta_families -->

## δ 型函数族、光滑化逼近与魏尔斯特拉斯定理

### 1. δ 函数作为卷积的单位元

由例 1 可知，若 $f$ 在点 $x$ 连续，则当 $\alpha\to0$ 时，

$$
(f*\delta_\alpha)(x)\to f(x).
$$

遵照第 1 段关于 $\delta$ 函数概念的启发性想法，教材把这个关系写成极限等式：

$$
(f*\delta)(x)=f(x).
\tag{7}
$$

这个等式表明：关于卷积算子，$\delta$ 函数可解释为单位（中立）元素。只有当某个收敛于 $\delta$ 函数的函数族具有和 $\delta_\alpha$ 同样性质时，等式 (7) 才有清晰意义。

### 2. δ 型函数族的精确定义

**定义 4（δ 型函数族、逼近单位）**  
依赖于参变量 $\alpha\in A$ 的函数族 $\{\Delta_\alpha:\mathbb R\to\mathbb R,\ \alpha\in A\}$ 称为 $A$ 中关于基底 $\mathcal B$ 的 **δ 型函数族**，或**逼近单位**，如果满足：

1. 所有函数非负：$\Delta_\alpha(x)\ge0$；
2. 对任意 $\Delta_\alpha$，有 $\displaystyle\int_{\mathbb R}\Delta_\alpha(x)\,dx=1$；
3. 对点 $0\in\mathbb R$ 的任一邻域 $U$，有

$$
\lim_{\mathcal B}\int_U \Delta_\alpha(x)\,dx=1.
$$

考虑到前两个条件，条件 3 显然与

$$
\lim_{\mathcal B}\int_{\mathbb R\setminus U}\Delta_\alpha(x)\,dx=0
$$

等价。

**例 2（标准尺度化构造）**  
设 $\varphi:\mathbb R\to\mathbb R$ 是任意非负紧支可积函数，且

$$
\int_{\mathbb R}\varphi(x)\,dx=1.
$$

对 $\alpha>0$ 构造函数

$$
\Delta_\alpha(x):=\frac1\alpha\varphi\!\left(\frac x\alpha\right).
$$

当 $\alpha\to+0$ 时，这些函数构成逼近单位。

**例 3（多项式型 δ 序列）**  
考虑

$$
\Delta_n(x)=
\begin{cases}
\dfrac{(1-x^2)^n}{\displaystyle\int_{|x|<1}(1-x^2)^n\,dx}, & |x|\le1,\\[12pt]
0, & |x|>1.
\end{cases}
$$

为验证它是 δ 型序列，只需验证条件 3。对任意 $\varepsilon\in]0,1]$，

$$
0\le
\int_\varepsilon^1(1-x^2)^n\,dx
\le
\int_\varepsilon^1(1-\varepsilon^2)^n\,dx
=
(1-\varepsilon^2)^n(1-\varepsilon)\to0
\qquad(n\to\infty).
$$

同时

$$
\int_0^1(1-x^2)^n\,dx
>
\int_0^1(1-x)^n\,dx
=
\frac1{n+1}.
$$

由此推出条件 3 成立。

**例 4（三角型 δ 序列）**  
设

$$
\Delta_n(x)=
\begin{cases}
\cos^{2n}x\Big/\displaystyle\int_{-\pi/2}^{\pi/2}\cos^{2n}x\,dx, & |x|\le\pi/2,\\[10pt]
0, & |x|>\pi/2.
\end{cases}
$$

验证中用到

$$
\int_0^{\pi/2}\cos^{2n}x\,dx
=
\frac12 B\!\left(n+\frac12,\frac12\right)
=
\frac{\Gamma(n+\frac12)\Gamma(\frac12)}{2\Gamma(n+1)}
>
\frac{\Gamma(\frac12)}{2n}.
$$

另一方面，对 $\varepsilon\in]0,\pi/2[$，

$$
\int_\varepsilon^{\pi/2}\cos^{2n}x\,dx
\le
\int_\varepsilon^{\pi/2}\cos^{2n}\varepsilon\,dx
<
\frac\pi2(\cos\varepsilon)^{2n}.
$$

比较两个不等式，得

$$
\int_\varepsilon^{\pi/2}\Delta_n(x)\,dx\to0
\qquad(n\to\infty),
$$

因而满足 δ 型函数族条件 3。

### 3. 一致连续与 δ 型逼近定理

**定义 5（集合上的一致连续）**  
给定 $f:G\to\mathbb C$ 与 $E\subset G$。若对任意 $\varepsilon>0$，都存在 $\rho>0$，使得对任何 $x\in E$ 以及 $x$ 在 $G$ 中的 $\rho$ 邻域 $U_G^\rho(x)$ 内任何点 $y$，都有

$$
|f(x)-f(y)|<\varepsilon,
$$

则称 $f$ 在集合 $E$ 上一致连续。当 $E=G$ 时，这就是通常的一致连续。

**命题 5**  
设 $f:\mathbb R\to\mathbb C$ 是有界函数，$\{\Delta_\alpha,\alpha\in A\}$ 当 $\alpha\to\omega$ 时是 δ 型函数族。如果对每个 $\alpha\in A$，卷积 $f*\Delta_\alpha$ 存在，且 $f$ 在集合 $E\subset\mathbb R$ 上一致连续，则在 $E$ 上

$$
(f*\Delta_\alpha)(x)\Rightarrow f(x)
\qquad(\alpha\to\omega).
$$

即函数族 $f*\Delta_\alpha$ 在集合 $E$ 上一致收敛到 $f$。若 $E$ 只含一个点 $x$，则条件退化为 $f$ 在点 $x$ 连续，结论退化为

$$
(f*\Delta_\alpha)(x)\to f(x)
\qquad(\alpha\to\omega).
$$

**证明。**  
设在 $\mathbb R$ 上 $|f(x)|\le M$。任给 $\varepsilon>0$，按定义 5 选取 $\rho>0$，并令 $U(0)$ 为 $0$ 点在 $\mathbb R$ 中的 $\rho$ 邻域。利用卷积的对称性，对所有 $x\in E$ 一致地有

$$
\begin{aligned}
|(f*\Delta_\alpha)(x)-f(x)|
&=
\left|\int_{\mathbb R} f(x-y)\Delta_\alpha(y)\,dy-f(x)\right|\\
&=
\left|\int_{\mathbb R}\bigl(f(x-y)-f(x)\bigr)\Delta_\alpha(y)\,dy\right|\\
&\le
\int_{U(0)}
|f(x-y)-f(x)|\Delta_\alpha(y)\,dy
+
\int_{\mathbb R\setminus U(0)}
|f(x-y)-f(x)|\Delta_\alpha(y)\,dy\\
&<
\varepsilon\int_{U(0)}\Delta_\alpha(y)\,dy
+
2M\int_{\mathbb R\setminus U(0)}\Delta_\alpha(y)\,dy\\
&\le
\varepsilon
+
2M\int_{\mathbb R\setminus U(0)}\Delta_\alpha(y)\,dy.
\end{aligned}
$$

当 $\alpha\to\omega$ 时，最后一项趋于零，故从某个时刻起，对一切 $x\in E$ 有

$$
|(f*\Delta_\alpha)(x)-f(x)|<2\varepsilon.
$$

命题 5 证毕。

### 4. 光滑化核（mollifier）与一致逼近

**推论 1**  
任何一个在 $\mathbb R$ 上连续且具紧支集的函数，都能用无限次可微且具紧支集的函数一致逼近。

**证明与光滑化核构造。**  
设

$$
\varphi(x)=
\begin{cases}
k\cdot\exp\!\left(-\dfrac1{1-x^2}\right), & |x|<1,\\[8pt]
0, & |x|\ge1,
\end{cases}
$$

其中系数 $k$ 取得使

$$
\int_{\mathbb R}\varphi(x)\,dx=1.
$$

函数 $\varphi$ 是无限次可微且具紧支集的函数。按例 2 构造

$$
\Delta_\alpha(x)=\frac1\alpha\varphi\!\left(\frac x\alpha\right)
\qquad(\alpha\to+0),
$$

这是一族无限可微的 δ 型函数。若 $f\in C_0$，则显然 $f*\Delta_\alpha\in C_0$；又由命题 4，

$$
f*\Delta_\alpha\in C_0^{(\infty)}.
$$

最后，由命题 5，当 $\alpha\to+0$ 时，在 $\mathbb R$ 上

$$
f*\Delta_\alpha\Rightarrow f.
$$

这里构造的 $\Delta_\alpha$ 就是光滑化核，又称“磨光核”。教材以“磨光效应”说明其作用。现代术语中这族核通常称为 **mollifier**（补充讲解：该英文名未在教材本段逐字出现）。

**注 2**  
若 $f\in C_0^{(m)}$，则对任何 $n\in\{0,1,\ldots,m\}$，当 $\alpha\to+0$ 时，在 $\mathbb R$ 上有

$$
(f*\Delta_\alpha)^{(n)}\to f^{(n)}.
$$

事实上，

$$
(f*\Delta_\alpha)^{(n)}=f^{(n)}*\Delta_\alpha,
$$

利用命题 4 与注 1 便得到结论，再引用推论 1。

### 5. 魏尔斯特拉斯逼近定理

**推论 2（魏尔斯特拉斯逼近定理）**  
每一个在闭区间上连续的函数，在该区间上能用代数多项式一致逼近。

**证明。**  
通过线性变换，多项式仍变为多项式，连续性与一致逼近性也保持，因此只需在任一方便区间 $[a,b]\subset\mathbb R$ 上证明。设

$$
0<a<b<1,
\qquad
\rho=\min\{a,1-b\}.
$$

将给定函数 $f\in C[a,b]$ 延拓为 $\mathbb R$ 上的连续函数 $F$：当 $x\in\mathbb R\setminus]0,1[$ 时令 $F(x)=0$，在区间 $[0,a]$ 与 $[b,1]$ 上分别将 $0$ 与 $f(a)$、$f(b)$ 与 $0$ 线性连接。

取例 3 的 δ 型函数序列 $\Delta_n$。由命题 5，在 $[a,b]$ 上，当 $n\to\infty$ 时，

$$
F*\Delta_n\Rightarrow f=F|_{[a,b]}.
$$

当 $x\in[a,b]\subset[0,1]$ 时，

$$
\begin{aligned}
F*\Delta_n(x)
&=\int_{-\infty}^{\infty}F(y)\Delta_n(x-y)\,dy\\
&=\int_0^1 F(y)\Delta_n(x-y)\,dy\\
&=\int_0^1 F(y)p_n\bigl(1-(x-y)^2\bigr)^n\,dy\\
&=\int_0^1 F(y)\left(\sum_{k=0}^{2n}a_k(y)x^k\right)dy\\
&=\sum_{k=0}^{2n}\left(\int_0^1 F(y)a_k(y)\,dy\right)x^k,
\end{aligned}
$$

其中 $p_n$ 是归一化常数。最后一个表达式是 $2n$ 次多项式 $P_{2n}(x)$。因此当 $n\to\infty$ 时，在 $[a,b]$ 上

$$
P_{2n}\Rightarrow f.
$$

**注 3**  
对上边的论证稍作修改，可把区间 $[a,b]$ 换成 $\mathbb R$ 中任意紧集，魏尔斯特拉斯定理仍成立。

**注 4**  
对 $\mathbb R$ 中任何开集 $G$ 和任何 $f\in C^{(m)}(G)$，存在多项式序列 $\{P_k\}$，使对每个 $n\in\{0,1,\ldots,m\}$，在任一紧集 $K\subset G$ 上，当 $k\to\infty$ 时，

$$
P_k^{(n)}\Rightarrow f^{(n)}.
$$

若 $G$ 有界且 $f\in C^{(m)}(\overline G)$，则在 $\overline G$ 上也有

$$
P_k^{(n)}\Rightarrow f^{(n)}
\qquad(k\to\infty).
$$

**注 5**  
利用例 4 的三角型 δ 序列可证明：任何以 $2\pi$ 为周期的函数，可用形如

$$
T_n(x)=\sum_{k=0}^{n}
\bigl(a_k\cos kx+b_k\sin kx\bigr)
$$

的三角多项式一致逼近。

### 6. 非紧支 δ 型函数族及其应用

以上只使用了具紧支集的 δ 型函数族。教材强调，很多重要情形中的 δ 型函数族不是由具紧支集的函数构成的。

**例 5（泊松核与半平面 Dirichlet 问题）**  
函数族

$$
\Delta_y(x)=\frac1\pi\frac{y}{x^2+y^2}
\qquad(y\to+0)
$$

是在 $\mathbb R$ 上的 δ 型函数族。因为当 $y>0$ 时 $\Delta_y(x)>0$，并且

$$
\int_{-\infty}^{\infty}\Delta_y(x)\,dx
=
\frac1\pi\arctan\!\left(\frac xy\right)\bigg|_{-\infty}^{\infty}
=
1.
$$

对任何 $\rho>0$，当 $y\to+0$ 时，

$$
\int_{-\rho}^{\rho}\Delta_y(x)\,dx
=
\frac2\pi\arctan\!\left(\frac\rho y\right)
\to1.
$$

若 $f:\mathbb R\to\mathbb R$ 连续有界，则卷积 $f*\Delta_y$ 给出

$$
u(x,y)
=
\frac1\pi\int_{-\infty}^{\infty}
\frac{f(\xi)y}{(x-\xi)^2+y^2}\,d\xi.
\tag{8}
$$

称 (8) 为关于半平面 $y>0$ 的**泊松积分**。它在半平面

$$
\mathbb R_+^2=\{(x,y)\in\mathbb R^2\mid y>0\}
$$

上无穷次可微且有界。由积分号下求微分得

$$
\Delta u:=\frac{\partial^2u}{\partial x^2}
+\frac{\partial^2u}{\partial y^2}
=
f*
\left(\frac{\partial^2}{\partial x^2}
+\frac{\partial^2}{\partial y^2}\right)\Delta_y
=
0,
$$

即 $u$ 是调和函数。由命题 5，当 $y\to0$ 时 $u(x,y)\to f(x)$。于是泊松积分 (8) 解决了在半平面上构造有界调和函数并取给定边界值 $f$ 的问题。

**例 6（热核与热传导方程）**  
函数族

$$
\Delta_t(x)=\frac1{2\sqrt{\pi t}}
e^{-x^2/(4t)}
\qquad(t\to+0)
$$

在 $\mathbb R$ 上是 δ 型的。因为 $\Delta_t(x)>0$；由欧拉–泊松积分

$$
\int_{-\infty}^{\infty}e^{-v^2}\,dv=\sqrt\pi
$$

得

$$
\int_{-\infty}^{\infty}\Delta_t(x)\,dx=1.
$$

并且对任何 $\rho>0$，

$$
\int_{-\rho}^{\rho}
\frac1{2\sqrt{\pi t}}e^{-x^2/(4t)}\,dx
=
\frac1{\sqrt\pi}
\int_{-\rho/(2\sqrt t)}^{\rho/(2\sqrt t)}
e^{-v^2}\,dv
\to1
\qquad(t\to+0).
$$

若 $f$ 在 $\mathbb R$ 上有界连续，则卷积 $f*\Delta_t$ 给出

$$
u(x,t)
=
\frac1{2\sqrt{\pi t}}
\int_{-\infty}^{\infty}
f(\xi)e^{-(x-\xi)^2/(4t)}\,d\xi.
\tag{9}
$$

当 $t>0$ 时无穷次可微。由积分号下微分得到

$$
\frac{\partial u}{\partial t}
-\frac{\partial^2u}{\partial x^2}
=
f*
\left(\frac{\partial}{\partial t}
-\frac{\partial^2}{\partial x^2}\right)\Delta_t
=
0,
$$

即 $u$ 满足一维热传导方程。初始条件

$$
u(x,0)=f(x)
$$

应理解为由命题 5 给出的极限关系：当 $t\to+0$ 时，

$$
u(x,t)\to f(x).
$$

> [!warning] 易混概念与适用边界
> - $\Delta_\alpha$ 本身不是理想的 $\delta$ 函数，教材始终把 $\delta$ 理解为 δ 型函数族在基底 $\mathcal B$ 下的极限作用；只有当某族函数满足定义 4 时，才能写 $f*\delta=f$。现代分布语言中这是弱收敛 $\Delta_\alpha\rightharpoonup\delta$，但本节未展开广义函数的严格定义（补充讲解）。
> - 命题 4 给出的是卷积可微性的充分条件。$D^k(u*v)=u*D^kv$ 中不能无条件把 $D^k$ 移到 $u$；只有当 $u$ 也相应光滑时才可交换平滑一侧。
> - 教材本节明确给出卷积的对称性（交换律）、保位移性、微分法与光滑度提升；任务标题中的“结合律”未在提供的摘录中出现，故本文不将其作为本节定理。
> - 魏尔斯特拉斯逼近定理的证明依赖例 3 的紧支 δ 型序列；注 3–注 5 说明该论证可推广到任意紧集、导数逼近以及三角多项式逼近。

<!-- textbook-provenance:start -->
## 教材出处与纸质笔记坐标

- 教材：V. A. Zorich, 《Mathematical Analysis II》 (卓里奇《数学分析》第二卷，第4版)；第十七章 含参变量的积分 / §4. 函数的卷积和广义函数的初步知识
- PDF第403页；印刷页码：未核实 <!-- source:pdf:403 -->
- PDF第404页；印刷页码：未核实 <!-- source:pdf:404 -->
- PDF第405页；印刷页码：未核实 <!-- source:pdf:405 -->
- PDF第406页；印刷页码：未核实 <!-- source:pdf:406 -->
- PDF第407页；印刷页码：未核实 <!-- source:pdf:407 -->
- PDF第408页；印刷页码：未核实 <!-- source:pdf:408 -->
- PDF第409页；印刷页码：未核实 <!-- source:pdf:409 -->
- PDF第410页；印刷页码：未核实 <!-- source:pdf:410 -->
- PDF第411页；印刷页码：未核实 <!-- source:pdf:411 -->
- PDF第412页；印刷页码：未核实 <!-- source:pdf:412 -->
- 纸质活页：`[卡片-ZORICH-CON-17-02]`
- 教材导航：[[00_教材索引]]
<!-- textbook-provenance:end -->
