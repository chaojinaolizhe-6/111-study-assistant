---
tags: [定理卡]
aliases:
  - Beta函数与Gamma函数基本联系恒等式
  - 欧拉 Beta-Gamma 联系公式
  - Euler beta-gamma connection identity
  - Beta-Gamma relation
created: 2026-09-18
updated: 2026-09-18
---

# 定理卡：Beta函数与Gamma函数基本联系恒等式（B(α,β)=Γ(α)Γ(β)/Γ(α+β)）

> [!summary] 核心论断
> 在欧拉积分定义域 $\alpha>0$，$\beta>0$ 内，Beta 函数与 Gamma 函数满足 $ \mathrm{B}(\alpha,\beta)=\frac{\Gamma(\alpha)\Gamma(\beta)}{\Gamma(\alpha+\beta)} $。教材（Zorich《数学分析 II》第17章 §3）把它列为公式(18)，并通过把 $\Gamma(\alpha+\beta)\mathrm{B}(\alpha,\beta)$ 写成双重反常积分、交换积分顺序、再作线性变量替换 $u=xy$ 而证明。

<!-- unit:u17_03_euler_connection -->

## 完整表述与条件

教材第17章 §3 在给出欧拉积分后，先指出 Beta 与 Gamma 的表达式（教材公式(6)与(10)）暗示下面的关系式，然后正式提出：

$$ \mathrm{B}(\alpha,\beta)=\frac{\Gamma(\alpha)\Gamma(\beta)}{\Gamma(\alpha+\beta)}. \tag{18} $$

条件方面：

- 给定片段 p.397 未逐字重复 Beta 与 Gamma 的定义域；但教材在前文定义欧拉积分时要求正参数。本片段所有使用均在 $\alpha>0,\ \beta>0$ 范围内。
- 右端分母 $\Gamma(\alpha+\beta)$ 在 $\alpha+\beta>0$ 时非零且为正，因此除法合法。
- 教材没有把公式(18)表述为“充要条件”命题；它是欧拉积分定义域上的恒等式。
- 教材在证明中使用了 Beta 的第二积分表示（教材公式(7)）：

$$ \mathrm{B}(\alpha,\beta)=\int_0^{+\infty}\frac{y^{\alpha-1}}{(1+y)^{\alpha+\beta}}\,dy. $$

## 证明思路与关键步骤

教材的证明不用极坐标替换，而是使用 Gamma 的伸缩表示、Fubini 型积分换序和一次变量替换 $u=xy$。

1. **伸缩形式的 Gamma 表示**  
   对 $y>0$，由 Gamma 定义可得

   $$ \Gamma(\alpha)=y^\alpha\int_0^{+\infty}x^{\alpha-1}e^{-xy}\,dx. $$

   因此也有

   $$ \frac{\Gamma(\alpha+\beta)y^{\alpha-1}}{(1+y)^{\alpha+\beta}}
   = y^{\alpha-1}\int_0^{+\infty}x^{\alpha+\beta-1}e^{-(1+y)x}\,dx. $$

2. **利用 Beta 的第二积分表示**  
   将上式代入

   $$ \Gamma(\alpha+\beta)\mathrm{B}(\alpha,\beta)
   =\int_0^{+\infty}\frac{\Gamma(\alpha+\beta)y^{\alpha-1}}{(1+y)^{\alpha+\beta}}\,dy, $$

   得到双重积分：

   $$ \Gamma(\alpha+\beta)\mathrm{B}(\alpha,\beta)
   =\int_0^{+\infty}\left(
   y^{\alpha-1}\int_0^{+\infty}x^{\alpha+\beta-1}e^{-(1+y)x}dx
   \right)dy. $$

3. **交换积分顺序**  
   教材在等号上标注了惊叹号，并说明“它是在 §2，例16 中已经研究过的”，即这一步换序依赖 §2 例16 的保证：

   $$ \Gamma(\alpha+\beta)\mathrm{B}(\alpha,\beta)
   =\int_0^{+\infty}\left(
   \int_0^{+\infty}y^{\alpha-1}x^{\alpha+\beta-1}e^{-(1+y)x}dy
   \right)dx. $$

   > [!note] 补充讲解
   > 这里被积函数在 $(0,+\infty)\times(0,+\infty)$ 上非负，因此换序可由非负可测函数情形的 Fubini/Tonelli 定理保证；若不用非负性，则需要证明绝对可积性。教材只引用 §2 例16，未在本片段重复该定理的全部条件。

