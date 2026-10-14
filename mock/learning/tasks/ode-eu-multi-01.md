---
id: ode-eu-multi-01
subject: 01-mock-diffeq
title: 多目标题：存在唯一性（模拟，边界测试：跨目标修复）
target_ids: [ode.existence-uniqueness, ode.integrating-factor]
version: 1
kind: practice
status: open
est_minutes: 25
device: any
due: 2026-10-07
acceptance: 无提示独立完成
---

# 多目标题（模拟，边界测试：修复按目标追踪）

> 【模拟数据】场景：先在本题的 ode.existence-uniqueness 下失败且错因已确认（confirmed），
> 随后只针对 ode.integrating-factor 独立通过。
> 按（题目,目标）粒度：ode.existence-uniqueness 仍应留在修复队列，不被后一次通过关闭。

判断 y' = sqrt(y)（y ≥ 0）初值问题的解是否唯一；并解 y' + y = e^x，y(0) = 1。
