# 第五章 傅里叶变换 — 逐页转写

> 来源：`subjects\04-数学物理方法1\课件\第五章+傅里叶变换+-+上传课件.pdf`（共 63 页）
> 转写方式：PDF 每页渲染为 PNG（dpi=110）后逐页看图读取公式；中文措辞取自 PDF 文本层（与图核对一致）。
> 约定：全部公式用 LaTeX；`⇌` 为课件用的变换符号；`−`／`+`、上下限、系数均按图逐字核对，不做修正。
> 自检：对系数最易抄错的若干闭式做了数值复核（p12 的 bₙ、p24 的 A(ω)、p26 的 B(ω)、p32 的 F(k)、p38 的 ∫ 与 F(k)、p50 的 f(x) 卷积等式、p60 的 F(k)、p61 的 g(x) 代回方程），并与原积分/原方程逐点对照一致。

---

## 全书结构

**前置（p1–p4）**：章首导论与目录。

- **§5.1 傅里叶级数：p5–p17**
  - p5 实数形式级数的展开式骨架 + 三角函数正交性五式 + δ_nm 定义
  - p6 由正交性"推出"实变函数级数系数 a₀、aₙ、bₙ
  - p7 实数形式级数小结（展开式 + 三个系数公式同页）
  - p8 偶函数→只余余弦级数；奇函数→只余正弦级数
  - p9 引入波数 kₙ=nπ/l，把展开式改写成 cos(kₙx)、sin(kₙx)
  - p10 令 ω=2π/l、t=x/2，改写为时间变量的周期信号形式（系数含 2/T）
  - p11 令 θ=πx/l，改写为 2π 周期函数 f(θ) 的形式
  - p12 例1 锯齿函数 f(x)=−x/l 展开（a₀、aₙ、bₙ 全部算完）
  - p13 例2 对称方波（±π/4）的系数只写成"= ?"，末尾直接给部分和结果
  - p14 例2 的部分和图示 m=1、2、3、24（Gibbs 现象直观）
  - p15 复数形式傅里叶级数：复指数基函数族、kₙ=nπ/l、系数 1/(2l)
  - p16 复数形式级数小结（空间变量版 + 时间变量版 cₙ=1/T∫…）
  - p17 三点说明：系数可为复数；只适用于有限区域；kₙ/ωₙ 取值不连续
- **§5.2 傅里叶变换：p18–p39**
  - p18 傅里叶积分定理与实数形式变换系数 A(k)、B(k)（各带 1/π）
  - p19 级数→积分的证明开端：Δkₙ=π/l、a₀→0、aₙ 项改写
  - p20 求和→积分（cos 项得 A(k)）；bₙ 项书写时整段照抄了 cos 式（见存疑）
  - p21 傅里叶变换存在的条件 + 第一类间断点定义
  - p22 奇函数→正弦积分公式；偶函数→余弦积分公式（系数变 2/π）
  - p23 时间变量 t 的实数形式 + 谱函数 A(ω)、B(ω)、圆频率；级数展开与积分变换的区别
  - p24 例1 矩形脉冲（半宽度 T）：A(ω)=2sin(ωT)/(πω) 及逆变换回原函数
  - p25 例2 截断正弦波（|t|<2Nπ/ω₀）：B(ω) 的积分与差化积
  - p26 例2 续：和差化积展开、合并得 B(ω) 与 f(t) 的积分表达式
  - p27 复数形式傅里叶变换（欧拉公式 + A(−k)=A(k)、B(−k)=−B(k)）
  - p28 复数形式续：第二项换 k→−k 后合并成 ∫_{-∞}^{∞}F(k)e^{ikx}dk
  - p29 复数形式变换对定义（F(k)=1/(2π)∫f e^{−ikx}dx）、正/逆变换的核
  - p30 时间变量版的复数变换对（核为 e^{−iωt}、e^{iωt}）+ 系数 1/(2π)、1/√(2π) 放置说明
  - p31 二维 (x,t) 与三维 (r,t) 的变换式，系数 1/(2π)²、1/(2π)⁴
  - p32 例3 高斯函数 sqrt(a/π)e^{−a²x²/2} 的变换 → 1/(π√(2a))e^{−k²/(2a²)}
  - p33 例4 求证 sin(ω₀t)/(πt) 与矩形谱 F(ω) 互为变换（正向积分）
  - p34 例4 续：留数定理求无穷积分（含实轴极点的公式），ω+ω₀>0 分支
  - p35 例4 续：三个区间讨论（矛盾支、ω>ω₀、ω<−ω₀）与最终结论
  - p36 例5 屏蔽库仑势 (1/r)e^{−r/λ} 的三维变换设置（球坐标、k 沿 z 轴）
  - p37 例5 续：角度积分化为 ∫₀^∞ e^{−r/λ}sin(kr)dr
  - p38 例5 续：两次分部积分得 kλ²/(1+k²λ²)，像函数 F(k)=λ²/(2π²(1+k²λ²))
  - p39 § 第五章作业 第 1–4 题
- **§5.3 傅里叶变换的性质：p40–p50**
  - p40 变换记号 f(x)⇌F(k)；(1) 线性定理
  - p41 (2) 导数定理I：f^{(n)}(x)⇌(ik)ⁿF(k)，要求 f^{(n−1)}(x)|_{x=±∞}=0
  - p42 (3) 导数定理II：(−ix)ⁿf(x)⇌F^{(n)}(k) 及其意义
  - p43 (4) 积分定理：∫_{−∞}^{x}f(ζ)dζ ⇌ F(k)/(ik)
  - p44 (5) 相似性定理：f(ax)⇌F(k/a)/|a|
  - p45 (6) 延迟定理：f(x−a)⇌e^{−ika}F(k)
  - p46 (7) 位移定理：e^{ik₀x}f(x)⇌F(k−k₀)；(8) 卷积定义与卷积定理（系数 2π）
  - p47 卷积定理证明（换元 + 延迟定理）
  - p48 (9) 乘积定理：f₁f₂⇌F₁*F₂
  - p49 例1 已知卷积积分等式反求 f(x)：用留数算 F[1/(x²+a²)]
  - p50 例1 续：F[1/(x²+b²)]、比值、整理得 f(x)=a(b−a)/(πb)·1/(x²+(b−a)²)
- **§5.4 δ函数：p51–p63**
  - p51 δ函数定义引入：匀质细杆的线密度 ρ(x)，l→0 趋于质点
  - p52 δ函数定义式 δ(x−x₀)、无限窄/无穷大、归一化积分
  - p53 三维 δ 函数与乘积表示；质点/点电荷/脉冲三个物理实例
  - p54 性质 (1) 偶函数、导数奇函数；(2) 用阶跃函数 H(x) 表示
  - p55 性质 (3) 挑选性（含 ∫f(x)xδ(x)dx=0）；(4) 复合函数 δ[φ(x)]
  - p56 辅助函数：两个特征 + rect 型例子及其证明
  - p57 辅助函数三例：(1/π)sin(kx)/x、洛伦兹 (1/π)ε/(x²+ε²)、高斯型
  - p58 δ 的傅里叶变换：C(k)=1/(2π)、积分表达式、三维版、k→∞ 的广义函数表示
  - p59 例1 sin ax、cos ax 的傅里叶变换
  - p60 例2 球坐标中 f(r)=(4π²/r)δ(r−r₀) 的变换
  - p61 例3 含 δ 函数的常微分方程 d²g/dx²−a²g=δ(x−x₀)
  - p62 例4 一般 f(x) 的常微分方程（格林函数法）
  - p63 § 第五章作业 第 5–7 题

---

## p1 ｜ 章首导论
- 标题行：第五章 傅里叶变换
- 中文要点：傅里叶变换是求解数学物理方法问题的重要工具之一，它的应用领域非常广泛，不仅涉及一些工程技术领域，如振动、传热、电磁、信息等，同时它还在理论物理，量子力学、电动力学等基础学科领域有重要的应用。（后段红字）特别是，对于一些线性的常微分或偏微分方程（或方程组），借助傅里叶变换，可以转化成线性的代数方程（或方程组）。
- 公式：无
- 例题/作业：无
- 图：无（背景为"仅供教学、请勿上传"水印）
- ⚠️存疑：无

## p2 ｜ 章首导论·傅里叶方法的作用
- 标题行：（无标题，四条项目符号）
- 中文要点：任何周期信号都可用正弦函数的级数表示；用傅里叶分析方法可以将任何一种流体的周期性运动分成具有不同频率和波长的正弦震荡的叠加；任何非周期信号都可用正弦函数的积分表示；对于一些线性的常微分或偏微分方程（或方程组），借助傅里叶变换，可以转化成线性的代数方程（或方程组）。
- 公式：无
- 例题/作业：无
- 图：无
- ⚠️存疑：无

## p3 ｜ 章首导论·傅里叶生平
- 标题行：傅里叶生平
- 中文要点：1768 年生于法国；1807 年提出"任何周期信号都可用正弦函数的级数表示"；1822 年发表"热的分析理论"，首次提出"任何非周期信号都可用正弦函数的积分表示"。
- 公式：无
- 例题/作业：无
- 图：右侧为傅里叶黑白肖像照片（无坐标信息）
- ⚠️存疑：无

## p4 ｜ 第五章目录
- 标题行：第五章 傅里叶变换
- 中文要点：§ 5.1 傅里叶级数；§ 5.2 傅里叶变换；§ 5.3 傅里叶变换的性质；§ 5.4 δ函数
- 公式：无
- 例题/作业：无
- 图：无
- ⚠️存疑：无

## p5 ｜ §5.1 傅里叶级数·(1) 实数形式的傅里叶级数
- 标题行：§ 5.1 傅里叶级数（页内二级标题"1、实数形式的傅里叶级数"）
- 中文要点：设 f(x) 是一个以 2l 为周期的函数，即：…则可以把它展开成如下形式的傅里叶级数：…利用三角函数的正交性…其中符号 δ_m 的定义为…
- 公式：
  - 周期性条件：
    $$f(x)=f(x+2l)$$
  - 实数形式展开式（本页核心）：
    $$f(x)=a_{0}+\sum_{n=1}^{\infty}\left[a_{n}\cos\frac{n\pi x}{l}+b_{n}\sin\frac{n\pi x}{l}\right]$$
  - 正交性关系（供 p6 推系数用），共五式：
    $$\frac{1}{l}\int_{-l}^{l}\sin\frac{n\pi x}{l}\sin\frac{m\pi x}{l}\,dx=\delta_{nm}$$
    $$\frac{1}{l}\int_{-l}^{l}\cos\frac{n\pi x}{l}\cos\frac{m\pi x}{l}\,dx=\delta_{nm}$$
    $$\frac{1}{l}\int_{-l}^{l}\cos\frac{n\pi x}{l}\sin\frac{m\pi x}{l}\,dx=0$$
    $$\frac{1}{l}\int_{-l}^{l}1\cdot\cos\frac{n\pi x}{l}\,dx=2\delta_{n0}$$
    $$\frac{1}{l}\int_{-l}^{l}1\cdot\sin\frac{n\pi x}{l}\,dx=0$$
  - δ 的定义：
    $$\delta_{nm}=\begin{cases}1, & n=m\\[2pt] 0, & n\neq m\end{cases}$$
- 例题/作业：无
- 图：无
- ⚠️存疑：文字写"其中符号 δ_m 的定义为"，但紧随其后的符号实际是 **δ_{nm}**（双下标），二者不一致；按图原文照录，未改动。

## p6 ｜ §5.1·展开系数公式
- 标题行：（红色小标题）推出实变函数傅里叶级数的系数
- 中文要点：如果 l 是一个具有长度量纲的物理量，那么傅里叶展开式就是周期函数 f(x) 按空间变量 x 展开的傅里叶级数。
- 公式（本页只给结果，无推导）：
  $$a_{0}=\frac{1}{2l}\int_{-l}^{l}f(x)\,dx$$
  $$a_{n}=\frac{1}{l}\int_{-l}^{l}f(x)\cos\frac{n\pi x}{l}\,dx\quad(n\neq0)$$
  $$b_{n}=\frac{1}{l}\int_{-l}^{l}f(x)\sin\frac{n\pi x}{l}\,dx$$
- 例题/作业：无
- 图：无
- ⚠️存疑：无（注意 a₀ 分母是 **2l**，aₙ、bₙ 分母是 **l**）

## p7 ｜ §5.1·实数形式级数小结
- 标题行：实数形式的傅里叶级数
- 中文要点：设 f(x) 是一个以 2l 为周期的函数，即：…则可以把它展开成如下形式的傅里叶级数：…
- 公式（展开式 + 三个系数同页，作为小结）：
  $$f(x)=f(x+2l)$$
  $$f(x)=a_{0}+\sum_{n=1}^{\infty}\left[a_{n}\cos\frac{n\pi x}{l}+b_{n}\sin\frac{n\pi x}{l}\right]$$
  $$a_{0}=\frac{1}{2l}\int_{-l}^{l}f(x)\,dx,\qquad a_{n}=\frac{1}{l}\int_{-l}^{l}f(x)\cos\frac{n\pi x}{l}\,dx\ (n\neq0),\qquad b_{n}=\frac{1}{l}\int_{-l}^{l}f(x)\sin\frac{n\pi x}{l}\,dx$$
- 例题/作业：无
- 图：无
- ⚠️存疑：无

## p8 ｜ §5.1·奇偶函数的级数形式
- 标题行：（红字）如果 f(x) 是偶函数，则 ／（红字）如果 f(x) 是奇函数，则
- 中文要点：如果 f(x) 是偶函数，则…；如果 f(x) 是奇函数，则…
- 公式：
  - 偶函数（只余余弦项，系数分母变 l、区间缩到 [0,l] 并乘 2）：
    $$f(x)=a_{0}+\sum_{n=1}^{\infty}a_{n}\cos\frac{n\pi x}{l},\qquad a_{n}=\frac{2}{l}\int_{0}^{l}f(x)\cos\frac{n\pi x}{l}\,dx\quad(n\neq0)$$
  - 奇函数（只余正弦项）：
    $$f(x)=\sum_{n=1}^{\infty}b_{n}\sin\frac{n\pi x}{l},\qquad b_{n}=\frac{2}{l}\int_{0}^{l}f(x)\sin\frac{n\pi x}{l}\,dx$$
- 例题/作业：无
- 图：无
- ⚠️存疑：偶函数一栏的 a₀ 本页未另写公式（沿用 p6 的 1/(2l)∫_{-l}^{l}，等价于 1/l∫₀^l）；图上只有 aₙ 的公式，未写 a₀ 的 2/l 形式。

## p9 ｜ §5.1·引入波数改写
- 标题行：（无独立标题，承 p7 的"实数形式的傅里叶级数"）引入波数：
- 中文要点：引入波数：…则可以把 f(x)=… 改写为：…其中系数为：…以后将看到，在研究有限长度细杆的振动或热传导等问题时，通常使用以上两式的傅里叶级数展开。
- 公式：
  $$k_{n}=n\pi/l\quad(n=0,1,2,\dots)$$
  $$f(x)=a_{0}+\sum_{n=1}^{\infty}\left[a_{n}\cos(k_{n}x)+b_{n}\sin(k_{n}x)\right]$$
  $$a_{0}=\frac{1}{2l}\int_{-l}^{l}f(x)\,dx,\qquad a_{n}=\frac{1}{l}\int_{-l}^{l}f(x)\cos(k_{n}x)\,dx\ (n\neq0),\qquad b_{n}=\frac{1}{l}\int_{-l}^{l}f(x)\sin(k_{n}x)\,dx$$
