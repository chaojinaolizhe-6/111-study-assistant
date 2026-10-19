# 当前续学入口（CURRENT）

> ✅ **这是唯一应当复制到新对话的交接文件**（由 `python -B tools/handoff.py` 生成）。
> 📌 **当前事实不在本文件里** —— 全部在 **`state/current.md`**（由 `learning/` 重算，含指纹可核）。
> 本文件只负责：①告诉你按什么顺序读；②把当前事实与人工意图**引用**过来；③给规则提醒。
> ⚠ 旧文件 `plan/handoff-prompt-2026-09-28.md` 已标为**历史、勿用**（它是 09-28 上午的快照，会把进度倒退）。
> 生成时间：**2026-10-19**（中国时间；系统英国日期 2026-10-19）。若与 `state/current.md` 不一致，**以 `state/current.md` 为准**。

---

```
请按本工作区的 tutor 规则继续带我学习（AGENTS.md / CLAUDE.md 会自动注入）。

【时间基准】系统时钟是英国时间，我的真实时间是中国大陆（UTC+8）。
所有「今天/明天/截止日/时间窗」一律按中国时间判断。今天是 2026-10-19（周一）。

【先读这些（按顺序）】
1. state/current.md —— **当前状态的唯一事实来源**（覆盖表、最近证据、帮助史、卡点、可数事实）
2. plan/today-2026-10-19.md —— 当天时间窗与清单（人工安排的权威；若不存在见下）
3. learning/curriculum-coverage.md —— 课程范围与证据对账（未登记目标/无题/无独立证据；目录未核全则覆盖未知）
4. plan/schedule.md —— 复习与再测的**日期化**排期（含「未来才开放、不得提前安排」的项）
5. .tutor/core/protocol.md —— 当前协议；learning/README.md 在入账或核对帮助史时按需读
6. .tutor/config/teaching-conventions.md —— 教学约定（三种模式、批改、讲解范围）
7. tools/observations.py --list —— 待处理学习者反馈；历史系统问题仅在维护时读

【当前状态（引用 state/current.md 的汇总）】
**当前课程/主线**：04-数学物理方法1（第三章：洛朗已收口，hurdle-2 → awaiting_retest；**孤立奇点已教完并三测（attempt-27～31），目标仍未通过 → 待换形态的延迟变式**）+ 01-理论力学（判据二概念层已结案 verified；但 `tm.t4.energy-criteria` 等级未升；**Topic 4 ③动量/④角动量/⑤力学相似仍无独立证据**——角动量与力学相似是**已声明但 0 题**的纸面目标，见 `learning/coverage.md` 第②节；**2026-10-08 新上传 Topic 5 课件**：Integrating the Equations of Motion，作业 **H5.1 在 p15**，尚未开始）+ 06-电工电子技术（实验1 已完成、报告已评审，全部实验做完后一起交）+ 03-微分方程（**期中改到 2026-10-20；复习目标 10-15 前完成；范围不变＝Lecture 1–12 方程组之前**）+ 07-俄语（`ru-adj-qword-01` 已测 partial；待做 `ru-noun-gender-fix-01` 与 `ru-qword-meaning-01`，due 10-02）+ 02-光学（**已滞后**：原 10-06 截止已过，10-05～10-07 系统无记录；学习者 2026-10-08 要求「明天之前跟上进度」；三课扫描件已在库，§1.5-2 傍轴近似已读图并已出学习指南）+ 10-形势与政策（选课窗口 **10-08 12:30 – 10-10 17:00**；任务 `xz-2026f-course-selection`；⚠ 年级是否 2025 级 `[待确认]`）+ 11-英语（雅思）（**2026-10-02 立项**：听力 8／口语 7／写作 6.5→7→上不封顶／阅读 8 保持＝**均分 7.5 通路**；学期 5h/周、**假期 15–20h/周**；考试拟大三中/末，**以训练水平为主**；计划与原理见 `subjects/11-英语-雅思/`；skill 与数据层适配进行中）

**最近一次收尾**：**2026-10-02 本轮（英语项目立项 + 计划定稿）**：新增第 11 个（**非课程**）目标项目 **英语（雅思）**——听力 8／口语 7／写作 6.5→7→上不封顶／阅读 8（保持），构成 **均分 7.5 通路**（8+8+6.5+7 = 29.5）；学习者现大二、考试拟大三中/末、**以训练水平为主不赶进度**，学期 **5h/周**、**假期 15–20h/周**（累计约 645–670h，这是结论从「不可行」翻转为「可行」的唯一原因）。已建立：`subjects/11-英语-雅思/`（训练计划 + 原理与反馈协议）、`learning/goals.yaml` 的 `ielts-english-75`（11 个目标，当前全部为**纸面目标**，无题）。两条关键口径：①**英文自由对话不算能力证据**（对话中导师给过英文 = 帮助史非零，只算输入量）；②**导师无音频输入 → `en.speak.pr` 在接入外部评分前只能记「未测」**，不得由逐字转写推断发音。**前一轮（2026-09-30 系统维护窗口）**：①**数理方法孤立奇点分类**（第三章最后一块）：诊断 `attempt-27` → 定向修复 `attempt-29` → 检验 `attempt-28`（3/5，判读为 partial）→ 再测 `attempt-30`（2/4）→ 补充题 `attempt-31` 答对；**缺口收窄到一个动作**：数零点阶数前没把非幂因子（`sin z`、`e^z − 1 − z`、`ln(1+z) − z`）**展开到首个非零项**——提示下会做、换函数就不自发。完整规则见 `subjects/04-数学物理方法1/讲义/§3.5-孤立奇点分类-完整规则-20260930.md`。⚠ **本轮订正**：`attempt-28` 原记「H0 + 无曝光」**与原始会话不符**——导师在提交前（seq387）已点名第 4 题「必须把分子展开到首个非零项」→ 已按可追溯订正改为 `practice` + `H2` + `partial@before_attempt`（**事件级与目标级两层都改**，corr-20260930-01～10），并把 `attempt-29` 的 `diagnosis_status` 由 confirmed 降回 pending_probe；另追加 `narr-20260930-01` 作废旧结论（全部见 `learning/corrections.jsonl`）。②**理论力学判据二**：`attempt-25`（H0、完全闭卷、未见变式、距补讲 2 天）判据层全对；唯一失分＝符号搬运（A3 把 U 写成 `+mg s sinα`）→ `hurdle-1` verified（概念层），但`tm.t4.energy-criteria` **等级不变**（困难结案 ≠ 目标升级）。③**维护成果**：状态改为**单一事实源 + 派生视图**（`state/current.md` 由 `learning/` 重算），并发写加锁并改为机器取号，复习排期落成带日期的任务。

**必须遵守的提醒**：⚠ **时区**：系统为英国时间，计划与截止一律按**中国大陆时间**（换算见 `tools/timebase.py`，规则见 `.tutor/config/time-environment.yml`）；所有脚本的日期基准已统一走该模块。⚠ **本工作区 2026-09-30 维护后的规则（开新会话先读这四条）**：①**当前状态只有一个来源** —— `state/current.md`（由 `learning/attempts.jsonl` + `corrections.jsonl` + `goals.yaml` 重算）；`AGENTS.md/CLAUDE.md` 的 STATUS 与 `plan/handoff-CURRENT.md` 只是**引用**它，**不要在别处再手写一份计数或进度叙述**。②**收尾只有一个入口** —— `python -B tools/session-close.py --today <中国日期>`（10 步：校验→派生→覆盖表→事实卡→STATUS→handoff→排期→订正影响面→**一致性核对**）；任何一步失败都会显式打印 FAIL，**不允许只更新计数就宣称状态已同步**。③**写入必须走锁** —— `tools/append_attempt.py --event-id auto` 在锁内**机器取号**（`learning/attempts/_ids.json`），不再靠人读文本预留 attempt-N；订正走 `tools/record_correction.py`（强制 `reason` + `source` + `evidence_ref`，没有证据不给订正）；原始事件**不改不删**。④**帮助史不能漏记** —— 测验/练习中给出**针对具体试题**的方法提示，或**透露过含答案的文件**，都算帮助：`max_hint_level` 记实际级别、`solution_exposure` 非 none。**「此前学过通用方法」不等于「本次试题已曝光」**，两者不要混为一谈（详见 `learning/README.md`）。⚠ **作答默认闭卷**（学习者 2026-09-30 明确：开卷会特别说明）→ 不再逐次追问 `closed_book`；**提问必须指名到物**。⚠ 中文引号一律用「」，半角引号会让事件成为非法 JSON（写前可跑 `python -B tools/write_check.py <文件>` 用真解析器自检）。⚠ **保留的教学要点**：讲「为什么」要带上下文、不得只给结论口诀；课件原文与 `[教学归纳]` 分开标；手写读不准标 `[待确认]` 且不得据此改判；**别让学习者逐字转写自己的手写**（给一步自查更省事）；学习者说「我还是没明白」时直接给完整规则 + 课件页码对照，比继续追问更有效；**困难结案 ≠ 目标升级**、**同日教学后检验不构成延迟证据**（`min_delay_days: 2`）；**不得用整条事件的总评去逐目标升级**。⚠ 电工实验硬规则：无预习报告不允许做实验、不带教材不允许进实验室（材料登记在 `subjects/06-电工电子技术/实验/INDEX.md`）。⚠ 历史更正（泰勒/洛朗判据三次更正、`attempt-5` 曝光史、`hurdle-1` 口诀降级等）**已归档**：全文见 `learning/corrections.jsonl` 与 `learning/attempts/corrections.md`，冷启动入口不再堆积纠错过程；系统级问题清单见 `ISSUES-待改进.md`。

【今天清单】
⚠ **`plan/today-2026-10-19.md` 尚未建立** —— 本轮没有人安排过今天；请先按下面的「回来先做什么」+ `plan/schedule.md` 的到期项，与学习者确认后再建。**不要凭空补一份。**

【回来先做什么】
**人工指定的下一步（权威）** —— 见上方 `next:` 行；要点摘录：

- ⓪**换会话/交接一律看 `plan/handoff-CURRENT.md`，当前事实只看 `state/current.md`**（两者都由 `python -B tools/session-close.py --today <中国日期>` 生成
- 旧 `plan/handoff-prompt-2026-09-28.md` 已作废勿复制）①**先做延迟变式**（孤立奇点 + 洛朗各一道，`kind = delayed-variant`
- 换形态、换函数、闭卷、H0
- **不得复用任何已作答题目**含 `sing-01/02/03` 与 `quiz-01`）——`plan/schedule.md` 会给出最早可做日期②**微分方程期中复习**：考试 **2026-10-20**（原 10-08 已作废），目标 **10-15 前**完成，范围＝Lecture 1–12（方程组之前）③**电工未见变式题**：C2H2 的 Q4（|Z|、I 曾由导师代算）与 Q5 谐振项
- 实验1 五个目标全部 needs_verify④电工报告补硬伤（补 25 mH 波形等
- 需 Multisim
- 不急）⑤**俄语**：`ru-noun-gender-fix-01` ＋ `ru-qword-meaning-01`，due 10-02 ⑥光学（**立即补进度，10-09 前跟上**
- 学习指南 `subjects/02-光学/讲义/§1.5-2-傍轴近似-学习指南-20261004.md`）⑦**Topic 4 剩余考点**（`tm.t4.angular-momentum-integral`、`tm.t4.mechanical-similarity` **已声明但 0 题**
- `tm.t3.lagrangian-construction` 0 题
- `tm.t4.cyclic-momentum` 两次作答全曝光）——按学习者指定**排在第三章之后**，出题前先与学习者确认范围⑧**形势与政策选课**（due 2026-10-10 17:00，窗口 10-08 12:30 开
- 课程清单 `.xls` 需校内网络下载）⑨**英语（雅思）**：计划与原理已定稿（`subjects/11-英语-雅思/`）
- 下一步＝(a) skill 与数据层适配（审计进行中，**改共用文件前先与学习者确认**）(b) 建 Phase 0 基线题（写作 T2 + T1、听力一遍听写、口语 Part 1/2/3 录音、阅读一套）(c) 学习者回填**真实校历**（学期起止、寒暑假周数）与**外部发音/写作反馈来源**（规格见训练计划 §6）⑩**理论力学 Topic 5**（2026-10-08 新上传：Integrating the Equations of Motion
- 作业 **H5.1 在 p15**，势能 `U(x)=A(e^(−2αx)−2e^(−αx))`）——学习时间待学习者确认
- Topic 4 的 ③④⑤ 仍未结

**机械候选（来自 `plan/schedule.md`，仅供核对，不等于安排）**：

1. `tm-h4-01`（题目截止｜practice）— 题目截止 2026-09-27（已逾期）
2. `mp1-ch3-quiz-01`（题目截止｜practice）— 题目截止 2026-09-28（已逾期）
3. `tm-t4-criteria-03`（题目截止｜practice）— 题目截止 2026-09-28（已逾期）
4. `ee-lab1-prep-01`（题目截止｜practice）— 题目截止 2026-09-29（已逾期）
5. `tm-t4-criteria-04`（题目截止｜mixed）— 题目截止 2026-09-29（已逾期）
6. `ee.ac.phasor-impedance`（能力再测｜延迟检验）— 已有独立通过（2026-09-28）；已验证通过日期跨度 0d < 2d；最早 2026-09-30 可换题复测（等待本身不算通过）

未来才开放（**不得提前做**）5 条，最早一条 = `pilot-ode-integrating-factor:milestone` @ 2026-10-22（独立解一阶线性 ODE（试点） 的 milestone = 2026-10-22）。

【规则提醒】
- 默认教学式：先让我短暂独立尝试 → 卡住给最小提示 → 收尾用无提示新题检查
- **讲「为什么」要带上下文**：不要只给结论口诀
- **课件原文与教学归纳分开标**：教学归纳请标 `[教学归纳，非课件原文]`
- 批改三层：**看见了什么** → **可能是什么原因**（假设）→ **怎样确认**（一个短问题或一步计算）
  ⚠ 不要把简短回答扩写成具体机制；⚠ 手写读不准标 `[待确认]` 问我，**不得据此改判**
- **作答默认闭卷**：用户会特别说明开卷，不逐题重复追问；未知帮助史不能由照片推断
- 曝光与提示**只能由会话记录或我确认**，不得由作业照片推断；依据不足用 `unknown`（unknown 阻断升级）
- **两条会话线可能并发写同一套文件**：入账一律用 `python -B tools/append_attempt.py --event-id auto`
  （锁内取号，不再靠人读文本预留 attempt-N）；收尾一律跑 `python -B tools/session-close.py --today <中国日期>`
- 公式用纯 Unicode（ẋ ẍ ½ ² √ Σ ∂ ≠ ⟹ Ω θ），**不用 $...$**（实测显示为字面美元符号）
```

