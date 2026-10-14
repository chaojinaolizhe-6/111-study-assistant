# 学习数据层（learning/）

> 能力测量、反馈与负载控制的数据层。原则：**内容稳定、事件追加、状态可重建**。
> 记忆状态与解题能力分离：SM-2 记忆状态在 `state/`（何时再测），能力证据账本在本目录（无帮助下通过了什么）。

## 文件

| 文件 | 角色 | 谁写 |
|------|------|------|
| goals.yaml | 能力目标（**含尚未出题的目标**——它是目标的事实源之一，`derive_state` 会读） | 导师与学习者共同确认后写 |
| tasks/ | 题目（id、target_ids、version、kind、acceptance、est_minutes、device） | 导师建题 |
| attempts.jsonl | 作答事件（追加式，程序校验） | 导师追加，**必须用 `tools/append_attempt.py`** |
| attempts/_ids.json | **机器可读取号计数器**（锁内递增，替代"人读文本预留 attempt-N"） | `append_attempt.py` |
| corrections.jsonl | **订正的唯一事实源**（原始事件不改不删） | `tools/record_correction.py` |
| learner-state.json | 能力状态（派生，勿手编；含 `source` 事实源指纹） | `tools/derive_state.py` |
| coverage.md | 课程覆盖台账（未安排/已安排未作答/需补练/独立通过/待延迟复测） | `tools/coverage.py` |
| policy.yml | 等级判定参数（工程初值，可调） | 导师与学习者共同确认后改 |
| attempts/ | 作答过程详档（可选，artifact_ref 指向） | 导师 |
| weekly-review.md | 每周复盘（四指标 + 判断与调整） | 导师每周 |

> **当前状态只看一处**：`state/current.md`（`tools/current_state.py` 生成，引用本目录的数据）。
> STATUS 块与 `plan/handoff-CURRENT.md` 只**引用**它，不在别处再写一份计数或进度叙述。

## 能力等级（参数见 policy.yml；工程初值，可调）

- 未测 → 需支持 → 曾独立完成 → 延迟通过 → 迁移通过
- "独立通过"**按目标判定**（2026-09-28 修）：该目标结果正确（`target_results[tid].final` 优先）
  且提示级别**明确为 0**（`target_results[tid].hint_level` 优先；`null`=未知，不算无提示）
  且 **`needs_verify` 不为真** 且答案未曝光（目标级 `exposure` 优先）且 mode≠worked-example
  且 closed_book=true（开卷通过单独记入 open_book_pass_dates，不计等级）。
  **不得用整条事件的总评去逐目标升级**——那会把同事件中待核验的目标一起升级，
  也会把同事件中已独立答对的目标一起压掉。
- ≥min_dates 个不同日期独立通过 = 延迟通过
- 另含 ≥min_variant_passes 次"未见变式通过" = 迁移通过
- **未见变式通过**：该题目在本事件之前从未被作答过（按 attempts.jsonl 行序），且 kind ∈ {delayed-variant, mixed}。
  先见过解答再重做通过 ≠ 迁移证据。
- 辅导后做对（hint>0）是学习进展，**不是独立掌握证据**；一次失误不清空历史

## 题目模板（learning/tasks/_template.md）

```markdown
---
id: <课程缩写>-<主题>-<序号>
subject: <课程目录名，如 03-微分方程>
title: <一句话题目名>
target_ids: [<知识点稳定ID>]
version: 1
kind: baseline | practice | delayed-variant | mixed | worked-example
status: open | blocked | done
est_minutes: 30
device: any | tablet | pc
due: YYYY-MM-DD      # 可省略
acceptance: <无提示独立完成的验收标准，可观察行为>
---
（题干。题干实质变化 → version+1）
```

## 题目升版规则（重要）

