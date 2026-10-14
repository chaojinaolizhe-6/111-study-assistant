# 待改进问题清单（ISSUES）

> **用途**：把运行中发现的**系统性问题**集中写在这里，供**第三方改进检查**时一眼看到。
> **为什么不写进聊天**：聊天记录会丢、远端前端顺序会乱；工作区文件才是权威记录。
> **谁写**：辅导会话（教学窗口）与维护会话都可以追加。**只追加、不改旧条目**；修好后在条目末尾标 `✅ 已修（日期 + 依据）`。
> 建立：2026-09-28（学习者要求："最好是在工作空间中用文本特别写一下这些出现的问题，这样第三方改进检查的时候能够简单看到"）。
> 同期更详细的代码复核见 `_scratch/improve/核查报告-20260928.md`。

---

## A. 台账 / 流程类（**最高优先**：会让学习内容静默丢失）

### A1. 自述文件是"死信"——写进去的缺口没有任何消费者
- **现象**：`subjects/学习进度-自述-2026-09-26.md` 自称"作为跨科规划的暂定依据"，但**没有任何程序或流程读它**。
- **后果**：自述里列出的缺口**没有一条**被转成任务、复习项或计划条目。
- **证据**：该文件 50 行完整存在；`learning/tasks/` 里没有光学/延拓/留数/课件对照的任何任务。
- **同类**：与 `corrections.md` 曾经的问题同源（写进去、无人读）。`corrections.md` 已于 2026-09-28 由 `tools/render_corrections.py` + `learning/corrections.jsonl` 修好，**自述文件尚未**。

### A2. 活动层完全由"截止日期"驱动 → 无截止的科目自动消失
- **现象**：有截止的科目动，没截止的不动。
- **证据**：`AGENTS.md` STATUS 的 `current_subject` 只有 3 科；`plan/week-plan.md` 只出现 `01-理论力学`、`06-电工电子技术`、`03-微分方程`。其余 6 科（02/04/05/07/08/09）在活动层零出现。
- **后果**：学习者自己提出的缺口（见 A5）随着时间从视野消失。

### A3. `progress.md` 规则"挂着不执行"
- **规则原文**：`subjects/*/progress.md` 表头写"会话记录由学习助手在每次学习/复习/测验后追加（rep + 反思 + 下一步）"。
- **实际**：**9 个 `progress.md` 全部停留在 2026-09-23 16:39**，五天零更新——包括 2026-09-28 大量活动的 01-理论力学。
- **问题**：挂着不执行的规则比没有规则更坏——它会让人以为有记录。**要么真写，要么废止并改写规则。**

### A4. 复习机制未建立（学习者明确要求过）
- **学习者原话（2026-09-26）**："电工学学得还行，就是感觉非常容易忘记，我可能需要有计划地定期复习。"
- **现状**：`state/due.md` = **0 个到期概念**；`state/mastery.json` 仅 **2 个概念**。
- **结论**：SM-2 队列基本是空的，"定期复习"从未落地。

### A5. 被遗漏的具体缺口（自述里有、活动层里无）
| 科目 | 自述原文缺口 | 现在的追踪状态 |
|---|---|---|
| 02-光学 | "没什么思路…感觉老师讲得很乱" | 仅存在于 `subjects/INDEX.md` 表格，**无任务、无计划、STATUS 不出现** |
| 04-数理方法1 | "级数章没很好掌握，**尤其延拓我没学明白**"、"**第四章（留数）还没学**" | 同上 |
| 03-微分方程 | "老师课件里有很多**知识库没有的方法**，我可能还需要掌握" | 同上（`ode-if-baseline-01` 是一阶线性基线，不是这条） |
| 06-电工 | "非常容易忘记，需要有计划地定期复习" | 见 A4 |

### A6. 记录端规则落后于判定端（**已实际造成一次误判**）
- **现象**：`.tutor/config/teaching-conventions.md:25` 仍写"答案曝光程度（none/partial/full、**发生在作答前还是反馈后**）"——只有**两种**时机。
- **但**：`tools/learninglib.py:223` 与 `learning/README.md:76,78` 已支持第三种 `during_attempt`，且它**阻断**独立通过。
- **后果**：写事件的窗口（教学会话）按旧规则办事，会把"做到一半被代算"记成 `after_attempt` → 而 `after_attempt` **不阻断** → **该目标静默升级为"独立通过"**。
- **已发生**：`attempt-9` 的电工 C2H2 Q4，事后靠 `corr-20260928-04` 才补回。
- **修法**：`teaching-conventions.md` §2 第 4 项改为三值并写明阻断规则；或删掉该处描述、只留指向 `learning/README.md` 的指针（避免同一规则两处实现）。

---

### A7. 考点覆盖无台账：注册了的目标没有题、没注册的考点直接消失（**学习者 2026-09-30 提出**）

- **学习者原话**：「而且第四章课件还有一点没处理，我们最后的相似性没说，动量也没考，角动量守恒也没考，我不知道你在干什么，所以这一点我在想你是不是可以总结成一个问题放在工作空间，下次改进我们调整，要是你就完全忘记了那几个考点，就是明显的问题，要是你有准备但是还没做，那就是学习体验很差的问题。」
- **核查结果（四类，性质不同，别混成一句"忘了"）**：

  | 考点 | 目标是否存在 | 实际状态 | 性质 |
  |---|---|---|---|
  | 拉格朗日量的构造（从情境写 L） | ✅ `tm.t3.lagrangian-construction` | **0 次作答、等级"未测"** —— 目标建了，**从未出过一道题** | **有准备、没执行**（学习者说的第二种） |
  | 动量守恒（空间均匀性 → 循环坐标 / 广义动量） | ✅ `tm.t4.cyclic-momentum` | 2 次作答（`attempt-4`、`attempt-7`），**两次都是 `full@before_attempt` 全曝光 + partial** → 仍停"需支持" | **有准备、验证方式失效**（与 E1 同源） |
  | 角动量守恒（空间各向同性，L⃗ 与投影守恒） | ❌ **不存在** | `subjects/01-理论力学/topics/T04-守恒定律.md` 页地图有 p25–29，**无任务、无验收、无目标** | **从未进入系统** |
  | 力学相似（2T = kU、时间标度 t′ = λ^(1−k/2)t） | ❌ **不存在** | 页地图有 p30–35（**且这 6 页从未读图**），**无任务、无验收、无目标** | **从未进入系统** |

