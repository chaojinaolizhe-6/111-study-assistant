---
tags: [解法卡]
aliases: ["朗道符号渐近展开与等价无穷小计算", "Landau Symbols, Big-O, Little-o, Asymptotic Expansions, and Equivalent Infinitesimals"]
created: 2026-09-17
updated: 2026-09-17
---

# 技术_朗道符号小o大O渐近展开与等价无穷小计算

> [!summary] 方法执行总览
> 适用问题：计算 $x\to 0$、$x\to\infty$ 或 $n\to\infty$ 时初等函数组合的极限，尤其是 $0/0$、$\infty-\infty$、$1^\infty$ 等未定式。核心步骤：先将涉及的基本初等函数展开成带 $O(\cdot)$ 或 $o(\cdot)$ 余项的局部多项式；再做代数化简；乘除因子可用等价无穷小替换，加减法必须保留足够高阶项，防止抵消后丢失主部。

<!-- unit:u03_02_exercises -->

## 原理与推导

### 教材给出的基本渐近公式

教材原文指出，以下渐近公式是例 37—40 所得公式的推广，当 $x\to 0$ 时成立：

$$
e^{x}=1+\frac{1}{1!}x+\cdots+\frac{1}{n!}x^{n}+O(x^{n+1}),\qquad x\to 0,
$$

$$
\cos x=1-\frac{1}{2!}x^{2}+\cdots+\frac{(-1)^{k}}{(2k)!}x^{2k}+O(x^{2k+2}),\qquad x\to 0,
$$

$$
\sin x=\frac{1}{1!}x-\frac{1}{3!}x^{3}+\cdots+\frac{(-1)^{k}}{(2k+1)!}x^{2k+1}+O(x^{2k+3}),\qquad x\to 0,
$$

$$
\ln(1+x)=x-\frac{1}{2}x^{2}+\cdots+\frac{(-1)^{n-1}}{n}x^{n}+O(x^{n+1}),\qquad x\to 0,
$$

$$
(1+x)^{\alpha}=1+\frac{\alpha}{1!}x+\frac{\alpha(\alpha-1)}{2!}x^{2}+\cdots+\frac{\alpha(\alpha-1)\cdots(\alpha-n+1)}{n!}x^{n}+O(x^{n+1}),\qquad x\to 0.
$$

这些公式把初等函数在 $0$ 附近表示成“幂函数 + 高阶无穷小”的形式，是处理极限时最直接的“渐近字典”。

### 教材给出的阶化简链条

当 $x\to 0$ 时，教材原文给出如下关系：

$$
O(x^{m+1})
= x^{m+1}\cdot O(1)
= x\cdot x^{m}\cdot O(1)
= x^{m}\cdot o(1)
= o(x^{m}).
$$

其含义是：若 $f(x)=O(x^{m+1})$，则 $f$ 不仅比 $x^{m+1}$ 增长得不快，而且相对于 $x^{m}$ 是高阶无穷小。此链条在合并余项、判断最终极限时经常使用。

### 补充讲解：朗道符号的严格定义与运算法则

> [!note] 说明
> 本次提供的资料页未包含大 $O$、小 $o$、等价 $\sim$ 的原始定义段；以下内容为根据通用定义整理的补充讲解，不是教材原句。

设函数 $f,g$ 在 $a$ 的某个去心邻域内有定义，且 $g$ 在该邻域内不恒为零。

- 大 $O$：$f(x)=O(g(x))$ 当 $x\to a$，指存在常数 $M>0$ 和邻域 $U$，使得 $|f(x)|\le M|g(x)|$ 在 $U$ 上成立。
- 小 $o$：$f(x)=o(g(x))$ 当 $x\to a$，指 $\lim_{x\to a} f(x)/g(x)=0$。
- 等价：$f(x)\sim g(x)$ 当 $x\to a$，指 $\lim_{x\to a} f(x)/g(x)=1$。
- 同阶：$f$ 与 $g$ 同阶，指 $f(x)=O(g(x))$ 且 $g(x)=O(f(x))$；常见充分条件是比值趋于非零有限极限。

常用代数法则（在相同极限过程中）：

$$
O(f)+O(f)=O(f),\qquad o(f)+o(f)=o(f),
$$

$$
O(f)\cdot O(g)=O(fg),\qquad O(f)\cdot o(g)=o(fg),\qquad o(f)\cdot o(g)=o(fg).
$$

