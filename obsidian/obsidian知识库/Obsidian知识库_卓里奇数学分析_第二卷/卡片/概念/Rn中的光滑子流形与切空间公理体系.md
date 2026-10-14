---
tags: [概念卡]
aliases:
  - "Rⁿ 中的光滑子流形与切空间公理体系"
  - "Smooth Submanifolds and Tangent Spaces"
  - "k维曲面"
  - "局部图册定义"
created: 2026-09-18
updated: 2026-09-18
---

# Rⁿ 中的光滑子流形与切空间公理体系

> [!summary] 核心认知先验
> 教材先以“局部同胚于 $\mathbb R^k$”定义拓扑曲面，再要求局部图光滑且处处秩 $k$，得到光滑曲面。其目的是确保局部参数化是正则嵌入，从而能定义切空间、法空间并做积分。正则局部参数化可扩张为全维数微分同胚，这是从参数定义过渡到隐式定义/切片定义的关键。

<!-- unit:u12_01_surface_def -->
## 定义、条件与直观

### 定义 1（$k$ 维曲面 / $k$ 维流形）

若集合 $S\subset\mathbb R^n$ 的每一点都有在 $S$ 内的邻域 $p$ 同胚于 $\mathbb R^k$，就说 $S$ 是 $\mathbb R^n$ 中维数为 $k$ 的曲面，即 $k$ 维曲面或 $k$ 维流形。

这里“在 $S$ 内的邻域”指 $U_S(x)=S\cap U(x)$，其中 $U(x)$ 是 $x$ 在 $\mathbb R^n$ 中的邻域；教材约定在不致混淆时简写为 $U$ 或 $U(x)$。$S$ 上带有从 $\mathbb R^n$ 诱导来的自然度量，因此可以谈论 $U$ 到 $\mathbb R^n$ 中的拓扑映射。

### 定义 2（图 / 局部图）

实现定义 1 中同胚的映射

$$
\varphi:\mathbb R^k\to U\subset S
$$

叫做曲面 $S$ 的**图**或**局部图**；$\mathbb R^k$ 是**参数域**，$U$ 是图在曲面 $S$ 上的**有效域**。点 $x=\varphi(t)\in U$ 对应参数 $t=(t^1,\dots,t^k)\in\mathbb R^k$，于是在 $U$ 内由局部图确定一个**曲线坐标**。

教材指出，把 $\mathbb R^k$ 换成与 $\mathbb R^k$ 同胚的任一拓扑空间，不会改变所描述的曲面对象。通常取 $\mathbb R^k$ 中的开方体 $I^k$ 或开球 $B^k$ 作为标准参数域。采用开方体时，图常写成

$$
\varphi:I^k\to U\subset S \tag{1}
$$

它局部地给出曲面 $S$ 的参数方程 $x=\varphi(t)$。此时 $k$ 维曲面本身可局部地看成“变了形的标准 $k$ 维区间 $I^k$”。

若整个曲面只用一张图就能表示出来，就称为**初等曲面**。例如连续函数 $f:I^k\to\mathbb R$ 在 $\mathbb R^{k+1}$ 内的图是初等曲面；但二维球面就不能只用一张图给出，其图册中至少要有两张图（参看本节末第 4 题）。

### 定义 3（图册）

设

$$
A(S):=\{\varphi_i:I_i^k\to U_i,\ i\in\mathbb N\}
$$

是曲面 $S$ 的一组局部图。若这些局部图的有效域全体覆盖整个曲面，即 $S=\bigcup_i U_i$，则称 $A(S)$ 为曲面 $S$ 的**图册**。同一曲面的两个图册的并仍是该曲面的图册。

### 光滑曲面：从切片定义到图册定义

若仅要求局部参数化是同胚，可能出现“同胚于二维球面、但其内部不同胚于球体”的怪异曲面，即所谓“带角的球面”（脚注指出这是亚历山大的例子）。为避免这类与分析实质无关的困难，第 8 章 §7 曾把 $\mathbb R^n$ 内的光滑 $k$ 维曲面定义为满足下列切片条件的集合 $S\subset\mathbb R^n$：

