# 记录订正（Corrections Log）

> ⚠ **本文件由 `python -B tools/render_corrections.py` 从 `learning/corrections.jsonl` 自动生成，请勿手工编辑。**
>
> `learning/corrections.jsonl` 是订正的**唯一事实源**。`tools/validate_attempts.py`、
> `tools/derive_state.py`、`tools/plan-week.py` 三处消费者统一：**先应用订正，再在应用订正后的记录上判定**。
> 原始事件 `learning/attempts.jsonl` 与手写照片只增不改、不删。

## 字段订正（24 条，已进入判定链路）

### attempt-5

| 范围 | 目标 | 字段 | 原值 | 修正值 | 来源 | 日期 |
|---|---|---|---|---|---|---|
| 目标级 | `tm.t4.energy-criteria` | `exposure` | (无) | partial | record_audit | 2026-09-28 |
| 目标级 | `tm.t4.energy-criteria` | `exposure_timing` | (无) | before_attempt | record_audit | 2026-09-28 |
| 事件级 | `—` | `solution_exposure` | none | partial | record_audit | 2026-09-28 |
| 目标级 | `tm.t4.energy-criteria` | `note` | 判据二首次独立通过：对 H4.1 的 L 独立答出广义速度是 ẋ、T 只有二次项故 T₂=mẋ²/2 且 T₁=T₀=0…（共 168 字，全文见 corrections.jsonl） | 【曝光史订正 2026-09-28，原写『无答案曝光』作废】旧窗口在同一目标上早已讲解并套用过：seq1017 给出『判…（共 498 字，全文见 corrections.jsonl） | record_audit | 2026-09-28 |

**理由与证据**

- `corr-20260928-17` / tm.t4.energy-criteria / `exposure`：原记录（事件级）写 solution_exposure=none、note 写『无答案曝光』，不成立。旧窗口在同一目标上早已讲解并套用过：seq1017 给出『判据二：T = T₂ 且 T₁ = T₀ = 0 → 欧拉定理 Σq̇∂T/∂q̇ = 2T → E = T+U』并逐条套用 H4.1 的 L 得出结论；seq2257 整节讲『齐次次数』，给出 Σq̇∂T/∂q̇ = 2T₂ + T₁、E = T₂ − T₀ + U、E = T+U ⟺ T₁ = T₀ = 0。本次作答内容正是这套算法套到 H4.1 的结果。目标级字段原本不存在，故 from 记 null（不假写成 none）
  - 证据：旧窗口日志 old.jsonl seq1017（H4.1 反馈：判据二讲解 + 套用结论）、seq2257（齐次次数课：2T₂+T₁、E=T₂−T₀+U）
- `corr-20260928-18` / tm.t4.energy-criteria / `exposure_timing`：讲解发生在**更早的会话**（旧窗口），相对本次作答属作答前曝光；显式写目标级，不再依赖事件级回退。目标级字段原本不存在，故 from 记 null
  - 证据：旧窗口日志 old.jsonl seq1017 / seq2257（均早于 attempt-5 的 ts 2026-09-28）
- `corr-20260928-19` / (事件级) / `solution_exposure`：事件级汇总取该事件的实际曝光；本事件只有 tm.t4.energy-criteria 一个目标，且该目标已曝光（见 corr-20260928-17），故汇总不得为 none
  - 证据：learning/corrections.jsonl corr-20260928-17
- `corr-20260928-20` / tm.t4.energy-criteria / `note`：note 里的『无答案曝光』与已核实的历史讲解直接矛盾（§3a）。改写后：既记录曝光史，也保留 hint_level=0 与 needs_verify=true 的真实部分，不整条抹掉
  - 证据：旧窗口日志 old.jsonl seq1017 / seq2257

### attempt-8

| 范围 | 目标 | 字段 | 原值 | 修正值 | 来源 | 日期 |
|---|---|---|---|---|---|---|
| 目标级 | `ee.ac.phasor-impedance` | `note` | Q2：U = 311/√2（=220 V）、f = ω/(2π) = 314/(2π)（=50 Hz）、220 V 是有…（共 188 字，全文见 corrections.jsonl） | Q2：U = 311/√2（=220 V）、f = ω/(2π)（=50 Hz）、220 V 是有效值，正确。Q3：\|Z…（共 362 字，全文见 corrections.jsonl） | learner_statement | 2026-09-28 |

