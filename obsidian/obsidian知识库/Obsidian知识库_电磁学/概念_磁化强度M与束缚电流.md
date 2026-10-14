---
tags:
  - 电磁学
  - 磁化强度
  - 束缚电流
  - 磁偶极矩
  - 抗磁性
  - 顺磁性
  - 铁磁性
aliases:
  - 磁化强度与束缚电流
  - 束缚电流微观机制
created: 2025-04-11
updated: 2025-04-11
---

> [!summary] 核心认知先验
> 宏观磁化强度 $\mathbf{M}$ 是单位体积内微观磁偶极矩的统计平均，其旋度与叉积分别给出体束缚电流密度 $\mathbf{J}_b$ 与面束缚电流密度 $\mathbf{K}_b$。束缚电流的物理本质是真实电荷的闭合循环运动，**不存在磁荷**，因此 $\nabla \cdot \mathbf{J}_b \equiv 0$ 严格成立。物质的磁性响应（抗磁、顺磁、铁磁）源于电子轨道与自旋磁矩在外场下的不同动力学行为。

---

## 一、推导机理与核心数学定义

### 1.1 微观磁矩的起源

原子尺度上的磁矩主要来自两个渠道：

1. **电子轨道运动**：电子绕核做圆周运动，等效于一个闭合电流环。设电子电荷为 $-e$，轨道角动量为 $\mathbf{L}$，则轨道磁矩为

$$
\boldsymbol{\mu}_{\text{orb}} = -\frac{e}{2m_e}\mathbf{L} = -\frac{\mu_B}{\hbar}\mathbf{L},
$$

其中 $\mu_B = \dfrac{e\hbar}{2m_e}$ 为玻尔磁子。

2. **电子自旋**：自旋角动量为 $\mathbf{S}$，对应自旋磁矩

$$
\boldsymbol{\mu}_{\text{spin}} = -g_e\frac{\mu_B}{\hbar}\mathbf{S},
$$

其中 $g_e \approx 2.0023$ 为电子 $g$ 因子。

### 1.2 宏观磁化强度矢量

设体积 $\Delta V$ 内包含 $N$ 个磁偶极子，第 $i$ 个磁偶极子的磁矩为 $\boldsymbol{\mu}_i$，则宏观磁化强度定义为

$$
\mathbf{M} \equiv \lim_{\Delta V \to 0} \frac{1}{\Delta V}\sum_{i=1}^{N}\boldsymbol{\mu}_i.
$$

**直觉**：$\mathbf{M}$ 是单位体积的净磁偶极矩密度，量纲为 $\text{A/m}$（安培每米），它刻画了物质被磁化的程度与方向。

### 1.3 束缚电流的矢量势推导

