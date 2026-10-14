# 审查报告：YusenZhang0601/tutor

> 审查日期：2026-09-23 · 审查方式：读全部源码与文档 + 模拟数据端到端实测（见 `mock/`）

## 1. 来源与版本

- 仓库：https://github.com/YusenZhang0601/tutor
- 下载方式：git clone（完整历史，9 个提交）
- 版本：commit `c6f85760e894ba90f61272297a918a426c1913ba`（2026-09-05，作者 TonyRainforest）
- 许可证：MIT
- 原始副本保存在 `upstream/tutor/`，未做任何改动；记录见 `upstream/PROVENANCE.md`

## 2. 项目性质（重要结论）

**不是可运行的应用**：没有服务器、没有 UI、没有依赖安装。它是一个"文件型 AI 辅导协议模板"：
方法（`.tutor/core/`：协议、9 个技能、SM-2 参数）+ 8 个 Python 校验/生成脚本 + 文件状态约定。
由 AI 代理（本 DSH 会话）读取并执行。这正好符合需求：辅导逻辑用现成协议，状态存文件，DSH 作为执行者。

## 3. 实际实现（代码级核实，且已在 mock 实例跑通）

| 功能 | 依据 |
|------|------|
| 诊断→讲解→测验→复习→门禁→进化的 7 步辅导循环 | `.tutor/core/protocol.md` + 9 个技能 SKILL.md |
| SM-2 间隔复习算法（ef/interval/reps/due，遗忘惩罚） | `skills/schedule-review/SKILL.md` + `settings.yml` |
| 到期复习队列自动生成（due.md）+ 跨主题交错排序 | `scripts/refresh-status.py`、`plan-review.py`（实测通过） |
| 学习路径规划：概念前置依赖图 + 拓扑层级 + 门禁 | `scripts/concept-graph.py`（实测生成 Mermaid 图） |
| 状态一致性校验（frontmatter↔mastery.json↔日志↔索引↔STATUS） | `scripts/validate-core.py`（48KB，实测全套通过） |
| 文件状态持久化（state/ + 概念笔记 frontmatter） | 实测：跨会话续学信息齐全 |
| 多学科并存（subjects/*/topics/*/*.md 全局扫描） | mock 两门课并存实测通过 |
| 弱项追踪（mistakes.md 偏向出题） | `state/mistakes.md` + quiz 技能，实测 |

## 4. 只有文档宣称、仓库里并不随附（运行时生成，非缺失）

- `state/`（mastery.json、due.md、mistakes.md、reviews.jsonl）：首次运行校验器自动初始化（实测）
- `.tutor/data/review-cards.json`、`.tutor/config/learner-profile.md`：同上，自动初始化
- `subjects/<学科>/` 具体内容：由 /plan 与教学会话逐步创建（这是设计行为）

## 5. 完全缺失（全库 grep 零匹配，已确认）

| 缺失功能 | 证据 |
|---------|------|
| 学期层面跨课程时间排期（课表、截止日期、日历时隙） | 全库搜 `deadline/calendar/课表/截止/排期/日程/timetable/time-slot`：0 匹配 |
| 设备时段限制（白天平板/晚上电脑） | 同上，无任何设备概念 |
| 作业登记与状态流转（未开始/进行中/待订正/已提交） | 只有概念级 SM-2 状态 |
| 课件文件夹/三态标记（老师已讲/我已看过/能独立完成） | tutor 只有概念级 new/learning/mastered/lapsed |

→ 结论："学习路径规划"（`/plan`：单学科内概念序列+前置图）与"结合课表及截止日期的时间排期"（跨课程日历）**是两个不同功能**：前者已实现并实测；后者完全不存在，需补充。已补：`tools/plan-week.py`（唯一新增脚本）+ `plan/inputs.yml`。

## 6. 适配点（tutor 在 DSH 中的加载方式）