**理由与证据**

- `corr-20260928-12` / ee.ac.phasor-impedance / `note`：① 相位读图歧义已按学习者对原稿的确认消除，须保留来源且不再重复询问；② 『漏乘电流模值』经放大重读不成立，但按本地约定不把导师辨读当事实，故降级为待转写而非直接改判；③ 按学习者指示，不因这一处确认就把整个相量／阻抗目标计为独立通过
  - 证据：subjects/06-电工电子技术/作业/20260928-diag-Q123.jpg（3× 放大重读：_scratch/improve/zoom-diag-Q3b.png）

### attempt-9

| 范围 | 目标 | 字段 | 原值 | 修正值 | 来源 | 日期 |
|---|---|---|---|---|---|---|
| 目标级 | `ee.ac.series-rlc` | `hint_level` | 0 | 4 | photo_reread | 2026-09-28 |
| 目标级 | `ee.ac.series-rlc` | `needs_verify` | False | True | record_audit | 2026-09-28 |
| 目标级 | `ee.ac.series-rlc` | `exposure` | (无) | partial | record_audit | 2026-09-28 |
| 目标级 | `ee.ac.series-rlc` | `exposure_timing` | (无) | during_attempt | photo_reread | 2026-09-28 |
| 目标级 | `ee.ac.series-rlc` | `note` | Q4：ω = 314、U = 220 V、X_L = 2πfL = 4.8π Ω、Z = 20 + j4.8π，建模全对…（共 188 字，全文见 corrections.jsonl） | Q4 分两段记。【独立部分】ω = 314、U = 220 V、L = 4.8×10⁻² H、X_L = 2πfL = …（共 285 字，全文见 corrections.jsonl） | record_audit | 2026-09-28 |
| 事件级 | `—` | `max_hint_level` | 0 | 4 | record_audit | 2026-09-28 |
| 事件级 | `—` | `exposure_timing` | after_attempt | during_attempt | record_audit | 2026-09-28 |
| 事件级 | `—` | `error_hypothesis` | 五题的概念、建模与数值全部正确，无理解性错误。反复出现的唯一问题是『量名／单位标签』，共 3 处：①诊断 Q3(b) 把…（共 187 字，全文见 corrections.jsonl） | Q1、Q2、Q3、Q5 的概念、列式与数值全部正确；Q4 的 \|Z\| 与 I 两处留空后由导师代算（见 target_r…（共 224 字，全文见 corrections.jsonl） | record_audit | 2026-09-28 |
| 目标级 | `ee.ac.reactance` | `exposure` | (无) | none | photo_reread | 2026-09-28 |
| 目标级 | `ee.ac.phasor-impedance` | `exposure` | (无) | none | photo_reread | 2026-09-28 |
| 目标级 | `ee.ac.resonance` | `exposure` | (无) | none | photo_reread | 2026-09-28 |
| 目标级 | `ee.ac.resonance` | `exposure` | none | partial | learner_statement | 2026-09-28 |
| 目标级 | `ee.ac.resonance` | `exposure_timing` | (无) | unknown | learner_statement | 2026-09-28 |
| 目标级 | `ee.ac.resonance` | `needs_verify` | False | True | learner_statement | 2026-09-28 |
| 目标级 | `ee.ac.resonance` | `note` | Q5(1)：同相 ⟹ 谐振 ⟹ R = U/I = 100 Ω；İ = 1∠0° ⟹ U̇_C = −j180 V、U̇…（共 230 字，全文见 corrections.jsonl） | Q5(1)：同相 ⟹ 谐振 ⟹ R = U/I = 100 Ω；İ = 1∠0° ⟹ U̇_C = −j180 V、U̇…（共 520 字，全文见 corrections.jsonl） | learner_statement | 2026-09-28 |

**理由与证据**

- `corr-20260928-01` / ee.ac.series-rlc / `hint_level`：Q4 原稿的 |Z| = 与 İ = U̇/|Z| = 两处留空（照片可证），|Z| 与 I 由导师按学习者要求代算 —— 属示范剩余步骤，本次提示级别不是 H0
  - 证据：subjects/06-电工电子技术/作业/20260928-C2H2-Q4.jpg