- 例题/作业：无
- 图：无（有红色虚线箭头把改写后的 cos(kₙx)、sin(kₙx) 分别指向原式的 nπx/l）
- ⚠️存疑：无

## p10 ｜ §5.1·改为时间变量（周期信号）
- 标题行：（无独立标题）如果令 ω=2π/l, t=x/2（ω 为基波角频率），则式：
- 中文要点：如果令 ω=2π/l, t=x/2（ω 为基波角频率），则式：…变为…其中 ωₙ=nω，展开系数为：…T=2π/ω 为周期。这样，可以把 f(t) 看成是一个随时间变化的周期函数，上式为该函数的傅里叶级数展开。由此可以看出，任何一个随时间周期性变化的信号(如方波、锯齿波等)都可以分解(变换)成直流、基波及高次谐波成份之和。
- 公式：
  - 代换关系（本页的设定）：
    $$\omega=\frac{2\pi}{l},\qquad t=\frac{x}{2},\qquad \omega_{n}=n\omega,\qquad T=\frac{2\pi}{\omega}$$
  - 周期信号展开式（红字"周期信号"）：
    $$f(t)=a_{0}+\sum_{n=1}^{\infty}\left[a_{n}\cos(\omega_{n}t)+b_{n}\sin(\omega_{n}t)\right]$$
  - 系数（各自标注物理含义）：
    $$a_{0}=\frac{1}{T}\int_{-T/2}^{T/2}f(t)\,dt\quad\longrightarrow\ \text{直流系数}$$
    $$a_{n}=\frac{2}{T}\int_{-T/2}^{T/2}f(t)\cos(\omega_{n}t)\,dt\quad(n\neq0)\ \longrightarrow\ \text{余弦分量系数}$$
    $$b_{n}=\frac{2}{T}\int_{-T/2}^{T/2}f(t)\sin(\omega_{n}t)\,dt\quad\longrightarrow\ \text{正弦分量系数}$$
- 例题/作业：无
- 图：无
- ⚠️存疑：无（`t=x/2` 已放大核对，确为 x/2；与 ωₙt=n(2π/l)(x/2)=nπx/l、T=l、x∈[−l,l]↔t∈[−T/2,T/2] 自洽）

## p11 ｜ §5.1·改为 θ=πx/l（2π 周期）
- 标题行：（无独立标题）如果令 θ=πx/l，则式：
- 中文要点：如果令 θ=πx/l，则式：…变为…其中展开系数为：…这样，可以把上式看成是以 2π 为周期的函数 f(θ) 的傅里叶级数展开。
- 公式：
  $$\theta=\frac{\pi x}{l}$$
  $$f(\theta)=a_{0}+\sum_{n=1}^{\infty}\left[a_{n}\cos n\theta+b_{n}\sin n\theta\right]$$
  $$a_{0}=\frac{1}{2\pi}\int_{-\pi}^{\pi}f(\theta)\,d\theta,\qquad a_{n}=\frac{1}{\pi}\int_{-\pi}^{\pi}f(\theta)\cos n\theta\,d\theta\ (n\neq0),\qquad b_{n}=\frac{1}{\pi}\int_{-\pi}^{\pi}f(\theta)\sin n\theta\,d\theta$$
- 例题/作业：无
- 图：无
- ⚠️存疑：无

## p12 ｜ §5.1·例题·例1（锯齿函数）
- 标题行：例1 将右图所示的锯齿函数 … 展开成傅里叶级数。
- 中文要点：例1 将右图所示的锯齿函数 f(x)=… 展开成傅里叶级数。解：根据傅里叶展开系数的公式，先求系数
- 公式（题面 + 解答全过程）：
  - 题面函数（分段定义，含周期延拓）：
    $$f(x)=\begin{cases}-\dfrac{x}{l}, & -l\leq x\leq l\\[4pt] f(x+2l) & \end{cases}$$
  - a₀：
    $$a_{0}=\frac{1}{2l}\int_{-l}^{l}f(x)\,dx=\frac{1}{2l}\int_{-l}^{l}\left(-\frac{x}{l}\right)dx=0$$
  - aₙ（n≥1）：
    $$a_{n}=\frac{1}{l}\int_{-l}^{l}f(x)\cos\frac{n\pi x}{l}\,dx=\frac{1}{l}\int_{-l}^{l}\left(-\frac{x}{l}\right)\cos\frac{n\pi x}{l}\,dx=0\quad(n\geq1)$$
  - bₙ（分部积分，中间步骤用 dcos 写法）：
    $$b_{n}=\frac{1}{l}\int_{-l}^{l}f(x)\sin\frac{n\pi x}{l}\,dx=\frac{1}{l}\int_{-l}^{l}\left(-\frac{x}{l}\right)\sin\frac{n\pi x}{l}\,dx=\frac{1}{n\pi l}\int_{-l}^{l}x\,d\cos\frac{n\pi x}{l}=\frac{2(-1)^{n}}{n\pi}$$
  - 结果（蓝箭头标出）：
    $$f(x)=\sum_{n=1}^{m}\frac{2(-1)^{n}}{n\pi}\sin\left(\frac{n\pi x}{l}\right)\qquad(-l\leq x\leq l)$$
- 例题/作业：见上，本题为完整解答（a₀、aₙ、bₙ 三步全给）。
- 图：图 5-1，右上角灰底坐标图。横轴 x，刻度依次标 −2l、−l、0、l、2l；纵轴 f(x)，刻度标 1、−1。实线为过原点的直线段，在 x=−l 处取 f=1、在 x=l 处取 f=−1（斜率 −1/l）；两侧用虚线延续同样的斜线表示周期延拓，虚线在 x=−2l、2l 处穿过相应水平。
- ⚠️存疑：结果里上限写的是 **m**（不是 ∞），与本页"先求系数"的写法配套（m 应为部分和阶数，p14 用 m=1,2,3,24 画图）；课件未说明 m 的含义。

## p13 ｜ §5.1·例题·例2（对称方波）
- 标题行：例2 将右图所示的对称方波 … 展开成傅里叶级数。
- 中文要点：例2 将右图所示的对称方波 f(x)=… 展开成傅里叶级数。解：根据傅里叶展开系数的公式，先求系数
- 公式：
  - 题面函数（振幅 ±π/4）：
    $$f(x)=\begin{cases}\pi/4, & 0<x<\pi\\[2pt] -\pi/4, & -\pi<x<0\end{cases}$$
  - 三个系数（**本页全部只写到"= ?"，未演算**）：
    $$a_{0}=\frac{1}{2l}\int_{-l}^{l}f(x)\,dx=\;?$$
    $$a_{n}=\frac{1}{l}\int_{-l}^{l}f(x)\cos\frac{n\pi x}{l}\,dx=\;?\qquad(n\geq1)$$
    $$b_{n}=b_{n}=\frac{1}{l}\int_{-l}^{l}f(x)\sin\frac{n\pi x}{l}\,dx=\;?$$
  - 结果（蓝箭头标出）：
    $$f(x)=\sum_{n=1}^{m}\frac{\sin(2n-1)x}{2n-1}\qquad(-\pi<x<\pi)$$
- 例题/作业：见上。注意本题系数留空（"= ?"），只给最终级数，中间推导由学生补。
- 图：右上角灰底坐标图，纵轴标 f，横轴刻度 −3、−2、−1、1、2、3，纵轴刻度 0.25、0.5、0.75、−0.25、−0.5、−0.75；**但曲线未绘出（图框内只有坐标轴，空白）**。
- ⚠️存疑：① 第三行课件原文写成 **"b_n = b_n ="**（重复了一遍，疑似笔误）；② 结果式分母为 2n−1、无 π/4 前置因子；③ 题面定义在 (−π,π)，须取 l=π，但页内 aₙ、bₙ 公式仍写 l，未说明 l=π。

## p14 ｜ §5.1·例2 的部分和图示
- 标题行：（无标题，四张图，标注 m=1、m=2、m=3、m=24）
- 中文要点：无（纯图页）
- 公式：无（图为 p13 结果式取 m=1,2,3,24 的部分和）
- 例题/作业：无（承接 p13 例2）
- 图：四张灰底坐标图，纵轴名分别为 s1、S2、S3、S24；横轴刻度均为 −3、−2、−1、1、2、3。红字标注 m=1、m=2、m=3、m=24。
  - m=1：单峰正弦状，峰值 1、谷值约 −1（纵轴刻度 1、0.5、−0.5、−1）；
  - m=2：双峰，峰高约 0.85，两峰间有凹谷约 0.6，纵轴刻度 0.75、0.5、0.25、−0.25、−0.5、−0.75；
  - m=3：三峰，平顶已较接近方波，纵轴刻度 0.75、0.5、0.25、−0.25、−0.5、−0.75；
  - m=24：接近方波，但跳变处与两端出现明显振荡（Gibbs 现象），纵轴刻度 0.75、0.5、0.25、−0.25、−0.5、−0.75。
- ⚠️存疑：四张图横轴范围只到 ±3，与题面区间 (−π,π)≈(−3.14,3.14) 接近但不完全等同；图未标出坐标轴原点符号。

## p15 ｜ §5.1·(2) 复数形式的傅里叶级数
- 标题行：2、复数形式的傅里叶级数
- 中文要点：也可以把一个周期性变化的函数展开成复数形式的傅里叶级数。选取复指数函数族 … 为基函数族，则可以把一个周期变化为 2l 的函数 f(x) 表示为：… 其中 kₙ=nπ/l 为波数。利用基函数族的正交性，… 则展开系数：… （红字）尽管 f(x) 为实数，但其傅里叶展开系数有可能是复数。
- 公式：
  - 基函数族：
    $$\varphi_{n}(x)=e^{in\pi x/l}\quad(n=0,\pm1,\pm2,\dots)$$
  - 展开式（系数下标从 −∞ 到 ∞）：
    $$f(x)=\sum_{n=-\infty}^{\infty}c_{n}e^{ik_{n}x},\qquad k_{n}=n\pi/l$$
  - 基函数族正交性（本页的关键归一化：1/(2l)）：
    $$\frac{1}{2l}\int_{-l}^{l}\varphi_{n}^{*}(x)\varphi_{m}(x)\,dx=\delta_{nm}$$
  - 展开系数：
    $$c_{n}=\frac{1}{2l}\int_{-l}^{l}f(x)e^{-ik_{n}x}\,dx$$
- 例题/作业：无
- 图：无
- ⚠️存疑：无（系数分母 **2l**，与实数形式 aₙ 的 1/l 不同）

## p16 ｜ §5.1·复数形式级数小结（含时间变量版）
- 标题行：傅里叶级数
- 中文要点：傅里叶级数 … 其中 kₙ=nπ/l 为波数 … 则展开系数为：… 若选取基函数族为 …，则 f(t) 可以展开为 … 其中 … 为周期
- 公式：
  - 空间变量版（蓝字）：
    $$f(x)=\sum_{n=-\infty}^{\infty}c_{n}e^{ik_{n}x},\qquad k_{n}=n\pi/l$$
    $$c_{n}=\frac{1}{2l}\int_{-l}^{l}f(x)e^{-ik_{n}x}\,dx$$
  - 时间变量版（红字）：
    $$\varphi_{n}(t)=e^{in\omega t}\quad(n=0,\pm1,\pm2,\dots)$$
    $$f(t)=\sum_{n=-\infty}^{\infty}c_{n}e^{in\omega t}$$
    $$c_{n}=\frac{1}{T}\int_{-T/2}^{T/2}f(t)e^{-in\omega t}\,dt,\qquad T=\frac{2\pi}{\omega}$$
- 例题/作业：无
- 图：无
- ⚠️存疑：无（时间版系数分母是 **T**，空间版是 **2l**，两者不可混用）

## p17 ｜ §5.1·说明（三点）
- 标题行：说明
- 中文要点：
  1. 尽管 f(x) 为实数，但其傅里叶级数展开系数有可能是复数，即基函数族可以为复变函数。
  2. 无论是实数形式的，还是复数形式的傅里叶级数展开，它们只适应于函数 f(x) 在**有限区域**中的展开。
  3. 展开式中的波数 kₙ 或频率 ωₙ，取值是不连续的，即 n=0,1,2,…（实数形式的展开）或 n=0,±1,±2,…（复数形式的展开）。
- 公式：
  $$k_{n}\ \text{或}\ \omega_{n}\ \text{取值不连续}:\quad n=0,1,2,\dots\ (\text{实数形式的展开});\qquad n=0,\pm1,\pm2,\dots\ (\text{复数形式的展开})$$
- 例题/作业：无
- 图：无
- ⚠️存疑：无

## p18 ｜ §5.2 傅里叶变换·(1) 实数形式的傅里叶积分变换
- 标题行：§ 5.2 傅里叶变换（页内二级标题"1、实数形式的傅里叶积分变换"）
- 中文要点：傅里叶积分定理：设函数 f(x) 是区间 [-∞, ∞] 上的非周期函数，而且是分段光滑的，如果积分 ∫_{-∞}^{∞}|f(x)|dx 存在，则 f(x) 可以表示成如下傅里叶积分：… 其中傅里叶变换系数为：… 上式即为实数形式的傅里叶变换式。
- 公式：
  - 定理条件里的绝对可积：
    $$\int_{-\infty}^{\infty}|f(x)|\,dx\ \text{存在}$$
  - 傅里叶积分（本页主结果，注意两个积分都从 0 起）：
    $$f(x)=\int_{0}^{\infty}A(k)\cos(kx)\,dk+\int_{0}^{\infty}B(k)\sin(kx)\,dk$$
  - 变换系数（各带 1/π，对 x 从 −∞ 到 ∞）：
    $$A(k)=\frac{1}{\pi}\int_{-\infty}^{\infty}f(x)\cos(kx)\,dx,\qquad B(k)=\frac{1}{\pi}\int_{-\infty}^{\infty}f(x)\sin(kx)\,dx$$
- 例题/作业：无
- 图：无
- ⚠️存疑：定理中的区间原文写作"[-∞, ∞]"，用了闭区间方括号（通常应写 (−∞,∞)），照录不改。

