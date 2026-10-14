---
tags:
  - 量子力学
  - 角动量耦合
  - 克莱布施-戈登系数
  - 解法卡
aliases:
  - CG系数
  - 角动量相加
  - Clebsch-Gordan系数
created: 2025-04-15
updated: 2025-04-15
---

> [!summary] 算法执行总览
> 角动量相加问题的核心算法是：在非耦合表象基 $\{|j_1 m_1\rangle |j_2 m_2\rangle\}$ 与耦合表象基 $\{|J M\rangle\}$ 之间建立酉变换。该变换矩阵元即克莱布施-戈登(CG)系数 $C^{j_1 j_2 J}_{m_1 m_2 M}$。求解流程为：先由三角不等式确定 $J$ 的允许值，再由 $M = m_1 + m_2$ 约束磁量子数，最后通过阶梯算符与正交归一性逐级构造耦合态。

---

## 一、推导机理与核心数学定义

### 1.1 物理图像与表象结构

考虑两个角动量算符 $\hat{\mathbf{J}}_1$ 与 $\hat{\mathbf{J}}_2$（可为轨道角动量或自旋），它们作用在不同子空间，故互相对易：

$$
[\hat{J}_{1i}, \hat{J}_{2j}] = 0, \quad \forall i, j \in \{x, y, z\}
$$

系统总角动量定义为矢量相加：

$$
\hat{\mathbf{J}} = \hat{\mathbf{J}}_1 + \hat{\mathbf{J}}_2
$$

**非耦合表象**（直积表象）：以 $\{\hat{J}_1^2, \hat{J}_{1z}, \hat{J}_2^2, \hat{J}_{2z}\}$ 为完备对易算符集，基矢为：

$$
|j_1 m_1\rangle |j_2 m_2\rangle \equiv |j_1, m_1; j_2, m_2\rangle
$$

该表象维数为 $(2j_1+1)(2j_2+1)$。

**耦合表象**：以 $\{\hat{J}^2, \hat{J}_z, \hat{J}_1^2, \hat{J}_2^2\}$ 为完备对易算符集，基矢为 $|J M; j_1 j_2\rangle$（简写 $|J M\rangle$），满足：

$$
\hat{J}^2 |J M\rangle = J(J+1)\hbar^2 |J M\rangle, \quad \hat{J}_z |J M\rangle = M\hbar |J M\rangle
$$

### 1.2 三角不等式与量子数取值范围

总角动量量子数 $J$ 的允许值由**三角不等式**限定：

$$
|j_1 - j_2| \leq J \leq j_1 + j_2
$$

且 $J$ 以整数步长递增（若 $j_1, j_2$ 半整数则 $J$ 亦为半整数；若二者皆整数则 $J$ 为整数）。维数守恒给出校验关系：

$$
\sum_{J=|j_1-j_2|}^{j_1+j_2} (2J+1) = (2j_1+1)(2j_2+1)
$$

磁量子数满足**加法守恒律**：

$$
M = m_1 + m_2
$$

### 1.3 CG系数定义与展开式

耦合表象基矢可按非耦合表象基矢展开：

$$
|J M\rangle = \sum_{m_1=-j_1}^{j_1} \sum_{m_2=-j_2}^{j_2} C^{j_1 j_2 J}_{m_1 m_2 M} \, |j_1 m_1\rangle |j_2 m_2\rangle
$$

其中展开系数 $C^{j_1 j_2 J}_{m_1 m_2 M} = \langle j_1 m_1; j_2 m_2 | J M\rangle$ 即为**克莱布施-戈登系数**。由于 $M = m_1 + m_2$ 约束，实际求和仅对满足此条件的 $m_1, m_2$ 进行。

**正交归一性条件**：

$$
\sum_{m_1, m_2} C^{j_1 j_2 J}_{m_1 m_2 M} \, C^{j_1 j_2 J'}_{m_1 m_2 M'} = \delta_{JJ'} \delta_{MM'}
$$

$$
\sum_{J, M} C^{j_1 j_2 J}_{m_1 m_2 M} \, C^{j_1 j_2 J}_{m_1' m_2' M} = \delta_{m_1 m_1'} \delta_{m_2 m_2'}
$$

