---
tags:
  - 电动力学
  - 电磁学
  - 介质
  - 边界条件
  - 解法卡
aliases:
  - 电位移矢量
  - 介质边界匹配
  - D与E边界条件
created: 2026-05-12
updated: 2026-05-12
---

> [!summary] 算法执行总览
> 本卡处理介质静电场问题的核心算法链：**定义辅助场 $\mathbf{D}$ → 写出介质中高斯定律积分/微分形式 → 结合线性本构关系 $\mathbf{D}=\varepsilon\mathbf{E}$ → 在界面处分别提取法向与切向分量方程 → 联立求解场量**。执行时须始终区分自由电荷 $\rho_f$ 与束缚电荷 $\rho_b$ 的源角色，并牢记 $\mathbf{D}$ 的散度方程仅对自由电荷闭合。

---

## 一、推导机理与核心数学定义

### 1.1 电位移矢量的引入动机

介质极化后内部出现束缚体电荷密度 $\rho_b = -\nabla\cdot\mathbf{P}$ 与束缚面电荷密度 $\sigma_b = \mathbf{P}\cdot\hat{\mathbf{n}}$。原始高斯定律写为：

$$
\nabla\cdot\mathbf{E} = \frac{1}{\varepsilon_0}\left(\rho_f + \rho_b\right)
$$

将 $\rho_b = -\nabla\cdot\mathbf{P}$ 代入并移项：

$$
\nabla\cdot\left(\varepsilon_0\mathbf{E} + \mathbf{P}\right) = \rho_f
$$

由此定义**电位移矢量**：

$$
\boxed{\mathbf{D} \equiv \varepsilon_0\mathbf{E} + \mathbf{P}}
$$

其微分形式与积分形式分别为：

$$
\nabla\cdot\mathbf{D} = \rho_f \qquad\Longleftrightarrow\qquad \oint_{\partial V} \mathbf{D}\cdot d\mathbf{A} = Q_{f,\text{enc}}
$$

> **物理直觉**：$\mathbf{D}$ 场只“感知”自由电荷，将极化介质的微观复杂性封装进 $\mathbf{P}$ 中。凡涉及自由电荷分布求场的问题，先求 $\mathbf{D}$ 再反解 $\mathbf{E}$ 往往比直接求解 $\mathbf{E}$ 更便捷。

### 1.2 线性各向同性介质的本构关系

对于线性各向同性介质，极化强度正比于电场：

$$
\mathbf{P} = \varepsilon_0\chi_e\mathbf{E}
$$

代入定义式：

$$
\mathbf{D} = \varepsilon_0\mathbf{E} + \varepsilon_0\chi_e\mathbf{E} = \varepsilon_0(1+\chi_e)\mathbf{E} = \varepsilon_0\varepsilon_r\mathbf{E} = \varepsilon\mathbf{E}
$$

其中三个关键参数的关系为：

$$
\boxed{\varepsilon_r = 1 + \chi_e}, \qquad \varepsilon = \varepsilon_r\varepsilon_0
$$

### 1.3 边界条件的完整推导

#### (a) 法向分量 — 由高斯定律的积分形式导出

在两种介质（介电常数 $\varepsilon_1$、$\varepsilon_2$）交界面上构造一个极薄的“药丸盒”高斯面（厚度 $h \to 0$，底面面积 $\Delta A$），上下底面分别位于介质 1 与介质 2 中。对 $\mathbf{D}$ 应用高斯定律：

$$
\oint \mathbf{D}\cdot d\mathbf{A} = Q_{f,\text{enc}}
$$

当 $h \to 0$ 时，侧面积分贡献为零，仅剩上下底面贡献：

$$
D_{1n}\Delta A - D_{2n}\Delta A = \sigma_f \Delta A
$$

其中 $\hat{\mathbf{n}}$ 取为由介质 2 指向介质 1 的法向。化简得：

$$
\boxed{D_{1n} - D_{2n} = \sigma_f}
$$

若界面上无自由面电荷（$\sigma_f = 0$），则：

