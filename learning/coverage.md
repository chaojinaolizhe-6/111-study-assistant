# 学习状态事实卡（coverage.md）

> **本文件由 `python -B tools/coverage.py` 生成，勿手工编辑**（派生视图）。
> 事实源：`learning/attempts.jsonl`（不改不删）+ `learning/corrections.jsonl`（订正）+ `learning/goals.yaml`（目标）+ 题目 frontmatter。
> 生成日期：2026-10-31 ｜ 事件 52 条 ｜ 订正 55 条 ｜ attempts.jsonl sha256 `1388bfe3d536e51e…`
> 手写意图（今天做什么、为什么暂缓）不在这里：见 `plan/today-<日期>.md`、`plan/gaps.md`、`.tutor/config/status-narrative.yml`。

## ① 能力目标覆盖（含**尚未出题**的考点）

`覆盖状态` 的六个取值，语义互斥：

| 覆盖状态 | 含义 | 下一步该做什么 |
|---|---|---|
| 未安排（无题目） | 目标已声明，但**一道题都没有** | 先建题（不建题它就永远是纸面目标）|
| 已安排·未作答 | 有题、还没做过 | 排进当天清单，做无提示基线 |
| 已作答·需补练 | 做过，但没有一次无提示独立通过 | 补讲/补练 → 撤去帮助再测 |
| 已作答·开卷/受助通过 | 通过过，但开卷或受助 | 换题、闭卷、无提示重测 |
| 已独立通过·待延迟复测 | 有独立通过，但日期跨度不足或未见变式不足 | 排**具体日期**的延迟变式 |
| 独立通过 | 日期跨度与未见变式都达标（= 迁移通过）| 进入记忆维护队列 |

### ee-ac-circuits — 独立求解电工电子技术 交流电路（Chapter Two）计算题

课程 `06-电工电子技术`　状态 `active`　里程碑 `2026-10-24`

| 目标 | 覆盖状态 | 等级 | 题数 | 独立通过日期 | 未解决困难 | 延迟检验 |
|---|---|---|---|---|---|---|
| `ee.ac.phasor-impedance` | 已独立通过·待延迟复测 | 曾独立完成 | 4 | 2026-09-28 | — | 未满足（跨度 0d < 2d） |
| `ee.ac.reactance` | 已独立通过·待延迟复测 | 延迟通过 | 4 | 2026-09-28、2026-09-30 | — | 已满足（跨度 2d ≥ 2d） |
| `ee.ac.resonance` | 已独立通过·待延迟复测 | 曾独立完成 | 5 | 2026-09-28 | — | 未满足（跨度 0d < 2d） |
| `ee.ac.series-rlc` | 已独立通过·待延迟复测 | 曾独立完成 | 6 | 2026-09-28 | — | 未满足（跨度 0d < 2d） |

### tm-t4-conservation-laws — 独立求解理论力学 Topic 4 守恒定律问题

课程 `01-理论力学`　状态 `active`　里程碑 `2026-10-23`

| 目标 | 覆盖状态 | 等级 | 题数 | 独立通过日期 | 未解决困难 | 延迟检验 |
|---|---|---|---|---|---|---|
| `tm.t3.lagrangian-construction` | 已安排·未作答 | 未测 | 1 | — | — | 未满足（跨度 0d < 2d） |
| `tm.t4.angular-momentum-integral` | 已作答·需补练 | 需支持 | 1 | — | — | 未满足（跨度 0d < 2d） |
| `tm.t4.cyclic-momentum` | 已作答·需补练 | 需支持 | 3 | — | — | 未满足（跨度 0d < 2d） |
| `tm.t4.direct-check` | 已独立通过·待延迟复测 | 曾独立完成 | 4 | 2026-09-28 | — | 未满足（跨度 0d < 2d） |
| `tm.t4.energy-criteria` | 已作答·需补练 | 需支持 | 5 | — | hurdle-1 | 未满足（跨度 0d < 2d） |
| `tm.t4.energy-integral` | 已独立通过·待延迟复测 | 曾独立完成 | 3 | 2026-09-28 | — | 未满足（跨度 0d < 2d） |
| `tm.t4.mechanical-similarity` | 已安排·未作答 | 未测 | 1 | — | — | 未满足（跨度 0d < 2d） |

### tm-t5-1d-motion — 独立求解理论力学 Topic 5 一维势场中的运动（能量积分）

课程 `01-理论力学`　状态 `active`　里程碑 `2026-11-08`

| 目标 | 覆盖状态 | 等级 | 题数 | 独立通过日期 | 未解决困难 | 延迟检验 |
|---|---|---|---|---|---|---|
| `tm.t5.central-motion-types` | 已作答·需补练 | 需支持 | 2 | — | hurdle-4 | 未满足（跨度 0d < 2d） |
| `tm.t5.effective-potential` | 已作答·需补练 | 需支持 | 2 | — | hurdle-4 | 未满足（跨度 0d < 2d） |
| `tm.t5.law-of-motion` | 已作答·需补练 | 需支持 | 1 | — | — | 未满足（跨度 0d < 2d） |
| `tm.t5.potential-analysis` | 已作答·需补练 | 需支持 | 1 | — | — | 未满足（跨度 0d < 2d） |
| `tm.t5.turning-points` | 已作答·需补练 | 需支持 | 2 | — | — | 未满足（跨度 0d < 2d） |

### ode-systems-const-coeff — 独立求解常系数线性系统 Y′ = AY（微分方程·方程组章）

课程 `03-微分方程`　状态 `active`　里程碑 `2026-11-09`

| 目标 | 覆盖状态 | 等级 | 题数 | 独立通过日期 | 未解决困难 | 延迟检验 |
|---|---|---|---|---|---|---|
| `ode.sys.case-complex` | 已作答·需补练 | 需支持 | 1 | — | — | 未满足（跨度 0d < 2d） |
| `ode.sys.case-repeated` | 已作答·需补练 | 需支持 | 1 | — | — | 未满足（跨度 0d < 2d） |
| `ode.sys.eigen-basic` | 已作答·需补练 | 需支持 | 1 | — | — | 未满足（跨度 0d < 2d） |
| `ode.sys.ivp` | 未安排（无题目） | 未测 | 0 | — | — | 未满足（跨度 0d < 2d） |

### pilot-ode-integrating-factor — 独立解一阶线性 ODE（试点）

课程 `03-微分方程`　状态 `active`　里程碑 `2026-10-22`

| 目标 | 覆盖状态 | 等级 | 题数 | 独立通过日期 | 未解决困难 | 延迟检验 |
|---|---|---|---|---|---|---|
| `ode.integrating-factor` | 已安排·未作答 | 未测 | 1 | — | — | 未满足（跨度 0d < 2d） |

### ielts-english-75 — 雅思训练：听力 8.0 / 口语 7.0 / 写作冲高（均分 7.5 通路）

课程 `11-英语-雅思`　状态 `active`

| 目标 | 覆盖状态 | 等级 | 题数 | 独立通过日期 | 未解决困难 | 延迟检验 |
|---|---|---|---|---|---|---|
| `en.listen.decoding` | 未安排（无题目） | 未测 | 0 | — | — | 未满足（跨度 0d < 2d） |
| `en.listen.structure` | 未安排（无题目） | 未测 | 0 | — | — | 未满足（跨度 0d < 2d） |
| `en.read.timed` | 未安排（无题目） | 未测 | 0 | — | — | 未满足（跨度 0d < 2d） |
| `en.speak.fc` | 未安排（无题目） | 未测 | 0 | — | — | 未满足（跨度 0d < 2d） |
| `en.speak.gra` | 未安排（无题目） | 未测 | 0 | — | — | 未满足（跨度 0d < 2d） |
| `en.speak.lr` | 未安排（无题目） | 未测 | 0 | — | — | 未满足（跨度 0d < 2d） |
| `en.speak.pr` | 未安排（无题目） | 未测 | 0 | — | — | 未满足（跨度 0d < 2d） |
| `en.write.cc` | 已作答·需补练 | 需支持 | 3 | — | — | 未满足（跨度 0d < 2d） |
| `en.write.gra` | 已作答·需补练 | 需支持 | 3 | — | — | 未满足（跨度 0d < 2d） |
| `en.write.lr` | 已作答·需补练 | 需支持 | 3 | — | — | 未满足（跨度 0d < 2d） |
| `en.write.tr` | 已作答·需补练 | 需支持 | 3 | — | — | 未满足（跨度 0d < 2d） |

### ai-tech-c00 — 独立完成 C00 编程与开发衔接（解释器/环境/容器/函数/文件/调试/Git/Notebook）

课程 `13-AI技术学习`　状态 `active`

| 目标 | 覆盖状态 | 等级 | 题数 | 独立通过日期 | 未解决困难 | 延迟检验 |
|---|---|---|---|---|---|---|
| `ai-tech.c00-01` | 已安排·未作答 | 未测 | 1 | — | — | 未满足（跨度 0d < 2d） |
| `ai-tech.c00-02` | 未安排（无题目） | 未测 | 0 | — | — | 未满足（跨度 0d < 2d） |
| `ai-tech.c00-03` | 未安排（无题目） | 未测 | 0 | — | — | 未满足（跨度 0d < 2d） |
| `ai-tech.c00-04` | 未安排（无题目） | 未测 | 0 | — | — | 未满足（跨度 0d < 2d） |
| `ai-tech.c00-05` | 未安排（无题目） | 未测 | 0 | — | — | 未满足（跨度 0d < 2d） |
| `ai-tech.c00-06` | 未安排（无题目） | 未测 | 0 | — | — | 未满足（跨度 0d < 2d） |
| `ai-tech.c00-07` | 未安排（无题目） | 未测 | 0 | — | — | 未满足（跨度 0d < 2d） |
| `ai-tech.c00-08` | 未安排（无题目） | 未测 | 0 | — | — | 未满足（跨度 0d < 2d） |

### 未归入任何能力目标的目标（`goals.yaml` 缺声明）

| 目标 | 覆盖状态 | 等级 | 题数 |
|---|---|---|---|
| `ee.dc.kcl` | 已独立通过·待延迟复测 | 曾独立完成 | 3 |
| `ee.dc.source-vs-load` | 已作答·需补练 | 需支持 | 3 |
| `ee.dc.steady-state` | 已作答·需补练 | 需支持 | 3 |
| `mp.delta-function` | 已安排·未作答 | 未测 | 1 |
| `mp.fourier-series` | 已安排·未作答 | 未测 | 1 |
| `mp.fourier-transform` | 已安排·未作答 | 未测 | 1 |
| `mp.isolated-singularity` | 已作答·需补练 | 需支持 | 7 |
| `mp.laplace-inverse` | 已安排·未作答 | 未测 | 1 |
| `mp.laplace-ode` | 已安排·未作答 | 未测 | 1 |
| `mp.laplace-transform` | 已安排·未作答 | 未测 | 1 |
| `mp.laurent-expansion` | 已作答·需补练 | 需支持 | 3 |
| `mp.power-series-radius` | 已独立通过·待延迟复测 | 曾独立完成 | 3 |
| `mp.residue-applications` | 已作答·需补练 | 需支持 | 3 |
| `mp.residue-computation` | 已独立通过·待延迟复测 | 曾独立完成 | 3 |
| `mp.residue-definition` | 已作答·需补练 | 需支持 | 3 |
| `mp.taylor-expansion` | 已独立通过·待延迟复测 | 曾独立完成 | 3 |
| `ode.clairaut` | 已作答·需补练 | 需支持 | 2 |
| `ode.const-coeff-homogeneous` | 已作答·需补练 | 需支持 | 1 |
| `ode.exact-integ factor` | 已作答·开卷/受助通过 | 需支持 | 1 |
| `ode.first-order-linear` | 已作答·需补练 | 需支持 | 1 |
| `ode.homogeneous` | 已作答·需补练 | 需支持 | 2 |
| `ode.order-reduction` | 已作答·需补练 | 需支持 | 2 |
| `ode.riccati` | 已作答·需补练 | 需支持 | 1 |
| `ode.separable` | 已作答·需补练 | 需支持 | 1 |
| `ode.sys.cayley-hamilton` | 已安排·未作答 | 未测 | 1 |
| `ode.sys.matrix-exp` | 已安排·未作答 | 未测 | 1 |
| `ode.system-reduction` | 已作答·需补练 | 需支持 | 1 |
| `ode.undetermined-coefficients` | 已作答·需补练 | 需支持 | 1 |
| `ru.adj-agreement` | 已安排·未作答 | 未测 | 1 |
| `ru.noun-forms` | 已作答·需补练 | 需支持 | 2 |
| `ru.noun-gender` | 已作答·需补练 | 需支持 | 4 |
| `ru.qword-agreement` | 已独立通过·待延迟复测 | 曾独立完成 | 3 |
| `ru.qword.kakoy-agreement` | 已安排·未作答 | 未测 | 1 |
| `ru.syntax.chto-clause` | 已安排·未作答 | 未测 | 1 |
| `ru.syntax.potomy-chto` | 已安排·未作答 | 未测 | 1 |
| `ru.verb.znat-dumat` | 已安排·未作答 | 未测 | 1 |