### 1.4 阶梯算符递推构造法

定义总角动量升降算符：

$$
\hat{J}_{\pm} = \hat{J}_{1\pm} + \hat{J}_{2\pm}
$$

作用于耦合态：

$$
\hat{J}_{\pm} |J M\rangle = \hbar \sqrt{J(J+1) - M(M \pm 1)} \, |J, M \pm 1\rangle
$$

作用于非耦合直积态：

$$
\hat{J}_{\pm} |j_1 m_1\rangle |j_2 m_2\rangle = \hbar \sqrt{j_1(j_1+1) - m_1(m_1 \pm 1)} \, |j_1, m_1 \pm 1\rangle |j_2 m_2\rangle + \hbar \sqrt{j_2(j_2+1) - m_2(m_2 \pm 1)} \, |j_1 m_1\rangle |j_2, m_2 \pm 1\rangle
$$

**构造策略**：从最高权重态 $|J_{\max}, J_{\max}\rangle = |j_1, j_1\rangle |j_2, j_2\rangle$ 出发，反复施加 $\hat{J}_-$ 生成同一 $J$ 的全体 $M$ 分量；再对正交子空间重复此过程。

---

## 二、⚠️ 致命失分陷阱与临界边界

### 2.1 两自旋 1/2 耦合的符号约定

**陷阱核心**：自旋单态与三重态的归一化系数符号不可记反。

两自旋 $s_1 = s_2 = 1/2$ 耦合，$J$ 取值为 $0$ 或 $1$。三重态（$J=1$，对称）与单态（$J=0$，反对称）的完整展开为：

$$
|1, 1\rangle = |\uparrow\uparrow\rangle
$$

$$
|1, 0\rangle = \frac{1}{\sqrt{2}} \left( |\uparrow\downarrow\rangle + |\downarrow\uparrow\rangle \right)
$$

$$
|1, -1\rangle = |\downarrow\downarrow\rangle
$$

$$
|0, 0\rangle = \frac{1}{\sqrt{2}} \left( |\uparrow\downarrow\rangle - |\downarrow\uparrow\rangle \right)
$$

**关键判别**：$|0,0\rangle$ 中负号位于第二项（$|\downarrow\uparrow\rangle$ 前），而非第一项。若写成 $\frac{1}{\sqrt{2}}(|\downarrow\uparrow\rangle - |\uparrow\downarrow\rangle)$ 则整体相差一个全局相位 $e^{i\pi} = -1$，在计算期望值时虽不改变物理结果，但在干涉项与多粒子纠缠计算中会导致错误。

### 2.2 相位约定（Condon-Shortley约定）

标准 CG 系数采用 Condon-Shortley 相位约定：所有 CG 系数取实数，且最高权重系数取正：

$$
C^{j_1 j_2 J}_{j_1, J-j_1, J} > 0
$$

违反此约定将导致系数符号混乱。

### 2.3 阶梯算符作用时的边界条件

当 $M = J$ 时 $\hat{J}_+ |J, J\rangle = 0$；当 $M = -J$ 时 $\hat{J}_- |J, -J\rangle = 0$。在递推过程中若忽略此边界，将产生虚假的非零分量。

### 2.4 三角不等式遗漏

初学者常遗漏 $J$ 的中间取值。例如 $j_1 = 2, j_2 = 1$ 时，$J$ 可取 $1, 2, 3$ 三个值，而非仅取 $3$ 或仅取 $1$ 与 $3$。

### 2.5 维数不匹配

构造完成后必须验证：

$$
\sum_{J} (2J+1) = (2j_1+1)(2j_2+1)
$$

若不等，说明存在遗漏或重复。

---

## 三、经典范例手把手演算

### 3.1 范例：$j_1 = 1, j_2 = 1/2$ 的耦合

**第一步：确定 $J$ 取值范围**

$$
|1 - 1/2| = 1/2 \leq J \leq 1 + 1/2 = 3/2
$$

