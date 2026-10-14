---
tags:
  - QM/WKB
  - QM/半经典近似
  - QM/隧穿
  - QM/连接公式
aliases:
  - WKB近似
  - 玻尔-索末菲量子化
  - Gamow隧穿
created: 2025-01-01
updated: 2025-01-01
---

> [!summary] 算法执行总览
> WKB半经典近似的核心操作流程：在经典区域与经典禁区分别采用指数型振荡/衰减近似解，通过**转折点邻域的Airy函数线性势解**完成两类解的平滑衔接，最终导出量子化条件与隧穿几率。执行顺序为：① 分区写出WKB形式解 → ② 在转折点附近用Airy函数匹配相位与振幅 → ③ 提取连接公式 → ④ 施加边界条件（束缚态或隧穿）得到量化条件或透射系数。

---

## 一、推导机理与核心数学定义

### 1.1 定态Schrödinger方程与WKB拟设

一维定态Schrödinger方程：

$$
-\frac{\hbar^2}{2m}\frac{d^2\psi}{dx^2} + V(x)\psi = E\psi
$$

定义经典动量 $p(x) = \sqrt{2m[E - V(x)]}$。WKB方法的核心拟设是波函数具有形式

$$
\psi(x) = A(x) \exp\left[\frac{i}{\hbar} S(x)\right]
$$

将上式代入Schrödinger方程，保留至 $\hbar$ 的一阶项（半经典极限 $\hbar \to 0$），得到：

- **经典区域**（$E > V(x)$，$p(x)$ 为实数）：