- **根因**：`T04-守恒定律.md` 有**课件页地图**和"本节要会什么（三件事）"，但**没有任何消费者**——页地图只是给人看的叙述，
  **没有把「每个考点 → 一条带 acceptance 的任务 → 一次无提示作答」这条链建起来**。系统只追踪**困难（hurdles）**与**作业（HW）**，
  于是**没被诊断成困难的考点就静默消失**。与 **A1**（自述是死信）、**A2**（活动层只由截止驱动）、**A5**（被遗漏的具体缺口）同源。
- **后果（可复查）**：Topic 4 五个部分里，**③动量、④角动量、⑤力学相似三块没有任何一条独立证据**；
  考试若考到，属"没准备"而不是"没学会"。**能量判据一/二**是唯一被真正验收过的部分。
- **建议（待学习者确认后再执行，不擅自扩范围）**：
  1. 在 `T04-守恒定律.md` 建 **T04 考点覆盖表**，每考点三态：**已讲 / 已练 / 无提示通过**；**每次理力会话收尾检查一次未覆盖项**；
  2. 缺的目标先与学习者确认再建（候选 `tm.t4.angular-momentum`、`tm.t4.mechanical-similarity`）——按 `learning/README.md`，能力目标**不编造**；
  3. `tm.t3.lagrangian-construction` **必须出题**（现有目标 0 题＝纸面目标）；
  4. 动量 / 角动量 / 力学相似各出 1 道**无提示、闭卷、未见变式**题，**不得复用** `attempt-4`/`attempt-7` 已全曝光的题；
  5. **优先级（学习者 2026-09-30 指定）**：**先做完数学物理方法第三章（孤立奇点），再回来处理 L 的构造** —— 本条目**本轮不启动**。

---

## B. 判定链路 / 代码类（2026-09-28 代码复核发现）

> 复核方式：只读 + 只读校验（`validate_*`、`render_corrections --check`、`py_compile`）。以下每条都给了文件行号。

- **B1（fail-open）** `tools/learninglib.py:330`：`if exposure != "none" and timing != "after_attempt"` —— 只有 `after_attempt` 放行。**独立性判定完全押在一个手写字段上，无任何交叉校验。** 建议：`exposure != none` 时默认 `needs_verify = true`（fail-closed）；低成本替代是让 `session-close` 打印"`final=correct` 且 `exposure≠none` 且 `timing=after_attempt`"的抽查队列。
- **B2（防漂移有洞）** `tools/learninglib.py:478`：`if current == data["to"]: continue  # 已应用：幂等` —— 但该函数**总是拿原始记录**调用（`tools/validate_attempts.py:76`），原始记录里不可能已含订正后的值。故 `current == to` 只可能是**空操作或 `from` 记错**，不是"已应用"；这样的订正会被**静默接受**（既不报错也不生效）。修法：仅当 `from == to` 才算合法空操作，否则按 `from` 不一致报错。
- **B3（声明与实现不符）** `tools/derive_state.py:164-166`：版本元数据缺失的事件 `continue`，只计入 `unknown_version_events`，**不进 `upgrade_blocked`** —— 与"每个未升级事件都列出事件号、日期与具体原因"的说法不符。（当前 `unknown_version_events` 全为 0，不影响现有数字。）
- **B4（验证会改数据）** `tools/plan-week.py:355-357`：**无条件**重写 `learning/repair-queue.json`；`--out` 只管主产物。跑一次"验证"就改了数据（2026-09-28 实际发生：队列 2 条 → 5 条）。建议加 `--dry-run` / `--no-write-queue`。
- **B5（第四个消费方未纳入）** `tools/sync_status.py:23,78`：不导入订正层，直接读原始记录。**今天无害**（只用 `ts`、事件条数、hurdles，其余取自已订正的 `learner-state.json`），但没有不变量保证；一旦订正白名单加入 `ts`，STATUS 会与派生结果静默分歧。
- **B7（字段不可订正：closed_book）** `tools/learninglib.py:378` 的 `ALLOWED_EVENT_FIELDS` **不含 `closed_book`**，而它正是**升级的必要条件之一**（`independence_blockers` 在 `closed_book is not True` 时阻断）。
  - **后果**：记录时若按保守值填了 `false`，事后即使**学习者本人确认**其实是闭卷，也**无法通过 `corrections.jsonl` 订正**——只能留一条叙述条目，字段永远停在错值上。这与"订正是订正的唯一事实源"的设计目标不符。
  - **已实际发生**：`attempt-18`（2026-09-29）——导师按"未知不填成有利值"填了 `closed_book=false`，学习者随后答复「我自己做的」，但该字段改不了（见 `corrections.jsonl` 的 `narr-20260929-01`）。本次**无实际损害**：该事件已被 `hint_level=3` + `exposure=partial@before_attempt` + `needs_verify` 阻断，取任何值都不改变等级，也不会进 `open_book_pass_dates`。
  - **建议**：把 `closed_book` 加入 `ALLOWED_EVENT_FIELDS`（它由**学习者本人确认**，性质与 `solution_seen` 同类）；或至少在 `check_corrections` 报"不允许订正"时**说明该走哪条路**（现在只报错，不给出路）。
- **B6（规则不可满足）** `AGENTS.md` 写"`CLAUDE.md` 必须**逐字镜像**"，但两文件互指对方文件名，**必然有 4 行不同**（实测 79 行中 L1/L40/L44/L63）。应改为"**除互指文件名外**逐字一致"。
- **B8（并发会话会撞 `event_id`，撞号后没有安全出路）**（2026-09-30 实际发生）
  - **机制**：`tools/append_attempt.py` 的重复检查只认 `learning/attempts.jsonl` 里**已存在**的 id，**没有取号/预留机制**；`event_id` 又**不在** `ALLOWED_EVENT_FIELDS`（同 B7）→ 事后**无法订正**。而"预留"只写在**人读文本**里（当日计划、hurdle 的 note），程序看不见。
  - **已发生**：俄语会话按"下一个空号"写了 `attempt-24`，但 `plan/today-2026-09-30.md` 已把 `attempt-24` **文字预留**给理论力学判据二复测（"暂不写入"）；随后**并行的**物理会话实际占了 `attempt-25`。俄语会话只能**物理删掉刚追加的那一行**再以 `attempt-26` 重写（备份：`learning/attempts/_backup_before_renumber.jsonl`），`attempt-24` 成为**空号**。
  - **风险**：两条会话同时取到同一个号时，第二条会被拒（防重复计分本身是对的），但**被拒的一方要么丢记录、要么改号后与散落各处的文字引用不一致**。
  - **建议**：①`append_attempt.py` 加 `--event-id auto`（扫描取"最大号 +1"，**写入前再校验一次**）；②把"预留"落成**机器可读**文件（如 `learning/attempts/_reserved.json`），当日计划与 hurdle 都引用它；③撞号被拒时**打印下一个可用号**以及"哪些文件引用了旧号"，或把 `event_id` 加入可订正字段。
  - **附带教训**：并发会话下**任何"先读后写整个文件"的动作**（本次的删除重写）都有覆盖对方新行的风险——本次未覆盖（当前 25 行含对方的 `attempt-25`），但这是**运气**，不是机制。
  - **与 D4 的关系**：这是同一事件的另一半记录（D4 讲"并发写同一状态库"，本条讲"取号无机制 + 号不可订正"）。D4 曾把俄语事件读成"静默丢失"，**已在 D4 后追加澄清**：实为俄语线**主动撤回重编号**（`attempt-24` → `attempt-26`），`attempt-24` 成为空号。两条记录不矛盾，别当成两起事故。

