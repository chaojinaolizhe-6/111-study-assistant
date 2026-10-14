---
id: en-write-t2-baseline-01
subject: 11-英语-雅思
title: 学术类 Task 2 基线（汽车与替代交通；限时 40 分钟）
target_ids: [en.write.tr, en.write.cc, en.write.lr, en.write.gra]
version: 1
kind: baseline
status: open
est_minutes: 40
device: any
acceptance: 限时 40 分钟内、闭卷、不查词典写出 完整文章作为首次样本并记录是否达到250词要求；未达到仍保留实际样本和反馈，不把低于下限当基线无效
---

（题干）

**WRITING TASK 2**

You should spend about 40 minutes on this task.

Write about the following topic:

> The first car appeared on British roads in 1888. By the year 2000 there may be as many as
> 29 million vehicles on British roads.
>
> Alternative forms of transport should be encouraged and international laws introduced to
> control car ownership and use.
>
> To what extent do you agree or disagree?

Give reasons for your answer and include any relevant examples from your knowledge or experience.

Write at least 250 words.

---

## 题源与污染状态

- 题源：`subjects/11-英语-雅思/资料/官方补充-20261003/剑桥免费样题/写作-Task2-仅题面.pdf`（剑桥官方免费样题，Task 2A）。
- **结构性防污染**：本库**没有这道题的范文**。官方范文（`官方样题/ielts-academic-writing-example-responses-...pdf`、写作汇编 p8 起）对应的是**另外三道题**（子女与贫富、国际旅游、继续教育图表）。所以即使学习者日后打开范文库，**本题也不会被污染**。
- ⚠ 正式检查前避免本题示范；其他题范文/通用方法不能直接视为本题答案曝光。

## 交给学习者时必须说清的（正式检查条件；未知项记未知，产物保留）

1. **限时 40 分钟**，到点停笔（写没写完都要交）。
2. **闭卷、不查词典、不用任何翻译或语法工具**；想不起来的词就用你会写的词绕过去。
3. **计时内可检查和修改**，提交后保存该最终稿；后续重写另存版本。
   → 交的时候**同时告诉我**：实际用了几分钟、有没有查过任何东西。

---

## 核验要点（导师用，不对学习者展示）

### 一、事件字段（照此入账，不自由发挥）

| 字段 | 值 | 依据 |
|---|---|---|
| `mode` | `quiz` | 限时闭卷产出（ielts-session skill §1） |
| `max_hint_level` | `0` | 作答前不给任何英文、不给结构建议、不给词汇 |
| `solution_exposure` | `none` | 题面为首次呈现；未透露含答案文件路径 |
| `exposure_timing` | 不填 | 无曝光 |
| `closed_book` | `true` | 学习者长期约定，不再追问 |
| `kind` | `baseline` | 首次接触，非变式 |
| `needs_verify` | `true` | **基线只取观测值，本事件不用于升级任何目标** |
| `active_minutes` | 学习者实报 | `time_source` 用实测；未报则留空，**不得用 `estimated` 冒充实测** |

⚠ **`band` 字段尚未解锁**（`PER_TARGET_KEYS` 无此键，见 `数据层适配-20261002.md` §2 阶段 1）：
分档与计量**写进 `target_results[tid].note`** ＋ `subjects/11-英语-雅思/训练台账.md`（**该文件尚未建立，本次建立**）。
**不要往事件里加自由键**——顶层未知键虽能通过校验，但**无法用 `record_correction.py` 订正**。

### 二、四项分档怎么给（引 band descriptors 原文，不要只给数字）

标尺：`subjects/11-英语-雅思/资料/评分标准-官方-写作-band-descriptors.pdf`（Task 1 与 Task 2 同在一份）。

- **TR**（Task Response）：立场是否清楚且**贯穿全文**？观点是否**展开**（理由得到相关解释/例证/证据支撑），还是只罗列？
- **CC**：段落安排与逻辑推进；衔接手段是否**恰当**——⚠ 官方关注的是**是否机械或误用**，不是数量多少。
  *已核实的官方例子*：一份 Band 7.5 答卷被点评「some overuse of sequencers in paragraph 2 [Firstly | So | Also | Yet]」，**仍然拿到 7.5**；而 Band 4 的问题是 cohesive devices "mostly inaccurate"。**"连接词多"本身不扣分。**
- **LR**：词汇范围、搭配是否自然、语域是否一致；拼写与构词错误。
- **GRA**：句式多样性与准确性；错误是否妨碍理解。

**同时必须记录**（skill §2.2 要求）：
- `task`（T2）、`words`（实际词数）、`minutes`（实际用时，未知就记未知）
- **是否达到 250 词下限**（未达下限要反馈，不能推断固定扣多少分或仅据字数给分）

### 三、产出格式（照 skill §2.2，不多不少）

1. 四项分档（各附 band descriptors 的**可观察依据**，最好引原文短句）；
2. **最多 3 个**最高杠杆问题（一次给 10 个等于一个都改不掉）；
3. **重写指令**——**只重写有问题的那一段，不重写全文**；
4. 换题再测安排（`delayed-variant`，`min_delay_days=2`，换**未见题**，写清最早可做日期）。

### 四、基线判读口径（防止自我误导）

- 本次是**起点样本**，估分不是正式成绩。**不因分低而调整目标**（目标由训练计划 §1 定），只用来**决定配比**。
- **基线的核心产出是错误清单，不是那个分数**——导师给的是估算，非官方分（协议 §六.2）。
- 若 Phase 0 显示瓶颈不在解码而在词汇或句法，训练配比要整块改（协议 §1.2）——本次写作结果**不能**回答这个问题，需靠听力那一格。
- **不得**据本次结果宣称任何 `en.write.*` 目标「已掌握」；本次 `needs_verify=true` 本身就阻断升级。

### 五、收尾

`python -B tools/session-close.py --today <中国日期>`，12 步必须全 OK，任一步 FAIL 要如实报告未完整同步。

2026-10-04审查：此样本已提交（attempt-41），不得为首次基线重排。224词事实保留；旧TR理由/诊断已由订正层修正，通用结构教学不自动污染未来新题。普通教学不强制本文件的完整检查流程，用户要讲解就先讲。
