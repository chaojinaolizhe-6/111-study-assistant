---
tags:
  - 数学物理
  - 群论
  - 李群
  - 李代数
  - SO(3)
  - SU(2)
  - 拓扑学
  - 旋量
aliases:
  - 三维旋转群与二重覆盖
  - SO(3)与SU(2)关系
  - 李群生成元与李括号
created: 2024-01-15
updated: 2024-01-15
---

> [!summary] 核心认知先验
> 李群是兼有群结构与微分流形结构的数学对象，其局部性质完全由单位元处的切空间——李代数——刻画。三维旋转群 $SO(3)$ 与二维特殊酉群 $SU(2)$ 共享同一李代数 $\mathfrak{so}(3) \cong \mathfrak{su}(2)$，但二者拓扑性质截然不同：$SO(3)$ 非单连通（基本群为 $\mathbb{Z}_2$），而 $SU(2)$ 单连通且构成 $SO(3)$ 的二重覆盖。这一拓扑差异是量子力学中自旋为半整数粒子在 $2\pi$ 空间旋转下波函数获得负号的几何根源。

---

## 一、推导机理与核心数学定义

### 1.1 连续李群与群流形

**定义（李群）**：一个李群 $G$ 是同时具备群结构与光滑微分流形结构的集合，且群乘法映射 $G \times G \to G$（$(g_1, g_2) \mapsto g_1 g_2$）与逆映射 $G \to G$（$g \mapsto g^{-1}$）均为光滑映射。

**定义（群流形切空间与李代数）**：设 $G$ 为 $n$ 维李群，$e$ 为单位元。$G$ 在 $e$ 处的切空间 $T_e G$ 构成一个 $n$ 维实向量空间。在该切空间上定义**李括号** $[\cdot, \cdot]: T_e G \times T_e G \to T_e G$，满足双线性性、反对称性与雅可比恒等式，则 $(T_e G, [\cdot, \cdot])$ 称为李群 $G$ 的**李代数**，记作 $\mathfrak{g}$。

**直觉**：李代数捕捉了李群在单位元附近的无穷小结构。群中任意元素可通过指数映射从李代数元素生成，即 $g = \exp(X)$，其中 $X \in \mathfrak{g}$。

### 1.2 三维旋转群 $SO(3)$ 及其李代数

**定义（$SO(3)$）**：三维特殊正交群定义为

$$
SO(3) = \{ R \in GL(3, \mathbb{R}) \mid R^T R = I_3, \; \det R = +1 \}.
$$

**生成元与李代数**：考虑绕 $x$、$y$、$z$ 轴的无穷小旋转。定义三个 $3 \times 3$ 实反对称生成元矩阵：

$$
J_1 = \begin{pmatrix} 0 & 0 & 0 \\ 0 & 0 & -i \\ 0 & i & 0 \end{pmatrix}, \quad
J_2 = \begin{pmatrix} 0 & 0 & i \\ 0 & 0 & 0 \\ -i & 0 & 0 \end{pmatrix}, \quad
J_3 = \begin{pmatrix} 0 & -i & 0 \\ i & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix}.
$$

（此处采用量子力学惯例，引入因子 $i$ 使生成元为厄米矩阵。）有限旋转由指数映射给出：

$$
R(\theta, \hat{n}) = \exp(-i \theta \, \hat{n} \cdot \vec{J}) = \exp\!\left(-i \theta \sum_{k=1}^{3} n_k J_k\right).
$$

**李括号（对易子）**：直接矩阵乘法验证可得

$$
[J_i, J_j] = J_i J_j - J_j J_i = i \varepsilon_{ijk} J_k,
$$

其中 $\varepsilon_{ijk}$ 为三维列维-奇维塔符号（全反对称张量），隐含对重复指标 $k$ 求和。此即 $\mathfrak{so}(3)$ 李代数的结构方程。

### 1.3 二维特殊酉群 $SU(2)$ 及其李代数

**定义（$SU(2)$）**：