故 $J = 1/2$ 与 $J = 3/2$。维数校验：$(2 \times 1 + 1)(2 \times 1/2 + 1) = 3 \times 2 = 6$，而 $(2 \times 3/2 + 1) + (2 \times 1/2 + 1) = 4 + 2 = 6$，正确。

**第二步：最高权重态**

$$
|J=\tfrac{3}{2}, M=\tfrac{3}{2}\rangle = |j_1=1, m_1=1\rangle |j_2=\tfrac{1}{2}, m_2=\tfrac{1}{2}\rangle \equiv |1, 1\rangle |\tfrac{1}{2}, \tfrac{1}{2}\rangle
$$

**第三步：施加 $\hat{J}_-$ 生成 $J=3/2$ 链**

对 $|3/2, 3/2\rangle$ 施加 $\hat{J}_- = \hat{J}_{1-} + \hat{J}_{2-}$：

$$
\hat{J}_- |\tfrac{3}{2}, \tfrac{3}{2}\rangle = \hbar \sqrt{\tfrac{3}{2} \cdot \tfrac{5}{2} - \tfrac{3}{2} \cdot \tfrac{1}{2}} \, |\tfrac{3}{2}, \tfrac{1}{2}\rangle = \hbar \sqrt{3} \, |\tfrac{3}{2}, \tfrac{1}{2}\rangle
$$

另一方面：

$$
(\hat{J}_{1-} + \hat{J}_{2-}) |1, 1\rangle |\tfrac{1}{2}, \tfrac{1}{2}\rangle = \hbar \sqrt{1 \cdot 2 - 1 \cdot 0} \, |1, 0\rangle |\tfrac{1}{2}, \tfrac{1}{2}\rangle + \hbar \sqrt{\tfrac{1}{2} \cdot \tfrac{3}{2} - \tfrac{1}{2} \cdot (-\tfrac{1}{2})} \, |1, 1\rangle |\tfrac{1}{2}, -\tfrac{1}{2}\rangle
$$

$$
= \hbar \sqrt{2} \, |1, 0\rangle |\tfrac{1}{2}, \tfrac{1}{2}\rangle + \hbar \cdot 1 \cdot |1, 1\rangle |\tfrac{1}{2}, -\tfrac{1}{2}\rangle
$$

等号两边除以 $\hbar\sqrt{3}$：

$$
|\tfrac{3}{2}, \tfrac{1}{2}\rangle = \sqrt{\frac{2}{3}} \, |1, 0\rangle |\tfrac{1}{2}, \tfrac{1}{2}\rangle + \sqrt{\frac{1}{3}} \, |1, 1\rangle |\tfrac{1}{2}, -\tfrac{1}{2}\rangle
$$

**第四步：继续降至 $M = -1/2$ 与 $M = -3/2$**

对 $|3/2, 1/2\rangle$ 施加 $\hat{J}_-$：

$$
\hat{J}_- |\tfrac{3}{2}, \tfrac{1}{2}\rangle = \hbar \sqrt{\tfrac{3}{2} \cdot \tfrac{5}{2} - \tfrac{1}{2} \cdot (-\tfrac{1}{2})} \, |\tfrac{3}{2}, -\tfrac{1}{2}\rangle = \hbar \cdot 2 \cdot |\tfrac{3}{2}, -\tfrac{1}{2}\rangle
$$

对展开式逐项作用：

$$
\hat{J}_- \left[ \sqrt{\tfrac{2}{3}} |1, 0\rangle |\tfrac{1}{2}, \tfrac{1}{2}\rangle + \sqrt{\tfrac{1}{3}} |1, 1\rangle |\tfrac{1}{2}, -\tfrac{1}{2}\rangle \right]
$$

第一项贡献：

$$
\sqrt{\tfrac{2}{3}} \left[ \hbar\sqrt{2} |1, -1\rangle |\tfrac{1}{2}, \tfrac{1}{2}\rangle + \hbar \cdot 1 \cdot |1, 0\rangle |\tfrac{1}{2}, -\tfrac{1}{2}\rangle \right]
$$

第二项贡献：

$$
\sqrt{\tfrac{1}{3}} \left[ \hbar\sqrt{2} |1, 0\rangle |\tfrac{1}{2}, -\tfrac{1}{2}\rangle + \hbar \cdot 0 \cdot |1, 1\rangle |\tfrac{1}{2}, -\tfrac{3}{2}\rangle \right]
$$