题干实质变化（含换目标、换类别）时：
1. 把**旧 frontmatter 原样**存入 `learning/tasks/history/<id>.v<旧版本>.md`（历史元数据）；
2. 题目文件里 version+1 并更新目标/类别/题干。
- 事件按其所引版本的历史元数据解释：旧版本事件不会借用当前版本的类别或目标；
  有历史元数据 → 照常计分（成绩不与当前版本直接比较，见 version_mismatch_events）；
  无历史元数据 → 事件保留在统计中，但不用于升级（unknown_version_events）。

## 作答事件字段（见 tools/validate_attempts.py 的 REQUIRED）

关键约束：
- event_id 唯一；重试不得重复计分
- target_ids 必须是题目**在事件所引版本**下声明目标的非空子集——一道题不能给无关能力计分
- task_version 不一致 → 警告不阻断（按历史元数据解释；无元数据则保留但不升级）
- 测验模式禁提示；示例学习必须 solution_seen=true
- initial_result 与 final_result 同时保留；辅导后做对必须保留提示级别

### 可选字段（2026-09-27 新增；判定实现在 `tools/learninglib.py`）

| 字段 | 取值 | 作用 |
|------|------|------|
| `target_results` | `{target_id: {initial, hint_level, final, needs_verify, note, exposure?, exposure_timing?}}` | **按目标分别记**——"E 写对了、求导写错了"不再挤成一个总结果；`needs_verify=true` 表示该目标待核验，**且该目标本次不计独立通过（不升级）** |
| `target_results[tid].exposure` | `none` / `partial` / `full` | 该目标自己的答案曝光程度；缺省回退事件级 `solution_exposure` |
| `target_results[tid].exposure_timing` | `before_attempt` / `during_attempt` / `after_attempt` / `unknown` | 该目标的曝光时机；缺省回退事件级 |
| `solution_exposure` | `none` / `partial` / `full` | 答案曝光程度（整条事件的**汇总**，缺省回退 `solution_seen`）；反馈里展示过式子即非 `none` |
| `exposure_timing` | `before_attempt` / `during_attempt` / `after_attempt` / `unknown` | 曝光时机：作答前 / **作答进行中**（如留空后被代算）/ 反馈后。**只有反馈后不污染此前那次独立表现**；作答前与作答进行中**都阻断**独立通过 |
| `time_source` | `actual` / `self_reported` / `estimated` / `unknown` | 用时来源；只有 `actual/self_reported` 计入**实测时长**，`estimated` 单列，`unknown` 不给值 |

> ⚠ **事件级字段是汇总值，不是判定值**。当 `target_results` 存在时，`final_result` / `max_hint_level` /
> `solution_exposure` 只作**缺省回退**；实际升级逐目标判定。整条事件的总评不得覆盖同事件中
> 表现不同的其它目标。

### 判定口径（唯一实现：`tools/learninglib.py`）

- **独立通过**（`independence_blockers()`，逐目标）= 该目标答对 + 提示级别**明确为 0**
  + **`needs_verify` 不为真** + 答案未曝光 + 非示例学习（+闭卷）。
  - `hint_level=null` 表示"未知"，不计独立通过（旧实现把 null 当无提示，2026-09-27 已修）。
  - **`needs_verify=true` 的目标不得升级**（2026-09-28 修：此前只做统计、不阻断升级）。
  - **曝光按目标算**：`target_results[tid].exposure` 优先，回退事件级；
    只有 `exposure_timing=after_attempt`（反馈发生在**作答之后**）**不阻断**——该目标此前是否独立，
    由它自己的提示级别与 `needs_verify` 反映，不由汇总曝光决定；
    `before_attempt` 与 `during_attempt`（做到一半被代算）**都阻断**。
  - 每个未升级事件的**具体原因**写入 `learner-state.json` 的 `targets[*].upgrade_blocked`，
    收尾时由 `session-close.py` 汇总打印——"凭什么算独立完成"必须可复查。