$$
D_{1n} = D_{2n}
$$

#### (b) 切向分量 — 由静电场的保守性导出

由 $\nabla\times\mathbf{E} = 0$（静电场），沿界面构造一窄矩形回路（长边 $\Delta l$ 平行于界面，短边 $h \to 0$），应用环路定理：

$$
\oint \mathbf{E}\cdot d\mathbf{l} = 0
$$

短边贡献在 $h \to 0$ 时消失，仅剩两长边贡献：

$$
E_{1t}\Delta l - E_{2t}\Delta l = 0
$$

化简得：

$$
\boxed{E_{1t} = E_{2t}}
$$

#### (c) 折射法则 — 边界条件的推论

设电场 $\mathbf{E}_1$ 与法线夹角为 $\theta_1$，$\mathbf{E}_2$ 与法线夹角为 $\theta_2$。由切向连续 $E_1\sin\theta_1 = E_2\sin\theta_2$ 与法向关系 $D_{1n} = D_{2n}$（无自由面电荷时）即 $\varepsilon_1 E_1\cos\theta_1 = \varepsilon_2 E_2\cos\theta_2$，两式相除得：

$$
\boxed{\frac{\tan\theta_1}{\tan\theta_2} = \frac{\varepsilon_1}{\varepsilon_2}}
$$

---

## 二、⚠️ 致命失分陷阱与临界边界

### 陷阱 1：将 $\nabla\cdot\mathbf{D}=0$ 误判为 $\mathbf{D}=0$

$\nabla\cdot\mathbf{D}=0$ 仅表明 $\mathbf{D}$ 场无散度源（无自由电荷），但 $\mathbf{D}$ 仍可具有旋度源或非零的均匀分量。例如平行板电容器中充满均匀介质且无自由电荷的区域，$\mathbf{D}$ 为均匀非零场。**散度为零 ≠ 场为零**。

### 陷阱 2：忽略 $\mathbf{D}$ 的边界条件中 $\sigma_f$ 的符号约定

$D_{1n} - D_{2n} = \sigma_f$ 中，$\hat{\mathbf{n}}$ 的方向约定为从介质 2 指向介质 1。若法向取反，则等式右侧变号为 $-\sigma_f$。考试中须先明确法向指向再代入计算。

### 陷阱 3：混淆 $\mathbf{D}$ 与 $\mathbf{E}$ 在界面处的连续性

- $\mathbf{D}$ 的**法向分量**在无自由面电荷时连续；
- $\mathbf{E}$ 的**切向分量**始终连续；
- $\mathbf{E}$ 的**法向分量**在界面处**必然突变**（除非 $\varepsilon_1 = \varepsilon_2$），因为 $E_n = D_n/\varepsilon$ 而 $\varepsilon$ 在界面处跳变；
- $\mathbf{D}$ 的**切向分量**在界面处**必然突变**（除非 $\varepsilon_1 = \varepsilon_2$），因为 $D_t = \varepsilon E_t$ 而 $E_t$ 连续但 $\varepsilon$ 跳变。

### 陷阱 4：忽略束缚面电荷对 $\mathbf{E}$ 法向分量的贡献

若直接用 $\nabla\cdot\mathbf{E} = (\rho_f+\rho_b)/\varepsilon_0$ 求 $\mathbf{E}$ 的法向跳变，须计入 $\sigma_b$。正确关系为：

$$
E_{1n} - E_{2n} = \frac{\sigma_f + \sigma_b}{\varepsilon_0}
$$

而 $\sigma_b = \mathbf{P}\cdot\hat{\mathbf{n}}$ 在界面两侧取值不同，不可遗漏。

### 陷阱 5：线性关系 $\mathbf{D}=\varepsilon\mathbf{E}$ 的适用范围

该关系仅对**线性、各向同性、无铁电性**的介质成立。对于各向异性介质（晶体），$\mathbf{D}$ 与 $\mathbf{E}$ 为张量关系 $D_i = \sum_j \varepsilon_{ij}E_j$；对于非线性介质（铁电体），$\varepsilon$ 本身依赖于场强。此时边界条件的形式不变，但本构关系不可简单代入。

