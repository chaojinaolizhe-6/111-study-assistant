---
id: tm-t4-criteria-02
subject: 01-理论力学
title: 概念验收：直接给定 L，判断 E 是否守恒、是否等于 T+U（隔离判据二）
target_ids: [tm.t4.energy-criteria]
version: 1
kind: practice
status: open
est_minutes: 8
device: any
acceptance: 只做判断与代入，不要求建模：能说出 E 守恒的依据；能指出 T 里的 T₂ 项与 T₀ 项；能写出 E 而不写成 T+U
---

# 概念验收（只查判据二，不查建模）

> 目的：把"判据二"单独隔离出来。**题目已经把拉格朗日量给你**，你不需要做几何/建模。
> 与 `tm-t4-criteria-01.md`（转动圆环）的分工：那一题是**综合建模**，失败不能直接说明判据二不懂；这一题才是判据二的概念验收。

质量 $m$ 的珠子穿在一条光滑水平直杆上（无重力）。直杆绕通过其一端的**竖直轴**以**恒定角速度** $\Omega$ 转动。取 $r$ 为珠子到转轴的距离，已知

$$L=\frac12 m\dot r^2+\frac12 m\Omega^2 r^2$$

请回答：

1. 这个 $L$ 是否显含时间 $t$？由此判断 $E=\dot r\frac{\partial L}{\partial\dot r}-L$ 是否守恒，并说明依据。
2. 把动能写成 $T=T_2+T_1+T_0$ 的形式，指出每一项分别是什么（哪一项不含 $\dot r$）。
3. $E$ 等于 $T+U$ 吗？写出 $E$ 的表达式（本题 $U=0$，注意别直接把 $E$ 写成 $T$）。

> 记录：本题按**教学式**进行；若在提示后完成，如实记 `max_hint_level`，不升级为独立通过。