对每个点 $x_0\in S$，存在 $x_0$ 在 $\mathbb R^n$ 中的邻域 $U(x_0)$ 和微分同胚

$$
\psi:U(x_0)\to I^n=\{t\in\mathbb R^n\mid |t^i|<1,\ i=1,2,\dots,n\},
$$

并且

$$
U_S(x_0):=S\cap U(x_0),
$$

使得

$$
\psi(U_S(x_0))=I^k=I^n\cap\{t\in\mathbb R^n\mid t^{k+1}=\dots=t^n=0\}.
$$

显然这种意义下的光滑曲面也在定义 1 的意义下是曲面，因为映射

$$
x=\psi^{-1}(t^1,\dots,t^k,0,\dots,0)=\varphi(t^1,\dots,t^k)
$$

局部地将曲面参数化。反之，只有同胚条件时逆命题一般不成立；但当局部参数映射足够正则时，两种概念一致。

### 命题（正则局部参数化扩张为微分同胚）

若映射 $(1)$ 属于 $C^{(1)}(I^k,\mathbb R^n)$ 类，且在方体 $I^k$ 的每一点有最大秩 $k$，则存在 $\varepsilon>0$ 以及从 $n$ 维方体

$$
I_\varepsilon^n:=\{t\in\mathbb R^n\mid |t^i|<\varepsilon,\ i=1,\dots,n\}
$$

到 $\mathbb R^n$ 的微分同胚

$$
\varphi_\varepsilon:I_\varepsilon^n\to\mathbb R^n,
$$

使得

$$
\varphi|_{I^k\cap I_\varepsilon^n}
=
\varphi_\varepsilon|_{I^k\cap I_\varepsilon^n}.
$$

换句话说，在所给条件下，局部映射 $(1)$ 是 $n$ 维方体 $I_\varepsilon^n$ 的微分同胚在 $k$ 维方体 $I_\varepsilon^k:=I^k\cap I_\varepsilon^n$ 上的限制。

**证明要点**：为确定起见，设 $x=\varphi(t)$ 的前 $k$ 个坐标函数 $x^i=\varphi^i(t^1,\dots,t^k)$，$i=1,\dots,k$，已满足

$$
\det\left(\frac{\partial\varphi^i}{\partial t^j}\right)(0)\neq 0,\qquad i,j=1,\dots,k.
$$

根据隐函数定理，在 $(t_0,x_0)=(0,\varphi(0))$ 附近，关系式

$$
x^i=\varphi^i(t^1,\dots,t^k),\qquad i=1,\dots,n,
$$

与关系式

$$
t^j=f^j(x^1,\dots,x^k),\quad x^{k+\ell}=f^{k+\ell}(x^1,\dots,x^k),\qquad j=1,\dots,k,\ \ell=1,\dots,n-k,
$$

等价。于是映射

$$
\begin{cases}
t^j=f^j(x^1,\dots,x^k),\\
t^{k+\ell}=x^{k+\ell}-f^{k+\ell}(x^1,\dots,x^k)
\end{cases}
$$

是点 $x_0\in\mathbb R^n$ 的 $n$ 维邻域的微分同胚。取它的逆微分同胚在某个方体 $I_\varepsilon^n$ 上的限制作为 $\varphi_\varepsilon$ 即可。改变坐标尺度可使 $\varepsilon=1$，从而把 $I_\varepsilon^n$ 化为单位方体。

### 定义 4（$C^{(m)}$ 光滑曲面）

如果定义 1 所引入的 $\mathbb R^n$ 中的 $k$ 维曲面具有这样的图册，其局部图是光滑的 $C^{(m)}$ 类映射（$m\ge 1$），且在其定义域的每点的秩为 $k$，就称它为 $C^{(m)}$ 类光滑曲面。

教材特别强调：映射 $(1)$ 关于秩的条件很重要。例如由

$$
x^1=t^2,\qquad x^2=t^3
$$

