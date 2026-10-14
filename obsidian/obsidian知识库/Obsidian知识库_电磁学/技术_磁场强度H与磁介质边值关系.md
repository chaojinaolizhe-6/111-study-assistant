---
tags:
  - 电磁学
  - 磁场强度
  - 磁介质
  - 边值关系
  - 解法卡
aliases:
  - 磁场强度H与边值关系
  - 辅助磁场H
  - 磁介质边界条件
created: 2025-04-12
updated: 2025-04-12
---

> [!summary] 算法执行总览
> 本卡处理磁介质存在时磁场求解的完整策略：引入辅助场 $\mathbf{H}$ 以剥离束缚电流的显式贡献，将安培环路定律改写为仅含自由电流的形式；结合线性介质的本构关系 $\mathbf{B} = \mu \mathbf{H}$，在界面处通过法向 $\mathbf{B}$ 连续与切向 $\mathbf{H}$ 跳跃条件联立求解。核心操作路径为：**识别自由电流密度 $\mathbf{J}_f$ → 求解 $\mathbf{H}$ → 乘以 $\mu$ 得 $\mathbf{B}$ → 由界面条件校验**。

---

## 一、推导机理与核心数学定义

### 1.1 辅助磁场 $\mathbf{H}$ 的定义与动机

在真空中，磁场由总电流（传导电流与束缚电流之和）激发。磁化介质内部的束缚电流密度为 $\mathbf{J}_b = \nabla \times \mathbf{M}$，这使得直接求解 $\mathbf{B}$ 时需同时处理未知的 $\mathbf{M}$ 分布。为简化，定义辅助场：

$$
\mathbf{H} \equiv \frac{\mathbf{B}}{\mu_0} - \mathbf{M}
$$

对上式两侧取旋度：

$$
\nabla \times \mathbf{H} = \frac{1}{\mu_0} \nabla \times \mathbf{B} - \nabla \times \mathbf{M}
$$

由安培定律 $\nabla \times \mathbf{B} = \mu_0 (\mathbf{J}_f + \mathbf{J}_b)$ 及 $\mathbf{J}_b = \nabla \times \mathbf{M}$，代入得：

$$
\nabla \times \mathbf{H} = \mathbf{J}_f + \mathbf{J}_b - \mathbf{J}_b = \mathbf{J}_f
$$

**结论**：$\mathbf{H}$ 的旋度仅由自由传导电流密度 $\mathbf{J}_f$ 决定，束缚电流的贡献被 $\mathbf{M}$ 的旋度项精确抵消。对应的积分形式为：

$$
\oint_C \mathbf{H} \cdot d\boldsymbol{\ell} = I_{f,\text{enc}}
$$

其中 $I_{f,\text{enc}}$ 为穿过环路 $C$ 所张曲面的自由电流代数和。

### 1.2 线性磁介质的本构关系

对于各向同性线性介质，磁化强度正比于 $\mathbf{H}$：

$$
\mathbf{M} = \chi_m \mathbf{H}
$$

其中 $\chi_m$ 为磁化率（无量纲）。代入定义式：

$$
\mathbf{B} = \mu_0 (\mathbf{H} + \mathbf{M}) = \mu_0 (1 + \chi_m) \mathbf{H} \equiv \mu_0 \mu_r \mathbf{H} \equiv \mu \mathbf{H}
$$

定义相对磁导率 $\mu_r = 1 + \chi_m$，绝对磁导率 $\mu = \mu_0 \mu_r$。注意：**此关系仅在介质内部成立**，且要求介质为线性、均匀（或逐点均匀）。

### 1.3 界面匹配条件的推导

考虑两种磁介质（参数 $\mu_1, \mu_2$）的分界面，界面法向单位矢量 $\hat{\mathbf{n}}$ 由介质 1 指向介质 2。

**法向条件**：由 $\nabla \cdot \mathbf{B} = 0$（$\mathbf{B}$ 为螺线场），对跨越界面的薄饼状高斯面应用散度定理，令厚度趋于零，得：

$$
B_{1n} = B_{2n} \quad \Longleftrightarrow \quad \mu_1 H_{1n} = \mu_2 H_{2n}
$$

**切向条件**：由 $\nabla \times \mathbf{H} = \mathbf{J}_f$，对跨越界面的矩形环路应用斯托克斯定理，令短边趋于零，得：

$$
H_{1t} - H_{2t} = K_f
$$

其中 $K_f$ 为界面上的自由面电流密度（单位：A/m），方向垂直于 $\hat{\mathbf{n}}$ 与切向分量构成的平面。若界面无自由面电流，则 $H_{1t} = H_{2t}$。

---

## 二、⚠️ 致命失分陷阱与临界边界

