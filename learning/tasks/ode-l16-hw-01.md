---
id: ode-l16-hw-01
subject: 03-微分方程
title: Lecture 16–17 作业：求 e^(Ax) 并解 Y′ = AY（3 个矩阵）
target_ids: [ode.sys.matrix-exp, ode.sys.cayley-hamilton]
version: 1
kind: practice
status: open
est_minutes: 75
device: any
due: null
acceptance: 三题各自：写特征多项式→特征值→按 §3 的 Cayley–Hamilton 五步求 e^(Ax)（α 由 e^(λᵢx) = r(λᵢ) 定）→ 写出通解 Y = e^(Ax)C。⚠ 第 3 题为下三角阵（λ = −24, −2, 2 互异），仍走同一流程；三题**都不含重根亏损情形**，故本题不覆盖 g<m 分支。
---

# HW（Lecture 16–17 Matrix Exponential，课件 p44）

> 题面原文：**Find e^(Ax) and solving Y′ = AY.**　（For reading：C. Constanda, *Differential Equations*, Springer 2017, **PP. 167–174**）
> 课件：`subjects/03-微分方程/课件/16_17_matrix_exponential.pdf`（44 页，2026-10-13 老师发；**p44 是作业页**）
> 题面页图片：`subjects/03-微分方程/课件/16_17_matrix_exponential.pdf` p44（文字层可读，无需读图）
> **前置状态（2026-10-13）**：**Lecture 16–17 内容尚未学** ⟹ **先补讲再做**（矩阵指数定义与性质、Case 1 对角化、Cayley–Hamilton 法、基本解矩阵）。

## 题目

| # | A |
|---|---|
| (1) | `[[−6, −4], [8, 6]]` |
| (2) | `[[−4, 4], [−5, 4]]` |
| (3) | `[[−24, 0, 0], [4, −2, 0], [1, 0, 2]]` |

**截止**：课件与公告**均未给** → `[待确认]`（下一节课问老师；老师 10-13 刚发，通常下周交）。

## 核验要点（导师用，不对学习者展示；sympy 复核 ✓ 2026-10-13）

| # | 特征多项式 | 特征值 | e^(Ax) | 备注 |
|---|---|---|---|---|
| (1) | λ² − 4 | λ = 2, −2（互异） | **(sinh 2x / 2)·A + cosh 2x·E** = [[2e^(−2x) − e^(2x), e^(−2x) − e^(2x)], [2e^(2x) − 2e^(−2x), 2e^(2x) − e^(−2x)]] | α₀ = cosh 2x、xα₁ = sinh 2x / 2 |
| (2) | λ² + 4 | λ = ±2i | **(sin 2x / 2)·A + cos 2x·E** = [[cos 2x − 2 sin 2x, 2 sin 2x], [−(5/2) sin 2x, cos 2x + 2 sin 2x]] | α₀ = cos 2x、xα₁ = sin 2x / 2 |
| (3) | (λ+24)(λ+2)(λ−2) | λ = −24, −2, 2（互异；**下三角阵**，特征值即对角元） | [[e^(−24x), 0, 0], [(2/11)(e^(−2x) − e^(−24x)), e^(−2x), 0], [(1/26)(e^(2x) − e^(−24x)), 0, e^(2x)]] | e^(Ax) = α₂A²x² + α₁Ax + α₀E，由 e^(λᵢx) = r(λᵢ)（三条方程）定 α |

- **通解**：Y(x) = e^(Ax)·C（C 为任意常数列向量）；初值问题 Y(x₀) = Y₀ ⟹ Y = e^(A(x−x₀))Y₀。
- **方法对照**：课件给了两条路 —— ① Case 1（g = m）对角化 e^(Ax) = V e^(Λx) V⁻¹（p10–15）；② Cayley–Hamilton 化为 n−1 次多项式（p17–32，p32 有五步汇总）。本题三题都可用 ②，且都满足 g = m，①也行。
- ⚠ 与 Lecture 14–15 作业的关系：那 4 题考"特征值/特征向量/广义链"；这 3 题考"e^(Ax)"。**两套都要会**；期中范围是否含本章 `[待确认]`（见 `plan/inputs.yml` 的 de-midterm-review）。