## p19 ｜ §5.2·傅里叶积分定理的证明（开端）
- 标题行：（无独立标题）傅里叶级数展开式：／傅里叶积分变换式：
- 中文要点：傅里叶级数展开式：… 傅里叶积分变换式：…（红字）求和——求积分，f(x) 的区域 [-l, l] → [-∞, ∞]。证明：引入 Δkₙ=k_{n+1}−kₙ=π/l，则当 l→∞ 时，有 Δkₙ→0。对于 a₀，由于积分 ∫_{-∞}^{∞}f(x)dx 有限，则当 l→∞ 时，有 a₀=…→0
- 公式：
  - 对照用的级数展开式：
    $$f(x)=a_{0}+\sum_{n=1}^{\infty}\left[a_{n}\cos(k_{n}x)+b_{n}\sin(k_{n}x)\right]$$
  - 对照用的积分式：
    $$f(x)=\int_{0}^{\infty}A(k)\cos(kx)\,dk+\int_{0}^{\infty}B(k)\sin(kx)\,dk$$
  - 波数步长（本页证明的关键）：
    $$\Delta k_{n}=k_{n+1}-k_{n}=\pi/l$$
  - a₀ 的消失：
    $$a_{0}=\lim_{l\to\infty}\frac{1}{2l}\int_{-l}^{l}f(x)\,dx\to0$$
  - aₙ 求和改写（先凑 1/π，再乘 Δkₙ 以便取积分）：
    $$\sum_{n=1}^{\infty}a_{n}\cos(k_{n}x)=\lim_{l\to\infty}\sum_{n=1}^{\infty}\left[\frac{1}{l}\int_{-l}^{l}f(\zeta)\cos(k_{n}\zeta)\,d\zeta\right]\cos(k_{n}x)$$
    $$=\lim_{l\to\infty}\sum_{n=1}^{\infty}\left[\frac{1}{\pi}\int_{-l}^{l}f(\zeta)\cos(k_{n}\zeta)\,d\zeta\right]\cos(k_{n}x)\,\Delta k_{n}$$
- 例题/作业：无
- 图：无
- ⚠️存疑：无

## p20 ｜ §5.2·证明续（求和→积分）
- 标题行：（无标题，承接 p19 的推导）
- 中文要点：由于当 l→∞ 时，有 Δkₙ=π/l→0，即 k 变为连续变量，则根据积分定义，有… 同理，… 这样，在 l→∞ 时，傅里叶级数展开式就变成了积分式了。
- 公式：
  - cos 项的极限（得 A(k)）：
    $$\sum_{n=1}^{\infty}a_{n}\cos(k_{n}x)=\int_{0}^{\infty}\left[\frac{1}{\pi}\int_{-\infty}^{\infty}f(\zeta)\cos(k\zeta)\,d\zeta\right]\cos(kx)\,dk\equiv\int_{0}^{\infty}A(k)\cos(kx)\,dk$$
  - "同理"一句给出的 bₙ 起点：
    $$\sum_{n=1}^{\infty}b_{n}\sin(k_{n}x)=\lim_{l\to\infty}\sum_{n=1}^{\infty}\left[\frac{1}{l}\int_{-l}^{l}f(\zeta)\sin(k_{n}\zeta)\,d\zeta\right]\sin(k_{n}x)$$
  - 其后的两行（原文如此，仍写 cos）：
    $$=\int_{0}^{\infty}\left[\frac{1}{\pi}\int_{-\infty}^{\infty}f(\zeta)\cos(k\zeta)\,d\zeta\right]\cos(kx)\,dk$$
    $$\equiv\int_{0}^{\infty}B(k)\sin(kx)\,dk$$
- 例题/作业：无
- 图：无
- ⚠️存疑：**课件原文第二、三行把 cos 的整段式子照抄到"同理"的 bₙ（sin）推导中**，sin 被写成 cos；末行才写回 $B(k)\sin(kx)dk$。此处按图原样转写，不代改。

## p21 ｜ §5.2·变换存在条件与第一类间断点
- 标题行（绿框）：傅里叶积分变换 ／ 其中傅里叶变换系数为：
- 中文要点（红字标重点）：傅里叶变换存在的条件：函数 f(x) 在 (−∞,∞) 区间内**绝对可积**，即积分 ∫_{-∞}^{∞}|f(x)|dx **收敛**；函数 f(x) 在任意有限区间内满足狄里希利条件，即 f(x) **分段光滑**，且**至多具有第一类间断点**。第一类间断点：f(x) 在 x₀ 点不连续，但其左极限 f(x₀−0) 和右极限 f(x₀+0) 都存在且为有限值
- 公式：
  $$f(x)=\int_{0}^{\infty}A(k)\cos(kx)\,dk+\int_{0}^{\infty}B(k)\sin(kx)\,dk$$
  $$A(k)=\frac{1}{\pi}\int_{-\infty}^{\infty}f(x)\cos(kx)\,dx,\qquad B(k)=\frac{1}{\pi}\int_{-\infty}^{\infty}f(x)\sin(kx)\,dx$$
  $$\int_{-\infty}^{\infty}|f(x)|\,dx\ \text{收敛}$$
- 例题/作业：无
- 图：无
- ⚠️存疑：无

## p22 ｜ §5.2·正弦/余弦积分公式
- 标题行（绿框）：傅里叶积分变换 ／ 其中傅里叶变换系数为：
- 中文要点：如果 f(x) 是**奇函数**，则 A(k)=0，（红字）傅里叶正弦积分公式；如果 f(x) 是**偶函数**，则 B(k)=0，（红字）傅里叶余弦积分公式
- 公式（与 p18/p21 相同的总式与系数，作为对照）：
  $$f(x)=\int_{0}^{\infty}A(k)\cos(kx)\,dk+\int_{0}^{\infty}B(k)\sin(kx)\,dk$$
  $$A(k)=\frac{1}{\pi}\int_{-\infty}^{\infty}f(x)\cos(kx)\,dx,\qquad B(k)=\frac{1}{\pi}\int_{-\infty}^{\infty}f(x)\sin(kx)\,dx$$
  - 奇函数 → 正弦积分公式（系数变 **2/π**、区间缩到 0..∞）：
    $$f(x)=\int_{0}^{\infty}B(k)\sin(kx)\,dk,\qquad B(k)=\frac{2}{\pi}\int_{0}^{\infty}f(x)\sin(kx)\,dx$$
  - 偶函数 → 余弦积分公式：
    $$f(x)=\int_{0}^{\infty}A(k)\cos(kx)\,dk,\qquad A(k)=\frac{2}{\pi}\int_{0}^{\infty}f(x)\cos(kx)\,dx$$
- 例题/作业：无
- 图：两个蓝色粗箭头分别指向正弦/余弦公式组
- ⚠️存疑：无（此处系数为 2/π，注意与 p18 的 1/π 区分）

## p23 ｜ §5.2·时间变量版与级数/积分之区别
- 标题行：（无标题）如果 f(t) 是一个随时间变量 t 变化的非周期函数，则有：
- 中文要点：如果 f(t) 是一个随时间变量 t 变化的非周期函数，则有：…其中：…通常称 A(ω) 和 B(ω) 为谱函数，ω 为圆频率。（红字）傅里叶积分变换与傅里叶级数展开的区别：傅里叶级数展开——有界区域，波数或者频率取值是离散的；傅里叶积分变换——无界区域，波数或者频率取值是连续的
- 公式：
  $$f(t)=\int_{0}^{\infty}A(\omega)\cos(\omega t)\,d\omega+\int_{0}^{\infty}B(\omega)\sin(\omega t)\,d\omega$$
  $$A(\omega)=\frac{1}{\pi}\int_{-\infty}^{\infty}f(t)\cos(\omega t)\,dt,\qquad B(\omega)=\frac{1}{\pi}\int_{-\infty}^{\infty}f(t)\sin(\omega t)\,dt$$
- 例题/作业：无
- 图：无
- ⚠️存疑：无

## p24 ｜ §5.2·例题·例1（矩形脉冲）
- 标题行：例1 讨论矩形脉冲函数 … 的傅里叶积分变换，其中 T 为脉冲半宽度。
- 中文要点：例1 讨论矩形脉冲函数 f(t)=… 的傅里叶积分变换，其中 T 为脉冲半宽度。解：由于 f(t) 是偶函数，则 B(ω)=0… 特别当 t=0 及 T=1 时，可以得到：…（红字）这与前面用留数定理得到的结果一致
- 公式：
  - 题面（矩形脉冲，半宽度 T）：
    $$f(t)=\begin{cases}1, & |t|<T\\[2pt] 0, & |t|>T\end{cases}$$
  - 因偶函数只算 A(ω)：
    $$A(\omega)=\frac{2}{\pi}\int_{0}^{\infty}f(t)\cos(\omega t)\,dt=\frac{2}{\pi}\int_{0}^{T}\cos(\omega t)\,dt=\frac{2}{\pi\omega}\sin(\omega T)$$
  - 逆变换回原函数（蓝箭头）：
    $$f(t)=\int_{0}^{\infty}A(\omega)\cos(\omega t)\,d\omega=\frac{2}{\pi}\int_{0}^{\infty}\frac{\sin\omega T}{\omega}\cos\omega t\,d\omega=\begin{cases}1, & |t|<T\\[2pt] 0, & |t|>T\end{cases}$$
  - 特例（t=0、T=1）得到的著名积分：
    $$\int_{0}^{\infty}\frac{\sin\omega}{\omega}\,d\omega=\frac{\pi}{2}$$
- 例题/作业：见上（完整解答）。
- 图：无
- ⚠️存疑：f(t) 在 |t|=T 处未定义（题面只写 <、>），照录。

## p25 ｜ §5.2·例题·例2（截断正弦波，上半）
- 标题行：例2 讨论函数 … 的傅里叶积分变换
- 中文要点：例2 讨论函数 f(t)=… 的傅里叶积分变换。解：由于 f(t) 是奇函数，则 A(ω)=0… 利用 sin(ω₀t)sin(ωt)=…
- 公式：
  - 题面（奇函数，|t|<2Nπ/ω₀ 内为 A sin(ω₀t)）：
    $$f(t)=\begin{cases}A\sin(\omega_{0}t), & |t|<2N\pi/\omega_{0}\\[2pt] 0, & |t|>2N\pi/\omega_{0}\end{cases}$$
  - B(ω) 的积分：
    $$B(\omega)=\frac{2}{\pi}\int_{0}^{\infty}f(t)\sin(\omega t)\,dt=\frac{2}{\pi}\int_{0}^{2N\pi/\omega_{0}}A\sin(\omega_{0}t)\sin(\omega t)\,dt$$
  - 积化和差（本页用的工具式）：
    $$\sin(\omega_{0}t)\sin(\omega t)=\frac{1}{2}\left[\cos(\omega_{0}t-\omega t)-\cos(\omega_{0}t+\omega t)\right]$$
  - 代入后逐项积分：
    $$B(\omega)=\frac{A}{\pi}\int_{0}^{2N\pi/\omega_{0}}\left[\cos(\omega_{0}t-\omega t)-\cos(\omega_{0}t+\omega t)\right]dt$$
    $$=\frac{A}{\pi}\left[\frac{1}{\omega_{0}-\omega}\sin(\omega_{0}t-\omega t)\Big|_{0}^{2N\pi/\omega_{0}}-\frac{1}{\omega_{0}+\omega}\sin(\omega_{0}t+\omega t)\Big|_{0}^{2N\pi/\omega_{0}}\right]$$
    $$=\frac{A}{\pi}\left[\frac{1}{\omega_{0}-\omega}\sin\left(2N\pi-\frac{2N\pi\omega}{\omega_{0}}\right)-\frac{1}{\omega_{0}+\omega}\sin\left(2N\pi+\frac{2N\pi\omega}{\omega_{0}}\right)\right]$$
- 例题/作业：见上（本页为解答前半）。
- 图：无
- ⚠️存疑：**N 在题面中未定义**（只出现在区间 2Nπ/ω₀ 里），课件没说明它是什么；按原文保留。

## p26 ｜ §5.2·例2 续（和差化积与结果）
- 标题行：（无标题，继续例2）
- 中文要点：利用 … 则 … 
- 公式：
  - 把 sin(2Nπ∓…) 展开：
    $$\sin\left(2N\pi-\frac{2N\pi\omega}{\omega_{0}}\right)=\sin(2N\pi)\cos\left(\frac{2N\pi\omega}{\omega_{0}}\right)-\cos(2N\pi)\sin\left(\frac{2N\pi\omega}{\omega_{0}}\right)$$
    $$\sin\left(2N\pi+\frac{2N\pi\omega}{\omega_{0}}\right)=\sin(2N\pi)\cos\left(\frac{2N\pi\omega}{\omega_{0}}\right)+\cos(2N\pi)\sin\left(\frac{2N\pi\omega}{\omega_{0}}\right)$$
  - 合并（sin2Nπ=0、cos2Nπ=1）：
    $$B(\omega)=\frac{A}{\pi}\frac{1}{\omega_{0}-\omega}\left[\sin(2N\pi)\cos\left(\frac{2N\pi\omega}{\omega_{0}}\right)-\cos(2N\pi)\sin\left(\frac{2N\pi\omega}{\omega_{0}}\right)\right]$$
    $$-\frac{A}{\pi}\frac{1}{\omega_{0}+\omega}\left[\sin(2N\pi)\cos\left(\frac{2N\pi\omega}{\omega_{0}}\right)+\cos(2N\pi)\sin\left(\frac{2N\pi\omega}{\omega_{0}}\right)\right]$$
    $$=-\frac{A}{\pi}\sin\left(\frac{2N\pi\omega}{\omega_{0}}\right)\left[\frac{1}{\omega_{0}-\omega}+\frac{1}{\omega_{0}+\omega}\right]=\frac{2A}{\pi}\frac{\omega_{0}}{\omega^{2}-\omega_{0}^{2}}\sin\left(\frac{2N\pi\omega}{\omega_{0}}\right)$$
  - 最终积分表达式（蓝箭头）：
    $$f(t)=\int_{0}^{\infty}B(\omega)\sin\omega t\,d\omega=\frac{2A\omega_{0}}{\pi}\int_{0}^{\infty}\frac{1}{\omega^{2}-\omega_{0}^{2}}\sin\left(\frac{2N\pi\omega}{\omega_{0}}\right)\sin\omega t\,d\omega$$
- 例题/作业：见上（例2 解答完成）。
- 图：无
- ⚠️存疑：无

## p27 ｜ §5.2·(2) 复数形式的傅里叶变换
- 标题行：2、复数形式的傅里叶变换
- 中文要点：利用欧拉公式：… 则 … 由于 …
- 公式：
  - 起点（实数形式）：
    $$f(x)=\int_{0}^{\infty}A(k)\cos(kx)\,dk+\int_{0}^{\infty}B(k)\sin(kx)\,dk$$
  - 欧拉公式（本页工具）：
    $$\cos(kx)=\frac{1}{2}\left(e^{ikx}+e^{-ikx}\right),\qquad \sin(kx)=\frac{1}{2i}\left(e^{ikx}-e^{-ikx}\right)$$
  - 代入并整理：
    $$f(x)=\int_{0}^{\infty}A(k)\frac{1}{2}\left(e^{ikx}+e^{-ikx}\right)dk+\int_{0}^{\infty}B(k)\frac{1}{2i}\left(e^{ikx}-e^{-ikx}\right)dk$$
    $$=\frac{1}{2}\int_{0}^{\infty}\left[A(k)-iB(k)\right]e^{ikx}dk+\frac{1}{2}\int_{0}^{\infty}\left[A(k)+iB(k)\right]e^{-ikx}dk$$
  - 系数的奇偶性（为下一步换 k→−k 做准备）：
    $$A(-k)=\frac{1}{\pi}\int_{-\infty}^{\infty}f(x)\cos(-kx)\,dx=\frac{1}{\pi}\int_{-\infty}^{\infty}f(x)\cos(kx)\,dx=A(k)$$
    $$B(-k)=\frac{1}{\pi}\int_{-\infty}^{\infty}f(x)\sin(-kx)\,dx=-\frac{1}{\pi}\int_{-\infty}^{\infty}f(x)\sin(kx)\,dx=-B(k)$$