## ② 已声明但**一道题都没有**的考点（不会因为没有题目而从系统消失）

| 目标 | 所属能力目标 | 等级 | 说明 |
|---|---|---|---|
| `ai-tech.c00-02` | ai-tech-c00 | 未测 | 目标已声明、从未出题 → 目前没有任何能力证据 |
| `ai-tech.c00-03` | ai-tech-c00 | 未测 | 目标已声明、从未出题 → 目前没有任何能力证据 |
| `ai-tech.c00-04` | ai-tech-c00 | 未测 | 目标已声明、从未出题 → 目前没有任何能力证据 |
| `ai-tech.c00-05` | ai-tech-c00 | 未测 | 目标已声明、从未出题 → 目前没有任何能力证据 |
| `ai-tech.c00-06` | ai-tech-c00 | 未测 | 目标已声明、从未出题 → 目前没有任何能力证据 |
| `ai-tech.c00-07` | ai-tech-c00 | 未测 | 目标已声明、从未出题 → 目前没有任何能力证据 |
| `ai-tech.c00-08` | ai-tech-c00 | 未测 | 目标已声明、从未出题 → 目前没有任何能力证据 |
| `en.listen.decoding` | ielts-english-75 | 未测 | 目标已声明、从未出题 → 目前没有任何能力证据 |
| `en.listen.structure` | ielts-english-75 | 未测 | 目标已声明、从未出题 → 目前没有任何能力证据 |
| `en.read.timed` | ielts-english-75 | 未测 | 目标已声明、从未出题 → 目前没有任何能力证据 |
| `en.speak.fc` | ielts-english-75 | 未测 | 目标已声明、从未出题 → 目前没有任何能力证据 |
| `en.speak.gra` | ielts-english-75 | 未测 | 目标已声明、从未出题 → 目前没有任何能力证据 |
| `en.speak.lr` | ielts-english-75 | 未测 | 目标已声明、从未出题 → 目前没有任何能力证据 |
| `en.speak.pr` | ielts-english-75 | 未测 | 目标已声明、从未出题 → 目前没有任何能力证据 |
| `ode.sys.ivp` | ode-systems-const-coeff | 未测 | 目标已声明、从未出题 → 目前没有任何能力证据 |

> ⚠ 「没有题目」既**不等于**已掌握，也**不等于**没学过——它表示**系统里没有任何证据**。
> 处理方式必须由学习者指定（见 `plan/gaps.md` / `ISSUES-待改进.md` A7），本文件不自动建题。

## ③ 覆盖状态分布

| 覆盖状态 | 目标数 |
|---|---|
| 未安排（无题目） | 15 |
| 已安排·未作答 | 17 |
| 已作答·需补练 | 32 |
| 已作答·开卷/受助通过 | 1 |
| 已独立通过·待延迟复测 | 11 |
| 独立通过 | 0 |
| **合计** | **76** |

## ④ 四个维度分开看（**不要挤成一个「等级」**）

| 目标 | ① 作业完成 | ② 概念困难已解决 | ③ 独立作答表现 | ④ 延迟检验 |
|---|---|---|---|---|
| `ai-tech.c00-01` | 未开始（0次作答） | 无困难记录 | 无作答 | ❌ |
| `ai-tech.c00-02` | —（无题目） | 无困难记录 | 无作答 | ❌ |
| `ai-tech.c00-03` | —（无题目） | 无困难记录 | 无作答 | ❌ |
| `ai-tech.c00-04` | —（无题目） | 无困难记录 | 无作答 | ❌ |
| `ai-tech.c00-05` | —（无题目） | 无困难记录 | 无作答 | ❌ |
| `ai-tech.c00-06` | —（无题目） | 无困难记录 | 无作答 | ❌ |
| `ai-tech.c00-07` | —（无题目） | 无困难记录 | 无作答 | ❌ |
| `ai-tech.c00-08` | —（无题目） | 无困难记录 | 无作答 | ❌ |
| `ee.ac.phasor-impedance` | 进行中 | 无困难记录 | 独立通过 1 次（2026-09-28） | ❌ |
| `ee.ac.reactance` | 进行中 | 无困难记录 | 独立通过 2 次（2026-09-28、2026-09-30） | ✅ |
| `ee.ac.resonance` | 进行中 | 无困难记录 | 独立通过 1 次（2026-09-28） | ❌ |
| `ee.ac.series-rlc` | 进行中 | 无困难记录 | 独立通过 1 次（2026-09-28） | ❌ |
| `ee.dc.kcl` | 进行中 | 无困难记录 | 独立通过 1 次（2026-09-30） | ❌ |
| `ee.dc.source-vs-load` | 进行中 | 无困难记录 | 0 次独立通过（5 次作答，其中 5 次受助/曝光） | ❌ |
| `ee.dc.steady-state` | 进行中 | 无困难记录 | 0 次独立通过（4 次作答，其中 4 次受助/曝光） | ❌ |
| `en.listen.decoding` | —（无题目） | 无困难记录 | 无作答 | ❌ |
| `en.listen.structure` | —（无题目） | 无困难记录 | 无作答 | ❌ |
| `en.read.timed` | —（无题目） | 无困难记录 | 无作答 | ❌ |
| `en.speak.fc` | —（无题目） | 无困难记录 | 无作答 | ❌ |
| `en.speak.gra` | —（无题目） | 无困难记录 | 无作答 | ❌ |
| `en.speak.lr` | —（无题目） | 无困难记录 | 无作答 | ❌ |
| `en.speak.pr` | —（无题目） | 无困难记录 | 无作答 | ❌ |
| `en.write.cc` | 进行中 | 无困难记录 | 0 次独立通过（2 次作答，其中 2 次受助/曝光） | ❌ |
| `en.write.gra` | 进行中 | 无困难记录 | 0 次独立通过（2 次作答，其中 2 次受助/曝光） | ❌ |
| `en.write.lr` | 进行中 | 无困难记录 | 0 次独立通过（2 次作答，其中 2 次受助/曝光） | ❌ |
| `en.write.tr` | 进行中 | 无困难记录 | 0 次独立通过（2 次作答，其中 2 次受助/曝光） | ❌ |
| `mp.delta-function` | 未开始（0次作答） | 无困难记录 | 无作答 | ❌ |
| `mp.fourier-series` | 未开始（0次作答） | 无困难记录 | 无作答 | ❌ |
| `mp.fourier-transform` | 未开始（0次作答） | 无困难记录 | 无作答 | ❌ |
| `mp.isolated-singularity` | 进行中 | 无困难记录 | 0 次独立通过（8 次作答，其中 8 次受助/曝光） | ❌ |
| `mp.laplace-inverse` | 未开始（0次作答） | 无困难记录 | 无作答 | ❌ |
| `mp.laplace-ode` | 未开始（0次作答） | 无困难记录 | 无作答 | ❌ |
| `mp.laplace-transform` | 未开始（0次作答） | 无困难记录 | 无作答 | ❌ |
| `mp.laurent-expansion` | 进行中 | ❌ 未解决 hurdle-2 | 0 次独立通过（5 次作答，其中 5 次受助/曝光） | ❌ |
| `mp.power-series-radius` | 进行中 | 无困难记录 | 独立通过 1 次（2026-10-03） | ❌ |
| `mp.residue-applications` | 进行中 | 无困难记录 | 0 次独立通过（2 次作答，其中 2 次受助/曝光） | ❌ |
| `mp.residue-computation` | 进行中 | 无困难记录 | 独立通过 1 次（2026-10-01） | ❌ |
| `mp.residue-definition` | 进行中 | 无困难记录 | 0 次独立通过（2 次作答，其中 2 次受助/曝光） | ❌ |
| `mp.taylor-expansion` | 进行中 | ❌ 未解决 hurdle-2 | 独立通过 1 次（2026-10-03） | ❌ |
| `ode.clairaut` | 进行中 | 无困难记录 | 0 次独立通过（2 次作答，其中 2 次受助/曝光） | ❌ |
| `ode.const-coeff-homogeneous` | 进行中 | 无困难记录 | 0 次独立通过（1 次作答，其中 1 次受助/曝光） | ❌ |
| `ode.exact-integ factor` | 进行中 | 无困难记录 | 仅开卷/受助通过（1 次） | ❌ |
| `ode.first-order-linear` | 进行中 | 无困难记录 | 0 次独立通过（1 次作答，其中 1 次受助/曝光） | ❌ |
| `ode.homogeneous` | 进行中 | 无困难记录 | 0 次独立通过（2 次作答，其中 2 次受助/曝光） | ❌ |
| `ode.integrating-factor` | 未开始（0次作答） | 无困难记录 | 无作答 | ❌ |
| `ode.order-reduction` | 进行中 | 无困难记录 | 0 次独立通过（2 次作答，其中 2 次受助/曝光） | ❌ |
| `ode.riccati` | 进行中 | 无困难记录 | 0 次独立通过（1 次作答，其中 1 次受助/曝光） | ❌ |
| `ode.separable` | 进行中 | 无困难记录 | 0 次独立通过（1 次作答，其中 1 次受助/曝光） | ❌ |
| `ode.sys.case-complex` | 进行中 | 无困难记录 | 0 次独立通过（2 次作答，其中 2 次受助/曝光） | ❌ |
| `ode.sys.case-repeated` | 进行中 | 无困难记录 | 0 次独立通过（2 次作答，其中 2 次受助/曝光） | ❌ |
| `ode.sys.cayley-hamilton` | 未开始（0次作答） | 无困难记录 | 无作答 | ❌ |
| `ode.sys.eigen-basic` | 进行中 | 无困难记录 | 0 次独立通过（2 次作答，其中 2 次受助/曝光） | ❌ |
| `ode.sys.ivp` | —（无题目） | 无困难记录 | 无作答 | ❌ |
| `ode.sys.matrix-exp` | 未开始（0次作答） | 无困难记录 | 无作答 | ❌ |
| `ode.system-reduction` | 进行中 | 无困难记录 | 0 次独立通过（1 次作答，其中 1 次受助/曝光） | ❌ |
| `ode.undetermined-coefficients` | 进行中 | 无困难记录 | 0 次独立通过（1 次作答，其中 1 次受助/曝光） | ❌ |
| `ru.adj-agreement` | 未开始（0次作答） | 无困难记录 | 无作答 | ❌ |
| `ru.noun-forms` | 进行中 | 无困难记录 | 0 次独立通过（2 次作答，其中 2 次受助/曝光） | ❌ |
| `ru.noun-gender` | 进行中 | 无困难记录 | 0 次独立通过（2 次作答，其中 2 次受助/曝光） | ❌ |
| `ru.qword-agreement` | 进行中 | ❌ 未解决 hurdle-3 | 独立通过 1 次（2026-09-30） | ❌ |
| `ru.qword.kakoy-agreement` | 未开始（0次作答） | 无困难记录 | 无作答 | ❌ |
| `ru.syntax.chto-clause` | 未开始（0次作答） | 无困难记录 | 无作答 | ❌ |
| `ru.syntax.potomy-chto` | 未开始（0次作答） | 无困难记录 | 无作答 | ❌ |
| `ru.verb.znat-dumat` | 未开始（0次作答） | 无困难记录 | 无作答 | ❌ |
| `tm.t3.lagrangian-construction` | 未开始（0次作答） | 无困难记录 | 无作答 | ❌ |
| `tm.t4.angular-momentum-integral` | 进行中 | 无困难记录 | 0 次独立通过（1 次作答，其中 1 次受助/曝光） | ❌ |
| `tm.t4.cyclic-momentum` | 进行中 | 无困难记录 | 0 次独立通过（4 次作答，其中 4 次受助/曝光） | ❌ |
| `tm.t4.direct-check` | 进行中 | 无困难记录 | 独立通过 1 次（2026-09-28） | ❌ |
| `tm.t4.energy-criteria` | 进行中 | ✅ 已结案 hurdle-1 | 0 次独立通过（6 次作答，其中 6 次受助/曝光） | ❌ |
| `tm.t4.energy-integral` | 进行中 | 无困难记录 | 独立通过 1 次（2026-09-28） | ❌ |
| `tm.t4.mechanical-similarity` | 未开始（0次作答） | 无困难记录 | 无作答 | ❌ |
| `tm.t5.central-motion-types` | 进行中 | ❌ 未解决 hurdle-4 | 0 次独立通过（2 次作答，其中 2 次受助/曝光） | ❌ |
| `tm.t5.effective-potential` | 进行中 | ❌ 未解决 hurdle-4 | 0 次独立通过（2 次作答，其中 2 次受助/曝光） | ❌ |
| `tm.t5.law-of-motion` | 进行中 | 无困难记录 | 0 次独立通过（1 次作答，其中 1 次受助/曝光） | ❌ |
| `tm.t5.potential-analysis` | 进行中 | 无困难记录 | 0 次独立通过（1 次作答，其中 1 次受助/曝光） | ❌ |
| `tm.t5.turning-points` | 进行中 | 无困难记录 | 0 次独立通过（2 次作答，其中 2 次受助/曝光） | ❌ |