给出的解析映射 $\mathbb R\ni t\mapsto(x^1,x^2)\in\mathbb R^2$ 在平面 $\mathbb R^2$ 内确定一条在点 $(0,0)$ 处有尖点的曲线；这条曲线不是 $\mathbb R^2$ 中的一维光滑曲面，因为光滑曲面应在每一点有切面（一维切面）。因此，**不要把 $C^{(m)}$ 类光滑道路与 $C^{(m)}$ 类光滑曲线混淆**。

教材还指出：定义 4 与第 8 章 §7 的切片定义一致；定义 4 的优越性在于它很容易提升成抽象流形的定义，而不必局限于 $\mathbb R^n$ 中。

## 性质与教材例子

### 例 1（隐式正则值给出光滑曲面）

设 $F^i\in C^{(m)}(\mathbb R^n,\mathbb R)$，$i=1,\dots,n-k$，是一组光滑函数，且方程组

$$
\begin{cases}
F^1(x^1,\dots,x^n)=0,\\
\cdots\cdots\cdots\\
F^{n-k}(x^1,\dots,x^n)=0
\end{cases}
\tag{2}
$$

在其解集 $S$ 的每一点处的秩为 $n-k$。则此方程组或者没有解，或者其解集 $S$ 在 $\mathbb R^n$ 中构成 $C^{(m)}$ 类 $k$ 维光滑曲面。

证明由隐函数定理直接推出：在任何点 $x_0\in S$ 的邻域内，不计变量标号的变化，方程组 $(2)$ 等价于

$$
\begin{cases}
x^{k+1}=f^{k+1}(x^1,\dots,x^k),\\
\cdots\cdots\cdots\\
x^n=f^n(x^1,\dots,x^k),
\end{cases}
$$

其中 $f^{k+\ell}\in C^{(m)}$。改写成

$$
x^1=t^1,\ \dots,\ x^k=t^k,\qquad
x^{k+\ell}=f^{k+\ell}(t^1,\dots,t^k),
$$

就得到 $x_0\in S$ 邻域内的参数方程；再作参数域变换即可化为标准局部图。

### 例 2（球面与圆）

在 $\mathbb R^n$ 中，方程

$$
(x^1)^2+\cdots+(x^n)^2=r^2\qquad(r>0)
\tag{3}
$$

给出的球面是 $\mathbb R^n$ 内的 $n-1$ 维光滑曲面，因为其解集非空，且在 $S$ 的任何点，方程左端的梯度不为零。

当 $n=2$ 时得到 $\mathbb R^2$ 内的圆。利用极坐标

$$
x^1=r\cos\theta,\qquad x^2=r\sin\theta
$$

可在任何形如 $\theta_0<\theta<\theta_0+2\pi$ 的区间上给出微分同胚参数化。为构成圆的图册，两张图（例如 $\theta_0=0$ 和 $\theta_0=-\pi$ 对应的两张图）就够了；但只用一张标准图 $(1)$ 不够，因为圆是紧的，而 $I^1=B^1$ 不是紧的，紧性是拓扑变换下的不变性质。

对于 $\mathbb R^3$ 中的二维球面，用 $\psi$ 表示向量 $(x^1,x^2,x^3)$ 与 $Ox^3$ 轴正向的夹角，$\varphi$ 表示向径在 $(x^1,x^2)$ 平面上的投影的极角，可得

$$
x^3=r\cos\psi,\quad
x^2=r\sin\psi\sin\varphi,\quad
x^1=r\sin\psi\cos\varphi.
$$

### 一般极坐标与雅可比

$\mathbb R^n$ 中的极坐标 $(r,\theta_1,\dots,\theta_{n-1})$ 由

$$
\begin{aligned}
x^1&=r\cos\theta_1,\\
x^2&=r\sin\theta_1\cos\theta_2,\\
&\vdots\\
x^{n-1}&=r\sin\theta_1\sin\theta_2\cdots\sin\theta_{n-2}\cos\theta_{n-1},\\
x^n&=r\sin\theta_1\sin\theta_2\cdots\sin\theta_{n-2}\sin\theta_{n-1}
\end{aligned}
\tag{4}
$$

引入。该变换的雅可比为

$$
J=r^{n-1}\sin^{n-2}\theta_1\sin^{n-3}\theta_2\cdots\sin\theta_{n-2}.
\tag{5}
$$

