---
id: ode-if-baseline-01
subject: 01-mock-diffeq
title: 基线题 v2：改为线性方程组（模拟，升版换目标+换类别）
target_ids: [ode.linear-systems]
version: 2
kind: delayed-variant
status: open
est_minutes: 30
device: any
due: 2026-10-07
acceptance: 无提示独立求解并验证
---

# 基线题 v2（模拟，边界测试：升版后 kind 与目标都变了）

> 【模拟数据】v1 目标是 ode.integrating-factor（kind=baseline，见 history/ode-if-baseline-01.v1.md）；
> v2 换成 ode.linear-systems 且 kind=delayed-variant。
> 旧 v1 事件必须按 v1 元数据解释：不得因 v2 是变式类而获得"未见变式"计分，
> 也不得因 v2 换了目标而被目标校验拒绝。

解 x' = 2x + y，y' = x + 2y，x(0) = 1，y(0) = 0。