---

## C. 冷启动指令与事实源不一致

- **两套脚本并存**：
  - `.tutor/core/scripts/`（8 个，来自 upstream 模板）：`concept-graph` `evaluate-learning` `evolve-tutor` `plan-review` `refresh-status` `validate-core` `validate-instance` `validate-study`
  - `tools/`（13 个，本地改造）：`plan-week` `sync_status` `session-close` `validate_attempts` `derive_state` `learninglib` 等
- **冲突点**：`AGENTS.md` 的 "Sync Rules" 指向 `.tutor/core/scripts/validate-study.py` 与 `refresh-status.py`；而**本工作区本地约定**的收尾指向 `tools/session-close.py`。功能重叠（refresh-status ↔ sync_status；plan-review ↔ plan-week；validate-* ↔ validate_attempts/hurdles）。
- **风险**：新会话按冷启动读 `AGENTS.md`，可能走**旧脚本族**，与当前事实源（`learning/attempts.jsonl` + `learning/corrections.jsonl` + `tools/`）不一致。**未实测**（没有运行 `.tutor/core/scripts/` 下的脚本，它们会写 `AGENTS.md`）。
- **建议**：明确哪一族是权威，另一族标"历史/勿用"或删除；`AGENTS.md` 的 Sync Rules 与本地约定统一到同一套。

---

## D. 环境 / 客户端类

- **D1. 远端客户端不渲染 `$...$`**：显示为字面美元符号。已定案改用**纯 Unicode 数学**，规则见 `.tutor/config/teaching-conventions.md` §6（2026-09-28 重定）。证据链：官方前端在**流式阶段**用不含 math 的 `parseGfm`（`@deepseek-ai/dsh-client-ui-primitives/lib/index.js:6786`，注释 "no math"），消息结束后才 finalize 换 `parseGfmWithMath`（`:6798`）走 KaTeX（`:6970`）；remote 插件 `ds-harness-remote@0.4.17` 只有 `facets.host`，全 dist 搜 `katex|markdown|marked|remark|micromark` **0 命中** → 插件不参与对话渲染。
- **D2. 远端前端消息顺序错乱**（学习者 2026-09-28 报告："没有给我反馈正确的对话顺序"）→ 应对：**以工作区状态文件为权威记录，聊天窗口不是**。
- **D3. 时间基准双轨**：系统时钟为英国时间，学习者在中国大陆（+7h）。所有"今天/截止"按中国时间判定，规则见 `.tutor/config/time-environment.yml`。易错点：跨午夜时两者差一天。

- **D4. 两条会话线并发写同一状态库（无并发保护，2026-09-30 实测）**：学习者在**两个对话**并行学习（本线＝理论力学/数理方法，另一线＝电工实验/俄语），
  但两线**写的是同一套文件**：`learning/attempts.jsonl`、`learning/learner-state.json`、`learning/hurdles.jsonl`、`plan/*`。
  - **实测时间线（中国时间 2026-09-30）**：① 本线读到 `attempt-24` = **俄语 `ru-adj-qword-01`** 事件（`subjects/07-俄语/作业/2026-09-30-独立检验1-作答照片.jpg`）；
    ② 数分钟后本线追加自己的事件时被**正确拒绝**（`REFUSED: event_id 'attempt-24' 已存在` —— 去重保护生效 ✅）；
    ③ 本线改用 `attempt-25` 写入成功；④ 再读时 **`ru events: []`** —— 那条俄语事件**已不在文件里**，
    `derive_state` 的 `by_level` 也随之回退（`未测` 2→4、`曾独立完成` 7→6）。即：**已落盘的作答事件在几分钟内消失**。
  - **现有保护只覆盖一半**：`append_attempt.py` 有 `event_id` 去重与"先校验后写入、失败回滚"，**有效**（本轮亲测）；
    但 `derive_state.py` / `sync_status.py` / `session-close.py` / 手写 `hurdles.jsonl` **没有任何锁或版本检查**——
    两条线各自 `derive_state` 会互相覆盖 `learner-state.json`，**STATUS 与叙述文件也可能一写一改**。
  - **风险**：事件静默丢失或重复计分；`learner-state.json` 被写入较旧的一次派生结果（等级与"独立通过日期"看起来倒退）；
    `AGENTS.md`/`CLAUDE.md` 的 STATUS 是两线共用的一块，后写者覆盖先写者。
  - **建议（择一，需学习者拍板）**：① **单写者约定** —— 只有一条线做"记账/派生"（另一条线只产出作答与照片，交由本线统一入账）；
    ② 或加**写锁/版本戳**（`_scratch/.writelock` + 写入前比对 mtime/哈希，冲突则拒绝并提示）；
    ③ 至少在 `session-close.py` 里打印"本次运行前后的 `attempts.jsonl` 行数与 mtime"以便发现竞态。