这些法则可以在不写出余项具体表达式的情况下做“阶的计算”。例如教材中的链条 $O(x^{m+1})=x^{m+1}O(1)=o(x^m)$ 就是这种代数运算的体现。

## 教材例题与验证

### 例43：用高阶展开处理加减抵消

求

$$
\lim_{x\to 0}\frac{x-\sin x}{x^{3}}.
$$

识别：当 $x\to 0$ 时，$\sin x\sim x$。若在减法中直接作等价替换，则分子变为 $x-x=0$，丢失了主部。因此必须把 $\sin x$ 展开到至少三阶，并保留 $O(x^5)$。

关键演算：

$$
\frac{x-\sin x}{x^{3}}
=
\frac{x-\left(x-\dfrac{1}{3!}x^{3}+O(x^{5})\right)}{x^{3}}
=
\frac{\dfrac{1}{3!}x^{3}+O(x^{5})}{x^{3}}
=
\frac{1}{3!}+O(x^{2}).
$$

于是

$$
\lim_{x\to 0}\frac{x-\sin x}{x^{3}}
=
\lim_{x\to 0}\left(\frac{1}{3!}+O(x^{2})\right)
=
\frac{1}{3!}
=
\frac{1}{6}.
$$

结果检查：主部为 $x^3/6$，与 $x^3$ 同阶，极限为 $1/6$；余项 $O(x^2)$ 趋于 $0$。

### 例44：$x\to\infty$ 下的根式与余弦展开

求

$$
\lim_{x\to\infty}x^{2}\left(\sqrt[7]{\frac{x^{3}+x}{1+x^{3}}}-\cos\frac{1}{x}\right).
$$

> [!note] OCR 还原说明
> 教材原文图像中根指数因扫描识别显示为 $\tau$ 或 $\eta$ 等符号；根据展开系数最终得到 $9/14$，可还原根指数为 $7$。下文按 7 次根号记录。该处以教材原图为最终依据。

识别：$x\to\infty$ 时根式内部分趋于 $1$，$\cos(1/x)\to 1$，差是 $1/x^2$ 量级。应把两项都展开到 $1/x^2$ 阶，余项保留到 $O(1/x^3)$。

第一步，化简根式内部：

$$
\frac{x^{3}+x}{1+x^{3}}
=
\frac{1+\dfrac{1}{x^{2}}}{1+\dfrac{1}{x^{3}}}
=
\left(1+\frac{1}{x^{2}}\right)\left(1+\frac{1}{x^{3}}\right)^{-1}.
$$

由二项式展开，

$$
\left(1+\frac{1}{x^{3}}\right)^{-1}
=
1-\frac{1}{x^{3}}+O\left(\frac{1}{x^{6}}\right),
$$

所以

$$
\frac{x^{3}+x}{1+x^{3}}
=
\left(1+\frac{1}{x^{2}}\right)\left(1-\frac{1}{x^{3}}+O\left(\frac{1}{x^{6}}\right)\right)
=
1+\frac{1}{x^{2}}+O\left(\frac{1}{x^{3}}\right).
$$

第二步，开七次方：

$$
\sqrt[7]{\frac{x^{3}+x}{1+x^{3}}}
=
\left(1+\frac{1}{x^{2}}+O\left(\frac{1}{x^{3}}\right)\right)^{1/7}.
$$

利用 $(1+u)^{\alpha}=1+\alpha u+O(u^{2})$，其中 $u=1/x^{2}+O(1/x^{3})$：

$$
\sqrt[7]{\frac{x^{3}+x}{1+x^{3}}}
=
1+\frac{1}{7}\frac{1}{x^{2}}+O\left(\frac{1}{x^{3}}\right).
$$

第三步，展开余弦项：

$$
\cos\frac{1}{x}
=
1-\frac{1}{2!}\frac{1}{x^{2}}+O\left(\frac{1}{x^{4}}\right)
=
1-\frac{1}{2x^{2}}+O\left(\frac{1}{x^{4}}\right).
$$

第四步，做差并合并：

$$
\sqrt[7]{\frac{x^{3}+x}{1+x^{3}}}-\cos\frac{1}{x}
=
\left(1+\frac{1}{7x^{2}}+O\left(\frac{1}{x^{3}}\right)\right)
-
\left(1-\frac{1}{2x^{2}}+O\left(\frac{1}{x^{4}}\right)\right)
=
\frac{9}{14x^{2}}+O\left(\frac{1}{x^{3}}\right).
$$