- `corr-20260928-02` / ee.ac.series-rlc / `needs_verify`：本目标最终答案的两个数值不是学习者产出；按『辅导后做对 ≠ 独立掌握』记受助完成，待未见同类题复测
  - 证据：learning/attempts.jsonl:9 target_results[ee.ac.series-rlc].note（由导师代算）
- `corr-20260928-03` / ee.ac.series-rlc / `exposure`：代算即在反馈中展示了结果，属该目标自己的答案曝光（正是事件级 solution_exposure=partial 的来源）；显式记录，不再依赖事件级汇总回退
  - 证据：learning/attempts.jsonl:9 solution_exposure=partial
- `corr-20260928-04` / ee.ac.series-rlc / `exposure_timing`：两处代算发生在学习者列式之后、结果产出之前，即作答进行中；旧枚举只有 before/after，无法如实表达，故新增 during_attempt
  - 证据：subjects/06-电工电子技术/作业/20260928-C2H2-Q4.jpg
- `corr-20260928-05` / ee.ac.series-rlc / `note`：原 note 一面写『由导师代算』、一面保留 hint_level=0 与 needs_verify=false，自相矛盾；改为分列独立部分与受助部分，既不整题抹掉也不冒充独立
  - 证据：subjects/06-电工电子技术/作业/20260928-C2H2-Q4.jpg
- `corr-20260928-06` / (事件级) / `max_hint_level`：事件级 max_hint_level 是汇总值（取本事件最大帮助级别）：本事件存在 H4 级帮助（代算两个结果），原记 0 与事实矛盾。逐目标判定不受影响——其余目标的 hint_level 仍为 0
  - 证据：learning/corrections.jsonl corr-20260928-01
- `corr-20260928-07` / (事件级) / `exposure_timing`：事件级取最保守值：本事件存在作答进行中的曝光（代算）。四个目标的 exposure 均已显式记录，此汇总值不再驱动任何判定
  - 证据：learning/corrections.jsonl corr-20260928-04
- `corr-20260928-08` / (事件级) / `error_hypothesis`：原总评写『五题全部正确、无理解性错误』与同事件中 Q4 两处代算矛盾，属夸大独立性；同时删去已被否定的『诊断 Q3(b) 漏电流模值』一条（见 corr-20260928-12）
  - 证据：learning/corrections.jsonl corr-20260928-01 / corr-20260928-12
- `corr-20260928-09` / ee.ac.reactance / `exposure`：本目标 Q2/Q3 为独立完成，未获代算或展示；显式标 none，使其判定不再依赖事件级汇总回退
  - 证据：subjects/06-电工电子技术/作业/20260928-C2H2-Q4.jpg
- `corr-20260928-10` / ee.ac.phasor-impedance / `exposure`：本目标 Q1 为独立完成，未获代算或展示；显式标 none，使其判定不再依赖事件级汇总回退
  - 证据：subjects/06-电工电子技术/作业/20260928-C2H2-Q123.jpg
- `corr-20260928-11` / ee.ac.resonance / `exposure`：本目标 Q5 为独立完成，未获代算或展示；显式标 none，使其判定不再依赖事件级汇总回退
  - 证据：subjects/06-电工电子技术/作业/20260928-C2H2-Q5.jpg
- `corr-20260928-21` / ee.ac.resonance / `exposure`：原记 none（依据是作业照片）不成立：会话 bb092a33 的 seq429 在提交（seq436）之前明确提示『它是这套里唯一考“同相⇒谐振”的题』——判据链的关键一环在提交前已给出。故该目标存在答案/思路曝光
  - 证据：会话 bb092a33 seq429（提示原文）/ seq436（提交原文）；corr-20260928-11 的 exposure=none 依据不足
- `corr-20260928-22` / ee.ac.resonance / `exposure_timing`：**不猜时机**：提交时间（seq436）≠ 实际完成时间，无法判定该提示落在作答的哪个阶段（学习者可能已自行推出）。故显式记 unknown——这不是回避，而是唯一如实的取值；unknown 会阻断独立通过，符合『独立性待确认』。目标级字段原本不存在，from 记 null
  - 证据：会话 bb092a33 seq423（我在做第五题）/ seq429（提示）/ seq436（提交）