- 例题/作业：无
- 图：无
- ⚠️存疑：无

## p28 ｜ §5.2·复数形式续（换 k→−k 合并）
- 标题行：（无标题，承接 p27 的式子）
- 中文要点：将上式右边第二项积分中的 k 换成 −k，并利用 A(−k)=A(k) 及 B(−k)=−B(k)，则得到
- 公式：
  - 起始式：
    $$f(x)=\frac{1}{2}\int_{0}^{\infty}\left[A(k)-iB(k)\right]e^{ikx}dk+\frac{1}{2}\int_{0}^{\infty}\left[A(k)+iB(k)\right]e^{-ikx}dk$$
  - 换元（第二项取 k→−k，含 d(−k)）：
    $$f(x)=\frac{1}{2}\int_{0}^{\infty}\left[A(k)-iB(k)\right]e^{ikx}dk-\frac{1}{2}\int_{0}^{-\infty}\left[A(-k)-iB(-k)\right]e^{i(-k)x}d(-k)$$
  - 用奇偶性化简：
    $$=\frac{1}{2}\int_{0}^{\infty}\left[A(k)-iB(k)\right]e^{ikx}dk-\frac{1}{2}\int_{0}^{-\infty}\left[A(k)-iB(k)\right]e^{ikx}dk$$
  - 翻转限：
    $$=\frac{1}{2}\int_{0}^{\infty}\left[A(k)-iB(k)\right]e^{ikx}dk+\frac{1}{2}\int_{-\infty}^{0}\left[A(k)-iB(k)\right]e^{ikx}dk$$
  - 合并成一个积分：
    $$=\frac{1}{2}\int_{-\infty}^{\infty}\left[A(k)-iB(k)\right]e^{ikx}dk\equiv\int_{-\infty}^{\infty}F(k)e^{ikx}dk$$
- 例题/作业：无
- 图：无
- ⚠️存疑：无（第二项积分限为 0→−∞，第三行起变为 ∫_{-∞}^{0} 并带正号，原文如此）

## p29 ｜ §5.2·复数形式的变换对与正逆变换的核
- 标题行：（无标题）即：
- 中文要点：即：… 其中 … 由于 … （绿框右）两式就是函数 f(x) 对空间变量 x 的复数形式的傅里叶变化关系式，k 为波数。（红字）通常称 f(x) 是原函数，对应的积分式为正变换，其变换的核为 e^{ikx}；称 F(k) 为像函数，对应的式子为逆变换，其变换的核为 e^{−ikx}。
- 公式：
  $$f(x)=\int_{-\infty}^{\infty}F(k)e^{ikx}dk,\qquad F(k)=\frac{1}{2}\left[A(k)-iB(k)\right]$$
  $$A(k)=\frac{1}{\pi}\int_{-\infty}^{\infty}f(x)\cos(kx)\,dx,\qquad B(k)=\frac{1}{\pi}\int_{-\infty}^{\infty}f(x)\sin(kx)\,dx$$
  $$F(k)=\frac{1}{2\pi}\int_{-\infty}^{\infty}f(x)\left[\cos(kx)-i\sin(kx)\right]dx=\frac{1}{2\pi}\int_{-\infty}^{\infty}f(x)e^{-ikx}dx$$
  - 绿框内的"变换对"（本页核心结论）：
    $$f(x)=\int_{-\infty}^{\infty}F(k)e^{ikx}dk,\qquad F(k)=\frac{1}{2\pi}\int_{-\infty}^{\infty}f(x)e^{-ikx}dx$$
- 例题/作业：无
- 图：无（绿底框为公式框）
- ⚠️存疑：**课件在此把话说反了**：文字称 f(x) 的积分为"正变换"、核为 e^{ikx}，称 F(k) 的式子为"逆变换"、核为 e^{−ikx}；而教科书惯例是 F(k)=…e^{−ikx} 为正变换。按原文照录，此处语义疑有笔误（核的指认与"正/逆"标签可能互换）。

## p30 ｜ §5.2·时间变量版的复数变换与系数约定
- 标题行：（无标题）而对于时间变量 t 的傅里叶变换，通常表示为：
- 中文要点：而对于时间变量 t 的傅里叶变换，通常表示为：… 其中 ω 为圆频率。与空间 x 的傅里叶变化不同的是：在正变换核中核为 e^{−iωt}，而在逆变换中核则为 e^{iωt}。注意：在傅里叶变换中，系数 1/(2π) 可以放在正变换积分或反变换积分的前面，也可以在正反两个变换积分前各放 1/√(2π)，但需保证两个系数的乘积为 1/(2π)。
- 公式：
  - 绿框内的变换对：
    $$f(t)=\int_{-\infty}^{\infty}F(\omega)e^{-i\omega t}d\omega,\qquad F(\omega)=\frac{1}{2\pi}\int_{-\infty}^{\infty}f(t)e^{i\omega t}dt$$
  - 系数约定（原文）：可放 1/(2π) 于任一侧，或两侧各放 1/√(2π)：
    $$\text{两侧各放 }\frac{1}{\sqrt{2\pi}},\qquad \text{两系数乘积 }=\frac{1}{2\pi}$$
- 例题/作业：无
- 图：无（绿底框为公式框）
- ⚠️存疑：本页时间变量版把 e^{−iωt} 放进 f(t) 的积分、把 e^{+iωt} 放进 F(ω) 的积分，与 p29 空间变量版的指数符号相反；课件明确以"与空间 x 的不同"来解释，照录。另：注意本页时间版的正变换核写作 e^{−iωt}，而 p29 空间版的正变换（F(k)）核实为 e^{−ikx}，两页文字自相矛盾（见 p29 存疑）。

## p31 ｜ §5.2·二维与三维的变换式
- 标题行：（无标题）对于一个随坐标 x 及时间 t 变化的物理量 f(x,t)，其傅里叶变换为
- 中文要点：对于一个**随坐标 x 及时间 t 变化**的物理量 f(x,t)，其傅里叶变换为 … 其中像函数为：… 更一般地，如果 f(r,t) 是一个在**三维无界空间中随时间变化**的函数，则它的傅里叶变换式为：… 其中 r=xe_x+ye_y+ze_z 是三维空间中的位置矢量，dr=dxdydz 及 k=k_xe_x+k_ye_y+k_ze_z 是三维空间中的波矢量，dk=dk_xdk_ydk_z
- 公式：
  - 二维 (x,t)（系数 (2π)²）：
    $$f(x,t)=\int_{-\infty}^{\infty}\int_{-\infty}^{\infty}F(k,\omega)e^{i(kx-\omega t)}dk\,d\omega,\qquad F(k,\omega)=\frac{1}{(2\pi)^{2}}\int_{-\infty}^{\infty}\int_{-\infty}^{\infty}f(x,t)e^{-i(kx-\omega t)}dx\,dt$$
  - 三维 (r,t)（系数 (2π)⁴），两个式子分别用三重积分号加 ∫_{−∞}^{∞}：
    $$f(\mathbf{r},t)=\iiint\!\!\int_{-\infty}^{\infty}F(\mathbf{k},\omega)e^{i(\mathbf{k}\cdot\mathbf{r}-\omega t)}d\omega\,d\mathbf{k},\qquad F(\mathbf{k},\omega)=\frac{1}{(2\pi)^{4}}\iiint\!\!\int_{-\infty}^{\infty}f(\mathbf{r},t)e^{-i(\mathbf{k}\cdot\mathbf{r}-\omega t)}dt\,d\mathbf{r}$$
  - 矢量定义：
    $$\mathbf{r}=x\mathbf{e}_{x}+y\mathbf{e}_{y}+z\mathbf{e}_{z},\quad d\mathbf{r}=dx\,dy\,dz;\qquad \mathbf{k}=k_{x}\mathbf{e}_{x}+k_{y}\mathbf{e}_{y}+k_{z}\mathbf{e}_{z},\quad d\mathbf{k}=dk_{x}dk_{y}dk_{z}$$
- 例题/作业：无
- 图：无
- ⚠️存疑：三维式前出现的是**三重积分号 + 一个 ∫_{−∞}^{∞}**（共四重），系数写 (2π)⁴；与二维式的 (2π)² 对应，照录。积分次序在 f 与 F 两式中相反（dωdk 与 dtdr），照录。

## p32 ｜ §5.2·例题·例3（高斯函数）
- 标题行：例3 求函数 … 的傅里叶积分变换式，其中 a>0
- 中文要点：例3 求函数 f(x)=… 的傅里叶积分变换式，其中 a>0。解：根据复数形式的空间变量的傅里叶变换式有 … 再利用 … 
- 公式：
  - 题面（归一化高斯，注意系数 √(a/π) 与指数 −a²x²/2）：
    $$f(x)=\sqrt{\frac{a}{\pi}}\,e^{-\frac{a^{2}x^{2}}{2}}$$
  - 变换：
    $$F(k)=\frac{1}{2\pi}\sqrt{\frac{a}{\pi}}\int_{-\infty}^{\infty}e^{-\frac{a^{2}x^{2}}{2}}e^{-ikx}dx=\frac{\sqrt{a}}{\pi^{3/2}}\int_{0}^{\infty}e^{-\frac{a^{2}x^{2}}{2}}\cos kx\,dx$$
  - 引用的积分公式（红字）：
    $$\int_{0}^{\infty}e^{-ax^{2}}\cos(bx)\,dx=\frac{1}{2}\sqrt{\frac{\pi}{a}}\,e^{-b^{2}/4a}$$
  - 结果（蓝箭头）：
    $$F(k)=\frac{1}{\pi\sqrt{2a}}\,e^{-\frac{k^{2}}{2a^{2}}}$$
  - 物理注释（原文）：函数 f(x) 相当于一维谐振子在坐标空间中的基态波函数，而 F(k) 则为谐振子在动量空间中的波函数。
- 例题/作业：见上（完整解答）。
- 图：无
- ⚠️存疑：题面指数 −a²x²/2 的负号在渲染中与分式横线相邻，已放大核对为负号（结果式 e^{−k²/(2a²)} 也要求指数为负）；若后续讲义要用，建议再核一次。

## p33 ｜ §5.2·例题·例4（sin ω₀t/πt 与矩形谱互为变换，正向）
- 标题行：例4 求证函数 … 与 … 是一对傅里叶变换
- 中文要点：例4 求证函数 f(t)=sin ω₀t/(πt) 与 F(ω)=… 是一对傅里叶变换。证明：根据复数形式的时间变量的傅里叶变换式有 … 反之，… 采用留数定理来求解无穷积分
- 公式：
  - 题面（一对变换）：
    $$f(t)=\frac{\sin\omega_{0}t}{\pi t},\qquad F(\omega)=\begin{cases}\dfrac{1}{2\pi}, & |\omega|<\omega_{0}\\[4pt] 0, & |\omega|>\omega_{0}\end{cases}$$
  - 第一方向（由 F(ω) 逆变换得 f(t)，矩形谱的积分）：
    $$f(t)=\int_{-\infty}^{\infty}F(\omega)e^{-i\omega t}d\omega=\frac{1}{2\pi}\int_{-\omega_{0}}^{\omega_{0}}e^{-i\omega t}d\omega=-\frac{1}{2\pi}\frac{1}{it}e^{-i\omega t}\Big|_{-\omega_{0}}^{\omega_{0}}=\frac{\sin(\omega_{0}t)}{\pi t}$$
  - 第二方向（正变换，拆成两个指数积分，留待 p34 求）：
    $$F(\omega)=\frac{1}{2\pi}\int_{-\infty}^{\infty}f(t)e^{i\omega t}dt=\frac{1}{2\pi}\int_{-\infty}^{\infty}\frac{\sin\omega_{0}t}{\pi t}e^{i\omega t}dt$$
    $$=\frac{1}{2\pi}\int_{-\infty}^{\infty}\frac{e^{i\omega_{0}t}-e^{-i\omega_{0}t}}{2i\pi t}e^{i\omega t}dt$$
    $$=\frac{1}{2\pi}\int_{-\infty}^{\infty}\frac{1}{2i\pi t}e^{i(\omega_{0}+\omega)t}dt-\frac{1}{2\pi}\int_{-\infty}^{\infty}\frac{1}{2i\pi t}e^{i(\omega-\omega_{0})t}dt$$
- 例题/作业：见上（证明进行中）。注意题面"其中 k 是实常数"属 p59 例1，本页无此句。
- 图：无
- ⚠️存疑：无（红字标出 1/(it) 与 sin(ω₀t)/(πt) 两处）

## p34 ｜ §5.2·例4 续（留数定理求积）
- 标题行：（绿框）留数定理求无穷积分的公式
- 中文要点：同理 … 当 ω+ω₀>0 且 ω−ω₀<0 时，即 |ω|<ω₀ 时，
- 公式：
  - 绿框内的留数公式（含实轴极点项，本页工具）：
    $$\int_{-\infty}^{\infty}f(x)e^{imx}dx=2\pi i\sum_{k}\operatorname{Res}\left[f(z_{k})e^{imz_{k}}\right]_{\text{上半平面}}+\pi i\operatorname{Res}\left[f(b)e^{imb}\right]_{\text{实轴}}$$
  - 第一个积分：
    $$\int_{-\infty}^{\infty}\frac{1}{2i\pi t}e^{i(\omega_{0}+\omega)t}dt=\begin{cases}\pi i\operatorname{Res}\left[\dfrac{1}{2i\pi t}e^{i(\omega_{0}+\omega)t}\right]_{t=0}=\dfrac{1}{2}, & \omega+\omega_{0}>0\\[10pt] -\pi i\operatorname{Res}\left[\dfrac{1}{2i\pi t}e^{i(\omega_{0}+\omega)t}\right]_{t=0}=-\dfrac{1}{2}, & \omega+\omega_{0}<0\end{cases}$$
  - 同理，第二个积分：
    $$\int_{-\infty}^{\infty}\frac{1}{2i\pi t}e^{i(\omega-\omega_{0})t}dt=\begin{cases}\dfrac{1}{2}, & \omega-\omega_{0}>0\\[8pt] -\dfrac{1}{2}, & \omega-\omega_{0}<0\end{cases}$$
  - |ω|<ω₀ 时的合成：
    $$\int_{-\infty}^{\infty}f(t)e^{i\omega t}dt=\int_{-\infty}^{\infty}\frac{1}{2i\pi t}e^{i(\omega_{0}+\omega)t}dt-\int_{-\infty}^{\infty}\frac{1}{2i\pi t}e^{i(\omega-\omega_{0})t}dt=\frac{1}{2}-\left(-\frac{1}{2}\right)=1$$