### 陷阱 6：误将 $\varepsilon_r$ 当作 $\chi_e$ 使用

$\varepsilon_r = 1 + \chi_e$，二者相差 1。在真空中 $\chi_e = 0$ 而 $\varepsilon_r = 1$。代入公式时须确认所用参数是介电常数还是电极化率。

---

## 三、经典范例手把手演算

### 题目

一个半径为 $R$ 的导体球，带有自由电荷 $Q$，被一层厚度为 $t$ 的线性介质壳（介电常数 $\varepsilon$）包裹，介质外为真空。求：(1) 各区域的 $\mathbf{D}$、$\mathbf{E}$ 场分布；(2) 介质内外表面上的束缚面电荷密度；(3) 验证介质壳内表面处 $\mathbf{E}$ 的法向跳变。

### 第一步：划分区域与对称性分析

- 区域 I：导体内部（$r < R$），静电场为零，$\mathbf{E} = 0$，$\mathbf{D} = 0$；
- 区域 II：介质壳内（$R < r < R+t$），$\varepsilon = \varepsilon_r\varepsilon_0$；
- 区域 III：介质壳外真空（$r > R+t$），$\varepsilon = \varepsilon_0$。

体系具有球对称性，$\mathbf{D}$、$\mathbf{E}$ 均沿径向。

### 第二步：由高斯定律求 $\mathbf{D}$

对半径 $r$ 的球形高斯面应用介质中高斯定律 $\oint\mathbf{D}\cdot d\mathbf{A} = Q_{f,\text{enc}}$：

**区域 II**（$R < r < R+t$）：高斯面包围导体，自由电荷 $Q_{f,\text{enc}} = Q$：

$$
D(r) \cdot 4\pi r^2 = Q \quad\Longrightarrow\quad \mathbf{D}_{II} = \frac{Q}{4\pi r^2}\hat{\mathbf{r}}
$$

**区域 III**（$r > R+t$）：高斯面仍包围导体，$Q_{f,\text{enc}} = Q$：

$$
\mathbf{D}_{III} = \frac{Q}{4\pi r^2}\hat{\mathbf{r}}
$$

> 注意：$\mathbf{D}$ 在介质与真空区域表达式相同，因为自由电荷总量相同且球对称。

### 第三步：由本构关系求 $\mathbf{E}$

**区域 II**（介质内）：

$$
\mathbf{E}_{II} = \frac{\mathbf{D}_{II}}{\varepsilon} = \frac{Q}{4\pi\varepsilon r^2}\hat{\mathbf{r}} = \frac{Q}{4\pi\varepsilon_0\varepsilon_r r^2}\hat{\mathbf{r}}
$$

**区域 III**（真空中）：

$$
\mathbf{E}_{III} = \frac{\mathbf{D}_{III}}{\varepsilon_0} = \frac{Q}{4\pi\varepsilon_0 r^2}\hat{\mathbf{r}}
$$

### 第四步：求束缚面电荷密度

由 $\mathbf{P} = \mathbf{D} - \varepsilon_0\mathbf{E}$，在介质内：

$$
\mathbf{P}_{II} = \frac{Q}{4\pi r^2}\hat{\mathbf{r}} - \varepsilon_0\cdot\frac{Q}{4\pi\varepsilon_0\varepsilon_r r^2}\hat{\mathbf{r}} = \frac{Q}{4\pi r^2}\left(1 - \frac{1}{\varepsilon_r}\right)\hat{\mathbf{r}}
$$

**内表面**（$r = R$，介质法向 $\hat{\mathbf{n}} = -\hat{\mathbf{r}}$ 指向导体）：

$$
\sigma_b^{\text{内}} = \mathbf{P}_{II}(R)\cdot(-\hat{\mathbf{r}}) = -\frac{Q}{4\pi R^2}\left(1 - \frac{1}{\varepsilon_r}\right)
$$

