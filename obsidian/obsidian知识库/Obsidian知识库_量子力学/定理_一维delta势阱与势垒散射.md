---
tags: [量子力学, 束缚态, 散射态, δ势, 奇异势, 边界条件, 反射系数, 透射系数]
aliases: [一维δ势阱束缚态, δ势垒反射透射, Delta势散射]
created: 2025-04-14
updated: 2025-04-14
---

> [!summary] 定理核心论断
> 对于一维奇异势 $V(x) = -\alpha\,\delta(x)$（$\alpha > 0$ 为阱，$\alpha < 0$ 为垒），波函数在奇异点处保持连续，但其一阶导数发生由势强度决定的有限跳跃。该势场恰好支持**唯一一个**束缚态（当 $\alpha > 0$），能量为 $E = -\dfrac{m\alpha^2}{2\hbar^2}$；同时支持 $E > 0$ 的连续散射态，其反射系数 $R$ 与透射系数 $T$ 满足 $R + T = 1$ 的几率守恒律。对于 $\alpha < 0$（势垒），$E > 0$ 时量子粒子仍以非零几率穿透，与经典预期截然相反。

---

## 一、推导机理与核心数学定义

### 1.1 奇异势的物理直觉与定态方程

考虑一维含时薛定谔方程：

$$
i\hbar \frac{\partial \Psi(x,t)}{\partial t} = \left[ -\frac{\hbar^2}{2m} \frac{d^2}{dx^2} + V(x) \right] \Psi(x,t)
$$

代入定态分离 $\Psi(x,t) = \psi(x)\, e^{-iEt/\hbar}$，得到定态薛定谔方程：

$$
-\frac{\hbar^2}{2m} \frac{d^2\psi(x)}{dx^2} + V(x)\,\psi(x) = E\,\psi(x)
$$

其中 $V(x) = -\alpha\,\delta(x)$。$\delta(x)$ 为狄拉克函数，满足 $\delta(x) = 0\ (x \neq 0)$ 且 $\int_{-\infty}^{+\infty} \delta(x)\, dx = 1$。势仅在 $x = 0$ 处有定义，因此对 $x \neq 0$ 的区域，方程为自由粒子方程：

$$
-\frac{\hbar^2}{2m} \frac{d^2\psi(x)}{dx^2} = E\,\psi(x) \quad (x \neq 0)
$$

### 1.2 边界条件的严格推导

**连续性条件**：对定态方程在 $[-\epsilon, +\epsilon]$ 上积分并令 $\epsilon \to 0^+$。由于 $\psi$ 本身为物理态（有限），$\int_{-\epsilon}^{\epsilon} E\,\psi(x)\, dx \to 0$，而 $\int_{-\epsilon}^{\epsilon} V(x)\psi(x)\, dx = -\alpha\,\psi(0)$（$\delta$ 的筛选性质）。因此：

$$
-\frac{\hbar^2}{2m} \left[ \psi'(0^+) - \psi'(0^-) \right] - \alpha\,\psi(0) = 0
$$

整理得**一阶导数跳跃条件**：

$$
\boxed{\; \psi'(0^+) - \psi'(0^-) = -\frac{2m\alpha}{\hbar^2}\,\psi(0) \;}
$$

**连续性条件**：由 $\psi$ 的物理可积性（束缚态）或有限流密度（散射态），$\psi$ 在 $x=0$ 处连续：

$$
\boxed{\; \psi(0^+) = \psi(0^-) = \psi(0) \;}
$$

> 直觉：$\delta$ 势相当于在 $x=0$ 处放置一个无限薄但强度有限的“作用层”，波函数不能突变（否则动能发散），但斜率可以突变——突变幅度正比于势强度与波函数在该点的值。

---

## 二、⚠️ 致命失分陷阱与临界边界

1. **误将 $\psi'(0^+) = \psi'(0^-)$ 当作连续条件**：这是**错误**的。对有限深方势阱，导数连续源于势能有限；对 $\delta$ 势，导数必须跳跃。跳跃量公式为 $\Delta\psi' = -\dfrac{2m\alpha}{\hbar^2}\psi(0)$，**符号与 $\alpha$ 相关**。