- 例题/作业：见上（例4 证明续）。
- 图：无
- ⚠️存疑：留数公式的实轴极点项写作 πiRes[…]，∑ 的下标为 k、上标位置无界；按图照录。

## p35 ｜ §5.2·例4 续（三区间讨论与结论）
- 标题行：（无标题，继续例4）
- 中文要点：当 ω+ω₀<0 且 ω−ω₀>0 时，即 ω<−ω₀ 且 ω>ω₀，**此条件是矛盾的**；当 ω+ω₀>0 且 ω−ω₀>0 时，即 ω>ω₀ 时，…；当 ω+ω₀<0 且 ω−ω₀<0 时，即 ω<−ω₀ 时，…；综上，… 得证 f(t) 与 F(ω) 是一对傅里叶变换
- 公式：
  - ω>ω₀：
    $$\int_{-\infty}^{\infty}f(t)e^{i\omega t}dt=\int_{-\infty}^{\infty}\frac{1}{2i\pi t}e^{i(\omega_{0}+\omega)t}dt-\int_{-\infty}^{\infty}\frac{1}{2i\pi t}e^{i(\omega-\omega_{0})t}dt=\frac{1}{2}-\frac{1}{2}=0$$
  - ω<−ω₀：
    $$\int_{-\infty}^{\infty}f(t)e^{i\omega t}dt=\int_{-\infty}^{\infty}\frac{1}{2i\pi t}e^{i(\omega_{0}+\omega)t}dt-\int_{-\infty}^{\infty}\frac{1}{2i\pi t}e^{i(\omega-\omega_{0})t}dt=-\frac{1}{2}-\left(-\frac{1}{2}\right)=0$$
  - 综合结论：
    $$\frac{1}{2\pi}\int_{-\infty}^{\infty}f(t)e^{i\omega t}dt=\begin{cases}\dfrac{1}{2\pi}, & |\omega|<\omega_{0}\\[6pt] 0, & |\omega|>\omega_{0}\end{cases}=F(\omega)$$
- 例题/作业：见上（例4 证明完成）。
- 图：无
- ⚠️存疑：无

## p36 ｜ §5.2·例题·例5（屏蔽库仑势，设置）
- 标题行：例5 在电介质(如等离子体)中…求函数 f(r) 的傅里叶变化
- 中文要点：例5 在电介质(如等离子体)中，带电粒子之间的相互作用势要受到屏蔽，即所谓的屏蔽库仑势 f(r)=…，其中 λ>0 为常数(屏蔽长度)。求函数 f(r) 的傅里叶变化。解：根据三维空间的傅里叶变换，则有 … 在球坐标系中，选取 k 的方向沿 z 轴，并利用 … 则有
- 公式：
  - 题面（屏蔽库仑势）：
    $$f(r)=\frac{1}{r}e^{-r/\lambda},\qquad \lambda>0$$
  - 三维变换：
    $$F(\mathbf{k})=\frac{1}{(2\pi)^{3}}\iiint\frac{e^{-r/\lambda}}{r}e^{-i\mathbf{k}\cdot\mathbf{r}}d\mathbf{r}$$
  - 球坐标下的两个工具式（本页关键）：
    $$d\mathbf{r}=r^{2}dr\sin\theta\,d\theta\,d\varphi,\qquad \mathbf{k}\cdot\mathbf{r}=kr\cos\theta$$
  - 代入后：
    $$F(\mathbf{k})=\frac{1}{(2\pi)^{3}}\int_{0}^{2\pi}d\varphi\int_{0}^{\pi}\sin\theta\,d\theta\int_{0}^{\infty}\frac{e^{-r/\lambda}}{r}e^{-ikr\cos\theta}r^{2}dr$$
- 例题/作业：见上（例5 解答开始）。
- 图：无
- ⚠️存疑：题面写作"求函数 f(r) 的**傅里叶变化**"（"化"字，非"变换"），照录。

## p37 ｜ §5.2·例5 续（角度积分）
- 标题行：（无标题，继续例5）
- 中文要点：（末行）下面采用分步积分法，求解 ∫₀^∞ e^{−r/λ}sin(kr)dr
- 公式（逐步）：
  $$F(\mathbf{k})=\frac{1}{(2\pi)^{3}}\int_{0}^{2\pi}d\varphi\int_{0}^{\pi}\sin\theta\,d\theta\int_{0}^{\infty}\frac{e^{-r/\lambda}}{r}e^{-ikr\cos\theta}r^{2}dr$$
  $$=\frac{1}{4\pi^{2}}\int_{0}^{\infty}e^{-r/\lambda}r\,dr\int_{0}^{\pi}\sin\theta\,e^{-ikr\cos\theta}d\theta$$
  $$=\frac{1}{4\pi^{2}}\int_{0}^{\infty}e^{-r/\lambda}r\,dr\int_{0}^{\pi}e^{-ikr\cos\theta}d(-\cos\theta)$$
  $$=\frac{1}{4\pi^{2}}\int_{0}^{\infty}e^{-r/\lambda}r\,dr\,\frac{1}{ikr}\left(e^{ikr}-e^{-ikr}\right)$$
  $$=\frac{1}{2\pi^{2}k}\int_{0}^{\infty}e^{-r/\lambda}\sin(kr)\,dr$$
- 例题/作业：见上（例5 解答中段）。
- 图：无
- ⚠️存疑：第二个等号把 ∫₀^{2π}dφ 直接算成 2π、并把 r²/r 约掉，系数由 1/(2π)³ 变为 1/(4π²)，照录。

## p38 ｜ §5.2·例5 续（分部积分与像函数）
- 标题行：（无标题，继续例5）
- 中文要点：即 … 像函数为 …
- 公式（两次分部积分，迭代方程）：
  $$\int_{0}^{\infty}e^{-r/\lambda}\sin(kr)\,dr$$
  $$=-\frac{1}{k}\int_{0}^{\infty}e^{-r/\lambda}d\cos(kr)=-\frac{1}{k}\left[e^{-r/\lambda}\cos(kr)\Big|_{0}^{\infty}-\int_{0}^{\infty}\cos(kr)\,de^{-r/\lambda}\right]$$
  $$=-\frac{1}{k}\left[0-1+\frac{1}{\lambda}\int_{0}^{\infty}\cos(kr)e^{-r/\lambda}dr\right]=\frac{1}{k}-\frac{1}{k^{2}\lambda}\int_{0}^{\infty}e^{-r/\lambda}d\sin(kr)$$
  $$=\frac{1}{k}-\frac{1}{k^{2}\lambda}\left[e^{-r/\lambda}\sin(kr)\Big|_{0}^{\infty}-\int_{0}^{\infty}\sin(kr)\,de^{-r/\lambda}\right]$$
  $$=\frac{1}{k}-\frac{1}{k^{2}\lambda^{2}}\int_{0}^{\infty}\sin(kr)e^{-r/\lambda}dr$$
  - 解出积分（本页关键结果）：
    $$\int_{0}^{\infty}e^{-r/\lambda}\sin(kr)\,dr=\frac{k\lambda^{2}}{1+k^{2}\lambda^{2}}$$
  - 像函数：
    $$F(\mathbf{k})=\frac{1}{2\pi^{2}k}\int_{0}^{\infty}e^{-r/\lambda}\sin(kr)\,dr=\frac{1}{2\pi^{2}}\frac{\lambda^{2}}{1+k^{2}\lambda^{2}}$$
- 例题/作业：见上（例5 解答完成）。
- 图：无
- ⚠️存疑：无

## p39 ｜ § 第五章作业（第 1–4 题）
- 标题行：§ 第五章作业
- 中文要点：见下逐题原文
- 公式/题面（逐题照抄）：
  1. 将函数 $f(x)=\cos^{3}x$ 表示成傅里叶级数的形式
  2. 将函数 $f(x)=x/3$ 在 $(-l,\,l)$ 区间内展开成傅里叶级数
  3. 将函数 $f(t)=A|\sin\omega t|$ 在 $(0,\,T)$ 区间内展开成傅里叶级数，其中 A 为常数。
  4. 将矩形波
     $$f(t)=\begin{cases}0, & -T/2\leq t<-T_{0}/2\\[2pt] H, & -T_{0}/2\leq t\leq T_{0}/2\\[2pt] 0, & T_{0}/2<t\leq T/2\end{cases}$$
     在区间内展开为复数形式的傅里叶级数，其中为常数。
- 例题/作业：以上四题即作业，课件未给解答。
- 图：无
- ⚠️存疑：第 4 题两处缺字：① "在区间内"未写出具体区间（按 f(t) 的分段应为 (−T/2, T/2) 或一个周期 T）；② "其中为常数"中的符号在 PDF 文本层与渲染图上都缺失（推测为"其中 H 为常数"，但不能确认，故不补）。建议讲义里注明按 (−T/2,T/2) 处理。

## p40 ｜ §5.3 傅里叶变换的性质·(1) 线性定理
- 标题行：§ 5.3 傅里叶变换的性质
- 中文要点：为了书写方便，我们将一维傅里叶积分变换 … 简记为：f(x)⇌F(k)，其中 f(x) 为原函数，F(k) 为像函数，符号"⇌"表示两者之间的变换。… 设 f₁(x) 及 f₂(x) 对应的像函数分别为 F₁(k) 及 F₂(k)，则有：… 其中 α，β 为常数。直接从傅里叶积分变化式出发，就可推出。
- 公式：
  - 一维变换对（本页约定）：
    $$f(x)=\int_{-\infty}^{\infty}F(k)e^{ikx}dk,\qquad F(k)=\frac{1}{2\pi}\int_{-\infty}^{\infty}f(x)e^{-ikx}dx$$
  - 记号：
    $$f(x)\rightleftharpoons F(k)$$
  - 线性定理（绿框）：
    $$\alpha f_{1}(x)+\beta f_{2}(x)\rightleftharpoons\alpha F_{1}(k)+\beta F_{2}(k)$$
- 例题/作业：无（线性定理未给证明，只说"直接从傅里叶积分变化式出发，就可推出"）
- 图：无
- ⚠️存疑：文字中 α 在正文排版为斜体 a（"其中 a，β 为常数"），与公式里的 α 不完全一致，照录为 α。

## p41 ｜ §5.3·(2) 导数定理I
- 标题行：(2) 导数定理I
- 中文要点：函数 f(x) 的 n 阶导数 f^{(n)}(x) 对应的傅里叶积分变换为：… 其中要求 … 证明：根据 …，有 … 类推
- 公式：
  - 定理（绿框）：
    $$f^{(n)}(x)\rightleftharpoons(ik)^{n}F(k)\qquad\text{其中要求}\quad f^{(n-1)}(x)\Big|_{x=\pm\infty}=0$$
  - 证明（n=1 的分部积分，边界项消失）：
    $$\frac{1}{2\pi}\int_{-\infty}^{\infty}f^{(1)}(x)e^{-ikx}dx$$
    $$=\frac{1}{2\pi}\int_{-\infty}^{\infty}e^{-ikx}df(x)=\frac{1}{2\pi}e^{-ikx}f(x)\Big|_{-\infty}^{\infty}-\frac{1}{2\pi}\int_{-\infty}^{\infty}f(x)\,de^{-ikx}$$
    $$=\frac{ik}{2\pi}\int_{-\infty}^{\infty}f(x)e^{-ikx}dx=(ik)F(k)$$
  - 类推（蓝箭头）：
    $$f^{(1)}(x)\rightleftharpoons(ik)F(k)\qquad\text{类推}\quad f^{(n)}(x)\rightleftharpoons(ik)^{n}F(k)\quad(n>1)$$
- 例题/作业：无
- 图：无
- ⚠️存疑：边界项写 $f^{(n-1)}(x)|_{x=\pm\infty}=0$（只写一阶导数的边界），未说明 $f,f',\dots$ 各阶都需为零；按原文照录。

## p42 ｜ §5.3·(3) 导数定理II
- 标题行：(3) 导数定理II
- 中文要点：… 其中 F^{(n)}(k) 是 F(k) 的 n 阶导数。证明：由傅里叶积分变换式 … 则有：… 即：… （红字）导数定理表明：原（像）函数的求导运算，经傅里叶变换后，变成了像（原）函数的代数运算
- 公式：
  - 定理（绿框）：
    $$(-ix)^{n}f(x)\rightleftharpoons F^{(n)}(k)$$
  - 证明（对 k 求导，红字标出 (−ix)ⁿ）：
    $$F^{(n)}(k)=\frac{d^{n}}{dk^{n}}\left[\frac{1}{2\pi}\int_{-\infty}^{\infty}f(x)e^{-ikx}dx\right]=\frac{1}{2\pi}\int_{-\infty}^{\infty}(-ix)^{n}f(x)e^{-ikx}dx$$
  - 即：
    $$(-ix)^{n}f(x)\rightleftharpoons F^{(n)}(k)$$
- 例题/作业：无
- 图：无
- ⚠️存疑：无

## p43 ｜ §5.3·(4) 积分定理
- 标题行：(4) 积分定理
- 中文要点：证明：令 …，则有 … 由导数定理得到：… 其中 Φ(k) 是 φ(x) 的像函数 … 因此 …
- 公式：
  - 定理（绿框，注意 ⇌ 上方的横线与"⇌"叠加，原文为变换记号）：
    $$\int_{-\infty}^{x}f(\zeta)\,d\zeta\rightleftharpoons\frac{1}{ik}F(k)$$
  - 证明：
    $$\varphi(x)=\int_{-\infty}^{x}f(\zeta)\,d\zeta,\qquad \varphi'(x)=f(x)\rightleftharpoons F(k)$$
    $$\varphi'(x)\rightleftharpoons ik\Phi(k)\qquad(\Phi(k)\ \text{是}\ \varphi(x)\ \text{的像函数})$$
    $$F(k)=ik\Phi(k)$$
  - 结论（蓝箭头）：
    $$\int_{-\infty}^{x}f(\zeta)\,d\zeta=\varphi(x)\rightleftharpoons\Phi(k)=\frac{1}{ik}F(k)$$
- 例题/作业：无
- 图：无
- ⚠️存疑：证明未验证 φ(−∞)=0（即导数定理I 所需的边界条件），照录。

## p44 ｜ §5.3·(5) 相似性定理
- 标题行：(5) 相似性定理
- 中文要点：其中 a 为常数。证明：… 令 y=ax … 当 a>0 时，则有 … 当 a<0 时，则有 …
- 公式：
  - 定理（绿框）：
    $$f(ax)\rightleftharpoons\frac{1}{|a|}F(k/a)\qquad\text{其中 }a\text{ 为常数}$$
  - 证明第一步（把 e^{−ikx} 凑成 e^{−i(k/a)(ax)}，并乘除 a）：
    $$\frac{1}{2\pi}\int_{-\infty}^{\infty}f(ax)e^{-ikx}dx=\frac{1}{2\pi}\int_{-\infty}^{\infty}f(ax)e^{-i\frac{k}{a}ax}\frac{1}{a}d(ax)\qquad\text{令 }y=ax$$
  - a>0：
    $$\frac{1}{2\pi}\int_{-\infty}^{\infty}f(ax)e^{-ikx}dx=\frac{1}{2\pi}\int_{-\infty}^{\infty}f(y)e^{-i\frac{k}{a}y}\frac{1}{a}dy=\frac{1}{a}F\left(\frac{k}{a}\right)$$
  - a<0（限上下翻转，多一个负号）：
    $$\frac{1}{2\pi}\int_{-\infty}^{\infty}f(ax)e^{-ikx}dx=\frac{1}{2\pi}\int_{\infty}^{-\infty}f(y)e^{-i\frac{k}{a}y}\frac{1}{a}dy=-\frac{1}{a}F\left(\frac{k}{a}\right)$$
  - 结论（蓝箭头）：
    $$f(ax)\rightleftharpoons\frac{1}{|a|}F(k/a)$$
