# 111学习助手 v4.0 架构跃迁计划书（供本地 GPT 深度评审版）

> **文档路径**：`D:\aaa_D_usual\DSH\111学习助手\PLAN-v4.0-架构升级计划书-供GPT评审.md`
> **工作区根目录**：`D:\aaa_D_usual\DSH\111学习助手`
> **当前版本基线**：v3.0（已完成只读/同步边界分离、收尾入口统一、未学门禁与可读性三段式升级，26 项回归测试全绿）
> **评审请求**：请本地 GPT 结合工作区内的真实脚本与数据文件，重点审查本计划在 **事实源防污染、能力判定严谨性、脚本耦合风险、以及认知减负有效性** 上是否存在漏洞或边界冲突。

---

## 零、 评审员文件导航表（全部真实路径，可直接读取核验）

为避免“只看计划书文字、无法验证脚本实现”，以下列出本计划涉及的全部核心文件相对路径（均相对于 `D:\aaa_D_usual\DSH\111学习助手\`）：

| 层级 | 核心文件相对路径 | 当前职责与关键实现位置 |
| :--- | :--- | :--- |
| **总规则与入口** | `AGENTS.md` / `CLAUDE.md` | 全局路由与铁律；两文件受 `tools/sync_status.py:42` `mirrored_except_names()` 强制要求除互指文件名外逐字镜像。 |
| **主技能与协议** | `.dsh/skills/tutor-assistant/SKILL.md`<br>`.tutor/core/protocol.md`<br>`.tutor/core/skills/capability-session/SKILL.md`<br>`.tutor/core/skills/prepare-materials/SKILL.md`<br>`.tutor/config/teaching-conventions.md` | 定义日常辅导、备课、测验与提示阶梯（H0–H4）。<br>⚠ 注意：`.tutor/docs/课件与教材协同学习.md` 与 `.tutor/config/knowledge-base.md` 被 `tools/chapter_guide.py:122` `policy_sha()` 计算 SHA256 指纹，改动会使既有章节地图变为 `stale`。 |
| **能力事实源（只追加）** | `learning/attempts.jsonl`（当前 50 条）<br>`learning/corrections.jsonl`（当前 17 条）<br>`learning/hurdles.jsonl`（当前 3 条）<br>`learning/observations.jsonl` | 核心事实源，受 `tools/derive_state.py` 的 `source_fingerprint()` 指纹保护，严禁直接手改历史行。入账唯一入口为 `tools/append_attempt.py`。 |
| **目标与策略配置** | `learning/goals.yaml`（当前 68 个 target）<br>`learning/policy.yml`<br>`learning/curriculum.json`（48 份资料）<br>`learning/materials.json` | 声明能力目标、掌握判定参数（`min_dates: 2, min_variant_passes: 1, min_delay_days: 2`）及课件范围。 |
| **核心派生与校验脚本** | `tools/learninglib.py`<br>`tools/derive_state.py`<br>`tools/coverage.py`<br>`tools/current_state.py`<br>`tools/reviews.py`<br>`tools/tutor_context.py`<br>`tools/chapter_guide.py`<br>`tools/material_reader.py`<br>`tools/session-close.py`<br>`tools/session-close-and-sync.py`<br>`tools/test_tutor.py`（26 个单元测试） | 负责状态派生、到期扫描、上下文汇总、章节备课校验与 12 步原子收尾。 |
| **学科进度与讲义** | `subjects/01-理论力学/progress.md`<br>`subjects/02-光学/progress.md`<br>`subjects/03-微分方程/progress.md` 等 | 记录各科课堂日志与「老师已讲 / 我已看过 / 能独立完成」三态表。 |

---

## 一、 前因后果：为什么要从 v3.0 走向 v4.0 架构跃迁？

### 1. v1–v2 阶段解决了什么？（防自欺与可复算账本）
早期 AI 辅导的最大问题是“顺着学生哄”——学生看懂了导师给的例题、或者在 H3 提示下写出一步，AI 就判定“已掌握”，甚至跨窗口丢失进度。为此，v1–v2 建立了一套极其严密的 **事件溯源能力账本（Event-Sourced Capability Ledger）**：
- 严格区分 **事务状态**（交了作业）与 **能力证据**（闭卷、H0 无提示、无事前曝光 `exposure=none`、隔天延迟变式通过）；
- 引入 `session-close.py` 12 步流水线，保证所有状态卡（`state/current.md`、`learning/coverage.md`、`STATUS` 块）100% 由脚本从 JSONL 事实源重算。

### 2. v3.0 阶段刚刚修补了什么？（消幻觉、理边界、顺表达）
在实际使用 DeepSeek 执行该 Skill 的过程中，暴露出两个体验痛点与五处规则边界瑕疵，已在 v3.0 修复：
1. **修补“未学幻觉”**：修复了 `tools/coverage.py:170` 将“有题但 0 次作答”标为 `进行中` 的缺陷（现改为 `未开始（0次作答）`），并在 `tools/tutor_context.py:14-85` 增加了对 `0 次作答目标` 及 `subjects/*/progress.md` 三态表中 `❌/未讲/未学` 条目的强制扫描与【未学门禁】。
2. **修补“提示不好读”**：消除了规则文档的分号电报体传染，确立了「① 定位与肯定 → ② 独立成行的纯 Unicode 公式与同类最简数字小例子 → ③ 唯一明确的下一步动作 + 底部单行状态栏」的三段式规范，并新增 `tools/cross_verify.py` 双角色审校。
3. **理清只读/收尾/冲突/失败边界**：采纳本地 GPT 上一轮的 5 条评审建议，隔离了只读任务与 Git 同步，统一对外收尾入口为 `tools/session-close-and-sync.py`。

### 3. 为什么 v3.0 仍然不够？（核心矛盾：重审计、轻建图、高摩擦）
尽管 v3.0 修好了 Bug，但从工作区沉淀的真实数据来看，系统目前处于一种 **「高强度记账，但低效率闭环」** 的结构性僵局：
- **数据证据 1**：`learning/attempts.jsonl` 已有 **50 条作答事件**，累计估算投入超过 1200 分钟，但 `learning/learner-state.json` 中 **`迁移通过 = 0/68`，`稳定证据 = 0`**，有 **41 个目标长期卡在 `needs_verify` 或 `未升级`**。
- **数据证据 2**：`learning/curriculum.json` 登记了 **48 份课程/教材资料**，但 `learning/chapter-guides/` 下真正完成备课建图的 **只有 `tm-topic-04.json` 1 份（占比 2.1%）**，其余 47 份全部为空（`units: []`）。
- **数据证据 3**：运行 `python -B tools/tutor_context.py` 时，系统报告 **`当前可做/到期任务：89`**，大量零散旧目标与未学目标混杂在一起刷屏。

**一句话总结前因后果**：
现有系统是一个 **「满分教务审计员」**（擅长判定“你这次不算独立掌握”），但还不是一个 **「高效的理工科认知教练」**（没能在课前帮 DeepSeek 真正脱机备好课，没能在课中先给学生建立全章方法决策树，也没能在课后提供低摩擦的 60 秒复测通道来消掉 `needs_verify`、沉淀考前防坑笔记）。这就是 v4.0 要解决的根本问题。

---

## 二、 现有系统的四大结构性瓶颈（附源码级定位）

### 瓶颈 A：备课与对话严重耦合，DeepSeek 在线即兴发挥导致注意力稀释
- **现状定位**：`tools/chapter_guide.py` 设计了极佳的章节备课缓存校验机制（校验 PDF `sha256`、`text_read_pages`、`visual_read_pages`、`formula_verified_pages`），但因为它要求导师在对话过程中手工一页页调 `material_reader.py` 再拼装复杂的 JSON，导致除了 `tm-topic-04.json` 之外，**没有任何其他章节成功生成过 `chapter-guide` 缓存**。
- **后果**：当学生学习《光学》《常微分方程》《数学物理方法1》《电工电子》或《理论力学》Topic 5 时，DeepSeek 必须在同一个对话回合内同时干 4 件事：① 现场抽取/阅读 PDF 页面 → ② 现场推导并心算公式 → ③ 思考教学切入点 → ④ 遵守 30 条记账与防曝光规则。在有限上下文注意力下，DeepSeek 极易顾此失彼。

### 瓶颈 B：缺乏自顶向下的「全章方法决策树」与课后「个人防坑晶体」沉淀
- **现状定位**：在 `subjects/01-理论力学/progress.md:42` 中，学习者曾明确抗议：*「这是学第 5 讲，不是“补最小集”；我需要完整的学习指引」*。
- **后果**：
  1. **课前缺森林**：现有 `capability-session` 默认直接切入单题单步，缺少在开章时先给出 **「本章核心物理/数学矛盾 → 2–3 个母公式 → 题型特征到解法的决策树（If-Then Schema）」**。
  2. **课后无结晶**：学习者在 50 次作答中暴露了非常典型的个人失分模式（例如：`attempt-50` 微分方程分离变量除以 `sin u + 1` 漏常数奇解、三重特征根漏写 `x²` 因子；光学凹透镜牛顿式把物方焦点方向搞反；理力求驻点符号 `x₀` 与初值撞车）。这些记录散落在 `attempts.jsonl` 的 `note` 字段和各科 `progress.md` 中，没有被自动汇总成每门课一页的 **《考前 5 分钟个人防坑与题型决策速查卡》**。

### 瓶颈 C：`reviews.py` 待办扫描逻辑把「未学目标」与「已过期琐碎题」全部推入今日到期队列（89 项噪音）
- **现状定位**：请审查 `tools/reviews.py` 的 `load_capability_retests(root, today)`（第 73–126 行）：
  ```python
  # tools/reviews.py 第 92-112 行现状：
  if not tasks:
      kind, reason, not_before = "建题", "目标已声明但**一道题都没有**（纸面目标）→ 先出题", today
  elif has_independent and not delay.get("satisfied"):
      ...
  elif needs_verify:
      kind, reason, not_before = "撤去帮助再测", "历史作答全部 needs_verify（受助/曝光）→ 需要无提示新题", today
  else:
      kind, reason, not_before = "补练", f"覆盖状态「{target.get('coverage')}」→ 继续练到能独立", today
  ```
- **三处逻辑缺陷**：
  1. **未过滤 `迁移通过` 目标**：如果某个目标未来达到了 `迁移通过`（`has_independent=True`, `delay['satisfied']=True`, `variant_passes >= 1`, `open_hurdles=[]`），它会直接落入第 110 行的 `else` 分支，被标为 `kind="补练", due=today`！也就是说，**哪怕全部学会了，待办数也永远不会减少**。
  2. **未区分「未学（0次作答）」与「已学待复测」**：全部 26 个 `attempts == 0` 的未学目标（含 8 个无题目的雅思/ODE目标和 18 个有题未学的目标），每一天都会以 `due = today` 进入 `all_review_items()`，导致 `tutor_context.py` 每天报出 89 个到期任务。
  3. **缺少旧切片题被综合题覆盖（`superseded`）的归档机制**：9 月下旬生成的单步切片题（如 `tm-t4-criteria-03`），在学习者已经进入后续章节或做完综合诊断后，仍永久挂在逾期列表榜首。

### 瓶颈 D：缺乏低摩擦的「60 秒单步微复测（Micro-Retest）」机制，导致 `needs_verify` 无法消解
- **现状定位**：根据 `learning/policy.yml` 与 `tools/derive_state.py:11-23`，一个目标要从 `需支持` 升级到 `曾独立完成` 乃至 `迁移通过`，必须有至少 1 次（稳定需 2 个不同日期，间隔 ≥ 2 天）满足 `closed_book=true`、`hint_level=0`、`exposure=none`、`needs_verify=false` 的正确作答，且其中至少 1 次来自 `kind ∈ {delayed-variant, mixed}` 的未曝光新题。
- **痛点**：规则本身非常科学，但**执行载体太重**。目前 `learning/tasks/` 里的题目大多是 15–30 分钟的多步综合大题（还常需手写拍照）。学习者平时赶新课作业已经满负荷，极难抽出整块 20 分钟重做旧大题，导致 41 个做过的目标永久卡在 `需支持（待核验）`。

---

## 三、 v4.0 架构升级方案（四大核心模块与精确文件改动）

> **核心设计原则**：
> 1. **不动摇事实源底座**：`learning/attempts.jsonl`、`corrections.jsonl`、`hurdles.jsonl` 的格式、锁机制、SHA256 指纹校验以及 `learning/policy.yml` 的独立掌握标准 **100% 保持原样，绝不放水**。
> 2. **把重活移到后台脚本，把清爽留给对话**：通过新增/升级 Python 工具完成离线备课、队列降噪、错因提炼与 60 秒微复测出题。

---

### 模块 1：修复待办噪音与三级队列分流（修改 `tools/reviews.py` + `tools/tutor_context.py`）

#### 1.1 修改文件与行号：`tools/reviews.py`（第 73–126 行 & 第 241–265 行）
1. **修复 `迁移通过` 漏过滤 Bug**：在 `load_capability_retests()` 开头（第 83 行后），若 `target.get("level") == "迁移通过" and not open_hurdles`，直接 `continue`（已达标目标转入 SM-2 记忆维护队列，不再每天生成“能力补练”待办）。
2. **将 `attempts == 0` 的未学目标从「每日能力再测队列」中剥离**：
   - 若 `target.get("attempts", 0) == 0`（即 `未安排（无题目）` 或 `已安排·未作答`），它属于 **「新课待开荒（untaught_backlog）」**，而不是 **「能力再测（retest）」**！
   - 在 `load_capability_retests()` 中，仅对 **`attempts > 0`（已学过但未独立通过、或待延迟复测）** 及 **存在 `open_hurdles`** 的目标生成再测条目。
   - 新增独立函数 `load_untaught_backlog(root: Path) -> list[dict]` 专门统计 0 次作答目标，供规划（`/plan`）使用，不再混入每日 `due_items` 造成 89 项刷屏。

#### 1.2 新增任务状态 `superseded`（已被综合题覆盖/归档）支持：`tools/reviews.py`（第 145–150 行）
- 在 `load_task_due_dates()` 中，目前只跳过 `task.get("status") == "done"`。
- 改为跳过 `task.get("status") in ("done", "superseded", "archived")`（同时在 `learning/README.md` 登记该合法状态值，不修改历史事件，仅用于未作答旧题的排期降噪）。

#### 1.3 `tools/tutor_context.py` 输出升级：每日「3+1 焦点视图」
- 将原来笼统的 `当前可做/到期任务：89` 拆分为清晰的三个优先级桶：
  1. **`🔥 刚性截止（外部作业/考试 & 本周到期题）`**（最多展示前 3 项）；
  2. **`⚡ 今日 60 秒微复测候选（已满足 ≥2 天延迟、可一键消掉 needs_verify 或升格的目标）`**（每次只精选 **1–2 项**，避免认知过载）；
  3. **`📦 后台待补练池`**（仅报总数，不刷屏）。

---

### 模块 2：60 秒单步打字微复测引擎（新增 `tools/micro_retest.py`）——合法打通 `0/68 → 迁移通过`

#### 2.1 为什么要单独建这个工具？
为了让学习者不用手写 20 分钟大题拍照，就能合法满足 `learning/policy.yml` 的严苛要求（`closed_book=true`, `hint_level=0`, `exposure=none`, `kind=delayed-variant`），我们需要一种 **「高信度、单步靶向、纯打字 60 秒可答完」的微变式题（Micro-Variant Task）**。

#### 2.2 工作原理与严格合规边界（请本地 GPT 重点审查此机制是否符合 `derive_state.py`）
1. **选点逻辑（`python -B tools/micro_retest.py --pick [--subject <科目>]`）**：
   扫描 `learning/learner-state.json`，筛选满足以下条件的目标 `tid`：
   - **情形 A（首张独立门票）**：`attempts > 0`，当前等级为 `需支持`（历史作答因 `hint_level > 0` 或 `exposure != none` 被阻断），且距离最近一次作答日期 `ts` 已满足 `today >= last_ts`；
   - **情形 B（跨日延迟升级门票）**：当前等级为 `曾独立完成`（已有 1 个独立通过日期 `d₁`），且 `days_between(d₁, today) >= min_delay_days (2天)`，正等待第 2 个不同日期的 `delayed-variant` 独立通过以直接升格为 **`迁移通过`**！
     > 📌 *实测数据支撑*：当前账本中，如 `ee.ac.phasor-impedance` 在 `2026-09-28` 已有 1 次独立通过，早已满足 `≥ 2 天` 跨度，只需 1 道未曝光的 `delayed-variant` 即可成为全库第一个 `迁移通过`！
2. **微变式题生成与落盘（`python -B tools/micro_retest.py --generate --target <tid>`）**：
   - 读取该目标的历史错因/卡点（来自 `attempts.jsonl` 的 `target_results[tid].note` 与 `hurdles.jsonl`）；
   - 自动在 `learning/tasks/` 下创建一道正式的轻量任务文件 `learning/tasks/micro-<tid>-<YYYYMMDD>.md`：
     - Frontmatter 严格遵守现有规范：`kind: delayed-variant`、`status: open`、`est_minutes: 3`、`target_ids: [<tid>]`；
     - **题干设计原则**（由脚本调用 DeepSeek API 生成并强制经 `tools/verify_math.py` 验算数值）：不做冗长背景铺垫，直接给出全新简单数值/参数，只考该目标最核心的那一个判断或一步计算（学习者直接打字一行即可作答，耗时 1–3 分钟）。
3. **批改与入账闭环**：
   - 学习者在聊天框直接打字报出答案（不给任何提示 `hint_level=0`，提交前不泄题 `exposure=none`）；
   - 核对无误后，导师调用现有的标准入口 `python -B tools/append_attempt.py --file <事件.json> --event-id auto --submission-id <ID>` 写入 `attempts.jsonl`（`active_minutes` 记实际 1–3 分钟，`time_source: "actual"`）。
   - **合规性结论**：完全复用现有 `append_attempt.py` 与 `derive_state.py`，零后门、零篡改，但把复测摩擦从 25 分钟降到了 60 秒！

---

### 模块 3：离线备课与章节认知包编译器（新增 `tools/compile_chapter_pack.py`）

#### 3.1 解决的问题
把 DeepSeek 从“边聊天边现翻 PDF”的窘境中彻底解放出来，将 `learning/curriculum.json` 中那 47 份还没建图的资料变成**预编译的高质量教案**。

#### 3.2 输入、处理流水线与输出路径
- **命令接口**：
  `python -B tools/compile_chapter_pack.py --chapter <chapter_id> [--textbook <教材路径>] [--pages <页码范围>]`
- **四步自动化流水线**：
  1. **PDF 提取与视觉扫描**：调用现有的 `tools/material_reader.py`（`prepare` + `render`），提取指定章节课件 PDF 的文本层与公式密集页图像，记录真实的 `text_read_pages` 与 `visual_read_pages`。
  2. **结构化章节地图生成（落盘 `learning/chapter-guides/<chapter_id>.json`）**：
     对齐课件小节与 `learning/goals.yaml` 中的 `target_ids`，通过 `tools/chapter_guide.py` 的 `save()` 接口写入（自动满足 `validate()` 与 `study_policy_sha256` 校验），同时补齐 `learning/curriculum.json` 中对应章节的 `units` 列表。
  3. **算术与公式交叉核验**：对课件中的核心例题与待编译母题，调用 `tools/verify_math.py` 与 `tools/cross_verify.py` 校验符号约定与正负号分支。
  4. **生成人读与 AI 授课双用《章节认知包》**：
     落盘路径：`subjects/<课程名>/讲义/<chapter_id>-章节认知地图与决策树.md`，固定包含 4 个标准区块：
     - **区块 ① 全章一页纸心智模型（Why & Big Picture）**：本章解决什么旧方法解决不了的矛盾？核心算子/守恒量是什么？
     - **区块 ② 题型特征 → 方法决策树（If-Then Schema 表）**：看到题干什么条件 → 选哪个公式 → 第一步设什么变量 → 边界自检看哪里。
     - **区块 ③ 符号与正负号红线表**（如凹透镜焦距与牛顿式 `x, x′` 方向、拉氏量循环坐标判据等，纯 Unicode 独立成行排版）。
     - **区块 ④ 三级预设脚手架（H1/H2/H3 平行小例子缓存）**：提前为本章每个 `target` 准备好 1 个最简数字平行小例子。对话授课时，助手直接读取该文件即可给出高质量 H2 提示，无需现场临时编造！

---

### 模块 4：个人错因指纹与考前防坑一页纸生成器（新增 `tools/build_error_playbook.py` 并接入 `session-close.py`）

#### 4.1 解决的问题
把散落在 `learning/attempts.jsonl`（50 条事件）、`learning/hurdles.jsonl` 和 `subjects/*/progress.md` 中的个人真实失误，自动结晶成每门课一页的 **《考前 5 分钟防坑与自检手账》**。

#### 4.2 实现机制与文件落盘路径
- **脚本路径**：`tools/build_error_playbook.py`
- **数据源（纯派生，不手写）**：
  1. 扫描 `learning/attempts.jsonl`（合并 `corrections.jsonl` 后）中所有 `initial_result != "correct"` 或 `final_result != "correct"` 或 `needs_verify == True` 的事件，按 `subject` 与 `target_id` 聚合其 `note` 中的「缺口 / 最早无效步骤 / 错因」；
  2. 扫描 `learning/hurdles.jsonl` 中的全部概念卡点（含已解决与未解决）；
  3. 扫描 `subjects/*/progress.md` 中的三态表与错因记录。
- **输出路径**：
  - 汇总视图：`state/error-playbook.md`（全科错因指纹与考前自检总表，纯派生文件）
  - 分科视图（可选或统一放在 `state/` 下避免污染 `subjects/` 手写区）：为严格遵守本仓库 **「`state/` 与 `learning/coverage.md` 为纯派生视图，`subjects/` 下保留人工/会话记录」** 的分层规范（见 `.gitignore` 与 `tools/git-sync.py:42` `GENERATED` 列表），建议统一生成到 **`state/error-playbook.md`**，并在 `tools/git-sync.py` 的 `GENERATED` 集合中登记该路径！
  - > 💡 **设计自检（请本地 GPT 确认）**：将错因手账放在 `state/error-playbook.md` 而非 `subjects/*/CHEATSHEET.md`，可以直接纳入 `tools/git-sync.py` 的 `GENERATED` 自动重算自愈列表，跨设备同步冲突时无需人工合并！
- **接入收尾流水线**：
  在 `tools/session-close.py` 的步骤 5（生成 `state/current.md`）之后，增加步骤 `5b 生成个人错因与防坑手账（state/error-playbook.md）`。

---

## 四、 科目台账补齐：将 `02-光学` 正式纳入 `learning/goals.yaml`

- **背景**：在 `subjects/02-光学/progress.md:73` 中明确记录了历史欠账：
  > *`⚠ 记账缺口：goals.yaml / learning/tasks/ 里没有 02-光学的目标与题目 ⟹ 本次作业三步均未进 attempts.jsonl`*
- **动作**：
  1. 在 `learning/goals.yaml` 中新增 `02-光学` 几何光学能力目标组（`opt-geom-imaging`），包含已学的单球面折射（`opt.spherical-refraction`）、薄透镜高斯公式（`opt.thin-lens-gauss`）、牛顿公式（`opt.thin-lens-newton`）、作图法（`opt.ray-tracing`）与磨镜者公式（`opt.lensmaker`）；
  2. 在 `learning/curriculum.json` 的 `02-光学` 对应课件下建立 `units` 映射；
  3. 历史已发生但未入 `attempts.jsonl` 的 10 月 10 日例题 1.4 练习，按实事求是原则：若补建 `opt-hw1-ex1.4.md` 并补录事件，必须显式标明 `mode: "practice"`, `max_hint_level: 3`, `solution_exposure: "partial"`, `exposure_timing: "before_attempt"`, `needs_verify: true`（受助当堂应用，不伪造独立通过）；或者保持历史 `attempts.jsonl` 字节完全不动，仅从下一道光学微复测新题开始正式记账。

---

## 五、 实施分期与回归验证矩阵

| 阶段 | 包含改动 | 验收标准（跑通才算过） |
| :--- | :--- | :--- |
| **Phase 1：队列降噪与光学建账** | 1. 修改 `tools/reviews.py`（过滤已达标项 + 剥离 0 次作答项到 `untaught_backlog` + 支持 `superseded`）<br>2. 升级 `tools/tutor_context.py` 为「3+1 焦点视图」<br>3. 在 `learning/goals.yaml` 补齐 `02-光学` 目标 | - `python -B tools/test_tutor.py` 全部通过（含新增队列分流测试）<br>- `tutor_context.py` 的日常到期项从 89 项降至真实待复测/刚性截止项<br>- `session-close-and-sync.py --no-sync` 12 步全绿 |
| **Phase 2：60 秒微复测与错因手账** | 1. 新增 `tools/micro_retest.py`<br>2. 新增 `tools/build_error_playbook.py` 并接入 `tools/session-close.py` 与 `tools/git-sync.py` (`GENERATED`)<br>3. 更新 `.tutor/core/skills/capability-session/SKILL.md` 支持开课前 60 秒微复测 | - 用 `micro_retest.py --pick` 能精准选出 `ee.ac.phasor-impedance` 等满 2 天跨度的升级候选<br>- 生成 `state/error-playbook.md` 涵盖全部历史失分点<br>- `session-close-and-sync.py --no-sync` 全绿 |
| **Phase 3：离线章节认知包编译器** | 1. 新增 `tools/compile_chapter_pack.py`<br>2. 更新 `.tutor/core/skills/prepare-materials/SKILL.md`<br>3. 拿 1 章真实课件（如 `02-光学` 或 `01-理论力学` Topic 5）实测生成章节地图与决策树讲义 | - 生成的 `learning/chapter-guides/<id>.json` 100% 通过 `chapter_guide.py check`<br>- 生成的决策树讲义通过 `cross_verify.py` 审校 |

---

## 六、 请本地 GPT 重点审阅的 5 个问题（Review Checklist）

1. **`tools/reviews.py` 队列剥离的边界**：将 `attempts == 0` 的未学目标从 `load_capability_retests()`（每日复习/再测队列）剥离到 `load_untaught_backlog()`，是否会影响现有的周计划排期脚本 `tools/plan-week.py`？（注：我们已核查 `plan-week.py`，它独立调用 `load_learning_tasks()` 和 `load_repair_tasks()`，不依赖 `reviews.load_capability_retests()`，请 GPT 复核确认）。
2. **`micro_retest.py` 的防放水边界**：60 秒单步打字微复测题（`kind: delayed-variant`, `est_minutes: 3`）与 20 分钟综合题在 `derive_state.py` 中具有同等的升级权重。是否需要限制：**“微复测可以消除 `needs_verify` 或完成同型独立验证（升至 `曾独立完成` / `延迟通过`），但最终升至最高级 `迁移通过` 的那道 `delayed-variant` 必须包含至少两步串联或完整小问”**？
3. **`state/error-playbook.md` 的分层归属**：将自动派生的个人错因防坑手账放在 `state/error-playbook.md` 并加入 `tools/git-sync.py` 的 `GENERATED` 列表（冲突时自动重算自愈），是否比放在 `subjects/*/` 下更符合本仓库的派生/事实源分离原则？
4. **`02-光学` 历史作答的处理方式**：对于 10 月 10 日已在 `subjects/02-光学/progress.md` 记录但未进 `attempts.jsonl` 的例题 1.4，是 **方案 A（保持 `attempts.jsonl` 历史字节零改动，只建 target，从下一道新题开始记 attempt）** 更稳妥，还是 **方案 B（追加一条带 `ts: 2026-10-10, needs_verify: true` 的历史受助事件）** 更好？
5. **备课编译器 `compile_chapter_pack.py` 的视觉回执真实性**：`tools/chapter_guide.py:48-70` 强制要求 `formula_verified_pages <= visual_read_pages`。自动编译脚本在渲染 PNG 后，是否应当只登记 `text_read_pages`，而将 `visual_read_pages` / `formula_verified_pages` 留给多模态读图或 `verify_math.py` 实际验算过的页面，以严格遵守“不虚报读图回执”的铁律？