> **困难结案 ≠ 目标升级**：`hurdle` 结案只说明「那个卡点讲通了」，
> 目标等级只看「有没有在无提示、闭卷、未见变式的条件下独立答对」。
> **交了作业 ≠ 会做**：作业完成是事务状态，不进入等级判定。

## ⑤ 未升级的作答事件与原因（可复查）

| 目标 | 事件 | 日期 | 未升级原因 |
|---|---|---|---|
| `ee.ac.phasor-impedance` | `attempt-8` | 2026-09-28 | 待核验 |
| `ee.ac.phasor-impedance` | `attempt-34` | 2026-09-30 | 结果=not_attempted；待核验 |
| `ee.ac.phasor-impedance` | `attempt-35` | 2026-09-30 | 待核验；曝光=partial@before_attempt |
| `ee.ac.reactance` | `attempt-12` | 2026-09-28 | 结果=partial；待核验 |
| `ee.ac.reactance` | `attempt-34` | 2026-09-30 | 结果=not_attempted；待核验 |
| `ee.ac.resonance` | `attempt-9` | 2026-09-28 | 待核验；曝光=partial@unknown |
| `ee.ac.resonance` | `attempt-22` | 2026-09-29 | 示例学习；非闭卷；提示H4；待核验；曝光=full@before_attempt |
| `ee.ac.resonance` | `attempt-23` | 2026-09-30 | 非闭卷；提示H4；待核验；曝光=full@before_attempt |
| `ee.ac.resonance` | `attempt-34` | 2026-09-30 | 结果=not_attempted；待核验 |
| `ee.ac.resonance` | `attempt-35` | 2026-09-30 | 结果=not_attempted；提示H3；待核验；曝光=partial@before_attempt |
| `ee.ac.series-rlc` | `attempt-9` | 2026-09-28 | 提示H4；待核验；曝光=partial@during_attempt |
| `ee.ac.series-rlc` | `attempt-22` | 2026-09-29 | 示例学习；非闭卷；提示H4；待核验；曝光=full@before_attempt |
| `ee.ac.series-rlc` | `attempt-23` | 2026-09-30 | 非闭卷；提示H4；待核验；曝光=full@before_attempt |
| `ee.ac.series-rlc` | `attempt-34` | 2026-09-30 | 结果=not_attempted；待核验 |
| `ee.ac.series-rlc` | `attempt-35` | 2026-09-30 | 待核验；曝光=partial@before_attempt |
| `ee.dc.kcl` | `attempt-20` | 2026-09-29 | 结果=partial |
| `ee.dc.kcl` | `attempt-22` | 2026-09-29 | 示例学习；非闭卷；提示H4；待核验；曝光=full@before_attempt |
| `ee.dc.kcl` | `attempt-23` | 2026-09-30 | 非闭卷；提示H4；待核验；曝光=full@before_attempt |
| `ee.dc.source-vs-load` | `attempt-21` | 2026-09-29 | 结果=incorrect；提示H3；曝光=partial@before_attempt |
| `ee.dc.source-vs-load` | `attempt-22` | 2026-09-29 | 示例学习；非闭卷；提示H4；待核验；曝光=full@before_attempt |
| `ee.dc.source-vs-load` | `attempt-23` | 2026-09-30 | 非闭卷；提示H4；待核验；曝光=full@before_attempt |
| `ee.dc.source-vs-load` | `attempt-34` | 2026-09-30 | 结果=not_attempted；待核验 |
| `ee.dc.source-vs-load` | `attempt-35` | 2026-09-30 | 结果=not_attempted；待核验；曝光=partial@before_attempt |
| `ee.dc.steady-state` | `attempt-22` | 2026-09-29 | 示例学习；非闭卷；提示H4；待核验；曝光=full@before_attempt |
| `ee.dc.steady-state` | `attempt-23` | 2026-09-30 | 非闭卷；提示H4；待核验；曝光=full@before_attempt |
| `ee.dc.steady-state` | `attempt-34` | 2026-09-30 | 结果=not_attempted；待核验 |
| `ee.dc.steady-state` | `attempt-35` | 2026-09-30 | 结果=not_attempted；提示H3；待核验；曝光=partial@before_attempt |
| `en.write.cc` | `attempt-41` | 2026-10-04 | 结果=partial；待核验 |
| `en.write.cc` | `attempt-42` | 2026-10-04 | 结果=partial；提示H2；待核验；曝光=partial@before_attempt |
| `en.write.gra` | `attempt-41` | 2026-10-04 | 结果=partial；待核验 |
| `en.write.gra` | `attempt-42` | 2026-10-04 | 结果=partial；提示H2；待核验；曝光=partial@before_attempt |
| `en.write.lr` | `attempt-41` | 2026-10-04 | 结果=partial；待核验 |
| `en.write.lr` | `attempt-42` | 2026-10-04 | 结果=partial；提示H2；待核验；曝光=partial@before_attempt |
| `en.write.tr` | `attempt-41` | 2026-10-04 | 结果=partial；待核验 |
| `en.write.tr` | `attempt-42` | 2026-10-04 | 结果=partial；提示H2；待核验；曝光=partial@before_attempt |
| `mp.isolated-singularity` | `attempt-10` | 2026-09-28 | 示例学习；非闭卷；提示H4；待核验；曝光=full@before_attempt |
| `mp.isolated-singularity` | `attempt-27` | 2026-09-30 | 结果=partial；提示H1；待核验；曝光=partial@before_attempt |
| `mp.isolated-singularity` | `attempt-28` | 2026-09-30 | 结果=partial；提示H2；曝光=partial@before_attempt |
| `mp.isolated-singularity` | `attempt-29` | 2026-09-30 | 提示H2；待核验；曝光=partial@before_attempt |
| `mp.isolated-singularity` | `attempt-30` | 2026-09-30 | 结果=partial |
| `mp.isolated-singularity` | `attempt-31` | 2026-09-30 | 提示H3；待核验；曝光=partial@before_attempt |
| `mp.isolated-singularity` | `attempt-39` | 2026-10-03 | 结果=partial |
| `mp.isolated-singularity` | `attempt-40` | 2026-10-03 | 提示H3；曝光=partial@before_attempt |
| `mp.laurent-expansion` | `attempt-10` | 2026-09-28 | 示例学习；非闭卷；提示H4；待核验；曝光=full@before_attempt |
| `mp.laurent-expansion` | `attempt-17` | 2026-09-29 | 结果=partial；提示H3；待核验；曝光=partial@before_attempt |
| `mp.laurent-expansion` | `attempt-18` | 2026-09-29 | 非闭卷；提示H3；待核验；曝光=partial@before_attempt |
| `mp.laurent-expansion` | `attempt-19` | 2026-09-29 | 结果=incorrect |
| `mp.laurent-expansion` | `attempt-38` | 2026-10-03 | 结果=partial |
| `mp.power-series-radius` | `attempt-10` | 2026-09-28 | 示例学习；非闭卷；提示H4；待核验；曝光=full@before_attempt |
| `mp.power-series-radius` | `attempt-15` | 2026-09-28 | 结果=partial；待核验；曝光=full@before_attempt |
| `mp.power-series-radius` | `attempt-16` | 2026-09-28 | 结果=partial；提示H2；待核验 |
| `mp.residue-applications` | `attempt-36` | 2026-10-01 | 结果=not_attempted；待核验 |
| `mp.residue-applications` | `attempt-46` | 2026-10-09 | 结果=partial；提示H3；待核验；曝光=partial@before_attempt |
| `mp.residue-computation` | `attempt-46` | 2026-10-09 | 结果=partial；提示H4；待核验；曝光=partial@before_attempt |
| `mp.residue-definition` | `attempt-36` | 2026-10-01 | 结果=partial |
| `mp.residue-definition` | `attempt-46` | 2026-10-09 | 结果=partial；提示H2；待核验；曝光=partial@before_attempt |
| `mp.taylor-expansion` | `attempt-10` | 2026-09-28 | 示例学习；非闭卷；提示H4；待核验；曝光=full@before_attempt |
| `mp.taylor-expansion` | `attempt-15` | 2026-09-28 | 待核验；曝光=full@before_attempt |
| `ode.clairaut` | `attempt-50` | 2026-10-08 | 非闭卷；结果=incorrect；待核验 |
| `ode.clairaut` | `attempt-51` | 2026-10-14 | 非闭卷；结果=partial；提示H4；待核验；曝光=full@before_attempt |
| `ode.const-coeff-homogeneous` | `attempt-50` | 2026-10-08 | 非闭卷；结果=partial；待核验 |
| `ode.first-order-linear` | `attempt-50` | 2026-10-08 | 非闭卷；结果=partial；待核验 |
| `ode.homogeneous` | `attempt-50` | 2026-10-08 | 非闭卷；结果=incorrect；待核验 |
| `ode.homogeneous` | `attempt-51` | 2026-10-14 | 非闭卷；结果=partial；提示H3；待核验；曝光=partial@before_attempt |
| `ode.order-reduction` | `attempt-50` | 2026-10-08 | 非闭卷；结果=partial；待核验 |
| `ode.order-reduction` | `attempt-51` | 2026-10-14 | 非闭卷；结果=partial；提示H3；待核验；曝光=partial@before_attempt |
| `ode.riccati` | `attempt-50` | 2026-10-08 | 非闭卷；结果=partial；待核验 |
| `ode.separable` | `attempt-50` | 2026-10-08 | 非闭卷；结果=partial；待核验 |
| `ode.sys.case-complex` | `attempt-48` | 2026-10-12 | 提示H3；曝光=partial@before_attempt |
| `ode.sys.case-complex` | `attempt-49` | 2026-10-13 | 提示H3；曝光=partial@before_attempt |
| `ode.sys.case-repeated` | `attempt-48` | 2026-10-12 | 结果=incorrect；提示H3；曝光=partial@before_attempt |
| `ode.sys.case-repeated` | `attempt-49` | 2026-10-13 | 提示H3；待核验；曝光=partial@before_attempt |
| `ode.sys.eigen-basic` | `attempt-48` | 2026-10-12 | 提示H3；曝光=partial@before_attempt |
| `ode.sys.eigen-basic` | `attempt-49` | 2026-10-13 | 提示H3；曝光=partial@before_attempt |
| `ode.system-reduction` | `attempt-11` | 2026-09-28 | 提示H2；待核验；曝光=partial@before_attempt |
| `ode.undetermined-coefficients` | `attempt-50` | 2026-10-08 | 非闭卷；结果=partial；待核验 |
| `ru.noun-forms` | `attempt-44` | 2026-10-08 | 结果=partial；提示H2；待核验；曝光=partial@before_attempt |
| `ru.noun-forms` | `attempt-45` | 2026-10-08 | 提示H2；待核验；曝光=partial@before_attempt |
| `ru.noun-gender` | `attempt-26` | 2026-09-30 | 结果=partial |
| `ru.noun-gender` | `attempt-43` | 2026-10-08 | 结果=partial；待核验 |
| `ru.qword-agreement` | `attempt-43` | 2026-10-08 | 待核验 |
| `tm.t4.angular-momentum-integral` | `attempt-37` | 2026-10-01 | 结果=partial；待核验 |
| `tm.t4.cyclic-momentum` | `attempt-4` | 2026-09-28 | 结果=partial；待核验；曝光=full@before_attempt |
| `tm.t4.cyclic-momentum` | `attempt-7` | 2026-09-28 | 结果=partial；待核验；曝光=full@before_attempt |
| `tm.t4.cyclic-momentum` | `attempt-32` | 2026-09-30 | 结果=partial；待核验；曝光=partial@before_attempt |
| `tm.t4.cyclic-momentum` | `attempt-33` | 2026-09-30 | 结果=partial；提示H2；待核验；曝光=partial@before_attempt |
| `tm.t4.direct-check` | `attempt-2` | 2026-09-26 | 结果=partial；提示H3；待核验 |
| `tm.t4.direct-check` | `attempt-6` | 2026-09-28 | 结果=partial；待核验；曝光=partial@before_attempt |
| `tm.t4.energy-criteria` | `attempt-3` | 2026-09-28 | 结果=partial；提示H3；待核验 |
| `tm.t4.energy-criteria` | `attempt-5` | 2026-09-28 | 待核验；曝光=partial@before_attempt |
| `tm.t4.energy-criteria` | `attempt-6` | 2026-09-28 | 曝光=partial@before_attempt |
| `tm.t4.energy-criteria` | `attempt-13` | 2026-09-28 | 结果=blocked；待核验；曝光=partial@before_attempt |
| `tm.t4.energy-criteria` | `attempt-14` | 2026-09-28 | 结果=partial；提示H2；待核验；曝光=partial@during_attempt |
| `tm.t4.energy-criteria` | `attempt-25` | 2026-09-30 | 结果=partial |
| `tm.t4.energy-integral` | `attempt-1` | 2026-09-26 | 结果=partial |
| `tm.t4.energy-integral` | `attempt-2` | 2026-09-26 | 提示H3 |
| `tm.t4.energy-integral` | `attempt-4` | 2026-09-28 | 曝光=full@before_attempt |
| `tm.t4.energy-integral` | `attempt-6` | 2026-09-28 | 曝光=partial@before_attempt |
| `tm.t4.energy-integral` | `attempt-7` | 2026-09-28 | 曝光=full@before_attempt |
| `tm.t5.central-motion-types` | `attempt-52` | 2026-10-19 | 结果=partial；提示H1；待核验；曝光=partial@before_attempt |
| `tm.t5.central-motion-types` | `attempt-53` | 2026-10-19 | 非闭卷；结果=partial；提示H4；曝光=full@before_attempt |
| `tm.t5.effective-potential` | `attempt-52` | 2026-10-19 | 结果=partial；提示H1；待核验；曝光=partial@before_attempt |
| `tm.t5.effective-potential` | `attempt-53` | 2026-10-19 | 非闭卷；结果=partial；提示H4；曝光=full@before_attempt |
| `tm.t5.law-of-motion` | `attempt-47` | 2026-10-12 | 结果=partial；提示H3；待核验；曝光=partial@before_attempt |
| `tm.t5.potential-analysis` | `attempt-47` | 2026-10-12 | 提示H3；待核验；曝光=partial@before_attempt |
| `tm.t5.turning-points` | `attempt-47` | 2026-10-12 | 提示H3；曝光=partial@before_attempt |
| `tm.t5.turning-points` | `attempt-52` | 2026-10-19 | 提示H1；曝光=partial@before_attempt |