2. **忽略 $\alpha$ 的符号区分**：$\alpha > 0$ 为吸引势（阱），存在束缚态；$\alpha < 0$ 为排斥势（垒），**不存在** $E < 0$ 的束缚态解。若将 $\alpha < 0$ 代入束缚态公式 $E = -m\alpha^2/(2\hbar^2)$ 会得到负能量，但该解不满足 $x \to \pm\infty$ 时 $\psi \to 0$ 的归一化条件——需检查指数衰减的符号。

3. **散射态中遗漏入射方向**：散射问题必须区分粒子从左侧入射（$x < 0$ 区域含入射波 $e^{ikx}$ 与反射波 $e^{-ikx}$，$x > 0$ 区域仅含透射波 $e^{ikx}$）与从右侧入射。若两侧都写双向行波，则无法唯一确定 $R$ 与 $T$。

4. **$\delta$ 势垒的经典直觉误导**：经典粒子遇势垒（$\alpha < 0$）必被反弹，$T_{\text{classical}} = 0$。但量子力学中，由于波函数的波动性与不确定性原理，粒子有非零透射几率。**这是考试中最常见的概念性失分点**。

5. **几率流密度计算错误**：反射系数与透射系数必须通过几率流密度 $j = \dfrac{\hbar}{2mi}\left(\psi^*\dfrac{d\psi}{dx} - \psi\dfrac{d\psi^*}{dx}\right)$ 定义，而非简单地取 $|A|^2$、$|B|^2$ 的比值。对平面波 $e^{ikx}$，$j = \dfrac{\hbar k}{m}$；对 $e^{-ikx}$，$j = -\dfrac{\hbar k}{m}$。方向必须计入。

6. **束缚态能量为负但有限**：$E = -\dfrac{m\alpha^2}{2\hbar^2}$ 是**唯一**束缚态能级，不存在激发态。这与有限深方势阱（可能有多个束缚态）不同，源于 $\delta$ 势只有一个束缚态的一般结论。

7. **$E = 0$ 的临界情形**：$E = 0$ 时 $k = 0$，平面波退化为常数，散射解的渐近形式需重新处理。此时 $R$ 与 $T$ 的定义需谨慎，通常取 $E \to 0^+$ 的极限。

---

## 三、经典范例手把手演算

### 3.1 束缚态求解（$\alpha > 0$）

**步骤 1**：设 $E < 0$，定义 $\kappa = \sqrt{\dfrac{-2mE}{\hbar^2}} > 0$。在 $x \neq 0$ 区域，方程为：

$$
\frac{d^2\psi}{dx^2} = \kappa^2 \psi
$$

**步骤 2**：通解为 $\psi(x) = A e^{\kappa x} + B e^{-\kappa x}$。束缚态要求 $x \to \pm\infty$ 时 $\psi \to 0$，因此：

$$
\psi(x) = \begin{cases} A\,e^{\kappa x}, & x < 0 \\ B\,e^{-\kappa x}, & x > 0 \end{cases}
$$

**步骤 3**：连续性条件 $\psi(0^+) = \psi(0^-)$ 给出 $A = B$。令 $A = B = C$，则：

$$
\psi(x) = C\,e^{-\kappa |x|}
$$

**步骤 4**：计算导数跳跃。对 $x < 0$，$\psi'(x) = C\kappa e^{\kappa x}$，故 $\psi'(0^-) = C\kappa$。对 $x > 0$，$\psi'(x) = -C\kappa e^{-\kappa x}$，故 $\psi'(0^+) = -C\kappa$。代入跳跃条件：

$$
(-C\kappa) - (C\kappa) = -\frac{2m\alpha}{\hbar^2} \cdot C
$$

化简：

$$
-2C\kappa = -\frac{2m\alpha}{\hbar^2} C
$$

$C \neq 0$（否则零解无物理意义），故：

$$
\kappa = \frac{m\alpha}{\hbar^2}
$$