4. **内层积分的变量替换 $u=xy$**  
   固定 $x>0$，对内层积分作 $u=xy$，则 $du=x\,dy$。于是

   $$ \int_0^{+\infty}y^{\alpha-1}x^{\alpha+\beta-1}e^{-(1+y)x}dy
   =x^{\beta-1}e^{-x}\int_0^{+\infty}(xy)^{\alpha-1}e^{-xy}x\,dy
   =x^{\beta-1}e^{-x}\Gamma(\alpha). $$

   因此

   $$ \Gamma(\alpha+\beta)\mathrm{B}(\alpha,\beta)
   =\int_0^{+\infty}x^{\beta-1}e^{-x}\Gamma(\alpha)\,dx
   =\Gamma(\alpha)\Gamma(\beta). $$

5. **两边除以 $\Gamma(\alpha+\beta)$**  
   由于 $\alpha+\beta>0$，$\Gamma(\alpha+\beta)>0$，故可除，得到

   $$ \mathrm{B}(\alpha,\beta)=\frac{\Gamma(\alpha)\Gamma(\beta)}{\Gamma(\alpha+\beta)}. $$

## 推论、使用方式与边界

### 先备事实：余元公式与 $\Gamma(1/2)$（p.396，公式(14)–(17)）

在证明公式(18)之前，教材已由欧拉–高斯公式及古典正弦乘积展开得到余元公式：

$$ \Gamma(\alpha)\Gamma(1-\alpha)=\frac{\pi}{\sin\pi\alpha},\quad 0<\alpha<1. \tag{14} $$

特别地，取 $\alpha=1/2$，得

$$ \Gamma\left(\frac12\right)=\sqrt{\pi}. $$

又由

$$ \Gamma\left(\frac12\right)=\int_0^{+\infty}x^{-1/2}e^{-x}dx
=2\int_0^{+\infty}e^{-u^2}du, \tag{17} $$

重新得到欧拉–泊松积分值

$$ \int_0^{+\infty}e^{-u^2}du=\frac{\sqrt{\pi}}{2}. $$

### 由恒等式得到的三角积分（p.397，例1）

例1 给出：

$$ \int_0^{\pi/2}\sin^{\alpha-1}\varphi\cos^{\beta-1}\varphi\,d\varphi
=\frac12\mathrm{B}\left(\frac{\alpha}{2},\frac{\beta}{2}\right). \tag{19} $$

证明只需作变量替换 $\sin^2\varphi=x$。再结合公式(18)和 $\Gamma(1/2)=\sqrt{\pi}$，特别地得到

$$ \int_0^{\pi/2}\sin^{\alpha-1}\varphi\,d\varphi
=\int_0^{\pi/2}\cos^{\alpha-1}\varphi\,d\varphi
=\frac{\sqrt{\pi}}{2}\frac{\Gamma\left(\frac{\alpha}{2}\right)}
{\Gamma\left(\frac{\alpha+1}{2}\right)}. \tag{20} $$

### $n$ 维球体积与球面积（p.398–399，例2、例3）

教材利用截面法和公式(20)得到 $n$ 维球体积系数 $c_n$ 的递推，并最终得

$$ V_n(r)=c_n r^n
=\frac{\pi^{n/2}}{\Gamma\left(\frac{n+2}{2}\right)}r^n
=\frac{\pi^{n/2}}{\frac n2\Gamma\left(\frac n2\right)}r^n. \tag{21} $$

再由 $dV_n(r)=S_{n-1}(r)dr$，得 $n$ 维球面面积

$$ S_{n-1}(r)=\frac{2\pi^{n/2}}{\Gamma\left(\frac n2\right)}r^{n-1}. $$

### 练习与自测题（p.399）

教材在 §3 末尾配有下列练习。

**练习 1** 中包含（题号按原文；给定 OCR 片段中 b 与 e 之间两条公式的题号未完整标出，按原顺序列出）：