> **追加（2026-09-30，俄语线）**：D4 时间线里「④ 再读时 `ru events: []` —— 那条俄语事件已不在文件里」**不是竞态导致的静默丢失，而是俄语线主动撤回重编号**。经过：俄语线先按「下一个空号」写了 `attempt-24`；随后发现 `plan/today-2026-09-30.md` 已把 `attempt-24` **文字预留**给判据二复测 → 为不占用该号，**主动删除自己刚追加的那一行**（撤回前备份：`learning/attempts/_backup_before_renumber.jsonl`），改以 **`attempt-26`** 重新写入（`append_attempt.py` 校验通过）。因此：①俄语事件**在库里**（`attempt-26`，`ru-adj-qword-01`，quiz/闭卷/H0）；②`attempt-24` 现为**空号**（原预留项实际记在 `attempt-25`）；③D4 观察到的 `by_level` 回退是**那几分钟的临时状态**，`derive_state` 重跑后已恢复（收尾时 `targets=20`，俄语两目标已计入）。**D4 的结论仍然成立**（并发写确实危险）；只是本例的"消失"是**人为重编号**，不是丢失 —— 两条记录并存，不矛盾。
>
> **又一例（同一天）**：`AGENTS.md` / `CLAUDE.md` 的 STATUS 叙述行**被并发编辑回退过一次** —— 俄语线写入的 ⑧ 子句在几分钟后消失（对方用的是写入前读到的副本）。俄语线已于收尾后**重写并核对两文件一致**。这正是 D4 第 3 条（写锁/版本戳）想解决的问题：**叙述行没有版本检查，后写者覆盖先写者**。

### D5. 组合附加符号（`⃗`）在客户端显示为方框 —— **规则写过但没写成通则，于是又犯**（2026-10-01 学习者截图反馈）

- **现象**：导师 2026-10-01 那条"叉乘证明链"整篇用 `a⃗`、`e⃗₁`、`r⃗ₐ` 之类写法 → 学习者屏幕上显示成"**方框 + 字母**"，反馈"看着很难受，是不是网络波动"。
- **根因**：`a⃗` 里的 `⃗` 是 **U+20D7 COMBINING RIGHT ARROW ABOVE**（组合附加符号，要贴在字母上显示）。本客户端对**组合符号**支持不良 → 回退成方框（□）。
- **不是网络问题**；也与 D1（`$...$` 不渲染）同族：**都属于"客户端渲染能力"这一类**，但 D1 是"数学定界符"，本条是"字符集/字体"。
- **规则其实早写过一半**：`.tutor/config/teaching-conventions.md` §6 在 2026-09-28 就写了「**θ、φ 用 `dθ/dt`（避开组合变音符）**」——但只举了两例、**没写成通则**，所以 2026-10-01 又犯。
- **已修（2026-10-01）**：§6 增设"**向量**"一行（一律不加上箭头；强调向量用**粗体**），并补 2026-10-01 实测追加块
  （禁用**一切组合附加符号** `⃗ ̂ ̇`；列出安全字符白名单；`ℝ`/`∧`/`⊗` 列为可疑待观察）。
- **建议（留给第三方改进检查）**：把"渲染安全字符白名单"从"经验条目"升级为**可执行检查** ——
  例：在 `tools/write_check.py` 里加一条"**检测组合附加符号**（U+0300–U+036F、U+20D0–U+20FF）并在写入前告警"，
  这样就不必依赖导师记忆（人一忘就复发，本条即例证）。

---

### D6. `web_fetch` 在本机**必然失败**：Clash Verge 的 fake-IP 触发 SSRF 护栏（**2026-10-02 实测**）

- **现象**：`web_fetch` 对**任何**域名都返回 `URL hostname "X" resolves to a non-public IP address`。
  2026-10-02 会话内 6 次尝试 **6 次失败**（`github.com`、`raw.githubusercontent.com`、`cdn.jsdelivr.net`、
  `eric.ed.gov`、`www.semanticscholar.org`、`ieltsidpindia.com`）——**错误文案一模一样**。
- **实测证据（DNS A 记录）**：

  | 域名 | 解析结果 |
  |---|---|
  | `github.com` | `198.18.0.42` |
  | `raw.githubusercontent.com` | `198.18.0.121` |
  | `cdn.jsdelivr.net` | `198.18.1.50` |
  | `www.cambridgeenglish.org` | `198.18.1.51` |
  | **`www.baidu.com`** | **`198.18.1.41`** |
  | `dsh.r2049.cn` | `198.18.1.52` |

  **全部落在 `198.18.0.0/15`** —— IANA 保留的**基准测试网段**，非公网地址，不可能是这些站点的真实 IP。
- **机制**：本机运行 `clash-verge-service`（PID 6060），系统代理 `127.0.0.1:7897`，DNS 处于 **fake-IP 模式**
  （对任何域名先返回 `198.18.x.x` 假 IP，真实连接由代理按规则转发）。
  `web_fetch` 在发请求前会做一次 DNS 解析并**拒绝非公网 IP**（防 SSRF 的标准护栏）→
  **假 IP 触发护栏 → 每一个域名都被拒**。**与"网站是否存在、是否被墙"无关。**
- **为什么 `web_search` 不受影响**：搜索走 harness 自己的检索后端，**不在本机解析目标域名**。
- **同源但独立的第二道墙**：沙箱内进程的 **TLS 不可用**——`curl.exe` 与 `git ls-remote`
  报同一句 `schannel: AcquireCredentialsHandle failed: SEC_E_NO_CREDENTIALS`（`http_code=000`），
  `Invoke-WebRequest` 报"基础连接已经关闭"。**因此命令行下载同样不通。**
- **影响**：**任何"让助手联网抓取/下载"的任务都做不了**（文档抓取、仓库下载、在线资源核对）。
- **可行的绕过（按成本从低到高）**：
  1. 用户在浏览器里复制内容粘贴给助手；
  2. 用户浏览器下载文件后放进工作区（助手再读）；
  3. 改代理 DNS：`enhanced-mode` 由 `fake-ip` 改 `redir-host`，或把目标域名加入 `fake-ip-filter` 例外
     —— **改完可立即用一条 DNS 命令重测**。
- **状态**：⏳ 未修（需用户侧改代理配置；助手不擅自改系统网络设置）。