当 $0<\theta_i<\pi$，$i=1,\dots,n-2$，且 $r>0$ 时，$J\neq 0$。故对固定 $r>0$，$(\theta_1,\dots,\theta_{n-1})\mapsto(x^1,\dots,x^n)$ 是局部微分同胚；再借助球面关于正交变换群作用的齐性，可在球面任意点的邻域建立局部图。

### 例 3（柱面）

当 $k<n$ 时，柱面

$$
(x^1)^2+\cdots+(x^k)^2=r^2\qquad(r>0)
$$

是 $\mathbb R^n$ 内的 $n-1$ 维曲面。它是变量 $(x^1,\dots,x^k)$ 的平面内的 $k-1$ 维球面与变量 $(x^{k+1},\dots,x^n)$ 的 $n-k$ 维平面的直积。取 $k-1$ 维球面的极坐标 $\theta_1,\dots,\theta_{k-1}$ 作为前 $k-1$ 个参数，再令 $t^k,\dots,t^{n-1}$ 分别等于 $x^{k+1},\dots,x^n$，即可局部参数化。

### 例 4（旋转环面）

在 $\mathbb R^3$ 中取平面 $x=0$ 内一条不与 $Oz$ 轴相交的曲线，将其绕 $Oz$ 轴旋转，得到二维曲面。曲线的局部坐标（经线参数）与旋转角（纬线参数）构成局部坐标。

特别地，若该曲线是以 $(0,b,0)$ 为中心、半径为 $a$ 的圆，且 $0<a<b$，则得到二维环面（轮胎曲面，图 69），参数方程可写成

$$
\begin{cases}
x=(b+a\cos\psi)\cos\varphi,\\
y=(b+a\cos\psi)\sin\varphi,\\
z=a\cos\psi.
\end{cases}
$$

其中 $\psi$ 是子午圆上的角参数，$\varphi$ 是纬线上的角参数。

> [!note] 教材原文呈现与补充讲解
> 任务提供的 OCR 文本中第三式为 $z=a\cos\psi$；按旋转构造，子午圆应在 $(y,z)$ 平面内满足 $y=b+a\cos\psi$、$z=a\sin\psi$，故此处高度疑为 OCR 将 $\sin\psi$ 误识为 $\cos\psi$。补充说明，不作为教材原文引用。

图 70 表示：二维环面是两个圆（两个线段端点粘合）的直积，因此可由矩形把对边按对应点粘接得到。

### 例 5（带子粘合与默比乌斯带）

把柔软的矩形带子按图 71a 中箭头粘接，可得到环（图 71c）或柱面（图 71b）；从拓扑学观点看，它们同胚。若按图 72a 中箭头粘接，则得到 $\mathbb R^3$ 中的曲面，即默比乌斯带（图 72b）。脚注注明：默比乌斯（A. F. Möbius，1790—1868）是德国数学家与天文学家。

<!-- unit:u12_01_tangent_spaces -->
## 曲面的切空间与法空间

> [!warning] 原文边界声明
> 任务提供的第 165–166 页文本只包含极坐标、柱面、旋转环面、环面与默比乌斯带的例子，并未包含“切空间由曲线切向量生成”“切空间基底为坐标偏导数”“正交法空间”等正式定义或定理。全书可确认的线索只有：第 163 页脚注“关于切平面，参看第 8 章 §7”，以及第 161、163 页关于光滑曲面“在每一点有切面”的表述。因此以下内容作为**补充讲解**，不标注为 Zorich 本节的逐字定义编号。

### 补充讲解：速度曲线定义

给定 $C^{(m)}$ 光滑曲面 $S\subset\mathbb R^n$ 和点 $x_0\in S$。切空间可定义为