- **开卷通过** 记入 `open_book_pass_dates`，不计等级。
- **延迟通过**：独立通过日期数 ≥ `min_dates` **且日期跨度 ≥ `min_delay_days`**（默认 2 天；相邻两天不算延迟证据）。
- **迁移通过**：再含 ≥ `min_variant_passes` 次未见变式通过；**只有迁移通过算稳定证据**。
- **全局时长去重**：同一次作答涉及多目标时按目标合计会重复；`summary.measured_minutes_global` 按**不同事件**去重。

## 困难观察（learning/hurdles.jsonl）

**没有作答**的困难（学习者明确说"不理解/不会"）**不写进 attempts**（不伪装成做错一道题），写在 `hurdles.jsonl`：
必填 `hurdle_id`、`target_ids`、`observed_at`、`source`（learner_statement / tutor_observation / review_feedback）、`status`（open / teaching / awaiting_retest / verified / closed）、`evidence_ref`。
校验：`python -B tools/validate_hurdles.py`；`derive_state` 把未解决困难挂到对应目标（`targets[*].open_hurdles`）并计入 `summary.open_hurdles`。

## 三种任务（别混用）

| 类型 | 含义 | 依据 |
|------|------|------|
| **补讲** | 当前尚未理解的内容 | `hurdles.jsonl` 的 `teaching` 项 + 对应任务 |
| **再测** | 讲解/订正之后、撤去帮助的检查 | 任务的 `acceptance`（如 `tm-h4-01-fix-01`、`tm-t4-criteria-02`） |
| **记忆复习** | 已理解、需保持的内容 | `state/` 的 SM-2 队列 |

## 历史订正（2026-09-28 重构：**订正必须程序可读**）

对既有判定的修正写在 **`learning/corrections.jsonl`**（订正的**唯一事实源**）；
原始事件 `attempts.jsonl` 与手写照片**只增不改、不删**。

为什么不是 `corrections.md`：它是给人读的自由文本，`validate_attempts` / `derive_state` /
`plan-week` **都读不到它**——订正对能力判定实际上是零影响，同一件事会在两个文件里留下
两种状态，而程序只认其中一种。现在三者统一：**先应用订正，再在"应用订正后的记录"上判定**。

- 校验：`python -B tools/validate_attempts.py` 会一并校验订正本身（字段合法、事件与目标存在、
  `from` 与当前值一致），并在影子副本上**顺序折叠**对照——防止同一字段上的两条订正互相掩盖。
  ⚠ 2026-09-30 修：`current == to` 不再**无条件**短路（旧写法会把 `from` 写错的订正静默接受）。
  只有 `from == to` 才算合法空操作。
- **写订正请用** `python -B tools/record_correction.py`（锁内追加 + 强制 `reason`/`source`/`evidence_ref`
  + 写后全量复核）——**没有证据不给订正**，这是"不能靠改写原始事件绕过"的落地方式。
  可订正的事件级字段见 `learninglib.ALLOWED_EVENT_FIELDS`（含 `closed_book`、`mode`）；
  **目标级字段**（`hint_level`/`exposure`/`exposure_timing`/`note` 等）用 `--scope target`。
  ⚠ 订正 `mode` 时必须保住不变量：**`quiz` 只允许 `max_hint_level=0`**——
  若事实是"测验里给过提示"，正确做法是把 `mode` 订正为 `practice`，**不是把 hint 改回 0**。
- 视图：`learning/attempts/corrections.md` 由 `python -B tools/render_corrections.py` **自动生成**，请勿手工编辑。
- **幂等**：重复运行结果一致；已生效的条目因 `from` 不再匹配而跳过。
- 新增事件请用 `python -B tools/append_attempt.py --file <事件.json> --event-id auto`：
  **锁内取号**（机器读 `attempts/_ids.json`，不再靠人读文本预留 attempt-N）、event_id 重复拒绝、
  以 **append 模式**只追加自己那一行（不会重写整个文件 → 不会覆盖并发会话的新记录）、
  写后全校验、失败**只回滚自己那一行**。