## ⑥ 订正台账（原始事件不改不删，订正单独成条）

共 55 条，全文见 `learning/corrections.jsonl`；人读渲染见 `learning/attempts/corrections.md`。

| 订正 | 事件 | 字段 | from → to | 证据 |
|---|---|---|---|---|
| `corr-20260928-01` | `attempt-9` | `ee.ac.series-rlc.hint_level` | `0` → `4` | subjects/06-电工电子技术/作业/20260928-C2H2-Q4.jpg |
| `corr-20260928-02` | `attempt-9` | `ee.ac.series-rlc.needs_verify` | `False` → `True` | learning/attempts.jsonl:9 target_results[ee.ac.series-rlc].note（由导师代算） |
| `corr-20260928-03` | `attempt-9` | `ee.ac.series-rlc.exposure` | `None` → `'partial'` | learning/attempts.jsonl:9 solution_exposure=partial |
| `corr-20260928-04` | `attempt-9` | `ee.ac.series-rlc.exposure_timing` | `None` → `'during_attempt'` | subjects/06-电工电子技术/作业/20260928-C2H2-Q4.jpg |
| `corr-20260928-05` | `attempt-9` | `ee.ac.series-rlc.note` | `'Q4：ω = 314、U = 220 V、X_L = 2πfL = 4.8π Ω、Z = 20 + j4.8π，建模全对；|Z| 与 I 两处结果留空，由导师按学习者要求代算（|Z| = √(20²+(4.8π)²) ≈ 25.05 Ω、I = 220/|Z| ≈ 8.78 A）。写法问题：写成 İ = U̇/|Z|，应为 |İ| = |U̇|/|Z| 或 İ = U̇/Z'` → `'Q4 分两段记。【独立部分】ω = 314、U = 220 V、L = 4.8×10⁻² H、X_L = 2πfL = 4.8π Ω、Z = 20 + j4.8π：列式与建模正确、原稿可证，这部分保留为学习者的独立表现。【受助部分】|Z| = 与 İ = 两处原稿留空，由导师按学习者要求代算（|Z| ≈ 25.05 Ω、I ≈ 8.78 A）—— 该两个结果不是学习者本人产出，故 final=correct 只表示答案正确，本目标记【受助完成】、不计独立通过、待未见同类题复测。写法项：İ = U̇/|Z| 应为 |İ| = |U̇|/|Z| 或 İ = U̇/Z。'` | subjects/06-电工电子技术/作业/20260928-C2H2-Q4.jpg |
| `corr-20260928-06` | `attempt-9` | `max_hint_level` | `0` → `4` | learning/corrections.jsonl corr-20260928-01 |
| `corr-20260928-07` | `attempt-9` | `exposure_timing` | `'after_attempt'` → `'during_attempt'` | learning/corrections.jsonl corr-20260928-04 |
| `corr-20260928-08` | `attempt-9` | `error_hypothesis` | `'五题的概念、建模与数值全部正确，无理解性错误。反复出现的唯一问题是『量名／单位标签』，共 3 处：①诊断 Q3(b) 把 Z = 50∠53° 写成 U̇ = Z·İ 的结果（漏电流模值）；②Q4 写 İ = U̇/|Z|（复数除以实数，不改变角度）；③Q5(2) 把阻抗 Z′ = 100 + j270 Ω 写成 U̇ = ... V。三处数值都对，属书写规范而非概念错误'` → `'Q1、Q2、Q3、Q5 的概念、列式与数值全部正确；Q4 的 |Z| 与 I 两处留空后由导师代算（见 target_results[ee.ac.series-rlc]），不构成学习者的独立表现，已改记受助完成。反复出现的唯一问题是『量名／单位标签』，共 2 处：①Q4 写 İ = U̇/|Z|（复数除以实数，不改变角度）；②Q5(2) 把阻抗 Z′ = 100 + j270 Ω 写成 U̇ = ... V。两处数值都对，属书写规范而非概念错误'` | learning/corrections.jsonl corr-20260928-01 / corr-20260928-12 |
| `corr-20260928-09` | `attempt-9` | `ee.ac.reactance.exposure` | `None` → `'none'` | subjects/06-电工电子技术/作业/20260928-C2H2-Q4.jpg |
| `corr-20260928-10` | `attempt-9` | `ee.ac.phasor-impedance.exposure` | `None` → `'none'` | subjects/06-电工电子技术/作业/20260928-C2H2-Q123.jpg |
| `corr-20260928-11` | `attempt-9` | `ee.ac.resonance.exposure` | `None` → `'none'` | subjects/06-电工电子技术/作业/20260928-C2H2-Q5.jpg |
| `corr-20260928-12` | `attempt-8` | `ee.ac.phasor-impedance.note` | `'Q2：U = 311/√2（=220 V）、f = ω/(2π) = 314/(2π)（=50 Hz）、220 V 是有效值，正确。Q3：|Z| = √(30²+40²) = 50 Ω、φ = 53°、Z = 30+j40 Ω，正确。待确认项：Q3(b) 手写结论只见『电压滞后』字样（[待确认]）；且把 Z = 50∠53° 写成 U̇ = Z·İ 的结果，漏了电流模值 I'` → `'Q2：U = 311/√2（=220 V）、f = ω/(2π)（=50 Hz）、220 V 是有效值，正确。Q3：|Z| = √(30²+40²) = 50 Ω、φ = 53°、Z = 30+j40 Ω，正确。【相位项】学习者 2026-09-28 确认**原稿写的是『电流滞后』**（来源：learner_statement）→ 与 Z = 30+j40（感性）一致，读图歧义消除，不再列为待确认项。【『漏乘电流模值 İ』一项】3× 放大重读该行，`U̇ = Z·İ = 50 İ ∠53°` 中 İ 存在 → 原判据不成立，已由『已判定的写法错误』降级为『待学习者逐字转写确认』，**不据导师辨读改判**。【判定】本目标**不因上述文档层面的澄清而升级**：needs_verify 保持 true，待未见同类题核定。'` | subjects/06-电工电子技术/作业/20260928-diag-Q123.jpg（3× 放大重读：_scratch/improve/ |
| `narr-20260927-01` | —（叙述） | — | — | 2026-09-27 对 attempt-2 的判定订正（原文归档）：该条不改字段，而是确立字段语义 —— 学习者 20… |
| `narr-20260928-01` | —（叙述） | — | — | 【旧结论作废声明】learning/attempts/corrections.md 在 2026-09-28 曾写过一条… |
| `narr-20260928-02` | —（叙述） | — | — | 记录规则（写给自己）：①结论正确 ≠ 推导正确 ≠ 独立完成，三者分开记；②反馈里展示过的内容即曝光，如实标注，曝光后照… |
| `corr-20260928-13` | `attempt-12` | `diagnosis_status` | `'pending_probe'` → `'confirmed'` | 会话 2026-09-28 学习者原话：『6我看错了，4我大致搞明白，你的答案是正确的』 |
| `corr-20260928-14` | `attempt-12` | `error_hypothesis` | `'两处错，性质不同：①Q4 把 Q3 刚刚用对的『大小写自洽』规则丢了，改按『符号像不像电感』筛选项（A 含 X_L 看着最电感，但 X_L = ωL 本是同一个量，区分点在大小写）——同卷内规则未迁移；②Q6 与当日诊断（attempt-8）的 Q5 是同一物理、换了表征（电路图 + 灯亮度），当日复现失败：诊断时答『I_R 不变、I_L 变小、I_C 变大』完全正确，这次却答 C。是表征迁移失败、看错支路、还是把 X_L↑ 当成 I↑，待学习者从 (a)-(d) 分辨'` → `'两处错因已定位（学习者 2026-09-28 答复后）：①Q4 = **记号规则未在同一份卷内迁移**——Q3 已按『大小写自洽』选对 B，Q4 却改按『符号像不像电感』选 A（A 含 X_L 看着最电感，但 X_L = ωL 本是同一个量，区分点只在大小写；正确为 C：I = U/(ωL)）；②Q6 = **读图错误**（原话『6我看错了』）——把灯 B、灯 C 各在哪条并联支路看反，**不是概念错误**：当日诊断（attempt-8 的 Q5）同一物理『I_R 不变、I_L 变小、I_C 变大』答得完全正确。结论：本卷两处错均**无概念缺口**，暴露的是两个独立环节——Q4 是『规则跨题迁移』，Q6 是『读电路图』'` | 会话 2026-09-28 学习者答复；照片 subjects/06-电工电子技术/作业/C2H1/微信图片_20260923151825_ |
| `corr-20260928-15` | `attempt-14` | `tm.t4.energy-criteria.note` | `'题1（传送带 T = ½m(ẋ+v₀)²）：T₂ = ½mẋ²、T₁ = m v₀ ẋ、T₀ = ½m v₀² —— **三项全对**，首次独立分出非零 T₁（提示级别 H2：导师已说明『展开成三项』并点名三个标签）。题2（移动悬点单摆）：三项 T 全对，且正确认出『L 里的加号项来自 U』，但把 U 写成 +mgl cosθ（正确为 −mgl cosθ，题面已给）——L = T − U，从 L 反推 U 要变号。属 state/mistakes.md『系数与正负号』条目现场复现。另：学习者主动提出 T₁ 在 E 中被消掉 vs 在 E−(T+U) 中出现的疑问，属对判据二结构的深层追问'` → `'题1（传送带 T = ½m(ẋ+v₀)²）：T₂ = ½mẋ²、T₁ = m v₀ ẋ、T₀ = ½m v₀² —— **三项全对**，首次独立分出非零 T₁（提示级别 H2：导师已说明『展开成三项』并点名三个标签）。题2（移动悬点单摆）：三项 T 全对，U 亦正确 —— **学习者 2026-09-28 澄清原意：『U 提供负号中和了那一项本身的负号』，即 −U = +mgl cosθ ⟹ U = −mgl cosθ，理解正确**。导师先前的『U 符号错』判定系对压缩答语（『展开式每项顺序对应』）的误读，已由 corr-20260928-15/16 撤销。另：学习者主动提出『T₁ 在 E 中被消掉，为何仍影响 E≠T+U』，并自行用 T+U 与 E 相减验证 —— 属对判据二结构的深层追问。'` | 会话 2026-09-28 学习者原话：『不是那个势能函数你理解错我的意思了，我就是说 U 提供负号中和了那一项本身的负号』 |
| `corr-20260928-16` | `attempt-14` | `error_hypothesis` | `'两类：①**符号类**（U 从 L 反推未变号）——与学习者自述『对系数包括正负处理非常不敏感』完全吻合，且是**结构性符号之外的搬运型符号错**，正是 mistakes.md 里那条待练的弱点；②**无概念缺口**（T₂/T₁/T₀ 分解与『哪一项来自 U』的判断都对）。剩余待补：写出 E 并与 T+U 相减，验证 E−(T+U) = −(T₁+2T₀)'` → `'**本事件无错答**。传送带与移动悬点单摆两个新系统上，T₂/T₁/T₀ 与 U 全部正确（含首次独立分出非零 T₁）。导师先前的『U 从 L 反推未变号』判定系误读学习者压缩答语，已撤销（见 corrections.jsonl 的 corr-20260928-15/16），**该条不再计入 state/mistakes.md 的『系数与正负号』证据**。学习者本次实际做到：①在新系统上独立完成三块分解；②主动追问并自行验证 `E − (T+U) = −(T₁ + 2T₀)`。**剩余**：判据二已有同日补讲证据，但缺『过几天的无提示未见变式』→ hurdle-1 转 awaiting_retest，尚不得关闭。'` | 会话 2026-09-28 学习者澄清；corrections.jsonl corr-20260928-15 |
| `corr-20260928-17` | `attempt-5` | `tm.t4.energy-criteria.exposure` | `None` → `'partial'` | 旧窗口日志 old.jsonl seq1017（H4.1 反馈：判据二讲解 + 套用结论）、seq2257（齐次次数课：2T₂+T₁、E=T |
| `corr-20260928-18` | `attempt-5` | `tm.t4.energy-criteria.exposure_timing` | `None` → `'before_attempt'` | 旧窗口日志 old.jsonl seq1017 / seq2257（均早于 attempt-5 的 ts 2026-09-28） |
| `corr-20260928-19` | `attempt-5` | `solution_exposure` | `'none'` → `'partial'` | learning/corrections.jsonl corr-20260928-17 |
| `corr-20260928-20` | `attempt-5` | `tm.t4.energy-criteria.note` | `'判据二首次独立通过：对 H4.1 的 L 独立答出广义速度是 ẋ、T 只有二次项故 T₂=mẋ²/2 且 T₁=T₀=0、依据是位置不显含 t（约束没动）。三点全对，无提示（H0）、无答案曝光。保留项：学习者同时声明『其实我不知道什么是约束』——结论对但前置概念未建立，故 needs_verify=true，需换一个约束在动的系统复测'` → `'【曝光史订正 2026-09-28，原写『无答案曝光』作废】旧窗口在同一目标上早已讲解并套用过：seq1017 给出『判据二：T = T₂ 且 T₁ = T₀ = 0 → 欧拉定理 → E = T+U』并逐条套用 H4.1 的 L 得出结论；seq2257 整节讲『齐次次数』，给出 Σq̇∂T/∂q̇ = 2T₂ + T₁、E = T₂ − T₀ + U、E = T+U ⟺ T₁ = T₀ = 0。本次作答内容（广义速度是 ẋ、T₂ = mẋ²/2、T₁ = T₀ = 0、依据位置不显含 t）正是这套算法套到 H4.1 的结果 → 属**已曝光后复现**，exposure = partial @ before_attempt，**不计独立通过**。本次过程本身确实没有追加提示（hint_level 仍为 0，如实保留）。保留项不变：学习者同时声明『其实我不知道什么是约束』——结论对但前置概念未建立，needs_verify 保持 true，需换一个约束在动的系统复测。⚠ 边界：本条只针对**同一目标、同一题**的历史讲解；不因『学过判据二这个方法』就把**其他新题**一并判为已曝光'` | 旧窗口日志 old.jsonl seq1017 / seq2257 |
| `corr-20260928-21` | `attempt-9` | `ee.ac.resonance.exposure` | `'none'` → `'partial'` | 会话 bb092a33 seq429（提示原文）/ seq436（提交原文）；corr-20260928-11 的 exposure=non |
| `corr-20260928-22` | `attempt-9` | `ee.ac.resonance.exposure_timing` | `None` → `'unknown'` | 会话 bb092a33 seq423（我在做第五题）/ seq429（提示）/ seq436（提交） |
| `corr-20260928-23` | `attempt-9` | `ee.ac.resonance.needs_verify` | `False` → `True` | learning/corrections.jsonl corr-20260928-21 / corr-20260928-22 |
| `corr-20260928-24` | `attempt-9` | `ee.ac.resonance.note` | `'Q5(1)：同相 ⟹ 谐振 ⟹ R = U/I = 100 Ω；İ = 1∠0° ⟹ U̇_C = −j180 V、U̇_C + U̇_L = 0 ⟹ X_C = X_L = 180 Ω。全对，独立完成。Q5(2)：X_L′ = 2X_L = 360 Ω、X_C′ = ½X_C = 90 Ω、判定感性，数值与结论全对；但把阻抗 Z′ = R + j(X_L′−X_C′) = 100 + j270 Ω 写成 U̇ = 100 + j270 V（量名与单位错）'` → `'Q5(1)：同相 ⟹ 谐振 ⟹ R = U/I = 100 Ω；İ = 1∠0° ⟹ U̇_C = −j180 V、U̇_C + U̇_L = 0 ⟹ X_C = X_L = 180 Ω。**答案与列式正确，予以保留**。⚠ **独立性待确认（2026-09-28 订正）**：已核实 seq429 在提交（seq436）**之前**提示『它是这套里唯一考“同相⇒谐振”的题』，判据链关键一环在提交前已给出 → 原记『全对，独立完成』不成立。但提交 ≠ 完成，无法判定提示落在作答的哪个阶段 → 按约定**不猜**：exposure = partial、exposure_timing = unknown、needs_verify = true，**本次不贡献独立通过**。Q5(2)：X_L′ = 360 Ω、X_C′ = 90 Ω、判定感性，数值与结论全对（书写项：把 Z′ = 100 + j270 Ω 写成 U̇ = … V）。补独立证据：用**未见同类题**复测。⚠ 与本卷其他目标**不连带**：ee.ac.reactance / ee.ac.phasor-impedance / ee.ac.series-rlc 不受本条影响'` | 会话 bb092a33 seq423 / seq429 / seq436 |
| `narr-20260928-03` | —（叙述） | — | — | 【证据依据降级声明 + 规则】corr-20260928-09/10/11 用**作业照片**推断『该目标未获代算或展示… |
| `narr-20260929-01` | —（叙述） | — | — | 【attempt-18 两处澄清 · 学习者 2026-09-29 答复】学习者原话：「那两点如实说明，我自己做的，我也… |
| `corr-20260930-01` | `attempt-28` | `mode` | `'quiz'` → `'practice'` | session-a46ca69d-4e69-4836-b718-8ac24b5ff8f1 seq387（导师消息，早于 seq394 提交） |
| `corr-20260930-02` | `attempt-28` | `max_hint_level` | `0` → `2` | session-a46ca69d-4e69-4836-b718-8ac24b5ff8f1 seq387（导师消息，早于 seq394 提交） |
| `corr-20260930-03` | `attempt-28` | `solution_exposure` | `'none'` → `'partial'` | session-a46ca69d-4e69-4836-b718-8ac24b5ff8f1 seq387（导师消息，早于 seq394 提交） |
| `corr-20260930-04` | `attempt-28` | `exposure_timing` | `None` → `'before_attempt'` | session-a46ca69d-4e69-4836-b718-8ac24b5ff8f1 seq387（导师消息，早于 seq394 提交） |
| `corr-20260930-05` | `attempt-28` | `mp.isolated-singularity.note` | `'**教学后检验（同日）**：H0（只给题意、全程无方法提示）、**完全闭卷**（学习者原话『完全闭卷』）。五个函数**均未在本次教学中出现过** → 本题此前从未作答，kind=mixed，符合「未见变式」定义；⚠ 但属**同日教学后检验**，**不构成延迟证据**（`policy.yml` `min_delay_days: 2`）。【逐题】1 `z/(e^z − 1)` →『可去』**✅**；2 `(e^z − 1)/z²` →『一阶极点』**✅**；3 `1/(z³(e^z − 1))` →『本性极点』**❌**（正确 **四阶极点**：e^z − 1 = z(1 + z/2 + …) ⟹ 分母 = z⁴(1 + z/2 + …) ⟹ 负幂项 z⁻⁴…z⁻¹ 有限个）；4 `(z − sin z)/z⁵` →『4 阶极点』**❌**（正确 **二阶极点**：z − sin z = z³/3! − z⁵/5! + … ⟹ 分子零点 3 阶 ⟹ 5 − 3 = 2）；5 `cos(1/z)` →『本性极点』**类型判对、术语错**（是**本性奇点**，**没有阶数**；『本性极点』自相矛盾）。【合计】3/5（子项计：1✅ 2✅ 5类型✅ 3❌ 4❌）→ `final=partial`，**目标不升级**。【两个错处的**共同根因（假设）**】凡因子**不是 z 的幂**（`sin z`、`e^z − 1`、`z − sin z`）时，**没有先把它展开到首个非零项**就数零点阶数：#4 直接把 `z − sin z` 当成 1 阶零点（5−1=4）；#3 未展开 `e^z − 1`（展开后分母最低次是 z⁴，四阶极点）。→ `diagnosis_status: pending_probe`，由下一步「把该因子展开到首个非零项」的两步自查确认。【下一步】先补这一个缺口（不是重讲整块），再出一道**换过函数**的同类新题；`mp.isolated-singularity` 保持未通过，第三章**不宣告收口**。'` → `'**订正（2026-09-30 维护）**：原记「H0 + 无曝光」不成立。原始会话 seq387（导师消息）在学习者提交（seq394）**之前**已点名第 4 题的方法方向：「第 4 题是主陷阱：**必须把分子展开到首个非零项**」；同一消息还把含全部五题答案的任务文件路径告诉了学习者。故本事件订正为 `mode=practice`、`max_hint_level=2`、`exposure=partial@before_attempt`（订正见 corrections.jsonl corr-20260930-01～04）。→ **本次不计独立通过、不升级**（原本也不升级：结果只到 partial）。【保留原判读，不作废】逐题结果（3/5）、两处失分、`z − sin z` 被当成 1 阶零点、`e^z − 1` 未展开 —— 这些**都成立**，但「**根因已确认**」这一层**不成立**：提示只点名了第 4 题，学习者仍把第 3 题答成『本性极点』（同一动作在**未被点名的题**上没有自发执行）→ 缺口性质仍是**假设**（见 attempt-29 的订正与 narrative 条目）。'` | session-a46ca69d-4e69-4836-b718-8ac24b5ff8f1 seq387（导师消息，早于 seq394 提交） |
| `corr-20260930-06` | `attempt-29` | `diagnosis_status` | `'confirmed'` → `'pending_probe'` | session-a46ca69d-4e69-4836-b718-8ac24b5ff8f1 seq387（导师消息，早于 seq394 提交） |
| `corr-20260930-07` | `attempt-29` | `mp.isolated-singularity.note` | `'**定向修复（`attempt-28` 之后的补漏步）**。导师先给出策略方向（H2：『数任何因子的零点阶数前，先把非幂因子展开到首个非零项』），随后两个小问由学习者作答：①`e^z − 1` 在 0 是**一阶零点** ✅；②`z − sin z` 在 0 是**三阶零点** ✅（两步全对）。由此 `attempt-28` 的两处失分**机械地**得出正确答案：第 3 题分母阶数 = 3 + 1 = 4 → **四阶极点**（原答『本性』）；第 4 题 5 − 3 = 2 → **二阶极点**（原答『4 阶』）。【判定】本次为**带提示（H2）的修复**：`max_hint_level=2` + `needs_verify=true` + 曝光 partial@before_attempt（策略由导师先给）→ **不计独立通过、不升级**；`attempt-28` 暴露的缺口机制（未展开到首个非零项）由此**确认**（此前为 `pending_probe`）。【下一步】`mp1-ch3-sing-03`（四个**全部换过**的函数；H0、闭卷）作修复后检验；⚠ 仍为同日 → 通过亦**不构成延迟证据**。'` → `'**订正（2026-09-30 维护）**：`diagnosis_status` 由 `confirmed` 改为 `pending_probe`。该字段原本依赖的前提是『学习者不知道第 4 题要展开到首个非零项』——而 attempt-28 订正后已知该提示在作答前已给出，因此本次两步全对**首先是提示起作用**，不能当作缺口机制被独立确认。【仍然成立的】① 本次是**带提示（H2）的修复**，不计独立通过（原本就是这样记的）；② 『未展开到首个非零项』这条机制**假说**已由后续证据支持：`attempt-30`（H0、闭卷、换过函数）第 3 题把 `ln(1+z) − z` 答成『一阶极点』（正确：可去，z 项相消），与 attempt-28 第 4 题同型 → 该假说**成立但尚未在无提示条件下被单独验证**。'` | session-a46ca69d-4e69-4836-b718-8ac24b5ff8f1 seq387（导师消息，早于 seq394 提交） |
| `narr-20260930-01` | —（叙述） | — | — | 【订正 2026-09-30】作废「`attempt-28` 暴露的缺口机制已由 `attempt-29` 确认」这一结… |
| `corr-20260930-08` | `attempt-28` | `mp.isolated-singularity.hint_level` | `0` → `2` | session-a46ca69d-4e69-4836-b718-8ac24b5ff8f1 seq387（导师消息，早于 seq394 提交） |
| `corr-20260930-09` | `attempt-28` | `mp.isolated-singularity.exposure` | `'none'` → `'partial'` | session-a46ca69d-4e69-4836-b718-8ac24b5ff8f1 seq387（导师消息，早于 seq394 提交） |
| `corr-20260930-10` | `attempt-28` | `mp.isolated-singularity.exposure_timing` | `None` → `'before_attempt'` | session-a46ca69d-4e69-4836-b718-8ac24b5ff8f1 seq387（导师消息，早于 seq394 提交） |
| `corr-20260930-11` | `attempt-32` | `error_hypothesis` | `'**单一概念混淆**：把「空间均匀性 → 动量」与「时间均匀性 → 能量」两条对称性对调（Topic 4 的骨架是三条：时间均匀↔能量、空间均匀↔动量、空间各向同性↔角动量）。机制层（整体平移 ⟹ δL = 0）方向正确，缺的只是两处：①把对称性名字说对；②从 δL = 0 用**拉格朗日方程**推到 `d/dt Σ∂L/∂v⃗ₐ = 0`。第③问属「知道要看 L 对坐标的依赖，但没形成判据」。已由学习者原话直接确认，无需再猜。'` → `'**【2026-09-30 订正】原诊断「把空间均匀性说成了时间均匀性」不成立** —— 学习者说明第二遍作答系**口误**，第一遍写的正是「**空间的均匀性**」（正确）。因此 Q1 的**真实缺口只剩一步**：从 `δL = 0` 未用拉格朗日方程推到 `d/dt Σ∂L/∂v⃗ₐ = 0`（守恒量那一步）。Q2 基本正确（`P⃗ = Σp⃗ₐ`、推广为广义动量）；Q3 方向对但未落到判据（`n⃗·F⃗ = 0` / `∂U/∂该方向 = 0` / `∂L/∂该坐标 = 0`，即**循环坐标**）。'` | 学习者 2026-09-30 原话「是我不小心写错了，我第一遍写对的」；本会话第一轮作答原文 |
| `corr-20260930-12` | `attempt-32` | `tm.t4.cyclic-momentum.note` | `'**Topic 4 ③动量守恒（空间均匀性）首次诊断**（教学式；三问）。学习者两轮作答，第二轮为准（原话）：「1因为时间的均匀性，在足够小位移下拉格朗日量对广义坐标变化为零；2凭什么？因为这个形式的简化是动量啊，我们把这个拓展为广义动量；3对不同坐标的拉氏函数的时间导数情况不一样」。【逐问】①**机制方向对、对称性说反**：把这一节该用的**空间均匀性**说成了**时间均匀性**（后者是 p6–12 的**能量**那条）；「整体平移/坐标变化 ⟹ δL = 0」这半句是对的，但**没有走到守恒量**（缺用拉格朗日方程得 `d/dt Σ∂L/∂v⃗ₐ = 0` 这一步）。②**基本正确**：说到「这个形式简化下来就是动量，并推广为广义动量」——对应课件 p15 给的第③条理由（`P⃗ = Σp⃗ₐ`）与 Topic 3 的 `pᵢ = ∂L/∂q̇ᵢ`。③**方向对、判据没落地**：只说到「拉氏函数对不同坐标的依赖/导数不一样」，未给出判据（`n⃗·F⃗ = 0` 或等价地 `∂U/∂该方向 = 0`、`∂L/∂该坐标 = 0`），也未点名**循环坐标**。【帮助史（如实记）】导师在出诊断题的同一条消息里**指了含答案的文件路径**（`learning/tasks/tm-t4-momentum-01.md`，含核验要点），故按工作区口径记 `solution_exposure=partial` + `exposure_timing=before_attempt`；chat 内未给任何方法提示 → `max_hint_level=0`。⚠ **教学教训（本人）**：出诊断/测验时**不要把含答案的文件路径写给学习者**——这会污染曝光史（同一模式在 `attempt-28` 上也发生过并已被订正）。'` → `'**Topic 4 ③动量守恒（空间均匀性）首次诊断**（教学式；三问；以**第一轮**作答为准 —— 第二轮的 Q1 系口误，见 event 级 `error_hypothesis` 的订正）。【逐问】①**对称性说对**（空间的均匀性）、机制方向对（足够小的整体平移下 L 不变 ⟹ `δL = 0`），但**没有走到守恒量**：缺用拉格朗日方程得 `d/dt Σ∂L/∂v⃗ₐ = 0` 这一步。②**基本正确**：『这个形式简化下来就是动量，并推广为广义动量』↔ 课件 p15 第③条理由（`P⃗ = Σp⃗ₐ`）与 Topic 3 的 `pᵢ = ∂L/∂q̇ᵢ`。③**方向对、判据未落地**：只说到『L 对不同坐标的依赖不一样』，未给出 `n⃗·F⃗ = 0` / `∂U/∂该方向 = 0` / `∂L/∂该坐标 = 0`，也未点名**循环坐标**——学习者随即明确要求**先解决循环坐标这个考点**。【帮助史（如实记）】出题的同一条消息里指了**含答案的文件路径**（`learning/tasks/tm-t4-momentum-01.md`）→ `solution_exposure=partial` + `exposure_timing=before_attempt`；chat 内未给方法提示 → `max_hint_level=0`。⚠ **教训**：出诊断/测验题时**不要把含答案的文件路径写给学习者**（同型失误在 `attempt-28` 已被订正一次）。'` | 同上：学习者澄清（learner_statement）+ 本会话第一轮作答原文 |
| `corr-20261003-01` | `attempt-38` | `error_hypothesis` | `'**单一根因：提出因子时少提一个 z**。`1/(z²(z+1))` 在 `|z|>1` 应写成 `(1/z³)·1/(1+1/z)`；学习者写成 `z^{−2}·1/(1+1/z)`，丢掉了把 `1/(z+1)` 化为 `(1/z)·1/(1+1/z)` 的那一个 `1/z`，导致通项整体差一个 `z`。**证据**：①两处指数（`z^{−2}` 与 `z^{−n−2}`）放大读数一致；②数值自检 `z = 2` 差 2 倍。**与历史的关系**：同属 hurdle-2『末步打包/因子』家族但**形态不同**——`attempt-19` 是「提出来的因子没乘回」，本次是「提出来的因子指数没数对」；而同一次提交里的 A2（提出 `(1/z)` 后乘回）**反而做对**，说明不是全面失能，而是**在分母含 `z` 的更高次幂时会漏算一次**。'` → `'**单一根因：提出因子时少提一个 z**。`1/(z²(z+1))` 在 `|z|>1` 应写成 `(1/z³)·1/(1+1/z)`；学习者写成 `z^{−2}·1/(1+1/z)`，丢掉了把 `1/(z+1)` 化为 `(1/z)·1/(1+1/z)` 的那一个 `1/z`，导致通项整体差一个 `z`。**证据**：①两处指数（`z^{−2}` 与 `z^{−n−2}`）放大读数一致；②数值自检 `z = 2` 差 2 倍。**与历史的关系**：同属 hurdle-2『末步打包/因子』家族但**形态不同**——`attempt-19` 是「提出来的因子没乘回」，本次是「提出来的因子指数没数对」；而同一次提交里的 A2（提出 `(1/z)` 后乘回）**反而做对**，说明不是全面失能，而是**在分母含 `z` 的更高次幂时会漏算一次**。\n\n【学习者自述，2026-10-03，来源＝本会话】B2 的缺口『不是知识点问题，只是计算时少提了一个系数』，并明确表示不再重写该行（已尊重其意愿，不再要求）。**因此该缺口的性质按学习者的自述记为执行/计算层面，不作为概念缺口重复讲解或再测**；批改时给出的『指数数对』提示与数值自查法（代 z=2）仍保留，供其自行取用。'` | 本会话 2026-10-03 学习者原话：B那个完全不是知识点问题，只是因为我的计算问题，少提出了一个系数，我拒绝再写一遍，没有意义 |
| `corr-20261004-ielts-audit-01` | `attempt-41` | `en.write.tr.note` | `"**Task 2 基线（首个观测值）· 分档 TR 5.5**。原稿存档 `subjects/11-英语-雅思/写作/20261004-Task2基线-原始稿.md`（一字未改）。【硬事实】**词数 224 < 250 下限**（按字母词计；11 句、5 段）。【符合 Band 6 的一面】prompt 的主要部分被触及、有明确立场（引言 'I strongly agree'）、理由相关（环境、交通）；对应官方 Band 6 原文 'The main parts of the prompt are addressed... A position is presented that is directly relevant to the prompt'。【低于 Band 6 的一面】①**无一处例子**——题面明确要求 'include any relevant examples'，全文零例证，对应 Band 6 'some supporting arguments and evidence may be less relevant or inadequate'，实际是 evidence 完全缺失；②**'to what extent' 从未展开**——没有反方、没有程度限定，结论段（第 5 段）变成口号；③**第 4–5 段漂移为『建议』**（'the most effective way...'、'It's high time for us to...'），不再回答『同意到什么程度』；④underlength —— 官方 Band 5.5 示例正是栽在未达下限。【仍待补】学习者未报『实际用时』与『是否查过任何东西』（已追问）；未补报前污染标记记为**未提供**。"` → `'2026-10-04审查订正：224词<250事实保留；I strongly agree已说明同意程度，无反方段不自动构成缺答。原堵车段有相关观察，不能称evidence完全为零；需补的是观察与限制汽车/替代交通的因果联系，并解释对international laws的立场。旧TR5.5由错误规则支撑，撤回作比较/提分依据，当前TR待重新校准。四段、TEEL和每段一个具体案例非官方规则。正式用时未知；默认闭卷约定继续沿用，不把未报查词自动记未知曝光。needs_verify=true保留，非正式成绩或独立通过。'` | subjects/11-英语-雅思/审查与修订-20261004.md；session-f5a6497d seq745/834/874/89 |
| `corr-20261004-ielts-audit-02` | `attempt-41` | `en.write.cc.note` | `"**Task 2 基线 · 分档 CC 6.0**。【符合 Band 6】分段合理（5 段，各段一个中心）、整体推进可见（环境 → 交通 → 对策 → 结论）；对应官方 Band 6 'Information and ideas are generally arranged coherently and there is a clear overall progression'。【符合 Band 6 的负面项】衔接手段**机械化**：句首 'And' 连用 3 次（'And this kind of pollution...'、'And the government...'、'And just return to...'）、'So' 起句、'From the environment protection angle'（生硬且搭配不自然）；对应官方 Band 6 'cohesion within and/or between sentences may be faulty or mechanical due to misuse, overuse or omission'。【另】第 1 段末尾 'Reasons are written below.' 属**元话语**，不是有效衔接；第 3 段存在逗号粘连（'..., it's just a waste of time and our environment'）。"` → `'2026-10-04审查订正：全文五段，有环境、拥堵和对策的总体顺序；内容有重复、衔接与论证关系需要说明。句首And/So本身不是错误，也不按次数扣分。Reasons are written below冗余，但不能仅由该句定档；逗号粘连是实际标点问题。旧CC6.0仅保留为历史机评参考，未校准，不据此宣称正式水平。'` | subjects/11-英语-雅思/审查与修订-20261004.md；session-f5a6497d seq745/834/874/89 |
| `corr-20261004-ielts-audit-03` | `attempt-41` | `en.write.lr.note` | `"**Task 2 基线 · 分档 LR 5.5**。【范围】中等偏窄且重复：pollution×5、environment×4、car×5、legislation×3。【高频错误】①搭配／词形：'build legislation system'（应为 a legal system / legislation）、'conduct the car production and ownership legislation'、'curb the pollution level in a limited range'（语义不清）、'green travelling'（非标准）、'persist on improving'（应为 persist in / insist on）、'the situation we confront with'（应为 face）；②**'as more as possible'**（应为 as much as possible）；③拼写 'bycicles'（bicycles）；④'less people'（应为 fewer people）；⑤'take actions'（action 不可数）。【判读】多数错误不阻断理解 → 未落入 Band 5 'may impede meaning'；但频率与搭配问题明确高于 Band 6 的 'occasional inaccuracies'。"` → `'2026-10-04审查订正：build legislation system等搭配不自然，as more as possible、bycicles、persist on improving、the situation we confront with需要修正；这里less people通常用fewer people。不要把green travelling说成绝对不能用，需看语域/自然度；take action适合这里，但actions在英语其他语境可以成立。未经重新计数的词频数字不沿用。旧LR5.5仅历史参考待校准，非正式分数。'` | subjects/11-英语-雅思/审查与修订-20261004.md；session-f5a6497d seq745/834/874/89 |
| `corr-20261004-ielts-audit-04` | `attempt-41` | `en.write.gra.note` | `"**Task 2 基线 · 分档 GRA 5.0**（四项中最低）。【最高频错误：主谓一致】'pollution come out'、'the government persist on improving'、'traffic jam occurs everyday and in every big cities'（单复数与冠词同时错）、'less people pay attention'。【句子层】①逗号粘连（run-on）：'And this kind of pollution is of no meaning and significance, it's just a waste of time and our environment'；②**Because 起句的残句**：'Because the more cars we permit on the road, the more danger we bring in to...'；③'It's high time for us to take actions'（结构可接受但搭配弱）；④'As a teenager in today's high-technology era'——与论证无关的自我介绍式开头。【判读】简单句基本可控、复杂句尝试了但错误集中：对应官方 Band 5 'Although complex sentences are attempted, they tend to be faulty' 与 Band 5 'grammatical errors are frequent'；未低到 Band 4（多数错误不阻断理解）。【可修性】主谓一致 + 逗号粘连是**规则明确、见效最快**的两项。"` → `'2026-10-04审查订正：pollution come out/the government persist存在主谓一致问题；in every big cities涉及every后单数，traffic jam在此泛指通常需复数；逗号连接两个独立句与Because从属片段是实际句法问题。less people是数量词选择，不是主谓一致；无关自我介绍是任务/语域问题，不充作语法错误。错误不因一次讲解就已修。旧GRA5.0仅历史参考待校准，当前仍需核验。'` | subjects/11-英语-雅思/审查与修订-20261004.md；session-f5a6497d seq745/834/874/89 |
| `corr-20261004-ielts-audit-05` | `attempt-41` | `error_hypothesis` | `"**基线综合分档 ≈ 5.5（TR 5.5 · CC 6.0 · LR 5.5 · GRA 5.0）**，瓶颈按杠杆排序：①**TR 层面『说了但不展开、零例子』**——每段只给主张便转下一段，这是词数不足（224）与 TR 未达 6 的**同一根因**；②**任务回应漂移**：后两段从『同意到什么程度』改成『应该怎么做』，且题面里 'international laws' 这一半完全未触及；③**GRA 高频基础错误**（主谓一致、逗号粘连）。**判读口径**：本次是 Phase 0 起点观测，**不因分低调整目标**（目标由训练计划 §1 定），只用来决定配比；导师给的是估算，非官方分；`needs_verify=true` 本身阻断任何升级。"` → `'2026-10-04审查订正：首份Task2存在政策回应不充分、理由与结论联系不够展开及真实搭配/语法问题。不能从单篇确诊“没话说不是知识问题”，也不能用缺反方、零具体案例或And/So数量解释TR/CC失分。224词事实保留，正式用时未知；旧TR估分及综合5.5不作为提分比较依据，具体瓶颈待局部练习确认。'` | subjects/11-英语-雅思/审查与修订-20261004.md；session-f5a6497d seq745/834/874/89 |
| `corr-20261004-ielts-audit-06` | `attempt-41` | `diagnosis_status` | `'confirmed'` → `'pending_probe'` | subjects/11-英语-雅思/审查与修订-20261004.md；session-f5a6497d seq745/834/874/89 |
| `corr-20261004-ielts-audit-07` | `attempt-42` | `en.write.tr.note` | `"**第 3 段重写（讲授后定向修复，第一次）**，原文 `写作/20261004-Task2基线-第3段重写.md`（83 词）。【做到的两格】①**T（topic sentence）新增**：`From the energy utilization efficiency angle, it's a great loss when we make use of our power.` —— 换到了能源效率这个新角度 ✅；②**收尾句新增**：`So we should take more bus and bicycle to travel around`。【**核心缺口未修：例证仍为零**】重写指令明确要求 1 个具体例证（范围＋具体对象＋结果三件套），提交中**一个例子都没有**；`As we see in the society, traffic jam occurs everyday...` 仍是泛化陈述。【另外两点】①**中间两句原封不动照抄**（与基线稿逐字相同），因此基线已标出的 `pollution come out`、`in every big cities`、逗号粘连**全部留存**——「重写」没有触及语言层；②新起句语义空：`it's a great loss when we make use of our power` 表意不清（消耗能源时的损失？），更像口号；③`take more bus and bicycle` 搭配错（应为 use public transport more and cycle）。【判定】**partial**：结构意识有进步（T、L 出现），但被点名的最高杠杆项（例证）未完成；本次因讲授在先，**不计独立通过**。"` → `'2026-10-04审查订正：83词受助局部重写。新增能源效率开头与建议结尾，但开头意思不清，新增句不自动证明T/L已做好。中间已有相关堵车观察，不能因缺地名/人物判零例证；撤回旧三件套与必须70–90词TEEL的判定依据。当前可观察缺口是未清楚连接少开车与减少无效耗油，不足以确诊不会举例。保留partial、H2、本题partial曝光与needs_verify；当前不是新题独立证据，不追加成绩。'` | subjects/11-英语-雅思/审查与修订-20261004.md；session-f5a6497d seq745/834/874/89 |
| `corr-20261004-ielts-audit-08` | `attempt-42` | `en.write.cc.note` | `"**第 3 段重写 · CC**：段内顺序较基线清楚（角度 → 现象 → 收尾），但第 2、3 句照抄导致句首 `And` 仍出现一次；逗号粘连（`..., it's just a waste of time and our environment`）留存未改。"` → `'2026-10-04审查订正：新增开头和收尾，段内联系仍需说明；同段的逗号粘连留存。句首And出现一次本身不能作为扣分或不连贯依据。不对83词单段硬套完整作文四项分数。'` | subjects/11-英语-雅思/审查与修订-20261004.md；session-f5a6497d seq745/834/874/89 |
| `corr-20261004-ielts-audit-09` | `attempt-42` | `en.write.lr.note` | `'**第 3 段重写 · LR**：新增搭配 `energy utilization efficiency`（可接受但偏术语，非学术写作常用块）；`take more bus and bicycle` **搭配错**；`less people`、`of no meaning and significance`（生硬）留存。**未使用结构讲义中点名的可复用搭配类型**。'` → `'2026-10-04审查订正：take more bus and bicycle不自然，可说use public transport more and cycle；less people在此用fewer people。energy utilization efficiency是否适合取决于实际表达，不强制使用讲义搭配；未用指定词块不是LR不通过理由。of no meaning and significance语义笼统。'` | subjects/11-英语-雅思/审查与修订-20261004.md；session-f5a6497d seq745/834/874/89 |
| `corr-20261004-ielts-audit-10` | `attempt-42` | `en.write.gra.note` | `'**第 3 段重写 · GRA**：基线标出的三处错误**一处未修**——主谓一致 `pollution come out`（应为 comes）、`traffic jam occurs everyday and in every big cities`（every + 复数 cities；应为 in every big city 或 in all big cities）、逗号粘连。新增句本身语法无错。→ **「重写=改语言」这一步没有发生**，这是本次最值得记的一点。'` → `'2026-10-04审查订正：pollution come out、every big cities、逗号粘连仍需修正，这是文本中的语言事实。新增句没有明显结构错误不等于意思清楚；旧记录不能从这次未改语言确诊态度/认知问题，也不默认多项语法都是同一轮重写交付。'` | subjects/11-英语-雅思/审查与修订-20261004.md；session-f5a6497d seq745/834/874/89 |
| `corr-20261004-ielts-audit-11` | `attempt-42` | `error_hypothesis` | `'**两个动作没做，一个是缺技能，一个是漏执行**：①**缺技能**——「把抽象主张具体化成一个场景」仍不会做（需要示范 + 单句练习），这是 TR 的根因；②**漏执行**——被明确点名的三处语法错误在「重写」时被原样保留，说明重写时只看结构、没通读语言。**判读提示**：不要把「照抄中间两句」理解为态度问题；更可能是他把「重写」理解成「在原有段落上加头加尾」。下一次指令要明确：**中间句必须改，或删掉重写**。'` → `'2026-10-04审查订正：旧诊断以已撤回的具体案例三件套为准，不能确诊缺技能或漏执行。可观察到新增开头/结尾但意思和因果联系仍不清楚，原稿若干语言错误留存。助手指令本身同时要求模板、案例、字数和三处语法，增加注意力负担。下一步只解释并改一句联系，不要求查政策、补案例或重复整段。'` | subjects/11-英语-雅思/审查与修订-20261004.md；session-f5a6497d seq745/834/874/89 |
| `corr-20261004-ielts-audit-12` | `attempt-42` | `diagnosis_status` | `'confirmed'` → `'pending_probe'` | subjects/11-英语-雅思/审查与修订-20261004.md；session-f5a6497d seq745/834/874/89 |