- DSH 自动加载目录内 `AGENTS.md`（实测：根目录、mock/ 内的 AGENTS.md 均被注入）→ 根目录放 AGENTS.md 即自动进入导师模式，STATUS 块随每次会话更新，实现跨对话续学。
- 命令拦截规则：DSH 无系统斜杠命令，用户输入 `/learn` 等普通文本，由我按协议拦截执行（上游 AGENTS.md 已写明此规则，实测可行）。
- `python3` → Windows 下用 `python`；技能里的 `Bash` 工具 → DSH 用 pwsh。
- 运行脚本建议 `python -B`（避免 __pycache__ 触发校验器 housekeeping 规则）+ `$env:PYTHONIOENCODING='utf-8'`（避免 GBK 控制台乱码）。
- refresh-status 与 validate-study 必须用同一 `--today` 日期（STATUS 块校验要求）。

## 7. 模拟验证结果（全部标注【模拟】，与真实记录隔离）

- 实例位置 `mock/`，模拟日期 2026-10-01 起，两门课（模拟-微分方程、模拟-光学）× 4 概念 × 2 作业。
- 通过项：状态引导、到期队列生成与跨课程交错、SM-2 成功/遗忘两条路径、弱项登记、概念图生成、
  严格校验全绿、排期脚本（截止优先/设备限制/余量/告警/跨天拆分）。
- 未通过项：无。照片解读未纳入 mock 通过项（当前模型不支持图像输入，见使用说明第 6 节）。
- mock 数据不进入根实例 state/ 与 subjects/（根实例 subjects 仅含 9 门真实课程空骨架，无任何编造进度）。

## 8. 备选项目

未安装 anything-to-course 与 OpenTutor：首选项目经审查适合复用（辅导协议+状态文件正是需求核心），
按"不要同时堆叠多套系统"的要求，仅在首选明显不适合时才评估备选——未触发该条件。

## 9. v2 升级附录：对"证据中心"建议的评估（2026-09-23）

评估结论：**核心成立，大部分采纳，四处调整，两处推迟**。

采纳并落地：
- 记忆状态与解题能力分离（SM-2 管"何时再测"，learning/ 能力账本管"无帮助下通过了什么"）；
  已实现：`learning/` 数据层 + `tools/validate_attempts.py` + `tools/derive_state.py`，
  mock 验证：H2 提示后做对未计入独立通过，2 日期无提示通过 + 1 变式 → 迁移通过。
- 事件追加、状态可重建、事件由程序校验（唯一 event_id、版本一致、测验禁提示、示例学习必记 solution_seen）。
- H0-H4 提示梯度按瓶颈升级（`.tutor/core/skills/capability-session/SKILL.md`，上游文件未改动，以新技能叠加）。
- 三条队列 + 阶段时间比例 + 周容量约束（`tools/plan-week.py` v2，mock 验证容量告警与类别配额）。
- 检查点代替强制中断（四要素保存）、每周四指标（`learning/weekly-review.md`）、信心自报（事件字段）。

调整之处：
1. 调度器：保留 SM-2 为唯一记忆调度器（与 tutor 校验器深度耦合，运行正常）；FSRS 迁移收益真实但
   需先积累评级数据，避免中途混用两个调度器。py-fsrs 列为候选实现。
2. 知识底座：先以本工作区 `subjects/` 概念笔记为知识层（带稳定 id）；Obsidian 桥接推迟到闭环跑通后，
   桥接时保持稳定 id 一一对应。vault/ 目录布局（知识/学习分离）在本工作区以 subjects/+learning/ 实现。
3. 泄题防护：采纳"宿主侧保存模式与提示级别、事件程序校验、参考解答与学生可见内容分离"，
   但诚实声明仍是提示级约定，未经对抗性测试，不承诺绝对。
4. 能力等级规则按建议实现为可调参数（derive_state.py），验收次数为工程初值。

推迟（现阶段不做）：向量数据库/复杂知识追踪、多智能体、SymPy 自动核验（可手工核验并标"不确定"）、
第二个 LLM 审核泄题（成本高且非绝对保证）。

证据边界（照录）：检索/间隔/自我解释/交错练习有研究支持，但不足以证明本系统对大学理论力学/电动力学有效；
本工作区不声称已验证学习效果，是否有效以学习者自己的延迟独立表现数据为准。

## 10. v2.1 边界复核修复记录（2026-09-24）

外部复核发现 5 处证据判定/队列问题 + 3 处描述偏差，全部修复并在 mock/ 重建边界场景回归（全绿）：