磁偶极子密度 $\mathbf{M}(\mathbf{r}')$ 在远场点 $\mathbf{r}$ 处产生的矢量势为

$$
\mathbf{A}(\mathbf{r}) = \frac{\mu_0}{4\pi}\int_V \frac{\mathbf{M}(\mathbf{r}') \times (\mathbf{r} - \mathbf{r}')}{|\mathbf{r} - \mathbf{r}'|^3}\, d^3r'.
$$

利用恒等式

$$
\nabla'\frac{1}{|\mathbf{r} - \mathbf{r}'|} = \frac{\mathbf{r} - \mathbf{r}'}{|\mathbf{r} - \mathbf{r}'|^3},
$$

代入得

$$
\mathbf{A}(\mathbf{r}) = \frac{\mu_0}{4\pi}\int_V \mathbf{M}(\mathbf{r}') \times \nabla'\frac{1}{|\mathbf{r} - \mathbf{r}'|}\, d^3r'.
$$

利用矢量恒等式 $\mathbf{M} \times \nabla' f = f(\nabla' \times \mathbf{M}) - \nabla' \times (f\mathbf{M})$，可得

$$
\mathbf{A}(\mathbf{r}) = \frac{\mu_0}{4\pi}\int_V \frac{\nabla' \times \mathbf{M}(\mathbf{r}')}{|\mathbf{r} - \mathbf{r}'|}\, d^3r' + \frac{\mu_0}{4\pi}\oint_S \frac{\mathbf{M}(\mathbf{r}') \times \hat{\mathbf{n}}'}{|\mathbf{r} - \mathbf{r}'|}\, dS'.
$$

与电流密度矢量势公式 $\mathbf{A} = \dfrac{\mu_0}{4\pi}\int \dfrac{\mathbf{J}}{|\mathbf{r}-\mathbf{r}'|}\, d^3r'$ 对照，定义：

$$
\boxed{\mathbf{J}_b = \nabla \times \mathbf{M}} \qquad \text{(体束缚电流密度)}
$$

$$
\boxed{\mathbf{K}_b = \mathbf{M} \times \hat{\mathbf{n}}} \qquad \text{(面束缚电流密度)}
$$

其中 $\hat{\mathbf{n}}$ 为磁介质表面的外法向单位矢量。

### 1.4 三类磁性材料的微观响应

| 类型 | 微观机制 | $\mathbf{M}$ 与外场方向 | 典型特征 |
|------|----------|------------------------|----------|
| **抗磁性** | 外场感生环流，冷茨定律抵抗磁通变化 | 反平行 | $\chi_m < 0$，极弱（$\sim 10^{-5}$） |
| **顺磁性** | 固有磁矩热运动被外场部分取向 | 平行 | $\chi_m > 0$，弱（$\sim 10^{-3}$） |
| **铁磁性** | 相邻原子自旋交换耦合，畴内自发磁化 | 平行且可保留 | $\chi_m \gg 1$，有磁滞回线 |

**抗磁性的冷茨微观图像**：外场 $\mathbf{B}_0$ 建立时，电子轨道感生附加环流，该环流产生的磁矩方向与外场相反（冷茨定律），表现为 $\mathbf{M}$ 反平行于 $\mathbf{B}_0$。此效应存在于所有物质中，但仅在无固有磁矩时被单独显现。

---

## 二、⚠️ 致命失分陷阱与临界边界

### 陷阱 1：磁荷不存在

**错误认知**：将 $\nabla \cdot \mathbf{B} = 0$ 与 $\nabla \cdot \mathbf{E} = \rho/\varepsilon_0$ 类比，误以为束缚电流对应某种"束缚磁荷"。

**正解**：束缚电流的物理本质是**真实电子电荷的闭合循环运动**。$\mathbf{J}_b = \nabla \times \mathbf{M}$ 只是对大量微观环流的宏观统计描述，不引入任何磁单极子。

### 陷阱 2：$\nabla \cdot \mathbf{J}_b \equiv 0$ 的严格性

对任意矢量场取旋度的散度恒为零：

$$
\nabla \cdot \mathbf{J}_b = \nabla \cdot (\nabla \times \mathbf{M}) \equiv 0.
$$

**推论**：束缚电流线永远是闭合的，不存在源头或汇。若计算得到 $\nabla \cdot \mathbf{J}_b \neq 0$，则必为计算错误。

### 陷阱 3：面束缚电流的方向判定

$\mathbf{K}_b = \mathbf{M} \times \hat{\mathbf{n}}$ 的叉积顺序不可颠倒。若误写为 $\hat{\mathbf{n}} \times \mathbf{M}$，方向将完全反转。

**记忆法则**：右手四指从 $\mathbf{M}$ 弯向 $\hat{\mathbf{n}}$，拇指指向 $\mathbf{K}_b$ 方向。

### 陷阱 4：均匀磁化与体束缚电流

若 $\mathbf{M}$ 为常数（均匀磁化），则

$$
\mathbf{J}_b = \nabla \times \mathbf{M} = 0,
$$

但面束缚电流 $\mathbf{K}_b = \mathbf{M} \times \hat{\mathbf{n}}$ **不一定为零**。均匀磁化的柱体侧面存在等效螺线管电流，这是求解磁场时必须计入的边界源。

### 陷阱 5：抗磁性并非"排斥"的宏观表现

抗磁性是**感生**效应，与磁矩是否固有无关。不要将抗磁性理解为磁矩被外场"推开"，而是外场变化过程中冷茨定律驱动的瞬态环流在稳态下的残留。

---

## 三、经典范例手把手演算

### 范例：均匀磁化圆柱体的束缚电流

**题目**：一半径为 $R$、长度为 $L$ 的圆柱形磁介质，沿轴向均匀磁化，磁化强度为 $\mathbf{M} = M_0 \hat{\mathbf{z}}$（$M_0$ 为常数）。求体束缚电流密度与面束缚电流密度。

**第一步：体束缚电流**

$$
\mathbf{J}_b = \nabla \times \mathbf{M} = \nabla \times (M_0 \hat{\mathbf{z}}).
$$

在柱坐标 $(s, \phi, z)$ 中展开旋度：

$$
\nabla \times \mathbf{M} = \frac{1}{s}\begin{vmatrix}
\hat{\mathbf{s}} & s\hat{\boldsymbol{\phi}} & \hat{\mathbf{z}} \\
\dfrac{\partial}{\partial s} & \dfrac{\partial}{\partial \phi} & \dfrac{\partial}{\partial z} \\
0 & 0 & M_0
\end{vmatrix}.
$$

由于 $M_0$ 为常数，所有偏导数为零：

$$
\mathbf{J}_b = \mathbf{0}.
$$

**第二步：面束缚电流**

圆柱面有三个表面：顶面、底面、侧面。

- **顶面**（$z = L/2$）：外法向 $\hat{\mathbf{n}} = \hat{\mathbf{z}}$，

$$
\mathbf{K}_b^{\text{top}} = \mathbf{M} \times \hat{\mathbf{n}} = M_0\hat{\mathbf{z}} \times \hat{\mathbf{z}} = \mathbf{0}.
$$

- **底面**（$z = -L/2$）：外法向 $\hat{\mathbf{n}} = -\hat{\mathbf{z}}$，

$$
\mathbf{K}_b^{\text{bottom}} = M_0\hat{\mathbf{z}} \times (-\hat{\mathbf{z}}) = \mathbf{0}.
$$

- **侧面**（$s = R$）：外法向 $\hat{\mathbf{n}} = \hat{\mathbf{s}}$，

$$
\mathbf{K}_b^{\text{side}} = M_0\hat{\mathbf{z}} \times \hat{\mathbf{s}} = M_0\hat{\boldsymbol{\phi}}.
$$

**第三步：物理诠释与验算**

侧面束缚电流沿 $\hat{\boldsymbol{\phi}}$ 方向环绕，等效于一个螺线管电流。该电流在柱内产生的磁场沿 $+\hat{\mathbf{z}}$ 方向，与 $\mathbf{M}$ 同向，自洽。

**验算**：总束缚电流的闭合性。侧面电流沿圆周方向流动，在顶面和底面处 $\mathbf{K}_b = 0$，电流线在侧面自行闭合，满足 $\nabla \cdot \mathbf{J}_b \equiv 0$ 的全局要求。

---

## 四、出处与纸质笔记坐标

**教材出处**：Purcell, *Electricity and Magnetism*, 3rd Ed., Ch.10 §10.1–§10.7, pp. 263–285。

- §10.1–10.2：磁矩与轨道运动（P263–P268）
- §10.3：磁化强度矢量 $\mathbf{M}$ 的定义（P269–P272）
- §10.4：束缚电流的推导（P273–P277）
- §10.5：抗磁性（P278–P280）
- §10.6：顺磁性（P281–P282）
- §10.7：铁磁性（P283–P285）

**纸质活页留痕槽位**：[活页-EM-31]

- 左页：$\mathbf{M}$ 定义与束缚电流推导全过程手写复演
- 右页：抗磁/顺磁/铁磁三栏对比表 + 圆柱体范例的完整演算
- 底部留白：错题订正区（记录 $\mathbf{K}_b$ 方向判断失误案例）

---

**全景图**：磁化强度 $\mathbf{M}$ 作为桥梁，连接微观磁矩（轨道+自旋）与宏观电流描述（$\mathbf{J}_b$、$\mathbf{K}_b$），其散度恒为零的特性确保了束缚电流的闭合性，而三类磁性材料则展现了 $\mathbf{M}$ 在不同微观动力学下的丰富响应模式。

---

[[00_电磁学_学习全景图]]