## ⑦ 困难观察（没有作答的「不会/不理解」，不伪装成做错的题）

| 困难 | 状态 | 目标 | 观察到 | 证据 |
|---|---|---|---|---|
| `hurdle-1` | verified | tm.t4.energy-criteria | 2026-09-26 | eval/会话原文-20260926.md；state/mistakes.md 同条记录；subjects/01-理论力 |
| `hurdle-2` | awaiting_retest | mp.taylor-expansion, mp.laurent-expansion | 2026-09-28 | 会话 2026-09-28（学习者原话：『我不会😭』）；相关任务 learning/tasks/mp1-ch3-hw-0 |
| `hurdle-3` | teaching | ru.qword-agreement | 2026-09-30 | 讲法见 subjects/07-俄语/topics/topic-02-疑问词какой在问什么.md；对照证据＝atte |
| `hurdle-4` | teaching | tm.t5.effective-potential, tm.t5.central-motion-types | 2026-10-19 | attempt-52（tm-t5-ueff-variant-01，partial）＋ 2026-10-19 会话内口头自 |

## ⑧ 题目清单（`learning/tasks/`）

| 题目 | 课程 | 类别 | 状态 | 目标 | 截止 |
|---|---|---|---|---|---|
| `ai-tech-c00-01-env-check` | — | baseline | open | ai-tech.c00-01 | — |
| `de-gap-attack-01` | — | practice | done | ode.homogeneous, ode.order-reduction, ode.clairaut | 2026-10-15 |
| `de-midterm-diag-01` | — | mixed | open | ode.separable, ode.homogeneous, ode.exact-integ factor, ode.first-order-linear, ode.riccati, ode.clairaut, ode.order-reduction, ode.const-coeff-homogeneous, ode.undetermined-coefficients | 2026-10-15 |
| `ee-c2-diag-01` | — | baseline | done | ee.ac.reactance, ee.ac.phasor-impedance, ee.ac.series-rlc, ee.ac.resonance | 2026-09-28 |
| `ee-c2h1-01` | — | practice | done | ee.ac.reactance, ee.ac.phasor-impedance, ee.ac.series-rlc | 2026-09-28 |
| `ee-c2h2-01` | — | practice | done | ee.ac.reactance, ee.ac.phasor-impedance, ee.ac.series-rlc, ee.ac.resonance | — |
| `ee-lab1-prep-01` | — | practice | open | ee.dc.kcl, ee.dc.steady-state, ee.dc.source-vs-load, ee.ac.series-rlc, ee.ac.resonance | 2026-09-29 |
| `ee-lab1-report-01` | — | practice | done | ee.dc.kcl, ee.dc.steady-state, ee.dc.source-vs-load, ee.ac.series-rlc, ee.ac.resonance | 2026-09-29 |
| `ee-variant-01` | — | mixed | open | ee.dc.kcl, ee.dc.steady-state, ee.dc.source-vs-load, ee.ac.reactance, ee.ac.phasor-impedance, ee.ac.series-rlc, ee.ac.resonance | 2026-09-30 |
| `en-write-t2-baseline-01` | — | baseline | open | en.write.tr, en.write.cc, en.write.lr, en.write.gra | — |
| `en-write-t2-fix-01` | — | practice | open | en.write.tr, en.write.cc, en.write.lr, en.write.gra | — |
| `en-write-t2-variant-01` | — | delayed-variant | open | en.write.tr, en.write.cc, en.write.lr, en.write.gra | — |
| `mp1-ch3-hw-01` | — | worked-example | done | mp.power-series-radius, mp.taylor-expansion, mp.laurent-expansion, mp.isolated-singularity | 2026-09-28 |
| `mp1-ch3-quiz-01` | — | practice | open | mp.power-series-radius, mp.taylor-expansion, mp.laurent-expansion, mp.isolated-singularity | 2026-09-28 |
| `mp1-ch3-sing-01` | — | practice | open | mp.isolated-singularity | 2026-09-30 |
| `mp1-ch3-sing-02` | — | mixed | open | mp.isolated-singularity | 2026-09-30 |
| `mp1-ch3-sing-03` | — | mixed | open | mp.isolated-singularity | 2026-09-30 |
| `mp1-ch3-sing-04` | — | practice | done | mp.isolated-singularity | 2026-10-03 |
| `mp1-ch3-variant-01` | — | delayed-variant | done | mp.laurent-expansion, mp.taylor-expansion, mp.power-series-radius | 2026-10-02 |
| `mp1-ch3-variant-02` | — | delayed-variant | done | mp.isolated-singularity | 2026-10-02 |
| `mp1-ch4-hw-01` | — | practice | open | mp.residue-definition, mp.residue-computation, mp.residue-applications | 2026-10-09 |
| `mp1-ch4-quiz-01` | — | mixed | open | mp.residue-definition, mp.residue-computation, mp.residue-applications | 2026-10-01 |
| `mp1-ch4-residue-01` | — | practice | open | mp.residue-definition, mp.residue-computation, mp.residue-applications | — |
| `mp1-ch5-hw-01` | — | practice | open | mp.fourier-series, mp.fourier-transform, mp.delta-function | 2026-10-16 |
| `mp1-ch6-hw-01` | — | practice | open | mp.laplace-transform, mp.laplace-inverse, mp.laplace-ode | 2026-10-16 |
| `ode-if-baseline-01` | — | baseline | open | ode.integrating-factor | — |
| `ode-l15-hw-01` | — | practice | open | ode.sys.eigen-basic, ode.sys.case-complex, ode.sys.case-repeated | 2026-10-18 |
| `ode-l16-hw-01` | — | practice | open | ode.sys.matrix-exp, ode.sys.cayley-hamilton | null |
| `ode-sys-hw-01` | — | practice | open | ode.system-reduction | 2026-09-28 |
| `ru-adj-qword-01` | — | delayed-variant | done | ru.noun-gender, ru.qword-agreement | 2026-10-02 |
| `ru-hw-02` | — | practice | open | ru.adj-agreement, ru.noun-gender, ru.noun-forms | 2026-10-09 |
| `ru-hw-04` | — | practice | open | ru.verb.znat-dumat, ru.syntax.chto-clause, ru.syntax.potomy-chto, ru.qword.kakoy-agreement | null |
| `ru-level-check-01` | — | baseline | open | ru.noun-gender, ru.qword-agreement | 2026-10-13 |
| `ru-noun-gender-fix-01` | — | delayed-variant | open | ru.noun-gender | 2026-10-02 |
| `ru-plural-01` | — | practice | open | ru.noun-forms | 2026-10-13 |
| `ru-qword-meaning-01` | — | delayed-variant | open | ru.qword-agreement | 2026-10-02 |
| `tm-h4-01` | — | practice | open | tm.t4.energy-integral, tm.t4.energy-criteria, tm.t4.direct-check | 2026-09-27 |
| `tm-h4-01-fix-01` | — | practice | done | tm.t4.direct-check | 2026-09-27 |
| `tm-h4-03` | — | practice | done | tm.t4.energy-integral, tm.t4.cyclic-momentum, tm.t4.direct-check | 2026-09-28 |
| `tm-h5-01` | — | practice | open | tm.t5.potential-analysis, tm.t5.turning-points, tm.t5.law-of-motion | 2026-10-15 |
| `tm-h5-02` | — | practice | open | tm.t5.effective-potential, tm.t5.central-motion-types | — |
| `tm-t4-angular-momentum-01` | — | mixed | blocked | tm.t4.angular-momentum-integral | 2026-09-30 |
| `tm-t4-criteria-01` | — | mixed | open | tm.t4.energy-criteria, tm.t4.energy-integral, tm.t4.direct-check | — |
| `tm-t4-criteria-02` | — | practice | open | tm.t4.energy-criteria | — |
| `tm-t4-criteria-03` | — | practice | open | tm.t4.energy-criteria | 2026-09-28 |
| `tm-t4-criteria-04` | — | mixed | open | tm.t4.energy-criteria | 2026-09-29 |
| `tm-t4-diag-01` | — | baseline | open | tm.t3.lagrangian-construction, tm.t4.cyclic-momentum | — |
| `tm-t4-momentum-01` | — | mixed | open | tm.t4.cyclic-momentum | 2026-09-30 |
| `tm-t4-similarity-01` | — | mixed | open | tm.t4.mechanical-similarity | 2026-09-30 |
| `tm-t5-ueff-variant-01` | — | practice | open | tm.t5.effective-potential, tm.t5.central-motion-types, tm.t5.turning-points | — |
| `xz-2026f-course-selection` | — | practice | done | — | 2026-10-10 17:00 |

（题目 51 道；作答事件 52 条；以上均由脚本重算，不含手写内容。）