$$
SU(2) = \{ U \in GL(2, \mathbb{C}) \mid U^{\dagger} U = I_2, \; \det U = +1 \}.
$$

**生成元与泡利矩阵**：$SU(2)$ 的李代数 $\mathfrak{su}(2)$ 由三个 $2 \times 2$ 厄米无迹矩阵张成，取

$$
J_i = \frac{\sigma_i}{2}, \quad i = 1, 2, 3,
$$

其中 $\sigma_i$ 为泡利矩阵：

$$
\sigma_1 = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad
\sigma_2 = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}, \quad
\sigma_3 = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}.
$$

泡利矩阵满足 $\sigma_i \sigma_j = \delta_{ij} I_2 + i \varepsilon_{ijk} \sigma_k$，由此直接推出

$$
[J_i, J_j] = \left[\frac{\sigma_i}{2}, \frac{\sigma_j}{2}\right] = \frac{1}{4} (2i \varepsilon_{ijk} \sigma_k) = i \varepsilon_{ijk} \frac{\sigma_k}{2} = i \varepsilon_{ijk} J_k.
$$

**结论**：$\mathfrak{su}(2) \cong \mathfrak{so}(3)$，二者作为实李代数同构。

### 1.4 覆盖映射 $SU(2) \to SO(3)$

**构造同态**：定义映射 $\Phi: SU(2) \to SO(3)$ 如下。对任意 $U \in SU(2)$ 和任意三维矢量 $\vec{x} = (x_1, x_2, x_3)$，构造厄米无迹矩阵

$$
X = \vec{x} \cdot \vec{\sigma} = \begin{pmatrix} x_3 & x_1 - i x_2 \\ x_1 + i x_2 & -x_3 \end{pmatrix}.
$$

定义变换 $X \mapsto X' = U X U^{\dagger}$。由于 $X'$ 仍为厄米无迹矩阵，可唯一写成 $X' = \vec{x}' \cdot \vec{\sigma}$，从而定义线性映射 $\vec{x} \mapsto \vec{x}' = R_U \vec{x}$。可验证 $R_U \in SO(3)$，且 $\Phi(U) = R_U$ 为群同态。

**核与二重覆盖**：计算核：

$$
\ker \Phi = \{ U \in SU(2) \mid U X U^{\dagger} = X, \; \forall X \} = \{ I_2, -I_2 \} \cong \mathbb{Z}_2.
$$

由第一同构定理：

$$
SU(2) / \mathbb{Z}_2 \cong SO(3).
$$

**拓扑对比**：

- $SO(3)$ 作为流形微分同胚于实射影空间 $\mathbb{RP}^3$，其基本群 $\pi_1(SO(3)) = \mathbb{Z}_2$，**非单连通**。
- $SU(2)$ 作为流形微分同胚于三维球面 $S^3$，其基本群 $\pi_1(SU(2)) = 0$，**单连通**。
- $\Phi$ 是 $SO(3)$ 的**万有覆盖**，覆盖重数为 2。

---

## 二、⚠️ 致命失分陷阱与临界边界

### 陷阱 1：$2\pi$ 旋转在 $SU(2)$ 中不回到单位元

**核心事实**：考虑绕 $z$ 轴旋转角 $\theta$。在 $SO(3)$ 中对应矩阵为

$$
R_z(\theta) = \begin{pmatrix} \cos\theta & -\sin\theta & 0 \\ \sin\theta & \cos\theta & 0 \\ 0 & 0 & 1 \end{pmatrix}.
$$

显然 $R_z(2\pi) = I_3$，即空间旋转 $360^\circ$ 回到恒等变换。但在 $SU(2)$ 中，对应元素为

$$
U_z(\theta) = \exp\!\left(-i \frac{\theta}{2} \sigma_3\right) = \begin{pmatrix} e^{-i\theta/2} & 0 \\ 0 & e^{i\theta/2} \end{pmatrix}.
$$

代入 $\theta = 2\pi$：