- `corr-20260928-23` / ee.ac.resonance / `needs_verify`：该目标本次不贡献独立通过（依据不足 + 已核实提示）。needs_verify=true 是本条的主机制，独立于 exposure 取值；补独立证据须用**未见同类题**
  - 证据：learning/corrections.jsonl corr-20260928-21 / corr-20260928-22
- `corr-20260928-24` / ee.ac.resonance / `note`：§3c：原 note 的『独立完成』与已核实的提交前提示矛盾。改写：保留答案正确与已完成部分，把独立性标为待确认，且不猜提示级别与曝光阶段
  - 证据：会话 bb092a33 seq423 / seq429 / seq436

### attempt-12

| 范围 | 目标 | 字段 | 原值 | 修正值 | 来源 | 日期 |
|---|---|---|---|---|---|---|
| 事件级 | `—` | `diagnosis_status` | pending_probe | confirmed | learner_statement | 2026-09-28 |
| 事件级 | `—` | `error_hypothesis` | 两处错，性质不同：①Q4 把 Q3 刚刚用对的『大小写自洽』规则丢了，改按『符号像不像电感』筛选项（A 含 X_L 看着…（共 237 字，全文见 corrections.jsonl） | 两处错因已定位（学习者 2026-09-28 答复后）：①Q4 = **记号规则未在同一份卷内迁移**——Q3 已按『大…（共 313 字，全文见 corrections.jsonl） | learner_statement | 2026-09-28 |

**理由与证据**

- `corr-20260928-13` / (事件级) / `diagnosis_status`：学习者 2026-09-28 答复了分辨问题：Q6『我看错了』＝ (a) 把灯 B、灯 C 各在哪条并联支路看反（读图错误，不是概念错误）；Q4 自述『大致搞明白』并确认正确选项为 C。两处错因均已定位，pending_probe → confirmed
  - 证据：会话 2026-09-28 学习者原话：『6我看错了，4我大致搞明白，你的答案是正确的』
- `corr-20260928-14` / (事件级) / `error_hypothesis`：原 error_hypothesis 把两种可能并列挂着『待分辨』；学习者已答复，按事实收敛为确定结论，避免同一件事在记录里留两种状态
  - 证据：会话 2026-09-28 学习者答复；照片 subjects/06-电工电子技术/作业/C2H1/微信图片_20260923151825_105_158.jpg（Q6 电路图）

### attempt-14

| 范围 | 目标 | 字段 | 原值 | 修正值 | 来源 | 日期 |
|---|---|---|---|---|---|---|
| 目标级 | `tm.t4.energy-criteria` | `note` | 题1（传送带 T = ½m(ẋ+v₀)²）：T₂ = ½mẋ²、T₁ = m v₀ ẋ、T₀ = ½m v₀² —— *…（共 297 字，全文见 corrections.jsonl） | 题1（传送带 T = ½m(ẋ+v₀)²）：T₂ = ½mẋ²、T₁ = m v₀ ẋ、T₀ = ½m v₀² —— *…（共 351 字，全文见 corrections.jsonl） | learner_statement | 2026-09-28 |
| 事件级 | `—` | `error_hypothesis` | 两类：①**符号类**（U 从 L 反推未变号）——与学习者自述『对系数包括正负处理非常不敏感』完全吻合，且是**结构性…（共 179 字，全文见 corrections.jsonl） | **本事件无错答**。传送带与移动悬点单摆两个新系统上，T₂/T₁/T₀ 与 U 全部正确（含首次独立分出非零 T₁）。…（共 310 字，全文见 corrections.jsonl） | learner_statement | 2026-09-28 |

**理由与证据**

- `corr-20260928-15` / tm.t4.energy-criteria / `note`：学习者 2026-09-28 澄清原意后撤销『U 符号错』判定：其答语『加号是从U来的』指的是 L 中该项为 −U（U 自身带负号，被 L=T−U 的减号中和），U = −mgl cosθ 判断正确。原记录把压缩答语读成 U = +mgl cosθ，属误读
  - 证据：会话 2026-09-28 学习者原话：『不是那个势能函数你理解错我的意思了，我就是说 U 提供负号中和了那一项本身的负号』
- `corr-20260928-16` / (事件级) / `error_hypothesis`：同上：撤销『符号类错答』的判定，改为『本事件无错答』，并从 state/mistakes.md 的『系数与正负号』证据里剔除本次
  - 证据：会话 2026-09-28 学习者澄清；corrections.jsonl corr-20260928-15