**外表面**（$r = R+t$，介质法向 $\hat{\mathbf{n}} = +\hat{\mathbf{r}}$ 指向真空）：

$$
\sigma_b^{\text{外}} = \mathbf{P}_{II}(R+t)\cdot(+\hat{\mathbf{r}}) = +\frac{Q}{4\pi (R+t)^2}\left(1 - \frac{1}{\varepsilon_r}\right)
$$

### 第五步：验证 $\mathbf{E}$ 的法向跳变

在介质内表面 $r=R$ 处，导体侧 $E = 0$，介质侧 $E_{II}(R) = Q/(4\pi\varepsilon_0\varepsilon_r R^2)$。法向跳变为：

$$
E_{\text{介质}} - E_{\text{导体}} = \frac{Q}{4\pi\varepsilon_0\varepsilon_r R^2} - 0 = \frac{Q}{4\pi\varepsilon_0\varepsilon_r R^2}
$$

由边界条件 $E_{1n} - E_{2n} = (\sigma_f + \sigma_b)/\varepsilon_0$，取介质为 1、导体为 2，导体表面自由面电荷 $\sigma_f = Q/(4\pi R^2)$，束缚面电荷 $\sigma_b^{\text{内}} = -Q(1-1/\varepsilon_r)/(4\pi R^2)$：

$$
E_{\text{介质}} - E_{\text{导体}} = \frac{1}{\varepsilon_0}\left[\frac{Q}{4\pi R^2} - \frac{Q}{4\pi R^2}\left(1-\frac{1}{\varepsilon_r}\right)\right] = \frac{Q}{4\pi\varepsilon_0\varepsilon_r R^2}
$$

与直接计算结果一致，验证完毕。

### 第六步：终解反代验算

验证 $\mathbf{D}$ 在 $r=R+t$ 界面处的法向连续性。该界面无自由面电荷（$\sigma_f = 0$），故 $D_{II}(R+t) = D_{III}(R+t)$：

$$
D_{II}(R+t) = \frac{Q}{4\pi (R+t)^2}, \qquad D_{III}(R+t) = \frac{Q}{4\pi (R+t)^2}
$$

二者相等，满足 $D_{1n} = D_{2n}$。同时验证 $E$ 的切向分量在此球对称问题中恒为零，自动满足 $E_{1t} = E_{2t}$。

---

## 四、出处与纸质笔记坐标

### 教材出处

- **Purcell, *Electricity and Magnetism*, 3rd Ed.**  
  - §9.6 电位移矢量 $\mathbf{D}$ 的定义与物理意义：P243-P248  
  - §9.7 介质中高斯定律的微分与积分形式：P248-P252  
  - §9.8 线性介质的本构关系与电极化率：P252-P256  
  - §9.9 边界条件的推导：P256-P259  
  - §9.10 折射法则与范例：P259-P262  

### 纸质活页留痕槽位

- **[活页-EM-30]**：本节核心公式推导留痕区（$\mathbf{D}$ 定义、高斯定律推导、边界条件全流程）  
- **[活页-EM-31]**：陷阱笔记区（抄录第二节全部 6 条陷阱并各配一道反例）  
- **[活页-EM-32]**：范例演算区（抄录第三节完整演算并标注每一步对应的物理定律）  
- **[活页-EM-33]**：错题订正区（预留）

---

### 知识全景图

```mermaid
graph TD
    A[自由电荷 ρ_f] -->|源| B[∇·D = ρ_f]
    C[束缚电荷 ρ_b = -∇·P] -->|源| D[∇·E = ρ_f+ρ_b / ε₀]
    B --> E[D ≡ ε₀E + P]
    E --> F[线性介质: D = εE]
    F --> G[边界条件: D₁n-D₂n = σ_f]
    D --> H[边界条件: E₁t = E₂t]
    G --> I[折射法则: tanθ₁/tanθ₂ = ε₁/ε₂]
    H --> I
    F --> J[ε_r = 1 + χ_e]

---

[[00_电磁学_学习全景图]]