$$
\psi(x) \approx \frac{C_1}{\sqrt{p(x)}} \exp\left(\frac{i}{\hbar}\int^x p(x') dx'\right) + \frac{C_2}{\sqrt{p(x)}} \exp\left(-\frac{i}{\hbar}\int^x p(x') dx'\right)
$$

- **经典禁区**（$E < V(x)$，定义 $\kappa(x) = \sqrt{2m[V(x) - E]} = |p(x)|$）：

$$
\psi(x) \approx \frac{D_1}{\sqrt{\kappa(x)}} \exp\left(\frac{1}{\hbar}\int^x \kappa(x') dx'\right) + \frac{D_2}{\sqrt{\kappa(x)}} \exp\left(-\frac{1}{\hbar}\int^x \kappa(x') dx'\right)
$$

### 1.2 转折点与WKB失效条件

转折点 $x_0$ 定义为 $E = V(x_0)$，即 $p(x_0) = 0$。此时 $\frac{1}{\sqrt{p(x)}}$ 发散，WKB近似完全失效。WKB近似的有效性判据为：

$$
\left| \frac{d\lambda}{dx} \right| \ll 1, \quad \lambda(x) = \frac{2\pi\hbar}{p(x)}
$$

即de Broglie波长在局部空间尺度内变化足够缓慢。在转折点附近，该条件必然被破坏。

### 1.3 转折点邻域的Airy函数衔接

在转折点 $x_0$ 附近，将势能线性化：

$$
V(x) \approx V(x_0) + V'(x_0)(x - x_0) = E + V'(x_0)(x - x_0)
$$

定义无量纲变量

$$
z = \left(\frac{2m|V'(x_0)|}{\hbar^2}\right)^{1/3} (x - x_0)
$$

则Schrödinger方程化为Airy方程：

$$
\frac{d^2\psi}{dz^2} - z\psi = 0
$$

其通解为Airy函数线性组合 $\psi(z) = a\,\text{Ai}(z) + b\,\text{Bi}(z)$。利用Airy函数的渐近形式（$z \to +\infty$ 指数衰减，$z \to -\infty$ 振荡），与两侧WKB解匹配，得到**连接公式**。

### 1.4 连接公式（右转折点 $x_0$，经典区域在左侧）

设经典区域为 $x < x_0$，禁区为 $x > x_0$。定义

$$
\phi(x) = \frac{1}{\hbar}\int_x^{x_0} p(x') dx' \quad (x < x_0)
$$

$$
\kappa(x) = \frac{1}{\hbar}\int_{x_0}^{x} |p(x')| dx' \quad (x > x_0)
$$

则连接公式为：

$$
\frac{C}{\sqrt{p(x)}} \cos\left(\phi(x) - \frac{\pi}{4}\right) \quad \longleftrightarrow \quad \frac{C}{\sqrt{2\kappa(x)}} \exp\left(-\kappa(x)\right)
$$

即禁区内的**指数衰减解**（不含增长项）唯一对应经典区域内的**余弦振荡解**，且相位修正为 $-\pi/4$。

### 1.5 玻尔-索末菲量子化条件

对束缚态，左右两个转折点 $x_1 < x_2$ 均需施加连接条件。左转折点要求波函数在 $x < x_1$ 的禁区内指数衰减，右转折点要求 $x > x_2$ 的禁区内指数衰减。两端的连接公式共同约束振荡区域的相位，得到：

$$
\frac{1}{\hbar}\int_{x_1}^{x_2} p(x) dx = \left(n + \frac{1}{2}\right)\pi, \quad n = 0, 1, 2, \cdots
$$

即

$$
\oint p(x) dx = 2\int_{x_1}^{x_2} p(x) dx = \left(n + \frac{1}{2}\right) 2\pi\hbar
$$

### 1.6 Gamow隧穿几率

对势垒穿透问题（入射能量 $E$ 低于势垒峰值），设转折点为 $x_1$ 与 $x_2$（$E = V(x_1) = V(x_2)$），隧穿几率在WKB框架下为：

$$
T \approx \exp\left(-\frac{2}{\hbar}\int_{x_1}^{x_2} |p(x)| dx\right)
$$

---

## 二、⚠️ 致命失分陷阱与临界边界

1. **转折点处直接代入WKB解**：$p(x_0)=0$ 导致 $\frac{1}{\sqrt{p(x)}}$ 发散，波函数在转折点处无界。任何试图在转折点处直接使用WKB公式的做法均为错误，必须采用Airy函数过渡。

2. **连接公式方向性误用**：连接公式具有严格的方向性——禁区内的指数衰减解对应经典区域的余弦解（相位 $-\pi/4$），而指数增长解对应正弦解。若禁区两侧均为衰减边界条件，则经典区域只能取余弦形式，不能随意混用正弦/余弦。

3. **相位因子遗漏**：连接公式中的 $\pi/4$ 相位偏移不可忽略。若遗漏该相位，玻尔-索末菲条件将退化为 $\oint p\,dx = n\cdot 2\pi\hbar$（整数 $n$），与精确解（如谐振子 $E_n = (n+1/2)\hbar\omega$）不符。

4. **量子化条件中 $n$ 的起始值**：玻尔-索末菲条件中的 $n$ 从 0 开始计数（$n = 0, 1, 2, \ldots$），对应基态 $n=0$。若误从 $n=1$ 开始，将遗漏基态能级。

5. **Gamow公式的适用边界**：$T \approx \exp(-2\gamma)$ 仅在 $\gamma = \frac{1}{\hbar}\int_{x_1}^{x_2}|p|dx \gg 1$ 时成立（弱隧穿极限）。当势垒很薄或入射能量接近势垒顶部时，前置因子（$\sim 1$ 量级）不可忽略，需使用更精确的传输矩阵方法。

6. **转折点处势能斜率 $V'(x_0) = 0$**：若转折点恰好是势能的极值点（如谐振子转折点处 $V'(x_0) \neq 0$ 但势垒顶部 $V'(x_0)=0$），线性化失效，需采用抛物近似（抛物柱函数），不能直接套用Airy连接公式。

7. **多转折点情形**：当 $E$ 与势能曲线有超过两个交点时，需分段处理并在每个转折点处分别匹配，不能将连接公式简单叠加。

---

## 三、经典范例手把手演算

### 3.1 一维无限深势阱的WKB修正（验证半整数量子化）

**问题**：质量为 $m$ 的粒子束缚在 $0 < x < a$ 的一维势阱中，阱内 $V=0$，阱壁为无限高陡壁。用WKB方法求能级。

**演算**：

**步骤1**：阱内 $p(x) = \sqrt{2mE}$ 为常数。转折点位于 $x=0$ 与 $x=a$（无限高势垒边界）。

**步骤2**：在 $x=0$ 处，波函数必须为零（刚性边界），不能直接套用光滑势垒的连接公式。WKB解在阱内为：

$$
\psi(x) = \frac{C}{\sqrt{p}} \sin\left(\frac{1}{\hbar}\int_0^x p\,dx'\right) = \frac{C}{\sqrt{p}} \sin\left(\frac{\sqrt{2mE}}{\hbar}x\right)
$$

**步骤3**：在 $x=a$ 处施加 $\psi(a)=0$：

$$
\sin\left(\frac{\sqrt{2mE}}{\hbar}a\right) = 0 \quad \Rightarrow \quad \frac{\sqrt{2mE}}{\hbar}a = n\pi, \quad n = 1, 2, 3, \ldots
$$

**步骤4**：解出能量：

$$
E_n = \frac{n^2\pi^2\hbar^2}{2ma^2}, \quad n = 1, 2, 3, \ldots
$$

**验算**：与精确解完全一致（无限深方阱精确解即为正弦函数）。此处WKB给出精确结果，因为 $p$ 为常数时WKB近似退化为精确解。

---

### 3.2 谐振子的WKB量子化

**问题**：$V(x) = \frac{1}{2}m\omega^2 x^2$，求WKB能级。

**演算**：

**步骤1**：转折点满足 $E = \frac{1}{2}m\omega^2 x_0^2$，即 $x_0 = \pm\sqrt{\frac{2E}{m\omega^2}}$。

**步骤2**：经典动量 $p(x) = \sqrt{2mE - m^2\omega^2 x^2} = m\omega\sqrt{x_0^2 - x^2}$。

**步骤3**：玻尔-索末菲条件：

$$
\oint p\,dx = 2\int_{-x_0}^{x_0} m\omega\sqrt{x_0^2 - x^2}\,dx = \left(n + \frac{1}{2}\right)2\pi\hbar
$$

**步骤4**：计算积分。令 $x = x_0\sin\theta$，$dx = x_0\cos\theta\,d\theta$，积分限 $\theta: -\pi/2 \to \pi/2$：

$$
\int_{-x_0}^{x_0}\sqrt{x_0^2 - x^2}\,dx = x_0^2\int_{-\pi/2}^{\pi/2}\cos^2\theta\,d\theta = x_0^2 \cdot \frac{\pi}{2}
$$

**步骤5**：代入：

$$
2m\omega \cdot x_0^2 \cdot \frac{\pi}{2} = m\omega\pi x_0^2 = \left(n+\frac{1}{2}\right)2\pi\hbar
$$

**步骤6**：利用 $x_0^2 = \frac{2E}{m\omega^2}$：

$$
m\omega\pi \cdot \frac{2E}{m\omega^2} = \frac{2\pi E}{\omega} = \left(n+\frac{1}{2}\right)2\pi\hbar
$$

**步骤7**：解出能量：

$$
E_n = \left(n + \frac{1}{2}\right)\hbar\omega, \quad n = 0, 1, 2, \ldots
$$

**验算**：与谐振子精确能级完全一致。此例说明连接公式中的 $\pi/4$ 相位修正（即半整数 $n+1/2$）对正确量子化至关重要。

---

### 3.3 方势垒隧穿的Gamow公式

**问题**：粒子以能量 $E$ 入射一维方势垒 $V(x) = V_0$（$0 < x < a$），$E < V_0$。求隧穿几率。

**演算**：

**步骤1**：转折点即势垒边界 $x_1 = 0$，$x_2 = a$。禁区内 $|p(x)| = \sqrt{2m(V_0 - E)}$ 为常数。

**步骤2**：Gamow公式：

$$
T \approx \exp\left(-\frac{2}{\hbar}\int_0^a \sqrt{2m(V_0 - E)}\,dx\right) = \exp\left(-\frac{2a}{\hbar}\sqrt{2m(V_0 - E)}\right)
$$

**步骤3**：定义 $\kappa = \frac{\sqrt{2m(V_0 - E)}}{\hbar}$，则：

$$
T \approx e^{-2\kappa a}
$$

**验算**：方势垒的精确隧穿系数为：

$$
T_{\text{exact}} = \left[1 + \frac{V_0^2\sinh^2(\kappa a)}{4E(V_0 - E)}\right]^{-1}
$$

当 $\kappa a \gg 1$ 时，$\sinh^2(\kappa a) \approx \frac{1}{4}e^{2\kappa a}$，则：

$$
T_{\text{exact}} \approx \left[\frac{V_0^2}{16E(V_0 - E)}e^{2\kappa a}\right]^{-1} = \frac{16E(V_0 - E)}{V_0^2}e^{-2\kappa a}
$$

WKB结果 $e^{-2\kappa a}$ 与精确解指数因子一致，前置因子 $\frac{16E(V_0-E)}{V_0^2}$ 在 $\kappa a \gg 1$ 时对数量级影响可忽略，验证了Gamow公式的指数主导行为。

---

## 四、出处与纸质笔记坐标

**指定教材**：Griffiths, *Introduction to Quantum Mechanics*, 3rd Edition  
**章节**：§9.1 (P348–P355) WKB近似的基本思想与连接公式；§9.2 (P355–P362) 量子化条件；§9.3 (P362–P368) 隧穿与Gamow因子

**纸质活页留痕槽位**：`[活页-QM-21]`

**手写推导建议**：
- 活页左栏：完整推导转折点邻域Airy方程约化过程（含无量纲变量 $z$ 的引入）
- 活页右栏：连接公式的渐近匹配细节（Airy函数 $z \to \pm\infty$ 渐近式与WKB解的系数比对）
- 底部留白：标注本节与谐振子精确解、方势垒精确隧穿系数的对照验算结果

**全景图挂载**：`![[QM-WKB-连接公式-全景图.png]]`

---

*本卡片覆盖Griffiths §9.1–§9.3全部核心考点，含推导机理、失分陷阱、完整演算与教材坐标，可直接配合活页-QM-21进行手写推导与错题订正。*

---
**知识图谱导航**：[[00_量子力学_学习全景图]]