- 例题/作业：无
- 图：无
- ⚠️存疑：无

## p45 ｜ §5.3·(6) 延迟定理
- 标题行：(6) 延迟定理
- 中文要点：其中 a 为常数。证明：… 令 y=x−a，则有 …
- 公式：
  - 定理（绿框）：
    $$f(x-a)\rightleftharpoons e^{-ika}F(k)\qquad\text{其中 }a\text{ 为常数}$$
  - 证明（拆出 e^{−ika}，并把 dx 写成 d(x−a)）：
    $$\frac{1}{2\pi}\int_{-\infty}^{\infty}f(x-a)e^{-ikx}dx=\frac{1}{2\pi}\int_{-\infty}^{\infty}f(x-a)e^{-ik(x-a)}e^{-ika}d(x-a)$$
    $$\text{令 }y=x-a:\qquad \frac{1}{2\pi}\int_{-\infty}^{\infty}f(x-a)e^{-ikx}dx=e^{-ika}\frac{1}{2\pi}\int_{-\infty}^{\infty}f(y)e^{-iky}dy$$
  - 结论（蓝箭头）：
    $$f(x-a)\rightleftharpoons e^{-ika}F(k)$$
- 例题/作业：无
- 图：无
- ⚠️存疑：无

## p46 ｜ §5.3·(7) 位移定理 与 (8) 卷积定理
- 标题行：(7) 位移定理 ／ (8) 卷积定理
- 中文要点：(7)…其中 k₀ 为常数。证明：… (8) 定义函数 f₁(x) 和 f₂(x) 的卷积为 … 则它的傅里叶积分变换为 … 其中 F₁(k) 和 F₂(k) 分别是函数 f₁(x) 和 f₂(x) 的像函数。
- 公式：
  - 位移定理（绿框）：
    $$e^{ik_{0}x}f(x)\rightleftharpoons F(k-k_{0})\qquad\text{其中 }k_{0}\text{ 为常数}$$
  - 位移定理证明（一行）：
    $$\frac{1}{2\pi}\int_{-\infty}^{\infty}e^{ik_{0}x}f(x)e^{-ikx}dx=\frac{1}{2\pi}\int_{-\infty}^{\infty}f(x)e^{-i(k-k_{0})x}dx$$
    $$e^{ik_{0}x}f(x)\rightleftharpoons F(k-k_{0})$$
  - 卷积定义（本页新增）：
    $$f_{1}(x)*f_{2}(x)=\int_{-\infty}^{\infty}f_{1}(x-\eta)f_{2}(\eta)\,d\eta$$
  - 卷积定理（绿框，系数为 **2π**）：
    $$f_{1}(x)*f_{2}(x)\rightleftharpoons2\pi F_{1}(k)F_{2}(k)$$
- 例题/作业：无
- 图：蓝箭头指向位移定理结论
- ⚠️存疑：卷积定理的 2π 系数与"F(k)=1/(2π)∫…"的约定配套，但课件未解释 2π 从何而来（证明见 p47）。注意与常见教材的 F₁F₂ 形式不同，不可混用。

## p47 ｜ §5.3·卷积定理的证明
- 标题行：证明：
- 中文要点：证明：由傅里叶积分变换式，有
- 公式（五步，蓝箭头给出结论）：
  $$f_{1}(x)*f_{2}(x)\rightleftharpoons\frac{1}{2\pi}\int_{-\infty}^{\infty}f_{1}(x)*f_{2}(x)e^{-ikx}dx$$
  $$=\frac{1}{2\pi}\int_{-\infty}^{\infty}\int_{-\infty}^{\infty}f_{1}(x-\eta)f_{2}(\eta)d\eta\,e^{-ikx}dx$$
  $$=\frac{1}{2\pi}\int_{-\infty}^{\infty}f_{2}(\eta)d\eta\int_{-\infty}^{\infty}f_{1}(x-\eta)e^{-ikx}dx$$
  $$=\frac{1}{2\pi}\int_{-\infty}^{\infty}f_{2}(\eta)d\eta\int_{-\infty}^{\infty}f_{1}(x-\eta)e^{-ik(x-\eta)}e^{-ik\eta}d(x-\eta)$$
  $$=\frac{1}{2\pi}\int_{-\infty}^{\infty}f_{2}(\eta)e^{-ik\eta}d\eta\int_{-\infty}^{\infty}f_{1}(x-\eta)e^{-ik(x-\eta)}d(x-\eta)$$
  $$=2\pi F_{1}(k)F_{2}(k)$$
  $$f_{1}(x)*f_{2}(x)\rightleftharpoons2\pi F_{1}(k)F_{2}(k)$$
- 例题/作业：无
- 图：蓝箭头指向最后一行
- ⚠️存疑：最后一步 $=2\pi F_1F_2$ 由 $\frac{1}{2\pi}\cdot 2\pi F_1\cdot 2\pi F_2$ 得到，课件未写出中间的两个 2π 来源，只给结果。

## p48 ｜ §5.3·(9) 乘积定理
- 标题行：(9) 乘积定理
- 中文要点：证明：… 根据卷积定义，有 …
- 公式：
  - 定理（绿框）：
    $$f_{1}(x)f_{2}(x)\rightleftharpoons F_{1}(k)*F_{2}(k)$$
  - 证明（把 f₂ 用逆变换代入）：
    $$\frac{1}{2\pi}\int_{-\infty}^{\infty}f_{1}(x)f_{2}(x)e^{-ikx}dx$$
    $$=\frac{1}{2\pi}\int_{-\infty}^{\infty}f_{1}(x)e^{-ikx}dx\int_{-\infty}^{\infty}F_{2}(\eta)e^{i\eta x}d\eta$$
    $$=\frac{1}{2\pi}\int_{-\infty}^{\infty}F_{2}(\eta)d\eta\int_{-\infty}^{\infty}f_{1}(x)e^{-i(k-\eta)x}dx$$
    $$=\int_{-\infty}^{\infty}F_{2}(\eta)F_{1}(k-\eta)\,d\eta$$
  - 结论：
    $$f_{1}(x)f_{2}(x)\rightleftharpoons F_{1}(k)*F_{2}(k)$$
- 例题/作业：无
- 图：无
- ⚠️存疑：第三行到第四行省去了 $2\pi F_1$ 与 $1/(2\pi)$ 相消的说明；照录。

## p49 ｜ §5.3·例题·例1（卷积反解 f(x)）
- 标题行：例1 已知积分 … 求 f(x)
- 中文要点：例1 已知积分 ∫…=1/(x²+b²)，其中 0<a<b，求 f(x)。解：根据卷积定义，有 … 对两边进行傅里叶变换，则有 …
- 公式：
  - 题面：
    $$\int_{-\infty}^{\infty}\frac{f(\eta)\,d\eta}{(x-\eta)^{2}+a^{2}}=\frac{1}{x^{2}+b^{2}},\qquad 0<a<b$$
  - 识别为卷积：
    $$\int_{-\infty}^{\infty}\frac{f(\eta)\,d\eta}{(x-\eta)^{2}+a^{2}}=f(x)*\left(\frac{1}{x^{2}+a^{2}}\right)=\frac{1}{x^{2}+b^{2}}$$
  - 两边取变换（用卷积定理，系数 2π）：
    $$2\pi\,\mathscr{F}\left[f(x)\right]\cdot\mathscr{F}\left[\frac{1}{x^{2}+a^{2}}\right]=\mathscr{F}\left[\frac{1}{x^{2}+b^{2}}\right]$$
  - 用留数算 $\mathscr{F}[1/(x^2+a^2)]$：
    $$\mathscr{F}\left[\frac{1}{x^{2}+a^{2}}\right]=\frac{1}{2\pi}\int_{-\infty}^{\infty}\frac{1}{x^{2}+a^{2}}e^{-ikx}dx$$
    $$=\begin{cases}\dfrac{1}{2\pi}(-2\pi i)\operatorname{Res}\left[\dfrac{e^{-ikz}}{z^{2}+a^{2}}\right]_{z=-ai}=\dfrac{1}{2\pi}(-2\pi i)\dfrac{e^{-ik(-ai)}}{-ai-ai}=\dfrac{e^{-ka}}{2a}, & k>0\\[14pt] \dfrac{1}{2\pi}(2\pi i)\operatorname{Res}\left[\dfrac{e^{-ikz}}{z^{2}+a^{2}}\right]_{z=ai}=\dfrac{1}{2\pi}(2\pi i)\dfrac{e^{-ik(ai)}}{ai+ai}=\dfrac{e^{ka}}{2a}, & k<0\end{cases}$$
- 例题/作业：见上（例1 解答前半）。
- 图：无
- ⚠️存疑：k>0 时取了下半平面极点 z=−ai（或等价地绕向下的围道），k<0 时取上半平面 z=ai；课件未说明围道选择依据，照录。

## p50 ｜ §5.3·例1 续（整理得 f(x)）
- 标题行：（无标题）即 ／ 同理 ／ 因此 ／ 整理得
- 中文要点：即 … 同理 … 因此 … 整理得 …
- 公式：
  - 即（k>0 与 k<0 合写为 |k|）：
    $$\mathscr{F}\left[\frac{1}{x^{2}+a^{2}}\right]=\frac{e^{-|k|a}}{2a},\qquad\text{同理}\quad \mathscr{F}\left[\frac{1}{x^{2}+b^{2}}\right]=\frac{e^{-|k|b}}{2b}$$
  - 因此（解出 f 的像函数）：
    $$\mathscr{F}\left[f(x)\right]=\frac{1}{2\pi}\mathscr{F}\left[\frac{1}{x^{2}+b^{2}}\right]\Big/\mathscr{F}\left[\frac{1}{x^{2}+a^{2}}\right]=\frac{1}{2\pi}\frac{e^{-|k|b}}{2b}\frac{2a}{e^{-|k|a}}$$
  - 整理得（把指数合并，并凑出 1/(2(b−a)) 的形式）：
    $$\mathscr{F}\left[f(x)\right]=\frac{a}{2\pi b}e^{-|k|(b-a)}=\frac{e^{-|k|(b-a)}}{2(b-a)}\,2(b-a)\frac{a}{2\pi b}=\frac{e^{-|k|(b-a)}}{2(b-a)}\frac{a(b-a)}{\pi b}$$
  - 结论（蓝箭头，反演出 f(x)）：
    $$f(x)=\frac{a(b-a)}{\pi b}\,\frac{1}{x^{2}+(b-a)^{2}}$$
- 例题/作业：见上（例1 解答完成）。
- 图：无
- ⚠️存疑：无

## p51 ｜ §5.4 δ函数·1、δ函数的定义（细杆→质点）
- 标题行：§ 5.4 δ函数（页内二级标题"1、δ函数的定义"）
- 中文要点：考虑一质量为 m，长度为 l 的匀质细杆，中心位于坐标原点 x=0 处，则细杆的线质量密度分布为：… 对 ρ(x) 积分，得到其质量为：… 当细杆长度无限小，即 l→0 时，细杆趋向于一个**质点**，其质量仍为 m，即 ∫ρ(x)dx=m，但其质量密度分布为：… （红字）质点的质量密度分布：在 x=0 点为无穷，在 x≠0 点为 0，且积分为 m。
- 公式：
  - 匀质细杆的线密度（本页的出发点）：
    $$\rho(x)=\begin{cases}0, & (|x|>l/2)\\[2pt] m/l, & (|x|\leq l/2)\end{cases}$$
  - 总质量：
    $$\int_{-\infty}^{\infty}\rho(x)\,dx=\int_{-l/2}^{l/2}\frac{m}{l}\,dx=m$$
  - l→0 后的密度（δ 的原型）：
    $$\rho(x)=\begin{cases}0, & (x\neq0)\\[2pt] \infty, & (x=0)\end{cases}\qquad\text{且}\quad\int_{-\infty}^{\infty}\rho(x)\,dx=m$$
- 例题/作业：无
- 图：无
- ⚠️存疑：l→0 后的 ρ(x) 写"∞（x=0）"，严格说应带"质量 m 的系数"，课件此处只作示意，照录。

## p52 ｜ §5.4·δ函数的定义式
- 标题行：（无标题，承 p51 的红字结论）
- 中文要点（红字）：为了描述**质点和点电荷的空间分布**，或**脉冲力的瞬时分布**，在物理学中可引入一个所谓的 δ 函数来描述，其定义式为 … 这表明 δ 函数的分布是无限窄，且当 x→x₀ 时它的值趋于无穷大。此外，δ 函数的积分是有限的，即：… 此积分也可表示为：…，其中 a<x₀<b
- 公式：
  - 定义式（本页核心）：
    $$\delta(x-x_{0})=\begin{cases}0, & x\neq x_{0}\\[2pt] \infty, & x=x_{0}\end{cases}$$
  - 归一化：
    $$\int_{-\infty}^{\infty}\delta(x-x_{0})\,dx=1$$
  - 有限区间写法：
    $$\int_{a}^{b}\delta(x-x_{0})\,dx=1,\qquad a<x_{0}<b$$
- 例题/作业：无
- 图：右侧灰底示意图，纵轴标 δ(x−x₀)、横轴标 x；原点标 0，另标 x₀ 处画一根极窄的尖峰（宽度近 0、高度趋于无穷），峰下箭头指向 x₀。
- ⚠️存疑：无

## p53 ｜ §5.4·三维 δ函数与物理实例
- 标题行：（无标题，三个物理实例 + 三维 δ）
- 中文要点：位于 x=a 处质量为 m 的**质点**，质量线密度为 mδ(x−a)；位于 x=a 处电量为 Q 的**点电荷**，电荷线密度为 Qδ(x−a)；位于 t=a 时刻强度为 I 的**脉冲信号**，信号函数为 Iδ(t−a)。在三维情况下，类似地有 … 三维的 δ 函数可以用一维 δ 函数的乘积来表示，即：… 这样有：…
- 公式：
  - 三个一维实例：
    $$m\delta(x-a),\qquad Q\delta(x-a),\qquad I\delta(t-a)$$
  - 三维 δ 函数：
    $$\delta(\mathbf{r}-\mathbf{r}_{0})=\begin{cases}0, & \mathbf{r}\neq\mathbf{r}_{0}\\[2pt] \infty, & \mathbf{r}=\mathbf{r}_{0}\end{cases}$$
  - 乘积表示：
    $$\delta(\mathbf{r}-\mathbf{r}_{0})=\delta(x-x_{0})\,\delta(y-y_{0})\,\delta(z-z_{0})$$
  - 三维归一化：
    $$\iiint_{-\infty}^{\infty}\delta(\mathbf{r}-\mathbf{r}_{0})\,d\mathbf{r}=1$$