---

## 仍需学习者确认的

- 叙述行 `note` 里标了 `[待确认]` 的事项（见 AGENTS.md 的 STATUS，逐条列出）。
- **已声明但没有任何题目的考点**：`ai-tech.c00-02`、`ai-tech.c00-03`、`ai-tech.c00-04`、`ai-tech.c00-05`、`ai-tech.c00-06`、`ai-tech.c00-07`、`ai-tech.c00-08`、`en.listen.decoding`、`en.listen.structure`、`en.read.timed`、`en.speak.fc`、`en.speak.gra`、`en.speak.lr`、`en.speak.pr`、`ode.sys.ivp` —— 要不要出题、什么时候出，需要你指定（系统不自动建题）。
- **未解决困难**：`hurdle-2`（awaiting_retest）、`hurdle-3`（teaching） —— 处置方式（补讲/补练/再测）需要你确认。
- **并发写约定**（ISSUES D4 已由本轮实现落地：锁 + 机器取号 + 原子写；若你另有偏好请说明）。

## 相关文件

| 用途 | 文件 |
|---|---|
| **当前状态（唯一事实源）** | `state/current.md` |
| 课程覆盖台账 | `learning/coverage.md` |
| 复习/再测排期 | `plan/schedule.md` |
| 当天清单（人工权威） | `plan/today-2026-10-19.md` |
| 答题与订正事实源 | `learning/attempts.jsonl` · `learning/corrections.jsonl` |
| 订正人读视图 | `learning/attempts/corrections.md` |
| 缺口台账 | `plan/gaps.md` |
| 系统问题清单 | `ISSUES-待改进.md` |
| 人工意图（叙述行唯一来源） | `.tutor/config/status-narrative.yml` |
| 历史交接（勿用） | `plan/handoff-prompt-2026-09-28.md` |