- a) $\mathrm{B}\left(\frac12,\frac12\right)=\pi$。
- b) $\mathrm{B}(\alpha,1-\alpha)=\int_0^{+\infty}\frac{x^{\alpha-1}}{1+x}dx$。
- [题号未标出] $\frac{\partial\mathrm{B}}{\partial\alpha}(\alpha,\beta)=\int_0^1 x^{\alpha-1}(1-x)^{\beta-1}\ln x\,dx$。
- [题号未标出] $\int_0^{+\infty}\frac{x^p}{(a+bx^q)^r}dx
  =\frac{a^{-r}}q\left(\frac ab\right)^{\frac{p+1}{q}}
  \mathrm{B}\left(\frac{p+1}{q},r-\frac{p+1}{q}\right)$。
- e) $\int_0^{+\infty}\frac{dx}{\sqrt[n]{1+x^n}}
  =\frac{\pi}{n\sin(\pi/n)}$。
- f) $\int_0^{+\infty}\frac{dx}{1+x^3}
  =\frac{2\pi}{3\sqrt 3}$。
- g) $\int_0^{+\infty}\frac{x^{\alpha-1}}{1+x}dx
  =\frac{\pi}{\sin\pi\alpha}$，$(0<\alpha<1)$。
- h) $\int_0^{+\infty}\frac{x^{\alpha-1}\ln^n x}{1+x}dx
  =\frac{d^n}{d\alpha^n}\left(\frac{\pi}{\sin\pi\alpha}\right)$，$(0<\alpha<1)$。
- i) 由极坐标方程 $r^n=a^n\cos n\varphi$ 给出的曲线的长度可用
  $a\,\mathrm{B}\left(\frac12,\frac1{2n}\right)$ 表示，$(n\in\mathbb N,\ a>0)$。

**练习 2**：

- a) $\Gamma(1)=\Gamma(2)$。
- b) $\Gamma'$ 在某点 $x_0\in\,]1,2[$ 为零；
- c) $\Gamma'$ 在 $]0,+\infty[$ 上单调上升；
- d) $\Gamma$ 在 $]0,x_0[$ 上单调下降，在 $[x_0,+\infty[$ 上单调上升；
- e) $\int_0^1\left(\ln\frac1u\right)^{x-1}\ln\frac1u\,du$ 当 $x=x_0$ 时等于零；
- f) $\Gamma(\alpha)\sim\frac1\alpha$，当 $\alpha\to+0$ 时；
- g) $\lim_{n\to\infty}\int_0^{+\infty}e^{-x^n}dx=1$。

**练习 3**：欧拉公式

$$ E:=\prod_{k=1}^{n-1}\Gamma\left(\frac kn\right)
=\frac{(2\pi)^{\frac{n-1}{2}}}{\sqrt n}. $$

### 边界说明

- 公式(18)本身的证明不依赖余元公式；但练习 1(g)(h) 等把 $\mathrm{B}(\alpha,1-\alpha)$ 化为 $\Gamma(\alpha)\Gamma(1-\alpha)$，再使用余元公式(14)完成计算。
- 教材在本片段只讨论正参数欧拉积分；若要将公式(18)推广到复参数，需要 Gamma 函数的解析延拓，教材在此处未展开。

> [!caution] 条件与反例
> 公式(18)在正参数 $\alpha>0$，$\beta>0$ 下由收敛的欧拉积分给出；教材没有在负参数或复参数下陈述该恒等式。换序步骤依赖 §2 例16 的保证，若被积函数不满足相应的可积/非负条件，不能无条件交换积分顺序。教材未提供反例，此处不额外构造。

教材坐标：Zorich, *Mathematical Analysis II*, 第17章 §3, pp. 396–399；公式(18)及其证明见 p.397；例1见 p.397；例2见 p.398；例3与练习见 p.399。

<!-- textbook-provenance:start -->
## 教材出处与纸质笔记坐标

- 教材：V. A. Zorich, 《Mathematical Analysis II》 (卓里奇《数学分析》第二卷，第4版)；第十七章 含参变量的积分 / §3. 欧拉积分
- PDF第396页；印刷页码：未核实 <!-- source:pdf:396 -->
- PDF第397页；印刷页码：未核实 <!-- source:pdf:397 -->
- PDF第398页；印刷页码：未核实 <!-- source:pdf:398 -->
- PDF第399页；印刷页码：未核实 <!-- source:pdf:399 -->
- 纸质活页：`[卡片-ZORICH-THM-17-04]`
- 教材导航：[[00_教材索引]]
<!-- textbook-provenance:end -->