$$
T_{x_0}S
=
\{v\in\mathbb R^n\mid \exists\,\gamma:(-\delta,\delta)\to S,\ \gamma(0)=x_0,\ \gamma'(0)=v\}.
$$

即在 $S$ 中经过 $x_0$ 的光滑曲线在 $x_0$ 处的速度向量全体。

### 补充讲解：局部坐标基底导数生成

若 $\varphi:I^k\to U\subset S$ 是 $x_0=\varphi(0)$ 附近的正则局部参数化，则上述切空间等于参数偏导数张成的 $k$ 维线性子空间：

$$
T_{x_0}S
=
\operatorname{span}\big\{\partial_1\varphi(0),\dots,\partial_k\varphi(0)\big\}.
$$

其中 $\partial_j\varphi(0)$ 是映射 $\varphi$ 对第 $j$ 个参数的偏导数。等价性来自链式法则：对 $S$ 上曲线 $\gamma(\tau)=\varphi(t(\tau))$，

$$
\gamma'(0)=\sum_{j=1}^k \dot t^j(0)\,\partial_j\varphi(0);
$$

反过来，取 $t(\tau)=v_j\tau$ 即得坐标方向的速度向量。

### 补充讲解：正交法空间

把切空间在 $\mathbb R^n$ 中的正交补定义为法空间：

$$
N_{x_0}S
=
(T_{x_0}S)^\perp.
$$

若 $S$ 由余维 $n-k$ 的隐式方程 $F=(F^1,\dots,F^{n-k}):\mathbb R^n\to\mathbb R^{n-k}$ 在正则值条件下给出，则在 $x_0\in S$ 处

$$
T_{x_0}S=\ker dF(x_0),
\qquad
N_{x_0}S=\operatorname{span}\{\nabla F^1(x_0),\dots,\nabla F^{n-k}(x_0)\}.
$$

当法空间可连续选取单位法向量时，把单位法向量映到单位球面的映射就是高斯映射。这些内容与第 8 章 §7 的切片定义自然相容：切片参数化

$$
\varphi(t^1,\dots,t^k)
=
\psi^{-1}(t^1,\dots,t^k,0,\dots,0)
$$

的偏导数 $\partial_1\varphi(0),\dots,\partial_k\varphi(0)$ 给出切空间的标准基底。

> [!warning] 易混概念与适用边界
> - **光滑道路不等于光滑曲线**：$C^{(m)}$ 类光滑道路只要求参数映射光滑；光滑曲线还要求参数映射处处秩为 $1$。$x^1=t^2,x^2=t^3$ 是光滑道路，但在 $(0,0)$ 有尖点，不是光滑曲线。
> - **拓扑曲面与光滑曲面**：定义 1 是纯拓扑条件；定义 4 额外要求图册光滑且局部图处处秩 $k$。命题保证正则局部参数化可扩张为全维数微分同胚，因此定义 4 与第 8 章 §7 的切片定义一致。
> - **初等曲面与图册**：初等曲面只要求一张图；紧球面不能只用一张标准图，这是紧性的拓扑不变性。
> - **切空间/法空间公式**：本节原文未在所提供的页码中给出；上述公式为标准重构，使用时应另行核对教材第 8 章 §7 或后续章节。

> [!tip] 自测题线索（据原文可确认）
> 原文明确出现的自测题线索为：本节末第 4 题——二维球面为什么至少需要两张图？（提示：紧性在同胚下保持不变。）任务文本未提供其他习题题号，故不补充。

<!-- textbook-provenance:start -->
## 教材出处与纸质笔记坐标

- 教材：V. A. Zorich, 《Mathematical Analysis II》 (卓里奇《数学分析》第二卷，第4版)；第十二章 Rⁿ 中的曲面及微分形式 / §1. Rⁿ 中的曲面
- PDF第160页；印刷页码：未核实 <!-- source:pdf:160 -->
- PDF第161页；印刷页码：未核实 <!-- source:pdf:161 -->
- PDF第162页；印刷页码：未核实 <!-- source:pdf:162 -->
- PDF第163页；印刷页码：未核实 <!-- source:pdf:163 -->
- PDF第164页；印刷页码：未核实 <!-- source:pdf:164 -->
- PDF第165页；印刷页码：未核实 <!-- source:pdf:165 -->
- PDF第166页；印刷页码：未核实 <!-- source:pdf:166 -->
- 纸质活页：`[卡片-ZORICH-CON-12-01]`
- 教材导航：[[00_教材索引]]
<!-- textbook-provenance:end -->
