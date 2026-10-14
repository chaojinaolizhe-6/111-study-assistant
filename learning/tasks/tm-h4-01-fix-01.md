---
id: tm-h4-01-fix-01
subject: 01-理论力学
title: 订正 H4.1 的关键行（U′ 符号）——只改这一行，不必重写全过程
target_ids: [tm.t4.direct-check]
version: 1
kind: practice
status: done
est_minutes: 10
device: any
due: 2026-09-27
acceptance: 写出正确的 U′(x) 与正确的拉格朗日方程 mẍ = −U′(x)；据此重算 dE/dt = ẋ[mẍ + U′(x)] = 0
---

# 订正任务：H4.1 的关键行

**背景**：H4.1 的直接验证里，$U'(x)$ 的符号写错（写成加号），但因为同一个错误式子被用在 dE/dt 与拉格朗日方程两处，**碰巧相消得到 0**。按批改约定："错误推导碰巧得到正确结论"不能判为通过（见 `learning/attempts/corrections.md`）。

**只订正这两行**（不必重写全部过程）：

1. 由 $U(x)=\frac{k}{2}\big(\sqrt{h^2+x^2}-l_0\big)^2$ 求 $U'(x)$；
2. 写出拉格朗日方程给出的 $m\ddot x=-\;U'(x)$；
3. 重算 $\frac{dE}{dt}=\dot x\big[m\ddot x+U'(x)\big]$，确认等于 0。

完成后：本目标 `tm.t4.direct-check` 从"待核验"转为可复核；若独立完成（无提示），记一次干净表现。