**步骤 5**：由 $\kappa$ 的定义反解能量：

$$
E = -\frac{\hbar^2 \kappa^2}{2m} = -\frac{\hbar^2}{2m} \cdot \frac{m^2\alpha^2}{\hbar^4} = -\frac{m\alpha^2}{2\hbar^2}
$$

**步骤 6**：归一化确定 $C$：

$$
1 = \int_{-\infty}^{+\infty} |\psi(x)|^2 dx = |C|^2 \int_{-\infty}^{+\infty} e^{-2\kappa|x|} dx = |C|^2 \cdot 2\int_0^\infty e^{-2\kappa x} dx = |C|^2 \cdot \frac{1}{\kappa}
$$

取 $C = \sqrt{\kappa} = \sqrt{\dfrac{m\alpha}{\hbar^2}}$（取实正相位），得归一化束缚态：

$$
\boxed{\; \psi(x) = \sqrt{\frac{m\alpha}{\hbar^2}}\; e^{-m\alpha|x|/\hbar^2}, \quad E = -\frac{m\alpha^2}{2\hbar^2} \;}
$$

**验算**：将 $\psi$ 代回薛定谔方程。对 $x \neq 0$，$\psi'' = \kappa^2 \psi$，故 $-\dfrac{\hbar^2}{2m}\kappa^2\psi = -\dfrac{\hbar^2\kappa^2}{2m}\psi = E\psi$，满足。在 $x = 0$ 处，跳跃条件已精确满足。✓

### 3.2 散射态求解（$E > 0$，$\alpha$ 任意符号）

**步骤 1**：设 $E > 0$，定义波数 $k = \sqrt{\dfrac{2mE}{\hbar^2}} > 0$。设粒子从左侧入射，则：

$$
\psi(x) = \begin{cases} e^{ikx} + r\,e^{-ikx}, & x < 0 \\ t\,e^{ikx}, & x > 0 \end{cases}
$$

其中入射波振幅归一化为 1，$r$ 为反射振幅，$t$ 为透射振幅。

**步骤 2**：连续性条件 $\psi(0^+) = \psi(0^-)$：

$$
1 + r = t
$$

**步骤 3**：导数跳跃条件。对 $x < 0$：$\psi'(x) = ik e^{ikx} - ikr\,e^{-ikx}$，故 $\psi'(0^-) = ik(1 - r)$。对 $x > 0$：$\psi'(x) = ikt\,e^{ikx}$，故 $\psi'(0^+) = ikt$。代入跳跃条件：

$$
ikt - ik(1-r) = -\frac{2m\alpha}{\hbar^2} \cdot t
$$

化简：

$$
ik(t - 1 + r) = -\frac{2m\alpha}{\hbar^2} t
$$

**步骤 4**：由连续性条件 $t = 1 + r$，代入：

$$
ik[(1+r) - 1 + r] = ik(2r) = -\frac{2m\alpha}{\hbar^2}(1+r)
$$

即：

$$
2ikr = -\frac{2m\alpha}{\hbar^2}(1+r)
$$

解出 $r$：

$$
r\left(2ik + \frac{2m\alpha}{\hbar^2}\right) = -\frac{2m\alpha}{\hbar^2}
$$

$$
r = \frac{-\dfrac{2m\alpha}{\hbar^2}}{2ik + \dfrac{2m\alpha}{\hbar^2}} = \frac{-\dfrac{m\alpha}{\hbar^2}}{ik + \dfrac{m\alpha}{\hbar^2}}
$$

令 $\beta = \dfrac{m\alpha}{\hbar^2}$（量纲为 $1/\text{长度}$），则：

$$
\boxed{\; r = \frac{-\beta}{ik + \beta} \;}
$$

**步骤 5**：由 $t = 1 + r$：

$$
t = 1 - \frac{\beta}{ik + \beta} = \frac{ik + \beta - \beta}{ik + \beta} = \frac{ik}{ik + \beta}
$$

$$
\boxed{\; t = \frac{ik}{ik + \beta} \;}
$$