因此

$$
x^{2}\left(\sqrt[7]{\frac{x^{3}+x}{1+x^{3}}}-\cos\frac{1}{x}\right)
=
x^{2}\left(\frac{9}{14x^{2}}+O\left(\frac{1}{x^{3}}\right)\right)
=
\frac{9}{14}+O\left(\frac{1}{x}\right).
$$

取极限得

$$
\lim_{x\to\infty}x^{2}\left(\sqrt[7]{\frac{x^{3}+x}{1+x^{3}}}-\cos\frac{1}{x}\right)
=
\frac{9}{14}.
$$

结果检查：两项的常数项 $1$ 抵消，主部来自 $1/x^{2}$ 项；若只展开到 $1/x$ 阶，差的主部会丢失。

### 例45：$1^\infty$ 型极限化为指数后展开

求

$$
\lim_{x\to\infty}\left[\frac{\left(1+\dfrac{1}{x}\right)^{x}}{e}\right]^{x}.
$$

识别：底数趋于 $1$，指数趋于 $\infty$，是 $1^\infty$ 型。取对数化为指数函数，再展开 $\ln(1+1/x)$。

关键演算：

$$
\left[\frac{\left(1+\frac{1}{x}\right)^{x}}{e}\right]^{x}
=
\exp\left(x\left[\ln\left(1+\frac{1}{x}\right)^{x}-1\right]\right)
=
\exp\left(x^{2}\ln\left(1+\frac{1}{x}\right)-x\right).
$$

由 $\ln(1+u)=u-\frac{1}{2}u^{2}+O(u^{3})$，令 $u=1/x$，得

$$
\ln\left(1+\frac{1}{x}\right)
=
\frac{1}{x}-\frac{1}{2x^{2}}+O\left(\frac{1}{x^{3}}\right).
$$

代入：

$$
x^{2}\ln\left(1+\frac{1}{x}\right)-x
=
x^{2}\left(\frac{1}{x}-\frac{1}{2x^{2}}+O\left(\frac{1}{x^{3}}\right)\right)-x
=
-\frac{1}{2}+O\left(\frac{1}{x}\right).
$$

因此

$$
\lim_{x\to\infty}\left[\frac{\left(1+\frac{1}{x}\right)^{x}}{e}\right]^{x}
=
\lim_{x\to\infty}\exp\left(-\frac{1}{2}+O\left(\frac{1}{x}\right)\right)
=
e^{-1/2}.
$$

结果检查：$O(1/x)\to 0$，指数函数的连续性保证可交换极限。

> [!warning] 边界与易错步骤
> 1. **加减法不能直接做等价替换**：如例43中 $\sin x\sim x$，但 $x-\sin x$ 的主部是 $x^3/6$。遇到加减抵消时，必须把相关函数展开到足够高阶，直到出现不抵消的首项。  
> 2. **余项阶要匹配分母或乘子**：例43分母为 $x^3$，展开 $\sin x$ 时必须保留到 $O(x^5)$，否则无法判定极限；例44乘子为 $x^2$，展开项必须到 $1/x^2$，余项保留到 $O(1/x^3)$。  
> 3. **换元方向**：$x\to\infty$ 时常令 $u=1/x$，把问题化成 $u\to 0$，但原极限中的 $O(1/x^k)$ 对应 $O(u^k)$，不要误写为 $O(x^k)$。  
> 4. **根式与分数幂**：对 $(1+u)^\alpha$ 展开时，$\alpha$ 可以是任意实数；教材例44中根指数需由最终系数确认，不能仅凭 OCR 识别。  
> 5. **$1^\infty$ 型必须取对数**：直接对底数或指数做等价替换通常不可靠；标准路径是 $A^B=e^{B\ln A}$，然后展开 $\ln A$。

## 练习组题号定位与提示

> [!note] 资料范围说明
> 给定资料页 134–137 只显示练习 1–11。若本卡标题所称“练习 1–32”指完整教材练习集，则第 12–32 题未包含在本次提供的资料中，不能确认其具体内容。

按所提供原文，可确认的练习及其与朗道符号的关系如下：

- **练习 1a,b**  
  函数方程与连续性唯一性。主要依赖指数函数与对数函数的结构，不是直接的 $O/o/\sim$ 计算题，但可视为等价关系与连续延拓的背景。