### 2.1 $\mathbf{B}$ 与 $\mathbf{H}$ 的物理地位混淆

$\mathbf{B}$ 是基本物理场，满足 $\nabla \cdot \mathbf{B} = 0$，其力效应由洛伦兹力公式 $\mathbf{F} = q\mathbf{v} \times \mathbf{B}$ 给出。$\mathbf{H}$ 是计算辅助场，**不具有直接的力学意义**。在永磁体内部（$\mathbf{M}$ 很大且与 $\mathbf{H}$ 反向的区域），可能出现 $\mathbf{H}$ 与 $\mathbf{B}$ 方向相反的情形。例如均匀磁化永磁体内部，退磁场 $\mathbf{H}_d$ 与磁化方向相反，但 $\mathbf{B}$ 仍沿磁化方向。

### 2.2 本构关系的适用范围误用

$\mathbf{B} = \mu \mathbf{H}$ 仅对线性介质成立。对于铁磁材料（如永磁体），$\mathbf{M}$ 与 $\mathbf{H}$ 无线性关系，必须回到定义式 $\mathbf{H} = \mathbf{B}/\mu_0 - \mathbf{M}$ 处理。**切勿将 $\mu_r$ 视为常数应用于铁磁质**。

### 2.3 切向条件的符号与方向错误

切向条件 $H_{1t} - H_{2t} = K_f$ 中，$H_{1t}$ 与 $H_{2t}$ 均为**切向分量的大小**（取正数），方向约定为：$\hat{\mathbf{n}} \times (\mathbf{H}_2 - \mathbf{H}_1) = \mathbf{K}_f$。若采用 $\mathbf{H}_1 - \mathbf{H}_2$ 的写法，符号会反转。建议始终使用矢量形式：

$$
\hat{\mathbf{n}} \times (\mathbf{H}_2 - \mathbf{H}_1) = \mathbf{K}_f
$$

### 2.4 法向条件的隐含陷阱

$B_{1n} = B_{2n}$ 中 $n$ 为界面法向。若介质 1 为线性介质而介质 2 为真空，则 $\mu_1 H_{1n} = \mu_0 H_{2n}$，即 $H$ 的法向分量在界面处**不连续**，跳跃比为 $\mu_1/\mu_0$。计算时须先明确 $\mathbf{B}$ 的法向连续，再反推 $\mathbf{H}$。

### 2.5 面电流密度 $K_f$ 的识别

$K_f$ 是**自由**面电流，不包括束缚面电流 $\mathbf{K}_b = \mathbf{M} \times \hat{\mathbf{n}}$。在无自由面电流的介质分界面上，$K_f = 0$，切向 $\mathbf{H}$ 连续；但切向 $\mathbf{B}$ 一般不连续（因 $\mu$ 不同）。

---

## 三、经典范例手把手演算

### 3.1 问题陈述

一无限长直导线（半径 $a$，忽略）载有电流 $I$，沿 $z$ 轴放置。导线外部包裹一层厚度为 $b-a$ 的线性磁介质壳层（内半径 $a$，外半径 $b$，相对磁导率 $\mu_r$），介质壳层外部为真空。求全空间 $\mathbf{H}$ 与 $\mathbf{B}$ 分布。

### 3.2 第一步：对称性分析与区域划分

系统具有柱对称性，磁场仅有 $\phi$ 方向分量。划分三个区域：
- 区域 I：$0 < \rho < a$（真空中，导线内部忽略）
- 区域 II：$a < \rho < b$（介质壳层，$\mu = \mu_0 \mu_r$）
- 区域 III：$\rho > b$（真空，$\mu_0$）

### 3.3 第二步：应用安培环路定律求 $\mathbf{H}$

取半径为 $\rho$ 的圆形安培环路，方向沿 $\hat{\boldsymbol{\phi}}$。由于 $\mathbf{H}$ 的旋度仅由自由电流决定，且自由电流仅存在于 $\rho = 0$ 的导线中：

**区域 I**（$0 < \rho < a$，真空中导线外部但仍在壳层内边界以内）：

$$
\oint \mathbf{H} \cdot d\boldsymbol{\ell} = H_\phi(\rho) \cdot 2\pi\rho = I
$$

$$
H_\phi^{(I)}(\rho) = \frac{I}{2\pi\rho}
$$

**区域 II**（$a < \rho < b$，介质壳层内）：

环路包围的自由电流仍为 $I$（壳层内无自由电流），故：

$$
H_\phi^{(II)}(\rho) = \frac{I}{2\pi\rho}
$$

**区域 III**（$\rho > b$，壳层外真空）：

$$
H_\phi^{(III)}(\rho) = \frac{I}{2\pi\rho}
$$