$$
U_z(2\pi) = \begin{pmatrix} e^{-i\pi} & 0 \\ 0 & e^{i\pi} \end{pmatrix} = \begin{pmatrix} -1 & 0 \\ 0 & -1 \end{pmatrix} = -I_2 \neq I_2.
$$

**结论**：$SU(2)$ 中旋转 $2\pi$ 产生整体因子 $-1$。仅当旋转 $4\pi$（即 $720^\circ$）时：

$$
U_z(4\pi) = \begin{pmatrix} e^{-i2\pi} & 0 \\ 0 & e^{i2\pi} \end{pmatrix} = I_2.
$$

**物理后果**：自旋 $1/2$ 粒子（费米子）的旋量波函数 $\psi$ 在空间旋转 $2\pi$ 下变换为 $\psi \to -\psi$，旋转 $4\pi$ 才恢复原状。这是 $SU(2)$ 二重覆盖 $SO(3)$ 的直接拓扑推论，也是自旋-统计关联的几何基础。

### 陷阱 2：混淆 $SO(3)$ 与 $SU(2)$ 的“旋转角”参数化

**易错点**：在 $SO(3)$ 中，参数 $\theta$ 的取值范围可限制为 $0 \leq \theta \leq \pi$（配合轴方向覆盖整个流形）；而在 $SU(2)$ 中，参数 $\theta$ 的自然范围为 $0 \leq \theta \leq 2\pi$（因 $U(\theta + 2\pi) = -U(\theta)$ 为不同群元）。若将 $SO(3)$ 的旋转角直接代入 $SU(2)$ 公式而遗漏因子 $1/2$，将导致错误的变换矩阵。

### 陷阱 3：生成元的厄米性与因子 $i$ 的约定

**易错点**：若采用数学约定 $R = \exp(\theta A)$（$A$ 反对称实矩阵），则 $[A_i, A_j] = \varepsilon_{ijk} A_k$（无因子 $i$）。物理约定 $R = \exp(-i\theta J)$ 下才有 $[J_i, J_j] = i\varepsilon_{ijk} J_k$。两种约定在文献中并存，混用将导致对易子符号错误和相位错误。

### 陷阱 4：$\det U = +1$ 条件的必要性

**易错点**：$U(2)$（一般酉群）包含 $U = e^{i\alpha} V$（$V \in SU(2)$），其李代数多出一个生成元（单位矩阵方向）。若忽略 $\det = +1$ 约束，将错误地认为 $U(2)$ 与 $SO(3)$ 共享李代数。事实上 $\mathfrak{u}(2) = \mathfrak{su}(2) \oplus \mathfrak{u}(1)$，维数为 4 而非 3。

### 陷阱 5：$\mathbb{Z}_2$ 核的几何意义

**易错点**：$SU(2)$ 中 $I_2$ 与 $-I_2$ 在 $\Phi$ 下映射到同一个 $SO(3)$ 元素。这意味着 $SO(3)$ 中的一条闭合路径（如从 $I_3$ 出发绕一圈回到 $I_3$）在 $SU(2)$ 中提升为从 $I_2$ 到 $-I_2$ 的**非闭合**路径。只有绕两圈的闭合路径才能提升为 $SU(2)$ 中的闭合路径。此即 $\pi_1(SO(3)) = \mathbb{Z}_2$ 的几何直观。

---

## 三、经典范例手把手演算

### 范例：验证 $SU(2)$ 中 $2\pi$ 旋转产生 $-I_2$，$4\pi$ 旋转回到 $I_2$

**步骤 1**：写出 $SU(2)$ 中绕 $\hat{n} = (n_1, n_2, n_3)$ 轴（单位矢量）旋转角 $\theta$ 的群元。

利用恒等式 $\exp(-i\theta \, \hat{n} \cdot \vec{\sigma}/2) = \cos(\theta/2) I_2 - i \sin(\theta/2)(\hat{n} \cdot \vec{\sigma})$，展开：