- 并发写入的互斥与原子替换实现见 `tools/workspace_lock.py`（`learning/.write.lock`）。

字段：`correction_id`、`event_id`、`scope`(`event`/`target`)、`target_id`、`field`、`from`、`to`、
`reason`、`source`(`learner_statement`/`photo_reread`/`tutor_review`/`record_audit`)、`evidence_ref`、`at`。
`kind=narrative` 的条目只带 `text`，用于归档人读叙述与「**旧结论作废**」声明。

> ⚠ 订正只对**已核实**的事实做。读图歧义、口述澄清这类证据较弱的情形，按本地约定标
> `[待确认]`，不据导师单方面辨读改判；`needs_verify=true` 的目标不得升级。

> ⚠ **证据来源规则（2026-09-28 加，勿违）**：`solution_exposure` / `exposure_timing`（以及 `hint_level`）
> **只能由会话记录或学习者确认**，**不得由作业照片推断**——照片能证明"写了什么"，证明不了
> "作答前有没有口头提示"。依据不足时写 `exposure_timing: unknown`（**unknown 会阻断独立通过**），
> 不要用 `before_attempt` / `during_attempt` 去猜。
> **反向同样成立**：依据不足 ≠ 确实受助——不得仅因"证据弱"就下调判定，那同样是猜测。
>
> ⚠ **曝光按本题 / 本目标记（2026-09-28 加）**：**学过某一方法，不等于后续所有新题都已曝光。**
> 需要追踪的是**本题答案、关键步骤、以及本次作答过程中的帮助**；不能把"接受过教学"永久算成答案污染。

> ⚠ **帮助史必须如实记（2026-09-30 加，本轮实际踩过）**：
> 下列情形**都算帮助**，必须写进 `max_hint_level` / `solution_exposure`：
> ① 测验或练习中给出**针对具体试题**的方法提示（哪怕只是一句"这题要先展开到首个非零项"）；
> ② 把**含答案的任务文件路径**告诉学习者（哪怕只是提了一句"别翻那个文件"）。
> **"此前学过通用方法" ≠ "本次试题得到具体提示"**——前者不是污染，后者必须记。
> 实测案例：`attempt-28` 原记 `H0 + 无曝光`，而导师在提交前（会话 seq387）已点名第 4 题的解法方向
> → 已订正为 `practice` + `H2` + `partial@before_attempt`（见 `corrections.jsonl` corr-20260930-01～10）。
> **提示后答对不自动证明根因唯一**：该次提示只点名了第 4 题，学习者仍把第 3 题答成"本性极点"
> → 缺口机制只能算**假说**（`diagnosis_status: pending_probe`），要靠换函数、无提示的延迟变式定案。

> ⚠ **展示值与判定值必须一致（2026-09-30 加）**：`target_results[tid]` 是**判定值**
> （`independence_blockers` 目标级优先），事件级 `max_hint_level` / `solution_exposure` 是**汇总展示值**。
> 订正时必须**两层一起改**；若事件级声称"H0 + 无曝光"而目标级记着帮助，
> `validate_attempts` 会报 WARN、`session-close` 的"1b 帮助史一致性"步骤会 FAIL——
> 因为**判定不会错，但看记录的人会被误导**。

## 曝光与修复的粒度规则

- **题目曝光全局计算**：某题在任何目标下被作答过即"已曝光"；
  此后任何目标下的通过都不构成"未见变式"（防止跨目标绕过曝光历史）。
- **修复按 (题目, 目标) 追踪**：一次通过只关闭它实际覆盖的目标；
  同题另一目标的待修复问题不会被连带关闭。

## 每周四指标（weekly-review.md）

1. 延迟无提示通过率（过几天还能独立完成吗）
2. 未见变式表现（条件/表征改变后还能选对方法吗）
3. 提示依赖（相近难度任务所需支持是否减少）
4. 时间成本（学习与系统维护分别用了多久）

原题与新题成绩分开看；不同难度题目不直接比较。