合并同类项并除以 $2\hbar$：

$$
|\tfrac{3}{2}, -\tfrac{1}{2}\rangle = \sqrt{\tfrac{2}{3}} \cdot \tfrac{\sqrt{2}}{2} |1, -1\rangle |\tfrac{1}{2}, \tfrac{1}{2}\rangle + \left( \sqrt{\tfrac{2}{3}} \cdot \tfrac{1}{2} + \sqrt{\tfrac{1}{3}} \cdot \tfrac{\sqrt{2}}{2} \right) |1, 0\rangle |\tfrac{1}{2}, -\tfrac{1}{2}\rangle
$$

化简系数：

$$
\sqrt{\tfrac{2}{3}} \cdot \tfrac{\sqrt{2}}{2} = \sqrt{\tfrac{1}{3}}, \quad \sqrt{\tfrac{2}{3}} \cdot \tfrac{1}{2} + \sqrt{\tfrac{1}{3}} \cdot \tfrac{\sqrt{2}}{2} = \tfrac{\sqrt{2}}{2\sqrt{3}} + \tfrac{\sqrt{2}}{2\sqrt{3}} = \sqrt{\tfrac{2}{3}}
$$

故：

$$
|\tfrac{3}{2}, -\tfrac{1}{2}\rangle = \sqrt{\tfrac{1}{3}} |1, -1\rangle |\tfrac{1}{2}, \tfrac{1}{2}\rangle + \sqrt{\tfrac{2}{3}} |1, 0\rangle |\tfrac{1}{2}, -\tfrac{1}{2}\rangle
$$

再施一次 $\hat{J}_-$ 得：

$$
|\tfrac{3}{2}, -\tfrac{3}{2}\rangle = |1, -1\rangle |\tfrac{1}{2}, -\tfrac{1}{2}\rangle
$$

**第五步：构造 $J=1/2$ 子空间**

$M = 1/2$ 的非耦合基矢张成空间为 $\{|1, 1\rangle |1/2, -1/2\rangle, \; |1, 0\rangle |1/2, 1/2\rangle\}$。$|3/2, 1/2\rangle$ 已占有一个线性组合，与之正交的态即为 $|1/2, 1/2\rangle$。

设 $|1/2, 1/2\rangle = a |1, 1\rangle |1/2, -1/2\rangle + b |1, 0\rangle |1/2, 1/2\rangle$。正交条件：

$$
\langle \tfrac{3}{2}, \tfrac{1}{2} | \tfrac{1}{2}, \tfrac{1}{2} \rangle = \sqrt{\tfrac{1}{3}} \, a + \sqrt{\tfrac{2}{3}} \, b = 0
$$

取 $a = \sqrt{2/3}, b = -\sqrt{1/3}$（Condon-Shortley约定取 $a > 0$）：

$$
|\tfrac{1}{2}, \tfrac{1}{2}\rangle = \sqrt{\tfrac{2}{3}} |1, 1\rangle |\tfrac{1}{2}, -\tfrac{1}{2}\rangle - \sqrt{\tfrac{1}{3}} |1, 0\rangle |\tfrac{1}{2}, \tfrac{1}{2}\rangle
$$

施加 $\hat{J}_-$ 得 $|1/2, -1/2\rangle$：

$$
\hat{J}_- |\tfrac{1}{2}, \tfrac{1}{2}\rangle = \hbar \sqrt{\tfrac{1}{2} \cdot \tfrac{3}{2} - \tfrac{1}{2} \cdot (-\tfrac{1}{2})} \, |\tfrac{1}{2}, -\tfrac{1}{2}\rangle = \hbar \cdot 1 \cdot |\tfrac{1}{2}, -\tfrac{1}{2}\rangle
$$

逐项计算：

$$
\sqrt{\tfrac{2}{3}} \left[ \

---
**知识图谱导航**：[[00_量子力学_学习全景图]]


### 纸质活页留痕槽位：[活页-QM-20]
- 请在此处记录推导手稿与疑难反思。