| 问题 | 修复 | 验证 |
|------|------|------|
| 见过答案的旧变式仍获"迁移通过" | variant pass 增加"该题此前从未被作答"条件（按 attempts.jsonl 行序） | mock：variant-02 先 worked-example 后通过 → variant_passes 仍为 1，不计入 |
| 复习排期漏项（逾期被过滤；当天到期排不进当天） | due ≤ horizon 无下界；排期窗口改为 day ≤ max(due, today)，逾期标注 | mock：mock-snell 逾期 2 天排入今天；mock-separable 今日到期排入当天 |
| 修复队列无闭环 | 按题目最后一条事件判定：独立通过→闭环；待确认且非独立→入队（含提示后做对但待确认） | mock：variant-01 修复后不再入队；probe-01（H2 做对+待确认）入队 |
| 题目升版本阻断整份状态重建 | 版本不一致降级为警告（不阻断）；计入 version_mismatch_events | mock：baseline v1→v2，3 条旧事件仅警告，derive 正常重建 |
| 作答可给无关目标计分 | target_ids 必须是题目声明目标的非空子集，越界即拒 | 负向测试：越界事件 exit 1 拒绝，恢复后 exit 0 |
| 闭卷条件未参与判定 | 独立通过要求 closed_book=true；开卷通过单独记 open_book_pass_dates | mock：attempt-0010 开卷通过不计独立通过 |
| 验收次数未配置化 | 参数移至 learning/policy.yml（require_closed_book/min_dates/min_variant_passes） | policy 在 mock 与根实例生效 |
| 修复题目与原题重复排期 | 入修复队列的题目从能力建设队列剔除 | mock：修复队列恰 2 项，原题不再并列 |
| 措辞：真实成效 | 文档区分"功能验证（模拟数据）"与"真实学习成效（未验证）" | README-使用说明 §5、本报告 |

已知剩余边界（如实记录，非本轮范围）：同日多次通过按 1 个日期计；跨目标作答（一题测多目标）按题目声明目标分别计分；
修复任务 est=20 分钟为工程初值；逾期任务的"今天补救"不改变 SM-2 状态（由学习会话另行更新）。

## 11. v2.2 第二轮边界复核修复记录（2026-09-24）

外部复核再发现 3 处证据可信度问题（可复现误判），全部修复并在 mock/ 重建场景回归：

| 问题 | 修复 | 验证（mock） |
|------|------|------|
| 版本不一致仅计数，旧成绩仍用当前类别计分；升版换目标会因目标校验拒绝而阻断重建 | 新增题目历史元数据 `learning/tasks/history/<id>.v<N>.md`；事件按所引版本解释 kind/target_ids；有历史→照常计分+警告；无历史→保留但不用于升级 | baseline v1（kind=baseline，目标 int）→ v2（kind=delayed-variant，目标 ls）：v1 通过事件未获变式计分、未被拒绝；v3 无元数据事件 unknown_version_events=1 且不计独立通过 |
| "首见"按目标分别计算可绕过曝光历史 | 题目曝光改为**整份日志全局**计算（任何目标下的任何作答都使该题曝光） | multi-01 先在 int 下 worked-example、后在 ls 下通过 → ode.linear-systems variant_passes=0，等级"延迟通过"（buggy 为"迁移通过"） |
| 修复闭环按整题关闭，漏掉其他目标的未解决问题 | 修复按 (题目, 目标) 粒度追踪最后事件，一次通过只关闭它覆盖的目标；未知版本事件不得关闭待修复项 | eu-multi-01 在 existence-uniqueness 失败(confirmed)、随后仅在 int 独立通过 → repair-ode-eu-multi-01-ode.existence-uniqueness 仍入队；probe-01 的 v3 未知版本通过未能关闭其 pending 修复 |

回归结果：mock 3 目标状态为 迁移通过/延迟通过/需支持 各 1，修复队列恰 3 项且均带目标粒度 id；
两实例 validate_attempts/derive_state/plan-week/tutor 校验全部通过；根实例仍为 1 题 0 作答（未测）。

结论口径（与复核一致）：**单目标、题目版本不变的 ODE 试点可以开始**；
跨目标、跨版本的能力等级现在按上述规则处理，但仍建议在真实数据积累后再做校准。