$$
U(\theta, \hat{n}) = \cos\frac{\theta}{2} \, I_2 - i \sin\frac{\theta}{2} \begin{pmatrix} n_3 & n_1 - i n_2 \\ n_1 + i n_2 & -n_3 \end{pmatrix}.
$$

**步骤 2**：取 $\hat{n} = \hat{z} = (0, 0, 1)$，则

$$
U(\theta, \hat{z}) = \cos\frac{\theta}{2} \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} - i \sin\frac{\theta}{2} \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix} = \begin{pmatrix} \cos(\theta/2) - i\sin(\theta/2) & 0 \\ 0 & \cos(\theta/2) + i\sin(\theta/2) \end{pmatrix}.
$$

利用欧拉公式 $e^{\pm i\theta/2} = \cos(\theta/2) \pm i\sin(\theta/2)$，得

$$
U(\theta, \hat{z}) = \begin{pmatrix} e^{-i\theta/2} & 0 \\ 0 & e^{i\theta/2} \end{pmatrix}.
$$

**步骤 3**：代入 $\theta = 2\pi$：

$$
U(2\pi, \hat{z}) = \begin{pmatrix} e^{-i\pi} & 0 \\ 0 & e^{i\pi} \end{pmatrix} = \begin{pmatrix} -1 & 0 \\ 0 & -1 \end{pmatrix} = -I_2.
$$

**步骤 4**：代入 $\theta = 4\pi$：

$$
U(4\pi, \hat{z}) = \begin{pmatrix} e^{-i2\pi} & 0 \\ 0 & e^{i2\pi} \end{pmatrix} = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} = I_2.
$$

**步骤 5**：验证 $\Phi(U(2\pi, \hat{z})) = R_z(2\pi) = I_3$。构造 $X = \vec{x} \cdot \vec{\sigma}$，计算

$$
X' = (-I_2) X (-I_2)^{\dagger} = (-I_2) X (-I_2) = I_2 X I_2 = X.
$$

故 $\vec{x}' = \vec{x}$，即 $R = I_3$。这确认了 $-I_2$ 与 $I_2$ 在 $SO(3)$ 中对应同一旋转，验证了核为 $\{\pm I_2\}$。

**步骤 6（反代验算）**：验证 $U(2\pi, \hat{z})$ 确实属于 $SU(2)$：

$$
U^{\dagger} U = (-I_2)^{\dagger}(-I_2) = (-I_2)(-I_2) = I_2, \quad \det(-I_2) = (-1)^2 = +1.
$$

满足 $SU(2)$ 定义。同时验证 $\Phi$ 为同态：对 $\theta_1, \theta_2$，

$$
U(\theta_1) U(\theta_2) = \begin{pmatrix} e^{-i\theta_1/2} & 0 \\ 0 & e^{i\theta_1/2} \end{pmatrix} \begin{pmatrix} e^{-i\theta_2/2} & 0 \\ 0 & e^{i\theta_2/2} \end{pmatrix} = \begin{pmatrix} e^{-i(\theta_1+\theta_2)/2} & 0 \\ 0 & e^{i(\theta_1+\theta_2)/2} \end{pmatrix} = U(\theta_1 + \theta_2),
$$

与 $R_z(\theta_1) R_z(\theta_2) = R_z(\theta_1 + \theta_2)$ 一致。

---

## 四、出处与纸质笔记坐标

### 教材出处

- **主教材**：Arfken & Weber, *Mathematical Methods for Physicists*, 7th Edition, Chapter 4, §4.1–§4.4, pp. 170–210。
  - §4.1：群论基本概念与定义（P170–P178）
  - §4.2：李群与李代数一般理论（P178–P190）
  - §4.3：$SO(3)$ 与旋转群表示（P190–P200）
  - §4.4

---
**知识图谱导航**：[[00_数学物理方法_学习全景图]]


### 纸质活页留痕槽位：[活页-MP-24]
- 请在此处记录推导手稿与疑难反思。