- **⚠ 2026-10-02 复核补充（修正本条上面的两处措辞，原条目保留不改）**：
  1. **不得据进程名断定学习者用的是哪款软件**。`clash-verge-service`（PID 6060，路径读不到）只能说明
     「**某个 Clash 系内核的后台服务在跑**」；学习者明确表示**自己不用 Clash Verge**，其客户端只有
     「智能模式／全局模式」两个开关。**进程名 ≠ 用户认知的软件名**——助手凭一个进程名就写出软件名，是过度推断。
  2. **测量有方法论盲区**：上面所有 DNS 探针都是**在沙箱内**执行的，因此**无法区分**两种来源：
     (a) 整机 DNS 被本地代理接管；(b) **只有沙箱进程**的 DNS 被拦截。
     关键旁证在沙箱里拿不到——`Get-DnsClientServerAddress` 返回空、`Get-NetAdapter` 报"拒绝访问"、
     `Get-NetTCPConnection` 报"拒绝访问"。**所以"改用户代理配置"这条建议，前提并未被证实。**
  3. **仍然确定的部分**：18 个域名（含 `example.com`、`www.qq.com`、`api.deepseek.com`、`www.baidu.com`）
     **全部**解析进 `198.18.0.0/15`，且同一域名两次解析结果一致 → 这是 **fake-IP 池**的确定性特征，
     **不是"被墙域名才有的现象"**（连 `api.deepseek.com` 也是假 IP）。
  4. **「智能模式／全局模式」开关大概率无效**：它管**流量路由**（哪些走代理、哪些直连），
     不管 **DNS 解析**；fake-ip 属 DNS 层设置，通常不在这个开关里。**不建议学习者为此折腾。**
  5. **结论修正**：在能拿到"整机 DNS 配置/网卡列表"这类旁证之前，本条**只应记录现象与两条可用替代路径**
     （浏览器复制粘贴／浏览器下载后放进工作区），**不应给出"改代理即可修复"的确定性建议**。

- **⚠ 2026-10-02 二次补充（工具层结论，可定案）**：
  - `web_fetch` 的实现在 **`@deepseek-ai/dsh-web-fetch-http`**，是**本机 HTTP 抓取**：
    `lib/index.js:4` 用 `node:dns/promises` 的 `lookup` **在本机解析域名**，
    `lib/index.js:69` **无条件**要求"任何解析结果都必须是公网单播地址"，否则抛 `WEB_BLOCKED_URL`
    （错误文案："URL hostname ... resolves to a non-public IP address"）。
  - 该 provider 的**可配置项只有** `maxResponseBytes`／`maxBodyChars`／`timeoutMs`／`maxRedirects`／`userAgent`
    （见其 README「Minimal configuration」）——**没有**"允许私网／走代理／自定义 DNS"这类开关。
    **因此不存在"设置一下就能让抓取走服务器"的办法。**
  - 该安装中**只有这一个 fetch provider**（包清单里无 `dsh-web-fetch-remote` 之类的远端实现）；
    而 `web_search` 走的是 **`dsh-web-search-deepseek`（远端后端）**——
    **这就是「搜索一直能用、抓取一直不能用」的结构性原因**，与网站是否可访问无关。
  - 在 DSH 全部已安装包中检索 `198.18` → **0 命中**，故 `198.18.0.0/15` **不是 harness 硬编码**，
    来源仍在本机网络层（Clash Verge Rev 配置 `dns_config.yaml:6-7` 与当前 profile 均写
    `enhanced-mode: fake-ip` + `fake-ip-range: 198.18.0.1/16`，与观测吻合；
    但 `verge.yaml:19` TUN 关闭、`ProxyEnable=0`、日志停在 2026-09-04 → **仍未能定案**）。
  - **定案办法（用户侧、沙箱外、10 秒）**：在普通 CMD 里执行 `nslookup github.com`——
    若返回 `198.18.x.x` 则是本机代理改写；若返回真实公网 IP，则**没有任何开关可修**，
    只能走"用户浏览器下载／复制粘贴"路径。**不要再让用户为此改代理设置。**

## 附：本清单的维护约定

1. **只追加**，不删旧条目；修好后在条目末尾标 `✅ 已修（日期 + 依据文件/行号）`。
2. 每条尽量带**可复查的证据**（文件路径 + 行号 + 实测输出），不写"感觉"。
3. 与学习事实相关的条目，同时在 `learning/` 或 `.tutor/config/` 建立关联，避免"清单里修了、规则里没改"。

---

## 2026-09-28 维护窗口（独占写入）结果

> 按本清单约定**只追加**：未改任何旧条目，在此集中记录已修与被修的内容。
> 快照：`backups/2026-09-28-before-maintenance/`（156 文件）；方案：`_scratch/improve/执行方案-20260928b.md`。

### ✅ 已修

| 条目 | 修法 | 依据 |
|---|---|---|
| **A1**（自述文件是死信） | **部分**：新增 `plan/gaps.md` 承接自述里**学习者明确提出**的缺口（每条有状态 + 下次查看触发点）。自述文件本身**尚未**加回链指针 | `plan/gaps.md` |
| **A6**（记录端规则落后判定端） | `teaching-conventions.md` §2 第 4 项不再重复"两种时机"，改为**指向** `learning/README.md` 的指针；并写入"曝光不得由作业照片推断" | `.tutor/config/teaching-conventions.md` |
| **B3**（声明与实现不符） | `derive_state.py` 的 `meta is None` 分支现在也写入 `upgrade_blocked`（reason＝版本元数据缺失） | `tools/derive_state.py` |
| **B4**（验证会改数据） | `plan-week.py` 新增 `--dry-run` / `--no-write-queue` | `tools/plan-week.py` |
| **B6**（镜像规则不可满足） | AGENTS/CLAUDE 改为"**除互指文件名外**逐字一致"（实测仍只有 L1/40/44/63 四行不同） | `AGENTS.md` / `CLAUDE.md` |
| **A5**（被遗漏的具体缺口） | 同上，并入 `plan/gaps.md` | `plan/gaps.md` |

### ⏳ 本轮**未**修（留给下一轮，不缩小范围假装完成）

| 条目 | 现状 |
|---|---|
| **B1**（fail-open：独立性判全押在 `exposure_timing`） | **未修**。本轮只做了数据侧补救（attempt-5 曝光史、resonance 待确认），**fail-closed 机制没动**。建议仍是：`exposure != none` 时默认 `needs_verify = true`，或让收尾打印抽查队列 |
| **B2**（防漂移残余洞） | **未修**。`check_corrections` 的 `current == to` 仍在 `from` 检查**之前**短路；`from==to` 之外的空操作仍会被静默接受 |
| **B5**（第四消费方未纳入订正层） | **未修**。`sync_status.py` 仍直接读原始记录；今天无害，但无不变量保证 |
| **A2**（活动层只由截止驱动） | **未修**。`gaps.md` 让无截止科目不至于消失，但 STATUS/周计划的驱动逻辑没改 |
| **A3**（9 个 `progress.md` 挂着不执行） | **未修**。仍停在 2026-09-23 16:39。要么真写、要么废止规则 |
| **A4**（复习机制未建立） | **未修**。`state/mastery.json` 概念集仍为空、`due.md` 仍为 0；学习者"需要定期复习"仍未落地 |
| **C**（两套脚本并存） | **未修**。`AGENTS.md` 的 Sync Rules 仍指向 `.tutor/core/scripts/`；与本地约定（`tools/`）并存 |