## 叙述与作废声明（5 条，不改字段、仅供阅读）

### 2026-09-27 — narr-20260927-01

2026-09-27 对 attempt-2 的判定订正（原文归档）：该条不改字段，而是确立字段语义 —— 学习者 2026-09-26 口述确认 U′(x) 写成加号；据此认定『错误推导碰巧得到正确结论，不能判为完整通过』。同时新增 solution_exposure（none/partial/full）与 exposure_timing，用以区分『反馈后见过正确式子』与『作答前已见过』；并新增 time_source，把助手估算从实测时长中拆出。事件本身未改。

### 2026-09-28 — narr-20260928-01

【旧结论作废声明】learning/attempts/corrections.md 在 2026-09-28 曾写过一条针对 attempt-8 / ee.ac.phasor-impedance 的结论：『needs_verify 由 true → false』『未化成小数与单位缺失不再记为缺口』。该结论与本文件 corr-20260928-12 冲突，**以本文件为准、旧结论作废**：needs_verify 保持 true，且单位/数值化一项不再由导师单方面改判。原因：旧结论把『学习者对原稿的口头澄清』直接当成了升级依据，并且没有进入任何程序可读的链路 —— 那正是本轮修掉的结构性问题（corrections.md 过去对 validate / derive / plan-week 均不可见）。

### 2026-09-28 — narr-20260928-02

记录规则（写给自己）：①结论正确 ≠ 推导正确 ≠ 独立完成，三者分开记；②反馈里展示过的内容即曝光，如实标注，曝光后照着改对不升级能力；③做到一半被代算属 during_attempt，不是 after_attempt；④时间：能计时的写 actual，学习者自述写 self_reported，助手估算写 estimated，不知道写 unknown，不把估计当实测；⑤订正只追加不改旧事件、不删照片，且**订正必须写进本文件**才可能影响判定。

### 2026-09-28 — narr-20260928-03

【证据依据降级声明 + 规则】corr-20260928-09/10/11 用**作业照片**推断『该目标未获代算或展示』，据此写了 exposure = none。**照片证明不了「作答前没有口头提示」** —— 这三条的**依据不足**，不应再被当作『未获展示』的证据引用。本轮处理：①只对 `ee.ac.resonance` 改判（该目标有**已核实的提示记录** bb092a33 seq429 → 独立性待确认，见 corr-20260928-21/22/23/24）；②`ee.ac.reactance`、`ee.ac.phasor-impedance` **不连带降级**——『依据不足』不等于『确实受助』，其 exposure 取值按 [待确认] 对待，列入待确认清单。规则（同步写入 learning/README.md）：**曝光与提示只能由会话记录或学习者确认，不得由作业照片推断**。

### 2026-09-29 — narr-20260929-01

【attempt-18 两处澄清 · 学习者 2026-09-29 答复】学习者原话：「那两点如实说明，我自己做的，我也不知道你他妈在说哪里读不准，可能是我划掉的。」据此收口两件事：①**closed_book**：学习者为**本人独立书写**（自述「我自己做的」，非抄录、非他人代笔）；但该答语**并未逐字回答「是否合上资料」**，且 `closed_book` **不在 `ALLOWED_EVENT_FIELDS`**（tools/learninglib.py:378）里、**无法用本文件订正** → attempts.jsonl 里的保守值 `false` **保持不动**（原始事件只增不改，不手改），本叙述即该字段的唯一真实来源；已另立 ISSUES-待改进.md 的 B7。⚠ **对判定零影响**：attempt-18 已被「提示H3 + 曝光 partial@before_attempt + 待核验」阻断独立通过，closed_book 取任何值都不改变等级，也**不会**计入 open_book_pass_dates（`is_open_book_pass` 仍为 False）。②**「读不准的那一行」关闭**：学习者说明那是**自己划掉的草稿**，不是最终答案行 → **不再要求逐字转写**，`[待确认]` 撤销；该题最终行「= −½ Σ_{n=0}^{∞}(z/2)ⁿ − (1/z) Σ_{n=0}^{∞}(1/z)ⁿ」维持**正确**判定。

---

生成命令：`python -B tools/render_corrections.py`
