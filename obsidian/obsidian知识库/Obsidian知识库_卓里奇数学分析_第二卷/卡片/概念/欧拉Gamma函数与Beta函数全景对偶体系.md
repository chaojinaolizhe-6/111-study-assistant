---
tags: [概念卡]
aliases: [欧拉积分, 欧拉Γ函数, 欧拉B函数, 欧拉贝塔函数, 欧拉伽玛函数, Euler Gamma Function, Euler Beta Function, Eulerian Integrals, Gamma and Beta Functions]
created: 2026-09-18
updated: 2026-09-18
---

# 欧拉Gamma函数与Beta函数全景对偶体系

> [!summary] 核心认知先验
> 在建立了含参变量（正常与反常）积分的连续性、可微性、可积性判别法之后，Zorich 以两类欧拉积分作为理论最重要的具体应用。B 函数源于 $[0,1]$ 上含参的 $x^{\alpha-1}(1-x)^{\beta-1}$ 型积分，Γ 函数源于 $[0,+\infty)$ 上含参的 $x^{\alpha-1}e^{-x}$ 型积分。二者分别称为第一类、第二类欧拉积分。Γ 函数通过递推关系将阶乘连续化为 $\Gamma(n+1)=n!$，并与 B 函数经由对称性、递推、欧拉–高斯公式形成对偶体系；余元公式与 $\Gamma(1/2)=\sqrt{\pi}$ 则把 Γ 函数同三角函数及欧拉–泊松积分连接起来。

<!-- unit:u17_03_beta_gamma_def -->

## 定义、条件与直观

### 两类欧拉积分的解析定义

教材仿效勒让德，对实参数 $\alpha,\beta$ 定义

$$ \mathrm{B}(\alpha,\beta) := \int_0^1 x^{\alpha-1}(1-x)^{\beta-1}\,dx, \tag{1} $$

$$ \Gamma(\alpha) := \int_0^{+\infty} x^{\alpha-1} e^{-x}\,dx. \tag{2} $$

这两个反常积分分别称为**第一类**和**第二类欧拉积分**；其中 (1) 称为欧拉 $\beta$ 函数（贝塔函数），特别经常用到的 (2) 称为欧拉 $\Gamma$ 函数（伽玛函数）。

### β 函数的收敛域

积分 (1) 在积分下限 $x=0$ 处收敛的必要充分条件是 $\alpha>0$；在积分上限 $x=1$ 处收敛的必要充分条件是 $\beta>0$。因此函数

$$ \mathrm{B}(\alpha,\beta),\qquad \alpha>0,\ \beta>0 $$

当两个条件同时成立时有定义。

> 直观上：$x\to0^+$ 时 $x^{\alpha-1}$ 的可积性要求 $\alpha>0$；$x\to1^-$ 时 $(1-x)^{\beta-1}$ 的可积性要求 $\beta>0$。

### Γ 函数的收敛域

从 (2) 看出：在下限 $0$ 处，Γ 函数积分仅当 $\alpha>0$ 时收敛；而在上限 $+\infty$ 处，由于快速衰减因子 $e^{-x}$，该积分对任意 $\alpha\in\mathbb R$ 都收敛。于是

$$ \Gamma(\alpha),\qquad \alpha>0 $$

当 $\alpha>0$ 时有定义。

> [!note] 教材注记（实参数与复参数）
> 教材此处处处假定 $\alpha,\beta$ 是实数；但注记明确指出，$\beta$ 函数和 $\Gamma$ 函数的性质的最全面描述、最深刻的应用，与参变量为复值的情形联系着。本卡所据页码 392–396 只给出实参数积分定义，复平面解析延拓不在这几页的正文中展开。

## 性质与教材例子

<!-- unit:u17_03_beta_gamma_def -->

### 1. β 函数的对称性

对任意 $\alpha>0,\beta>0$，

$$ \mathrm{B}(\alpha,\beta)=\mathrm{B}(\beta,\alpha). \tag{3} $$

证明只需在积分 (1) 中作变量替换 $x=1-t$。

### 2. β 函数的递推公式

若 $\alpha>1$，则

$$ \mathrm{B}(\alpha,\beta)=\frac{\alpha-1}{\alpha+\beta-1}\,\mathrm{B}(\alpha-1,\beta). \tag{4} $$

关键证明步骤（在 $\alpha>1,\beta>0$ 下用分部积分与恒等变换）：

$$ \mathrm{B}(\alpha,\beta)
=-\frac{1}{\beta}x^{\alpha-1}(1-x)^{\beta}\bigg|_0^1
+\frac{\alpha-1}{\beta}\int_0^1 x^{\alpha-2}(1-x)^{\beta}\,dx, $$

$$ =\frac{\alpha-1}{\beta}\int_0^1 x^{\alpha-2}\Big((1-x)^{\beta-1}-x(1-x)^{\beta-1}\Big)\,dx
=\frac{\alpha-1}{\beta}\mathrm{B}(\alpha-1,\beta)-\frac{\alpha-1}{\beta}\mathrm{B}(\alpha,\beta). $$

解出 $\mathrm{B}(\alpha,\beta)$ 即得 (4)。