- **练习 2a,b**  
  群同构。与朗道符号无直接关系。

- **练习 3a–d**  
  求极限：  
  a) $\lim_{x\to +0}x^x$；b) $\lim_{x\to+\infty}x^{1/x}$；c) $\lim_{x\to 0}\frac{\log_a(1+x)}{x}$；d) $\lim_{x\to 0}\frac{a^x-1}{x}$。  
  方法提示：a)、b) 先写成 $e^{x\ln x}$、$e^{(\ln x)/x}$；c) 用 $\log_a(1+x)=\frac{\ln(1+x)}{\ln a}$ 和 $\ln(1+x)\sim x$；d) 用 $a^x=e^{x\ln a}$ 和 $e^u-1\sim u$。

- **练习 4**  
  证明 $1+\frac12+\cdots+\frac1n=\ln n+c+o(1)$，$c$ 为欧拉常数。  
  方法提示：利用 $\ln\frac{n+1}{n}=\ln\left(1+\frac1n\right)=\frac1n+O\left(\frac1{n^2}\right)$，对 $n$ 求和，得到调和数与 $\ln n$ 的差收敛到常数。

- **练习 5a,b**  
  a) 正项级数 $a_n\sim b_n$ 时同敛散；b) $\sum \sin\frac{1}{n^p}$ 仅当 $p>1$ 收敛。  
  方法提示：a) 等价无穷小说明比值趋于 $1$，比较判别法；b) 用 $\sin(1/n^p)\sim 1/n^p$，从而退化为 $p$-级数。

- **练习 6a–d**  
  关于 $o(1/n)$ 与级数收敛速度的比较。核心是说明不存在“万能比较级数”。  
  方法提示：用 $o(1/n)$ 构造更慢收敛的正项级数；结论依赖小 $o$ 的严格定义。

- **练习 7a,b**  
  a) $\sum \ln a_n$ 收敛当且仅当部分积趋于非零极限；b) $\sum \ln(1+a_n)$ 绝对收敛当且仅当 $\sum a_n$ 绝对收敛。  
  方法提示：b) 利用 $\ln(1+a_n)\sim a_n$ 及练习 5a。

- **练习 8a–c**  
  无穷乘积收敛定义及对数判定。  
  方法提示：$\prod e_k$ 收敛等价于 $\sum \ln e_k$ 收敛；$e_n=1+a_n$ 时用 $\ln(1+a_n)\sim a_n$。

- **练习 9a–c**  
  求无穷乘积，包括韦达公式。  
  方法提示：利用对数化乘积为级数，或利用三角恒等式与函数方程；韦达公式可由 $\prod \cos(x/2^n)$ 的极限得到。

- **练习 10a–c**  
  比值渐近与高斯检验法。  
  方法提示：当 $\frac{a_n}{a_{n+1}}=1+\frac{p}{n}+\alpha_n$ 且 $\sum \alpha_n$ 绝对收敛时，可推出 $a_n\sim c/n^p$；这决定级数 $\sum a_n$ 的敛散性。

- **练习 11**  
  证明对任意正项序列 $a_n$，  
  $$
  \overline{\lim}_{n\to\infty}\left(\frac{1+a_{n+1}}{a_n}\right)^{n}\ge e,
  $$  
  且估值为最佳。方法提示：利用 $e$ 的极限定义与上极限性质，通过构造反例说明常数 $e$ 不可改进。

> [!summary] 关联本节笔记
> 本技术卡对应卓里奇《数学分析 I》第三章 §2“函数的极限”中的渐近展开与朗道符号应用。核心工具为 §2 的例 37—40 推广所得的带余项初等函数展开，以及例 43—45 的示范应用。可核实的教材页：134–137。

<!-- textbook-provenance:start -->
## 教材出处与纸质笔记坐标

- 教材：V. A. Zorich, 《Mathematical Analysis I》 (卓里奇《数学分析》第一卷，第4版)；第三章 极限 / §2. 函数的极限
- PDF第134页；印刷页码：未核实 <!-- source:pdf:134 -->
- PDF第135页；印刷页码：未核实 <!-- source:pdf:135 -->
- PDF第136页；印刷页码：未核实 <!-- source:pdf:136 -->
- PDF第137页；印刷页码：未核实 <!-- source:pdf:137 -->
- 纸质活页：`[活页-ZORICH-CARD-09]`
- 教材导航：[[00_教材索引]]
<!-- textbook-provenance:end -->