### 📌 本轮另外更正的**教学事实**（不在原清单里，由学习者复核发现）

1. **泰勒/洛朗判据错**：会话 bb092a33 L2504/L2523 的「中心有有限值 → 泰勒」**不充分、已作废**；正确为「中心附近是否**解析**」+「**指定区域**」两个条件。已改 `learning/tasks/mp1-ch3-quiz-01.md` §②、`learning/hurdles.jsonl` 的 `hurdle-2`、`plan/today-2026-09-28.md`。
2. **T₀/U「来源」口诀**：已降为**本题线索**并补反例（势能本身可含外部速度）；改 `hurdle-1.note`。
3. **attempt-5 曝光史**：原记"无答案曝光"不成立（旧窗口 seq1017/2257 已讲并套用过**同一题**），已订正 3 个字段 + note。
4. **`ee.ac.resonance` 独立性待确认**：seq429 在提交（seq436）前已给关键提示；不猜时机，记 `exposure=partial @ unknown` + `needs_verify=true`。
5. **订正传播**：新增 `tools/correction_impact.py`（**确定性关联**，不做关键词判定），并入 `session-close.py`；清掉 `tm-t4-criteria-03.md`、`state/mistakes.md` 里的已撤销结论。
6. **排期去重**：`ee-lab1-prep` 两个身份合一（120 → 60 分钟）；已交作业移出排期；悬空引用 `plan/today-2026-09-29.md` 已消除。

### 2026-09-28 验收尾项（第二轮，学习者复核后指出）

> 学习者只读抽查后指出 4 项未达验收标准，已全部补完并自检通过（自检脚本 `_scratch/improve/verify_round2.py`）。

| # | 问题 | 修法 |
|---|---|---|
| 1 | **泰勒/洛朗的"更正稿"仍不准确**：还写着「去心圆盘→洛朗」「可去奇点跟能不能泰勒是两件事」「换中心才换刀」——等于把两者教成**由区域形状决定的互斥选项** | 改写为：**泰勒是洛朗的特例**（负幂系数全 0）；中心解析则可泰勒，**限制到去心圆盘同一个泰勒展开仍然有效**；**可去奇点补定义后可以泰勒**（判可去要看**去心邻域解析且有界**，"单点有有限值"不够）；区域只决定"哪个展开在该区域收敛"。同步改 `hurdle-2`、`plan/today-2026-09-28.md`、`.tutor/config/status-narrative.yml`（note 里第一版说法也一并换掉，避免又留两套）。<br>**第三轮（学习者再指出）**：第 2 条仍留「要求的区域是外部 ⟹ 必须换成洛朗」，与 `e^z` 矛盾。已按学习者表述定稿：**是否有负幂项不能由"区域是外部还是圆环"来判断**；泰勒级数在其收敛圆盘内有效、限制到其中任一圆环仍有效；只有**不可去的孤立奇点**在充分小去心邻域才**必有非零负幂项**，可去奇点负幂系数全 0、补定义后可泰勒。并写入 `e^z` 在 `\|z\|>1` 仍由同一泰勒级数表示的**检验**；`1/(1−z)` 的内外对照保留，但理由改为"泰勒圆盘被最近奇点挡在半径 1 以内"（原写法"奇点落在外部区域内"不成立——`z=1` 在圆环 `1<\|z\|<∞` 的**内边界**上）。§③ 洛朗实操同步加"这是手法、负幂项来自函数奇性"的区分 |
| 2 | **旧交接文件仍会把进度倒退**（还写 H4.1 待订正 / H4.3 差最后一步 / 符号三次 / 判据二未验收 / 电工截止待确认） | `plan/handoff-prompt-2026-09-28.md` 顶部加 **⛔ 已作废、勿复制** 横幅；新建 **`plan/handoff-CURRENT.md`** 作为唯一续学入口。并纠正："**没有 `tm-h4-02` 编号 ≠ H4.2 进度未知**"——H4.2 的作答记在 `tm-t4-criteria-01`（同一 L）的 `attempt-3`，**作业照片可证已写完** |
| 3 | **判据二被重复安排 3 轮**（criteria-01/02/03 各 20 分钟 = 60，而实际状态是"补讲完成、待延迟复测"） | `tools/plan-week.py` 的修复队列改为**按目标合并**：同一目标只出一条"**错因覆盖复测**"（覆盖 3 个历史题目，20 分钟），历史 `first_seen` 仍按 (题目,目标) 保留在 `repair-queue.json` |
| 4 | **`--dry-run` 仍会写 `--out`**（默认输出就是正式周计划，容易误操作） | `--dry-run` 改为**真正不写任何文件**（不写 `--out`、不写队列，只打印预览）；`--no-write-queue` 保留"仍生成计划、只不写队列"的语义。实测两项行为均正确 |

**遗留项不扩大**：`B1`（fail-open）、`B2`（防漂移残余洞）、`B5`、`A2`、`A3`、`A4`、`C`（两套脚本并存）仍**未修**，留待后续集中处理。
下一轮建议（学习者指定）：落实**少量复测的具体时间与读取入口**，不再扩大维护清单。

---

## E. 教学 / 出题设计类（2026-09-28 教学窗口追加）

### E1. 复习清单把待考内容的答案原样列出 → 检验退化成开卷（**本轮实际发生**）
- **现象**：教学窗口给学习者写的复习清单 `learning/tasks/mp1-ch3-quiz-01.md` §① 里，直接列出了五个标准展开的**完整式子**（`1/(1−w) = 1 + w + w² + …`、`e^z = Σ zⁿ/n!`、`sin z`、`cos z`、`ln(1+z)`）、各自的成立范围，**以及比值法公式 `R = lim|aₙ/aₙ₊₁|`**。随后又**用同一批内容出题**（该文件 §二蓝图）→ **等同开卷考**。
- **后果**：该轮（`attempt-15`）的"答对"**不构成掌握证据**，已如实记 `solution_exposure=full` + `exposure_timing=before_attempt` + `needs_verify=true`。
  本轮真正有信息量的只有 **Q1(a)**——**在有答案可查的情况下仍然算错**（`Σ zⁿ/(n·2ⁿ)` 答 R = "2/z"，正确 R = 2），说明该点是理解/运算问题而非记忆问题。