- 例题/作业：无
- 图：无
- ⚠️存疑：无

## p54 ｜ §5.4·2、δ函数的性质 (1)(2)
- 标题行：2、δ函数的性质
- 中文要点：(1) δ(x) 函数是**偶函数**，它的导数则是奇函数，即：… (2) 可以用**阶跃函数** H(x)=… 来表示 δ(x) 函数，即 δ(x)=dH(x)/dx，这是因为：H(x)=∫δdx…
- 公式：
  - (1) 偶性 / 导数的奇性：
    $$\delta(-x)=\delta(x),\qquad \delta'(-x)=-\delta'(x)$$
  - (2) 阶跃函数定义：
    $$H(x)=\begin{cases}1, & x>0\\[2pt] 0, & x<0\end{cases}$$
  - 求导关系：
    $$\delta(x)=\frac{dH(x)}{dx}$$
  - 理由（积分式）：
    $$H(x)=\int_{-\infty}^{x}\delta(x)\,dx=\begin{cases}1, & x>0\\[2pt] 0, & x<0\end{cases}$$
- 例题/作业：无
- 图：无
- ⚠️存疑：$H(x)=\int_{-\infty}^{x}\delta(x)dx$ 的积分变量与被积变量同名（原文如此，通常应为 δ(ξ)dξ），照录。