**步骤 6**：计算反射系数与透射系数。几率流密度：

- 入射波 $e^{ikx}$：$j_{\text{inc}} = \dfrac{\hbar k}{m}$
- 反射波 $r\,e^{-ikx}$：$j_{\text{ref}} = -\dfrac{\hbar k}{m}|r|^2$
- 透射波 $t\,e^{ikx}$：$j_{\text{trans}} = \dfrac{\hbar k}{m}|t|^2$

因此：

$$
R = \frac{|j_{\text{ref}}|}{|j_{\text{inc}}|} = |r|^2 = \frac{\beta^2}{k^2 + \beta^2}
$$

$$
T = \frac{|j_{\text{trans}}|}{|j_{\text{inc}}|} = |t|^2 = \frac{k^2}{k^2 + \beta^2}
$$

**步骤 7**：验证几率守恒：

$$
R + T = \frac{\beta^2}{k^2 + \beta^2} + \frac{k^2}{k^2 + \beta^2} = \frac{k^2 + \beta^2}{k^2 + \beta^2} = 1
$$

✓

**步骤 8**：用能量表达。$k = \sqrt{2mE}/\hbar$，$\beta = m\alpha/\hbar^2$，则：

$$
\boxed{\; R = \frac{1}{1 + \dfrac{2\hbar^2 E}{m\alpha^2}}, \quad T = \frac{1}{1 + \dfrac{m\alpha^2}{2\hbar^2 E}} \;}
$$

**关键物理结论**：当 $\alpha < 0$（势垒），$\beta < 0$，但 $\beta^2$ 不变，因此 $R$、$T$ 表达式不变。**势垒与势阱在 $E > 0$ 时具有完全相同的反射与透射系数**。当 $E \to 0$ 时 $T \to 0$；当 $E \to \infty$ 时 $T \to 1$。对任意有限 $E > 0$，$T > 0$——量子粒子可穿透势垒。

---

## 四、出处与纸质笔记坐标

**指定教材**：Griffiths, *Introduction to Quantum Mechanics*, 2nd Edition  
**章节**：§2.5 The Delta-Function Potential（P78–P85）；§2.6 The Finite Square Well 中散射态对比讨论（P85–P99）  
**核心公式定位**：束缚态能量见教材 Eq.(2.132)；反射/透射系数见 Eq.(2.141)–(2.142)

**纸质活页留痕槽位**：[活页-QM-07]

**手写推导建议**：
- 左页：完整推导束缚态（含归一化积分过程）
- 右页：散射态推导，重点标注 $r$、$t$ 的复数性质与 $R$、$T$ 的实值化过程
- 底部留白：对比有限深方势阱的束缚态数目与散射共振现象

**全景图挂载**：

```mermaid
graph TD
    A[一维δ势 Vx = -αδx] --> B{α > 0?}
    B -->|是| C[束缚态 E < 0]
    B -->|否| D[无束缚态]
    C --> E[唯一束缚态<br>E = -mα²/2ℏ²]
    C --> F[归一化波函数<br>ψx = √κ e^{-κ|x|}]
    A --> G[散射态 E > 0]
    G --> H[边界条件<br>ψ连续 + 导数跳跃]
    H --> I[反射振幅 r = -β/ik+β]
    H --> J[透射振幅 t = ik/ik+β]
    I --> K[R = β²/k²+β²]
    J --> L[T = k²/k²+β²]
    K --> M[R + T = 1]
    L --> M
    M --> N[势垒穿透效应<br>经典 vs 量子]
```

---

> [!warning] 考试高频提醒
> 1. 写跳跃条件时，务必先明确 $\psi'(0^+)$ 与 $\psi'(0^-)$ 各自对应哪个区域的表达式，再代入。
> 2. 散射态中 $r$、$t$ 一般为复数，$R = |r|^2$、$T = |t|^2$ 才是实数几率。
> 3. 束缚态归一化系数 $C = \sqrt{\kappa}$ 的量纲为 $L^{-1/2}$，与波函数量纲

---
**知识图谱导航**：[[00_量子力学_学习全景图]]