**关键观察**：$\mathbf{H}$ 的分布与介质无关，仅由自由电流决定。

### 3.4 第三步：通过本构关系求 $\mathbf{B}$

**区域 I**（真空）：

$$
B_\phi^{(I)}(\rho) = \mu_0 H_\phi^{(I)} = \frac{\mu_0 I}{2\pi\rho}
$$

**区域 II**（介质）：

$$
B_\phi^{(II)}(\rho) = \mu H_\phi^{(II)} = \mu_0 \mu_r \cdot \frac{I}{2\pi\rho} = \frac{\mu_0 \mu_r I}{2\pi\rho}
$$

**区域 III**（真空）：

$$
B_\phi^{(III)}(\rho) = \mu_0 H_\phi^{(III)} = \frac{\mu_0 I}{2\pi\rho}
$$

### 3.5 第四步：界面条件验算

**界面 $\rho = a$**（真空/介质）：
- 法向方向为 $\hat{\boldsymbol{\rho}}$，而 $\mathbf{B}$ 仅有 $\hat{\boldsymbol{\phi}}$ 分量，故 $B_{1n} = B_{2n} = 0$，自动满足。
- 切向方向为 $\hat{\boldsymbol{\phi}}$，界面无自由面电流（$K_f = 0$），需验证 $H_{1t} = H_{2t}$：

$$
H_\phi^{(I)}(a) = \frac{I}{2\pi a}, \quad H_\phi^{(II)}(a) = \frac{I}{2\pi a}
$$

二者相等，条件满足。

**界面 $\rho = b$**（介质/真空）：
- 法向分量均为零，自动满足。
- 切向分量：

$$
H_\phi^{(II)}(b) = \frac{I}{2\pi b}, \quad H_\phi^{(III)}(b) = \frac{I}{2\pi b}
$$

相等，条件满足。

### 3.6 第五步：终解反代验算

验证 $\nabla \times \mathbf{H} = \mathbf{J}_f$ 的积分形式。取任意半径 $\rho > 0$ 的环路，均有：

$$
\oint \mathbf{H} \cdot d\boldsymbol{\ell} = \frac{I}{2\pi\rho} \cdot 2\pi\rho = I
$$

与自由电流 $I$ 一致。验证 $\nabla \cdot \mathbf{B} = 0$：由于 $\mathbf{B} = B_\phi(\rho)\hat{\boldsymbol{\phi}}$ 且 $B_\phi$ 仅依赖 $\rho$，在柱坐标中：

$$
\nabla \cdot \mathbf{B} = \frac{1}{\rho}\frac{\partial}{\partial \phi}(B_\phi) = 0
$$

满足螺线场条件。求解正确。

---

## 四、出处与纸质笔记坐标

### 4.1 教材出处

- **主参考**：Purcell, *Electricity and Magnetism*, 3rd Ed., Ch.10 §10.8–§10.11, pp.286–300
  - §10.8：$\mathbf{H}$ 的定义与安培环路定律的改写（pp.286–290）
  - §10.9：线性介质的磁化率与本构关系（pp.291–294）
  - §10.10：界面匹配条件的推导（pp.295–297）
  - §10.11：永磁体与 $\mathbf{H}$ 的反向问题（pp.298–300）

### 4.2 纸质活页留痕槽位

- **当前卡片**：[活页-EM-32]
- **关联前置卡片**：[活页-EM-30]（磁化强度 $\mathbf{M}$ 与束缚电流）、[活页-EM-31]（安培定律微分形式）
- **关联后续卡片**：[活页-EM-33]（磁路定理）、[活页-EM-34]（电磁感应中的 $\mathbf{H}$）

### 4.3 手写推导建议

在活页 EM-32 上完成以下推导留痕：
1. 从 $\nabla \times \mathbf{B} = \mu_0(\mathbf{J}_f + \nabla \times \mathbf{M})$ 出发，完整推导 $\nabla \times \mathbf{H} = \mathbf{J}_f$ 的每一步代数操作。
2. 画出界面法向高斯面与切向环路的示意图，标注各物理量的方向。
3. 重做范例 3.3 的完整计算，特别标注 $\rho = a$ 与 $\rho = b$ 处 $\mathbf{B}$ 的跳跃值：

$$
B_\phi^{(II)}(a) - B_\phi^{(I)}(a) = \frac{\mu_0 I}{2\pi a}(\mu_r - 1)
$$

4. 在页面边缘批注：永磁体内部 $\mathbf{H}$ 与 $\mathbf{B}$ 反向的物理图像（退磁场来源）。

---

*本卡片与活页 EM-32 配套使用，建议每两周复习一次界面条件推导，重点演练含面电流 $K_f$ 的切向条件应用场景。*

---

[[00_电磁学_学习全景图]]