## p55 ｜ §5.4·δ函数的性质 (3)(4)
- 标题行：（承 p54 的"2、δ函数的性质"）
- 中文要点：(3) δ(x) 函数具有**挑选性**，即：… 其中 f(x) 是 [-∞, ∞] 区间中的连续函数。… (4) 若 φ(x)=0 的实根为 xₖ(k=1,2,…)，且全为单根，则 …
- 公式：
  - (3) 挑选性：
    $$\int_{-\infty}^{\infty}f(x)\delta(x-x_{0})\,dx=f(x_{0})$$
  - 奇性推论（页中未加编号）：
    $$\int_{-\infty}^{\infty}f(x)\,x\,\delta(x)\,dx=0$$
  - (4) 复合函数的 δ：
    $$\delta[\varphi(x)]=\sum_{k=1}^{\infty}\frac{\delta(x-x_{k})}{|\varphi'(x_{k})|}$$
- 例题/作业：无
- 图：无
- ⚠️存疑：$\int f(x)x\delta(x)dx=0$ 未标注出处/条件（用的是 xδ(x)=0 的奇性），页内只单列一行，照录。

## p56 ｜ §5.4·3、δ函数的辅助函数（rect 型）
- 标题行：3、δ函数的辅助函数
- 中文要点：δ函数有两个重要的特征：（1）δ(x) 函数在 x=0 处为无穷大，在其它处为 0；（2）δ(x) 是归一化的分布函数，即 … 如果一个函数 f(x) 具有上述两个特征，就可以用来构造 δ(x)。例如 … 其中 … 证明：…
- 公式：
  - 两个特征：
    $$\delta(x)=0\ (x\neq0),\quad \delta(0)=\infty;\qquad \int_{-\infty}^{\infty}\delta(x)\,dx=1$$
  - 例子（矩形/rect 型，本页第一个辅助函数）：
    $$f(x)=\lim_{l\to0}\frac{1}{l}\operatorname{rect}\left(\frac{x}{l}\right)=\delta(x)$$
    $$\frac{1}{l}\operatorname{rect}\left(\frac{x}{l}\right)=\begin{cases}1/l, & |x|<l/2\\[2pt] 0, & |x|>l/2\end{cases}$$
  - 验证（三个式子）：
    $$f(0)=\lim_{l\to0}\frac{1}{l}=\infty,\qquad f(x\neq0)=0,\qquad \int_{-\infty}^{\infty}f(x)\,dx=\int_{-l/2}^{l/2}\frac{1}{l}\,dx=1$$
- 例题/作业：无（"证明"即上述三行验证）
- 图：右侧示意图，纵轴标 1/l，横轴标 −l/2 与 l/2；曲线为以 (−l/2,l/2) 为底、高 1/l 的矩形方框。
- ⚠️存疑：无

## p57 ｜ §5.4·辅助函数三例
- 标题行：（承 p56 的"3、δ函数的辅助函数"）
- 中文要点：例如 … 其中 … 利用了 … 例如 … 例如 … 利用了 …
- 公式（三个辅助函数，每个都只验证归一化积分）：
  - (i) sin(kx)/(πx) 型：
    $$f(x)=\lim_{k\to\infty}\frac{1}{\pi}\frac{\sin(kx)}{x}=\delta(x)$$
    $$\int_{-\infty}^{\infty}f(x)\,dx=\lim_{k\to\infty}\int_{-\infty}^{\infty}\frac{1}{\pi}\frac{\sin(kx)}{x}dx=\frac{1}{\pi}\lim_{k\to\infty}\int_{-\infty}^{\infty}\frac{\sin(kx)}{kx}d(kx)=1$$
    $$\text{利用了}\quad\int_{0}^{\infty}\frac{\sin x}{x}dx=\frac{\pi}{2}$$
  - (ii) 洛伦兹型（红字标 ε）：
    $$f(x)=\lim_{\varepsilon\to0}\frac{1}{\pi}\frac{\varepsilon}{x^{2}+\varepsilon^{2}}=\delta(x)$$
    $$\int_{-\infty}^{\infty}f(x)\,dx=\lim_{\varepsilon\to0}\int_{-\infty}^{\infty}\frac{1}{\pi}\frac{\varepsilon}{x^{2}+\varepsilon^{2}}dx=\frac{1}{\pi}\lim_{\varepsilon\to0}\int_{-\infty}^{\infty}\frac{1}{(x/\varepsilon)^{2}+1}d\frac{x}{\varepsilon}=1$$
  - (iii) 高斯型：
    $$f(x)=\lim_{\sigma\to0}\frac{1}{\sigma\sqrt{\pi}}e^{-x^{2}/\sigma^{2}}=\delta(x)$$
    $$\int_{-\infty}^{\infty}f(x)\,dx=\lim_{\sigma\to0}\int_{-\infty}^{\infty}\frac{1}{\sigma\sqrt{\pi}}e^{-x^{2}/\sigma^{2}}dx=\frac{1}{\sigma\sqrt{\pi}}\lim_{\sigma\to0}\int_{-\infty}^{\infty}e^{-(x/\sigma)^{2}}\sigma\,d\frac{x}{\sigma}=1$$
    $$\text{利用了}\quad\int_{0}^{\infty}e^{-x^{2}}dx=\frac{\sqrt{\pi}}{2}$$
- 例题/作业：无
- 图：无
- ⚠️存疑：三例都只验证了"积分=1"这一个特征，未验证"x≠0 时为 0"；另 (iii) 的中间式把 σ 同时留在系数与微分里（$\frac{1}{\sigma\sqrt\pi}\lim\int e^{-(x/\sigma)^2}\sigma d\frac{x}{\sigma}$），按图照录。

## p58 ｜ §5.4·4、δ函数的傅里叶变换
- 标题行：4、δ函数的傅里叶变换
- 中文要点：将 δ 函数表示成复数形式的傅里叶积分：… 其中 … 这样，δ 函数的积分表达式为 … 对于三维情况，δ 函数的积分表达式为 … 利用 δ 函数的傅里叶积分式，很容易推导出它的**广义函数表示式**。令 k→∞，则 …
- 公式：
  - 傅里叶积分表示：
    $$\delta(x)=\int_{-\infty}^{\infty}C(k)e^{ikx}dk$$
  - 像函数（δ 的变换，本页关键）：
    $$C(k)=\frac{1}{2\pi}\int_{-\infty}^{\infty}\delta(x)e^{-ikx}dx=\frac{1}{2\pi}$$
  - 积分表达式（绿框）：
    $$\delta(x)=\frac{1}{2\pi}\int_{-\infty}^{\infty}e^{ikx}dk$$
  - 三维版：
    $$\delta(\mathbf{r})=\frac{1}{(2\pi)^{3}}\iiint_{-\infty}^{\infty}e^{i\mathbf{k}\cdot\mathbf{r}}d\mathbf{k}$$
  - 广义函数表示式（令 k→∞）：
    $$\delta(x)=\lim_{k\to\infty}\frac{1}{2\pi}\int_{-k}^{k}e^{ikx}dk=\lim_{k\to\infty}\frac{1}{2\pi}\frac{1}{ix}\left(e^{ikx}-e^{-ikx}\right)=\lim_{k\to\infty}\frac{1}{\pi}\frac{\sin kx}{x}$$
- 例题/作业：无
- 图：无（绿底框为公式框）
- ⚠️存疑：极限式里的积分上限变量与指数里的 k 同名（原文如此，通常上限应记 K），照录；红字"令 k→∞，则"与上式连读。

## p59 ｜ §5.4·例题·例1（sin ax、cos ax 的变换）
- 标题行：例1 求函数 sin ax 和 cos ax 的傅里叶变换，其中 k 是实常数。
- 中文要点：例1 求函数 sin ax 和 cos ax 的傅里叶变换，其中 k 是实常数。解：由傅里叶积分变换，有 … 严格说，函数 sin ax 和 cos ax 并不满足绝对可积条件，但是利用 δ 函数的定义，可以计算出他们的傅里叶变换式。
- 公式：
  - sin 的变换：
    $$\frac{1}{2\pi}\int_{-\infty}^{\infty}\sin ax\,e^{-ikx}dx=\frac{1}{4\pi i}\left[\int_{-\infty}^{\infty}e^{-i(k-a)x}dx-\int_{-\infty}^{\infty}e^{-i(k+a)x}dx\right]$$
    $$=\frac{1}{2i}\left[\delta(k-a)-\delta(k+a)\right]$$
  - cos 的变换：
    $$\frac{1}{2\pi}\int_{-\infty}^{\infty}\cos ax\,e^{-ikx}dx=\frac{1}{4\pi}\left[\int_{-\infty}^{\infty}e^{-i(k-a)x}dx+\int_{-\infty}^{\infty}e^{-i(k+a)x}dx\right]$$
    $$=\frac{1}{2}\left[\delta(k-a)+\delta(k+a)\right]$$
- 例题/作业：见上（完整解答）。
- 图：无
- ⚠️存疑：题面写"其中 k 是实常数"，但 k 在计算中充当变换变量（真正的常数应是 a），疑为原文笔误（或指 a 为实常数）；按原文照录，不擅改。

## p60 ｜ §5.4·例题·例2（球坐标中的 δ 型函数）
- 标题行：例2 在球坐标系中计算函数 … 的傅里叶变换。
- 中文要点：例2 在球坐标系中计算函数 f(r)=… 的傅里叶变换。解：根据傅里叶变换，有 … 在球坐标系中，利用：… （蓝字）这个变换关系，将在第十章讨论积分变换法时用到。即 …
- 公式：
  - 题面：
    $$f(r)=\frac{4\pi^{2}}{r}\delta(r-r_{0})$$
  - 三维变换式：
    $$F(\mathbf{k})=\frac{1}{(2\pi)^{3}}\iiint\frac{4\pi^{2}}{r}\delta(r-r_{0})e^{-i\mathbf{k}\cdot\mathbf{r}}d\mathbf{r}$$
  - 球坐标工具式：
    $$d\mathbf{r}=r^{2}dr\sin\theta\,d\theta\,d\varphi,\qquad \mathbf{k}\cdot\mathbf{r}=kr\cos\theta$$
  - 逐次积分（δ 挑掉 r 积分）：
    $$F(\mathbf{k})=\frac{1}{(2\pi)^{3}}\int_{0}^{2\pi}d\varphi\int_{0}^{\pi}\sin\theta\,d\theta\int_{0}^{\infty}\frac{4\pi^{2}}{r}\delta(r-r_{0})e^{-ikr\cos\theta}r^{2}dr$$
    $$=\frac{4\pi^{2}}{(2\pi)^{3}}\,2\pi\int_{0}^{\pi}\sin\theta\,e^{-ikr_{0}\cos\theta}r_{0}\,d\theta$$
    $$=\frac{1}{ik}\left(e^{ikr_{0}}-e^{-ikr_{0}}\right)$$
  - 结论：
    $$\frac{4\pi^{2}}{r}\delta(r-r_{0})\rightleftharpoons\frac{1}{ik}\left(e^{ikr_{0}}-e^{-ikr_{0}}\right)$$
- 例题/作业：见上（完整解答）。
- 图：无
- ⚠️存疑：中间步 $=\frac{4\pi^2}{(2\pi)^3}2\pi\int_0^\pi \sin\theta e^{-ikr_0\cos\theta}r_0\,d\theta$ 未写出 $\int e^{-ikr_0\cos\theta}\sin\theta d\theta$ 的求值过程，直接给下一行结果，照录。

## p61 ｜ §5.4·例题·例3（含 δ 的常微分方程）
- 标题行：例3 利用傅里叶积分变换，求解如下含有 δ 函数的常微分方程
- 中文要点：例3 利用傅里叶积分变换，求解如下含有 δ 函数的常微分方程 … (−∞<x<∞)，其中 a>0，x₀ 为给定常数。解：令 …，即 g(x)⇌G(k)。根据导数定理 …，则 … 根据延迟定理 …，则 … 将方程两边进行傅里叶积分变换，得到：… 利用留数定理，得到 …
- 公式：
  - 方程（题面）：
    $$\frac{d^{2}g(x)}{dx^{2}}-a^{2}g(x)=\delta(x-x_{0})\qquad(-\infty<x<\infty),\ a>0,\ x_{0}\ \text{给定常数}$$
  - 变换的设：
    $$g(x)=\int_{-\infty}^{\infty}G(k)e^{ikx}dk\quad\text{即}\quad g(x)\rightleftharpoons G(k)$$
  - 两条定理的套用：
    $$f^{(n)}(x)\rightleftharpoons(ik)^{n}F(k)\ \Rightarrow\ \frac{d^{2}g(x)}{dx^{2}}\rightleftharpoons(ik)^{2}G(k)$$
    $$f(x-a)\rightleftharpoons e^{-ika}F(k)\ \Rightarrow\ \delta(x-x_{0})\rightleftharpoons e^{-ikx_{0}}\frac{1}{2\pi}$$
  - 代数方程与解：
    $$(ik)^{2}G(k)-a^{2}G(k)=e^{-ikx_{0}}\frac{1}{2\pi}\quad\text{即}\quad G(k)=-\frac{1}{2\pi}\frac{e^{-ikx_{0}}}{k^{2}+a^{2}}$$
  - 逆变换（蓝箭头）：
    $$g(x)=\int_{-\infty}^{\infty}G(k)e^{ikx}dk=-\frac{1}{2\pi}\int_{-\infty}^{\infty}\frac{e^{ik(x-x_{0})}}{k^{2}+a^{2}}dk$$
  - 留数定理结果：
    $$g(x)=-\frac{1}{2a}e^{-a|x-x_{0}|}$$
- 例题/作业：见上（完整解答）。
- 图：无
- ⚠️存疑："利用留数定理，得到 g(x)=…" 未给留数计算过程（这是本页最大跳步）；δ 的变换用 $e^{-ikx_0}\frac{1}{2\pi}$（延迟定理 + C(k)=1/(2π)）写出，照录。

## p62 ｜ §5.4·例题·例4（格林函数法）
- 标题行：例4 利用 δ 函数的性质，求解如下常微分方程
- 中文要点：例4 利用 δ 函数的性质，求解如下常微分方程 … 解：根据 δ 函数的性质，有 … 令 … 利用例3 的结果，有 … （红字）上述求法为求解无界区域中的常微分方程的格林函数法。将在第十一章讨论。
- 公式：
  - 方程与边界条件（题面，用大括号联立）：
    $$\begin{cases}\dfrac{d^{2}u(x)}{dx^{2}}-a^{2}u(x)=f(x)\quad(-\infty<x<\infty)\\[10pt] u(x)\Big|_{x\to\pm\infty}=0\end{cases}$$
  - 用 δ 的挑选性把 f 写成积分：
    $$f(x)=\int_{-\infty}^{\infty}\delta(x-x')f(x')\,dx'$$
  - 设叠加解：
    $$u(x)=\int_{-\infty}^{\infty}g(x,x')f(x')\,dx'$$
  - 归结为 g 的方程（蓝箭头）：
    $$\frac{d^{2}g(x,x')}{dx^{2}}-a^{2}g(x,x')=\delta(x-x')\qquad(-\infty<x<\infty)$$
  - 用例3 结果：
    $$g(x,x')=-\frac{1}{2a}e^{-a|x-x'|}$$
  - 最终解（蓝箭头）：
    $$u(x)=-\frac{1}{2a}\int_{-\infty}^{\infty}e^{-a|x-x'|}f(x')\,dx'$$
- 例题/作业：见上（完整解答）。
- 图：无
- ⚠️存疑：由"设 u=∫g f dx'"到"g 满足同一方程"这一步（线性叠加/交换求导与积分）未论证，直接给结论，照录。

## p63 ｜ § 第五章作业（第 5–7 题）
- 标题行：§ 第五章作业
- 中文要点：见下逐题原文
- 公式/题面（逐题照抄）：
  5. 求锯齿波
     $$f(t)=\begin{cases}0, & t<0\\[2pt] t, & 0\leq t\leq T\\[2pt] 0, & t>T\end{cases}$$
     复数形式的傅里叶变换。
  6. 求函数
     $$f(t)=\begin{cases}0, & (t<0)\\[2pt] e^{-\alpha t}, & (t\geq0)\end{cases}$$
     其中 α 为：(1) 有限大小的正数，即 α>0；(2) 无穷小的正数，即 α→0⁺
  7. 求如下函数：(1) $f(x)=\cos\left(\alpha x^{2}\right)$ (2) $f(x)=\sin\left(\alpha x^{2}\right)$ 的复数形式的傅里叶变换，其中 α>0
- 例题/作业：以上三题即作业，课件未给解答。
- 图：无
- ⚠️存疑：第 6 题原文"其中 α 为：(1) 有限大小的正数，即 α>0；（2）无穷小的正数，即 α→0⁺"，两小问并列，无其他条件；第 7 题两小问用 (1)(2) 连写在一行，照录。

---

## 跳步候选

> 判据：课件直接给结论、省略中间步骤、或把定理写成推论/引用的形式。

| 页码 | 课件原文短语（中文原文） | 缺了什么 |
|---|---|---|
| p5 | 利用三角函数的正交性 | 五条正交性积分全部直接列出，没有一条给出计算过程（如 ∫sin²= l 的来源） |
| p6 | 推出实变函数傅里叶级数的系数 | 只给 a₀、aₙ、bₙ 三个结果式，未演示"乘 cos(mπx/l) 后逐项积分、用 δ_nm 挑项"的推导 |
| p8 | 如果 f(x) 是偶函数，则／如果 f(x) 是奇函数，则 | 只给结果（偶→仅余弦、奇→仅正弦、区间半边化并乘 2），未说明奇偶函数在对称区间上积分的对消 |
| p9 | 引入波数：kₙ=nπ/l | 直接把 nπ/l 塞进 cos/sin 换成 cos(kₙx)，未说明"引入波数"的动机与量纲（1/长度） |
| p10 | 如果令 ω=2π/l, t=x/2（ω 为基波角频率） | 未说明 t=x/2 这个代换从何而来、为何 x∈[−l,l] 对应 t∈[−T/2,T/2]、系数由 1/l 变 2/T 的换算 |
| p11 | 如果令 θ=πx/l | 只写"变为"，未演示 dθ=(π/l)dx、上下限 −π..π、以及 1/(2π) 系数的换算 |
| p12 | 先求系数 | 写"先求系数"，但 bₙ 的两次分部积分只剩一行 dcos 记号，中间边界项与 ∫cos 消失未写 |
| p13 | a₀=…=？／aₙ=…=？／bₙ=…=？ | 三个系数全部留白只写"?"，然后直接跳到最终级数 Σ sin(2n−1)x/(2n−1)，整段推导缺失 |
| p14 | （仅四张 m=1,2,3,24 的图，无文字） | 未说明 m 是部分和阶数，也未解释 m=24 图上跳变处的振荡（Gibbs 现象）为何不消失 |
| p15 | 利用基函数族的正交性 | 直接写出 (1/2l)∫φₙ*φₘdx=δ_nm 并由此给 cₙ，未算这个积分，也未说明 1/(2l) 归一化常数与实数形式 1/l 的关系 |
| p19 | 对于 a₀，由于积分 ∫f(x)dx 有限 | 只用"积分有限"就断言 a₀→0，未写 (1/2l)·有限量 → 0 的估计 |
| p19 | 引入 Δkₙ=k_{n+1}−kₙ=π/l | 未说明为什么要把 aₙ 乘上 Δkₙ、也没写出 1/l = (1/π)(π/l) 的换算理由（这一步是级数转积分的关键） |
| p20 | 同理，Σbₙsin(kₙx)=… | 第二、三行把 cos 的整段式子照抄进 sin 的推导（sin 写成 cos），末行才换回 B(k)sin(kx)dk；等于 sin 方向的推导没真正做 |
| p22 | 如果 f(x) 是奇函数，则 A(k)=0 | 未给"奇×偶=奇在对称区间积分为 0"的论证，也未说明系数为何从 1/π 变 2/π、区间从 (−∞,∞) 变 (0,∞) |
| p24 | f(t)=∫A(ω)cos(ωt)dω=…={1，|t|<T；0，|t|>T} | 把 A(ω)=2sin(ωT)/(πω) 代回后，直接断言积分回到原矩形脉冲，未做这个含参积分（Dirichlet 积分）的求值 |
| p25 | 利用 sin(ω₀t)sin(ωt)=… | 只给积化和差公式，未说明为什么对奇函数只需算 B(ω)、以及上限 2Nπ/ω₀ 代入后如何化简 |
| p26 | =−A/π·sin(…)·[1/(ω₀−ω)+1/(ω₀+ω)]=… | 通分合并成 2A/π·ω₀/(ω²−ω₀²) 一步跳过，未写通分过程与符号变化 |
| p27 | 由于 A(−k)=…=A(k) 及 B(−k)=…=−B(k) | 只给奇偶性结果，未说明为何要用它（为 p28 换 k→−k 合并两个半线积分做准备） |
| p28 | 将上式右边第二项积分中的 k 换成 −k | 换元后积分限变号、d(−k) 出现负号、再翻转限这三步只在一行内完成，未逐一交代 |
| p29 | 通常称 f(x) 是原函数，对应的积分式为正变换，其变换的核为 e^{ikx} | 把 f(x) 的积分称为"正变换"、F(k) 的式子称为"逆变换"，与教科书惯例相反；未说明正/逆的约定，且与 p30"在正变换核中核为 e^{−iωt}"自相矛盾 |
| p30 | 注意：…系数 1/(2π) 可以放在正变换积分或反变换积分的前面 | 只说系数可放任一侧、乘积须为 1/(2π)，未说明这样做为何不改变变换对（归一化约定的等价性） |
| p31 | 更一般地，如果 f(r,t) 是一个在三维无界空间中随时间变化的函数 | 从二维 (x,t) 的 (2π)² 直接跳到三维 (r,t) 的 (2π)⁴，未说明每加一个积分变量就多一个 1/(2π) |
| p32 | 再利用 ∫₀^∞ e^{−ax²}cos(bx)dx=(1/2)√(π/a)e^{−b²/4a} | 高斯积分公式直接引用（未推导），也没写把 a→a²/2 代进去、b→k 代进去的具体替换 |
| p33 | 采用留数定理来求解无穷积分 | 只宣告方法，未给围道、未处理 t=0 是实轴极点这一特殊情形，留到 p34 且仍只给公式 |
| p34 | （绿框）∫f(x)e^{imx}dx=2πiΣRes+πiRes[f(b)e^{imb}]_{实轴} | 含实轴极点的留数公式直接给出（半留数 πi），未推导；且两条 ∫(1/(2iπt))e^{i(ω±ω₀)t}dt 的 ±1/2 结果未展示留数计算 |
| p36 | 在球坐标系中，选取 k 的方向沿 z 轴，并利用 dr=r²dr sinθdθdφ，k·r=kr cosθ | 只说"选取 k 沿 z 轴"，未说明为什么可以这样选（球对称性/旋转不变），也未说明 φ 积分先给出 2π |
| p37 | =1/(4π²)∫…rdr·(1/(ikr))(e^{ikr}−e^{−ikr}) | 把 ∫₀^π sinθ e^{−ikr cosθ}dθ 的求值一步跳过（换元 u=cosθ 的过程全无），r²/r 的约去也没写 |
| p38 | 下面采用分步积分法 | 两次分部积分被压成四行，边界项 e^{−r/λ}cos(kr)|₀^∞ = −1 的取值没写；最后由 ∫=1/k−(1/(k²λ²))∫ 解出 kλ²/(1+k²λ²) 也未展示移项 |
| p41 | 其中要求 f^{(n−1)}(x)|_{x=±∞}=0 | 只对 n=1 做了分部积分，n≥2 用"类推"两字带过；边界项为零的条件也没解释为何需要 |
| p43 | 由导数定理得到：φ′(x)⇌ikΦ(k) | 未验证 φ(−∞)=0（导数定理I 的前提），直接套用；φ 的定义含下限 −∞ 也未讨论收敛性 |
| p44 | 当 a<0 时，则有 | 只说明"限从 ∞ 到 −∞ 翻转得负号"，未讨论 a=0 的退化情形（定理要求 a≠0） |
| p46 | 定义函数 f₁(x) 和 f₂(x) 的卷积为…则它的傅里叶积分变换为…f₁*f₂⇌2πF₁F₂ | 卷积定理的 2π 系数直接给出（与常见教材的 F₁F₂ 形式不同），未说明它由 1/(2π) 的变换约定带来 |
| p47 | =2πF₁(k)F₂(k) | 最后一步从 (1/2π)·(2πF₁)·(2πF₂) 跳到 2πF₁F₂，两个 2π 的来源（F 定义里的 1/(2π)）未点明 |
| p48 | 根据卷积定义，有 f₁f₂⇌F₁*F₂ | 证明中第三行到第四行省掉 (1/2π)·2π 相消，且"根据卷积定义"一句其实是在证明结束才补的 |
| p49 | 对两边进行傅里叶变换，则有 2πF[f]·F[1/(x²+a²)]=F[1/(x²+b²)] | 未说明卷积定理的 2π 如何进式、为何可以直接除过去；也用到"F 是线性可逆"这一隐含前提 |
| p49 | =1/(2π)(−2πi)Res[…]_{z=−ai}（k>0）／=1/(2π)(2πi)Res[…]_{z=ai}（k<0） | 围道选择（k>0 取下半平面）与留数符号只在结果里体现，未画围道、未说明 |
| p51 | 当细杆长度无限小，即 l→0 时 | 从 ρ=m/l（|x|≤l/2）直接跳到 ρ=∞（x=0）、0（x≠0），l→0 的极限过程与"积分仍为 m"的相容性未论证 |
| p52 | 为了描述质点和点电荷的空间分布…在物理学中可引入一个所谓的 δ 函数来描述 | 定义式 δ(x−x₀)={0,∞} 是"引入"而非"推导"，未说明这样一个不是函数的对象如何合法（广义函数/分布） |
| p54 | 即 δ(x)=dH(x)/dx | 在广义函数意义下对含跳跃的 H(x) 求导未作任何说明，也未讨论 x=0 处 H 无经典导数 |
| p55 | (4) 若 φ(x)=0 的实根为 xₖ，且全为单根，则 δ[φ(x)]=Σδ(x−xₖ)/|φ′(xₖ)| | 复合函数公式直接给出，未推导（通常要用 φ 在根处的线性化 + δ 的缩放性质），也未讨论重根情形 |
| p56 | 如果一个函数 f(x) 具有上述两个特征，就可以用来构造 δ(x) | 只验证 rect 型例子的"积分=1"与"f(0)=∞"，未说明"两个特征"为何足以在广义函数意义下确定 δ |
| p57 | 例如 f(x)=lim_{k→∞}(1/π)sin(kx)/x=δ(x) | 三个例子都只算归一化积分、未验证 x≠0 时趋于 0，也未说明这个极限是在积分意义下（弱极限）成立 |
| p58 | 利用 δ 函数的傅里叶积分式，很容易推导出它的广义函数表示式 | "很容易"三字代替了 ∫_{−k}^{k}e^{ikx}dk 的求值与 k→∞ 的极限交换（广义函数意义下的极限）说明 |
| p59 | 严格说，函数 sin ax 和 cos ax 并不满足绝对可积条件，但是利用 δ 函数的定义，可以计算出他们的傅里叶变换式 | 明知不满足绝对可积仍直接套用积分公式，未说明这是在广义函数意义下取极限（ε→0⁺ 的衰减因子）才合法 |
| p60 | =1/(ik)(e^{ikr₀}−e^{−ikr₀}) | 中间 ∫₀^π sinθ e^{−ikr₀cosθ}dθ 的求值整段省略（只有上一行的设置式），一步跳到结果 |
| p61 | 利用留数定理，得到 g(x)=−(1/(2a))e^{−a|x−x₀|} | 从 ∫e^{ik(x−x₀)}/(k²+a²)dk 到 e^{−a|x−x₀|} 的留数计算（含 k 正负两支、闭合方向）全部省略，是本章最大的一处跳步 |
| p62 | 利用例3 的结果，有 g(x,x′)=−(1/(2a))e^{−a|x−x′|} | 把例3 的 x₀ 换成 x′ 直接搬用，未说明 g(x,x′) 与 g(x−x′) 的平移不变性；"设 u=∫gf dx′ 则 g 满足同方程"的叠加原理也未论证 |
| p62 | 上述求法为求解无界区域中的常微分方程的格林函数法。将在第十一章讨论。 | 只给了"格林函数法"这个名字与章节指引，方法的一般框架（为什么可以这样叠加）完全未讲 |