- **建议规则**：① 复习清单只给「**范围 + 要会做什么**」，**不给待考题的答案本身**；② 若学习者明确要求给答案（示例学习），**该内容不得再作为验收题**，验收必须另出「同技能、不同数、不提前给式子」的题；③ 出题前先自检「这道题的答案是否已经在我给出的材料里出现过」。
- **关联**：`learning/tasks/mp1-ch3-quiz-01.md` §①（复习范围）与 §二（验收蓝图）内容重叠，是本条的载体。

---

## 2026-09-30 维护窗口（系统维护，非教学）结果

> 按本清单约定**只追加**：未改任何旧条目。
> 快照：`backups/2026-09-30-before-maintenance/`（87 文件，含 `_SHA256SUMS.txt`）。
> 本轮方案与验收脚本：`_scratch/improve/`（隔离副本 `_scratch/improve/sandbox/`）。
> 范围：P0（状态一致性 / 记录可信 / 并发写）→ P1（课程覆盖 / 复习排期）。**未开始新学科教学、未打包、未改客户端。**

### ✅ 已修

| 条目 | 修法 | 依据（可复查） |
|---|---|---|
| **P0-1 状态多处各写一份、互相矛盾** | 新增 **`state/current.md`（当前状态唯一事实源）**，由 `tools/current_state.py` 从 `learning/` 重算；`AGENTS.md/CLAUDE.md` 的 STATUS 与 `plan/handoff-CURRENT.md` 改为**引用**它。冷启动顺序与导航已指向它 | `state/current.md`、`tools/current_state.py`、`tools/handoff.py` |
| **P0-1 交接文件过期到自相矛盾** | `plan/handoff-CURRENT.md` 改为**生成物**（静态协议 + 动态引用 + 人工意图）；旧手写快照必然过期的问题从机制上消除（原先写"孤立奇点完全未开始"，实际已有 `attempt-27～31`） | `tools/handoff.py`、`plan/handoff-CURRENT.md` |
| **P0-1 状态更新失败仍宣称已同步** | 收尾统一为 `tools/session-close.py`（11 步逐步报告），新增**第 10 步一致性核对**：STATUS 计数 vs 派生状态、镜像规则、**事实源指纹**三者任一不符 → FAIL | `tools/session-close.py` |
| **P0-2 `attempt-28` 记录与真实帮助情况不符** | 核对原始会话（`session-a46ca69d` seq387 早于 seq394 提交）后，用 `record_correction.py` 写入 **corr-20260930-01～10**：`mode` quiz→practice、`max_hint_level` 0→2、`solution_exposure` none→partial、`exposure_timing` null→before_attempt（**事件级 + 目标级都改**）；并把 `attempt-29.diagnosis_status` confirmed→**pending_probe**；追加 `narr-20260930-01` 作废旧结论。**原始事件未改未删、未重编号、未把有提示改成无提示** | `learning/corrections.jsonl`、`learning/attempts/corrections.md` |
| **B7（`closed_book` 字段不可订正）** | `ALLOWED_EVENT_FIELDS` 加入 `closed_book` 与 `mode`；新增订正后**不变量检查**（`quiz` 只允许 H0——事实是"测验中给过提示"时必须改 `mode` 而不是把 hint 写回 0） | `tools/learninglib.py` |
| **B2（防漂移残余洞）** | `current == to` 不再**无条件**短路（旧写法把 `from` 写错的订正静默接受）；只有 `from == to` 才算合法空操作 | `tools/learninglib.py` |
| **B1（fail-open：独立性判全押 `exposure_timing`）** | 改为 **fail-closed**：`exposure != none` 且时机缺失/`unknown` → **阻断**；`after_attempt` 仍放行（反馈后曝光不污染此前独立表现）；另加"升级必须留下可追溯依据"（`target_results[tid].note` 或 `artifact_ref`） | `tools/learninglib.py`、`_scratch/improve/test_failclosed.py`（11 项全过） |
| **B8（并发撞号 + 号不可订正）** | 取号改为**机器可读**：`learning/attempts/_ids.json` 计数器 + 扫描实际最大号，取较大值 +1，**全程在锁内**；`--event-id auto`；被拒时打印下一个可用号。**不再靠人读文本预留** | `tools/append_attempt.py`、`tools/workspace_lock.py` |
| **D4（两条会话线并发写同一状态库）** | 新增跨进程锁 `learning/.write.lock`（`O_CREAT|O_EXCL` + 残留锁回收）+ 原子替换写 + **读-改-写 CAS**；`append_attempt` 改 **append 模式**（只追加自己那一行，不重写整个文件）；`derive_state`/`sync_status`/`coverage`/`handoff`/`schedule` 全部加锁 + 原子写；`learner-state.json` 带**事实源指纹**，旧快照覆盖可被检测 | `tools/workspace_lock.py`、`_scratch/improve/test_concurrency.py`（13 项全过） |
| **A7（考点覆盖无台账 / 目标静默消失）** | **根因修掉**：`derive_state` 现在**读 `learning/goals.yaml`**（新增 `tools/goallib.py`），目标集合 = 目标声明 ∪ 题目 ∪ 历史版本 ∪ 事件；新增 `learning/coverage.md` 覆盖台账，含**"已声明但一道题都没有"**单列一节 | `learning/coverage.md`、`tools/coverage.py`、`tools/derive_state.py` |
| **A7 附带：一个"等级"挤掉四件事** | `learner-state.json` 每个目标新增 `status_dimensions`：**①作业完成 ②概念困难是否解决 ③独立作答表现 ④延迟检验结果**，另加 `coverage` 与 `tasks`；`state/current.md` 分开呈现 | `tools/derive_state.py`、`state/current.md` |
| **A4（复习机制未落地）** | `due_today` 不再正则匹配 `state/due.md`（生成产物，永远 0），改为**扫描 `subjects/**/topics/*.md` 的 `due`**（`tools/reviews.py`，与排期共用一份实现）；新增 **`plan/schedule.md`**：把"两天后再测"落成**带最早开始/截止/设备/预计时长**的日期化任务 | `tools/reviews.py`、`tools/schedule_reviews.py`、`plan/schedule.md` |
| **A2/A3 相关：已完成事项赖着不走** | `reviews.load_task_due_dates` 过滤掉**已作答/已提交**的题与 assignment（原先已做完的题一直在"已逾期"刷屏） | `tools/reviews.py` |
| **C（两套脚本并存）** | `AGENTS.md/CLAUDE.md` 的 Sync Rules 与导航改为指向 `tools/` 一族；`.tutor/core/scripts/` 明确标注**已停用**（不删除，保留上游溯源） | `AGENTS.md`、`CLAUDE.md` |
| **D3（时区）** | 新增 `tools/timebase.py`（中国大陆 UTC+8，IANA 换算，不写死差值）作为**所有日期判定的唯一入口**；排期/收尾/结转一律用中国日期 | `tools/timebase.py` |
| **E1 同类（写文件踩半角引号）** | 新增 `tools/write_check.py`：用**真解析器**（`compile` / `json.loads`）做写前自检，替换掉启发式（启发式误报太多）。本轮据此拦下 2 处 `tools/*.py` 语法错误 | `tools/write_check.py` |

