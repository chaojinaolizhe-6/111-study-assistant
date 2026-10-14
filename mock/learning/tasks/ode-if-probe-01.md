---
id: ode-if-probe-01
subject: 01-mock-diffeq
title: 探测题：提示后做对但错因待确认（模拟，边界测试）
target_ids: [ode.integrating-factor]
version: 2
kind: practice
status: open
est_minutes: 25
device: any
due: 2026-10-07
acceptance: 无提示独立完成并说明积分因子由来
---

# 探测题（模拟，边界测试：辅导后做对 ≠ 闭环）

> 【模拟数据】本场景验证：H2 提示后做对、错因 pending_probe 的事件应进入修复队列，
> 而不是因 final_result=correct 被跳过。

解 y' + 3y = 2e^x，y(0) = 0。