利用对称性 (3)，还可写出关于第二参数的递推式（当然假设 $\beta>1$）：

$$ \mathrm{B}(\alpha,\beta)=\frac{\beta-1}{\alpha+\beta-1}\,\mathrm{B}(\alpha,\beta-1). \tag{4'} $$

从 β 函数定义直接看出 $\mathrm{B}(\alpha,1)=\dfrac{1}{\alpha}$。因此对 $n\in\mathbb N$，

$$ \mathrm{B}(\alpha,n)
=\frac{n-1}{\alpha+n-1}\cdot\frac{n-2}{\alpha+n-2}\cdots\frac{1}{\alpha}\,\mathrm{B}(\alpha,1)
=\frac{(n-1)!}{\alpha(\alpha+1)\cdots(\alpha+n-1)}. \tag{5} $$

特别地，当 $m,n\in\mathbb N$ 时，

$$ \mathrm{B}(m,n)=\frac{(m-1)!(n-1)!}{(m+n-1)!}. \tag{6} $$

### 3. β 函数的另一种积分表示

有时很有用的等价表示是

$$ \mathrm{B}(\alpha,\beta)=\int_0^{+\infty}\frac{y^{\alpha-1}}{(1+y)^{\alpha+\beta}}\,dy. \tag{7} $$

通过变量替换 $x=\dfrac{y}{1+y}$ 从 (1) 即得 (7)。

### 4. Γ 函数的光滑性与导数公式

Γ 函数无限次可微，且

$$ \Gamma^{(n)}(\alpha)=\int_0^{+\infty} x^{\alpha-1}\ln^n x\cdot e^{-x}\,dx. \tag{8} $$

证明要点（积分号下求导的合法性）：

- 对任何固定的 $n\in\mathbb N$，证明积分 $\int_0^{+\infty}x^{\alpha-1}\ln^n x\,e^{-x}dx$ 关于 $\alpha$ 在每个区间 $[a,b]\subset]0,+\infty[$ 上一致收敛。
- 若 $0<a\le\alpha$，利用 $x^{a/2}\ln^n x\to0$（$x\to+0$）可找到 $c_n>0$，使当 $0<x\le c_n$ 时

$$ |x^{\alpha-1}\ln^n x\cdot e^{-x}| < x^{\frac{a}{2}-1}. $$

故由一致收敛性的强函数检验法，积分 $\int_0^{c_n}$ 关于 $\alpha$ 在 $[a,+\infty[$ 上一致收敛。

- 若 $\alpha\le b<+\infty$，则当 $x\ge1$ 时

$$ |x^{\alpha-1}\ln^n x\cdot e^{-x}|\le x^{b-1}|\ln^n x|\,e^{-x}, $$

从而 $\int_{c_n}^{+\infty}$ 关于 $\alpha$ 在 $]0,b]$ 上一致收敛。

- 综合可知导函数积分在任意 $[a,b]\subset]0,+\infty[$ 上一致收敛，故可积分号下求导，得到 (8)。

> [!note] 源文编号提示
> 所据扫描页中该段上下文有“积分(7)”“对积分(1)施行微分法”等字样；从内容看均指 Γ 函数的积分 (2)（或其导数积分 (8)），应是原书排版或 OCR 的编号偏移，本卡按数学内容表述。

### 5. Γ 函数的递推公式

$$ \Gamma(\alpha+1)=\alpha\Gamma(\alpha). \tag{9} $$

分部积分（$\alpha>0$）：

$$ \Gamma(\alpha+1):=\int_0^{+\infty}x^{\alpha}e^{-x}\,dx
=-x^{\alpha}e^{-x}\bigg|_0^{+\infty}
+\alpha\int_0^{+\infty}x^{\alpha-1}e^{-x}\,dx
=\alpha\Gamma(\alpha). $$

因为

$$ \Gamma(1)=\int_0^{+\infty}e^{-x}\,dx=1, $$

推出当 $n\in\mathbb N$ 时

$$ \Gamma(n+1)=n!. \tag{10} $$

即 Γ 函数与数论的算术函数 $n!$ 紧密联系。

### 6. 欧拉–高斯公式

$$ \Gamma(\alpha)=\lim_{n\to\infty}n^{\alpha}\cdot\frac{(n-1)!}{\alpha(\alpha+1)\cdots(\alpha+n-1)}. \tag{11} $$

推导要点：

- 在 (2) 中作变量替换 $x=\ln\dfrac{1}{u}$，得到 Γ 函数的新积分表示

$$ \Gamma(\alpha)=\int_0^1 \ln^{\alpha-1}\left(\frac{1}{u}\right)du. \tag{12} $$

- 利用第 16 章 §3 例 3 证明过的单调逼近：函数序列 $f_n(u)=n(1-u^{1/n})$ 在 $0<u<1$ 上单调递增收敛到 $\ln\dfrac1u$。由 §2 推论 2（或 §2 例 10），当 $\alpha\ge1$ 时

$$ \int_0^1\ln^{\alpha-1}\left(\frac1u\right)du
=\lim_{n\to\infty}n^{\alpha-1}\int_0^1 (1-u^{1/n})^{\alpha-1}du. \tag{13} $$

- 在最后积分中作 $u=v^n$，并利用 (12)、(13)、(1)、(3)、(5) 得到

$$ \Gamma(\alpha)=\lim_{n\to\infty}n^{\alpha}\int_0^1 v^{n-1}(1-v)^{\alpha-1}dv
=\lim_{n\to\infty}n^{\alpha}\mathrm{B}(n,\alpha)
=\lim_{n\to\infty}n^{\alpha}\mathrm{B}(\alpha,n), $$

$$ =\lim_{n\to\infty}n^{\alpha}\cdot\frac{(n-1)!}{\alpha(\alpha+1)\cdots(\alpha+n-1)}. $$

- 将递推公式 (4) 和 (9) 应用到已对 $\alpha\ge1$ 证明的关系式，即可把 (11) 推广到所有 $\alpha>0$。

### 7. 余元公式与 $\Gamma(1/2)=\sqrt{\pi}$

当 $0<\alpha<1$ 时，称 Γ 函数的自变量 $\alpha$ 与 $1-\alpha$ 互余；等式

$$ \Gamma(\alpha)\Gamma(1-\alpha)=\frac{\pi}{\sin\pi\alpha}\qquad(0<\alpha<1) \tag{14} $$

称为 Γ 函数的**余元公式**。

证明要点：

- 利用欧拉–高斯公式 (11)，对 $\Gamma(\alpha)$ 与 $\Gamma(1-\alpha)$ 分别写出乘积，经简单的恒等变形得到（扫描页中间代数行有 OCR 损坏，本卡按可读的最终结论写出）

$$ \Gamma(\alpha)\Gamma(1-\alpha)
=\frac{1}{\alpha}\prod_{n=1}^{\infty}\frac{1}{1-\frac{\alpha^2}{n^2}}. \tag{15} $$

- 配合古典展开式

$$ \sin\pi\alpha=\pi\alpha\prod_{n=1}^{\infty}\left(1-\frac{\alpha^2}{n^2}\right). \tag{16} $$

（教材此处不证明 (16)，留到第 18 章 §2 例 6 作为傅里叶级数一般定理的应用。）

- 对照 (15) 与 (16)，即得 (14)。

由 (14) 特别地得到

$$ \Gamma\left(\frac12\right)=\sqrt{\pi}. $$

又注意到

$$ \Gamma\left(\frac12\right)=\int_0^{+\infty}x^{-\frac12}e^{-x}\,dx
=2\int_0^{+\infty}e^{-u^2}\,du, \tag{17} $$

于是再次得到欧拉–泊松积分值

$$ \int_0^{+\infty}e^{-u^2}\,du=\frac12\sqrt{\pi}. $$

> [!warning] 易混概念与适用边界
> - **收敛域不同**：$\mathrm{B}(\alpha,\beta)$ 必须 $\alpha>0$ 且 $\beta>0$ 同时成立；$\Gamma(\alpha)$ 只需 $\alpha>0$，无穷远处由 $e^{-x}$ 保证收敛。
> - **递推方向与条件不同**：$\mathrm{B}$ 的递推公式 (4)/(4′) 要求被递降的参数分别 $>1$；$\Gamma$ 的递推 (9) 只要求 $\alpha>0$。两者的“基”分别为 $\mathrm{B}(\alpha,1)=1/\alpha$ 与 $\Gamma(1)=1$，并分别给出 $\mathrm{B}(m,n)$ 与 $\Gamma(n+1)=n!$。
> - **实参数假设与复参数提示**：教材原文约定 $\alpha,\beta\in\mathbb R$，同时明确提示完整性质与应用需考虑复参数；本卡所据页码 392–396 的原文未给出复平面解析延拓的构造。
> - **对数凸性与玻尔–莫勒鲁普定理**：任务大纲提及该内容，但本卡所据页码 392–396 的原文摘录没有出现，故无法从源文解构，本卡不复述。

**教材坐标**：V. A. Zorich《Mathematical Analysis II》第4版，第十七章 §3 欧拉积分，对应于所据扫描页 pp. 392–396（印刷页 380–384）。  
**纸质槽位**：`[卡片-ZORICH-CON-17-01]`。

<!-- textbook-provenance:start -->
## 教材出处与纸质笔记坐标

- 教材：V. A. Zorich, 《Mathematical Analysis II》 (卓里奇《数学分析》第二卷，第4版)；第十七章 含参变量的积分 / §3. 欧拉积分
- PDF第392页；印刷页码：未核实 <!-- source:pdf:392 -->
- PDF第393页；印刷页码：未核实 <!-- source:pdf:393 -->
- PDF第394页；印刷页码：未核实 <!-- source:pdf:394 -->
- PDF第395页；印刷页码：未核实 <!-- source:pdf:395 -->
- PDF第396页；印刷页码：未核实 <!-- source:pdf:396 -->
- 纸质活页：`[卡片-ZORICH-CON-17-01]`
- 教材导航：[[00_教材索引]]
<!-- textbook-provenance:end -->