### 本轮**订正的教学事实**（由学习者原始会话核实，非猜测）

1. **`attempt-28` 的帮助史**：导师在提交前已点名第 4 题的解法方向，原记 `H0 + 无曝光` 与原文矛盾 → 已订正（见上表）。
2. **"缺口机制已确认"降级**：该结论依赖"学习者不知道第 4 题要展开"这一前提，前提已被推翻 →
   `diagnosis_status` 由 `confirmed` 降为 `pending_probe`。
   **仍成立的部分**：`attempt-30`（H0、闭卷、换过函数）第 3 题仍失败 → 机制是**高支持度假说**，待无提示变式定案。
3. **等级与结案状态均未改动**：`mp.isolated-singularity` 仍 `需支持`、`hurdle-2` 仍 `awaiting_retest`、
   第三章仍**未宣告收口**——本轮只改"记录与事实是否一致"，**没有为让检查通过而提高任何学习状态**。

### ⏳ 本轮**未**修（不缩小范围假装完成）

| 条目 | 现状 |
|---|---|
| **A3**（10 个 `progress.md` 挂着不执行） | **未修**。仍停在 2026-09-23/09-30 少数几次更新；要么真写、要么废止规则，需学习者拍板 |
| **A1 尾部**（`subjects/学习进度-自述-2026-09-26.md` 未加回链指针） | **未修**（`plan/gaps.md` 已承接其缺口） |
| **B5**（`sync_status` 未导入订正层） | **部分**：计数改从事实源重算，但 `sync_status` 仍直接读原始 `attempts.jsonl` 取 `ts`/条数（今日无害，无不变量保证） |
| **B3 尾部**（`upgrade_blocked` 的表述与实现细节） | 已按 2026-09-28 修法保留；本轮未再动 |
| **`state/due.md`** | **已不再是 `due_today` 的来源**（改为扫 frontmatter）；该文件本身未删，仍可作为"上一次生成快照"；是否废止待定 |
| **`.tutor/core/skills/`** 下的上游技能文件 | 未改；其中 `capability-session/SKILL.md` 仍是教学模式的权威描述，但**其字段说明以 `learning/README.md` 为准** |

---

## F. 英语（雅思）项目适配相关（2026-10-02 数据层审计发现，**只读审查代码，未改任何文件**）

> 背景：为新增的英语项目要记录**连续分档**（雅思 0–9，0.5 一档）与**过程指标**（听写词级正确率、每分钟词数、停顿次数、自我纠正次数、四类错误占比），
> 而现有事件模型的判定字段是枚举（`correct|partial|incorrect`）。审计问题：能否**加法式**加入，而不破坏现有 10 门课。

### F1. `append_attempt.py --dry-run` **并非只读** —— 会写计数器
- **现象**：`tools/append_attempt.py:121-130`，`bump_counter` 在 dry-run 返回**之前**执行。
- **后果**：违反「dry-run 只读」契约；事件编号出现空洞（不是数据损坏，但「试跑」会改变后续取号）。
- **建议修法**：把 bump 移到 dry-run 分支之后；或 dry-run 时只计算 next-id、不落盘。
- **状态**：⏳ 未修。

### F2. 上游 `validate-core.py` 在文件缺失时会**创建** `state/reviews.jsonl`
- **现象**：`.tutor/core/scripts/validate-core.py:369-372`；`tools/validate_study_scoped.py` 仍会调用它。
- **后果**：名为"校验"的操作有副作用（创建文件）。而 `state/reviews.jsonl` 现为 **0 字节**、活动工具链不读它。
- **状态**：⏳ 未修（需与既有「上游模板脚本已停用」的口径一并处理）。

### F3. 校验强度**分层不一致**：目标级是白名单，事件顶层不是
- **现象**：`target_results[tid]` 内未知键 = **ERROR 硬拒收**（`tools/validate_attempts.py:138-140` + 白名单 `tools/learninglib.py:263-266`；`append_attempt.py:148-165` 写后校验失败会**回滚该行**）；
  而**事件顶层未知键完全不检查**（`validate_attempts.py:87-89` 只查 REQUIRED 是否缺失）→ 顶层乱加键会被**静默接受**、永久留在 `attempts.jsonl`，且**不能用 `record_correction.py` 订正**（`learninglib.py:439-450` 的 `ALLOWED_EVENT_FIELDS` 白名单）。
- **后果**：磁盘上可能积累无人读、也无法订正的字段；"严格校验"只在目标级成立。
- **建议**：明确策略——要么顶层也做白名单/WARN，要么在 `learning/README.md` 写明「顶层允许扩展键」的**意图**，别让它是偶然的。
- **状态**：⏳ 未修。

### F4. 事实源指纹**不覆盖** `goals.yaml` / 题目 frontmatter / `hurdles.jsonl` / `policy.yml`
- **现象**：`tools/derive_state.py:375-395` 的 sha256 只覆盖 `attempts.jsonl` + `corrections.jsonl` 的**原始字节**；`session-close.py:74-83`+`133-134` 的一致性核对只验 `state/current.md`。
- **后果**：改这些文件**不会 FAIL**，但若不重跑收尾就会**静默陈旧**。
  （本次新增目标 `ielts-english-75` 即属此类——已当场重跑 `session-close` 收口，非遗留问题。）
- **建议**：把 `goals.yaml` / `hurdles.jsonl` / `policy.yml` 纳入指纹或纳入第 10 步核对范围。
- **状态**：⏳ 未修（本次以「改完立即重跑收尾」规避）。
