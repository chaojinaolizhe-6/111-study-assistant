# 模拟验证实例说明（mock/）

> 【模拟数据】本目录内全部为模拟课程、模拟作业、模拟日期，与真实学习记录完全隔离。
> 根实例（subjects/、state/）从未写入任何模拟内容。

## 内容

- `subjects/01-mock-diffeq/` 模拟-微分方程（2 概念 + 课件/作业目录 + 1 张模拟"作业照片"PNG）
- `subjects/02-mock-optics/` 模拟-光学（2 概念 + 课件/作业目录）
- `state/` 模拟学习状态（mastery.json、reviews.jsonl、mistakes.md、due.md）
- `plan-inputs.yml` / `plan-output.md` 排期脚本的模拟输入与输出
- `make-mock-photo.py` 生成模拟照片的脚本（纯标准库）

## 验证记录（模拟日期 2026-10-01）

1. 首次 refresh-status --today 2026-10-01：状态文件引导 + due.md 生成 + STATUS 同步 + 概念图生成，校验全绿（4 概念、2 到期）。
2. plan-review --cards：到期概念跨课程交错排序正确（低 q 优先）。
3. 模拟一次学习会话：mock-separable q=5 → interval 1→6 天；mock-snell q=2 → lapsed、ef 2.5→2.3、interval 重置 1 天、登记弱项。
4. 会话后 refresh + validate 再次全绿（due 0、STATUS 更新为 last_session 2026-10-01）。
5. plan-review --today 2026-10-02 正确提示"due.md 未按该日期刷新"（防护生效）。
6. 排期脚本：截止优先、白天平板/晚上电脑约束、70% 余量、跨天拆分、排不下告警——全部符合预期（见 plan-output.md）。

## v2 模块验证（2026-09-24 追加）

- 能力账本（learning/）：2 道模拟题（基线 + 延迟变式）× 4 条作答事件。
  - validate_attempts：4 事件 2 题目全部通过（含"测验模式禁提示"等规则）。
  - derive_state：目标 ode.integrating-factor → 迁移通过；关键断言成立——
    attempt-0001（H2 提示后做对）未进入 independent_pass_dates，只有 10-04、10-06 两个无提示通过日。
  - 修复队列：attempt-0004（未答对、错因待确认）被排期脚本识别为修复任务。
- 三队列排期 + 容量：8 任务（含复习/能力/修复三类），阶段配额生效（复习类不再挤占解题类），
  周容量 260 > 上限 210 正确输出"容量不足"告警。
- 未通过项：无。

## v2.1 边界场景回归（2026-09-24 重建，对应外部复核的 5+3 项问题）

当前 mock 数据即边界场景（见 v2.2 更新）：8 道模拟题 × 16 条作答事件 × 2 概念（1 逾期 2 天 + 1 今日到期）× 3 能力目标。

- 迁移判定：attempt-0003 首次作答变式题即无提示通过 → variant_passes=1；
  attempt-0008 先见过解答（0006 worked-example）再通过 → **不计**迁移证据。
- 闭卷：attempt-0014 开卷通过 → 记入 open_book_pass_dates，不计独立通过。
- 排期：mock-snell 逾期 2 天未被过滤、排入今天（带"已逾期"标记）；mock-separable 今日到期排入当天。
- 负向测试（已执行后恢复）：无关目标计分事件被 validate_attempts 拒绝（exit 1）。
- 未通过项：无。

## v2.2 第二轮边界场景（2026-09-24，对应外部复核第 2 轮的 3 项问题）

- 版本按事件解释：baseline v1(kind=baseline,目标 int)→v2(kind=delayed-variant,目标 ls)，
  历史元数据在 tasks/history/ode-if-baseline-01.v1.md。
  - v1 通过事件按 v1 元数据计分（未获变式计分、未被目标校验拒绝）；
  - v3 无元数据事件（attempt-0016）：unknown_version_events=1，不计入独立通过，也不能关闭修复项。
- 全局曝光：multi-01 先在 ode.integrating-factor 下 worked-example，再在 ode.linear-systems 下通过 →
  ode.linear-systems variant_passes=0，等级"延迟通过"（旧实现会误判"迁移通过"）。
- 修复按目标：eu-multi-01 在 ode.existence-uniqueness 失败(confirmed)、随后仅在 ode.integrating-factor 独立通过 →
  repair-ode-eu-multi-01-ode.existence-uniqueness 仍入队（旧实现队列为空）。
- 最终状态：ode.integrating-factor=迁移通过；ode.linear-systems=延迟通过；ode.existence-uniqueness=需支持；
  修复队列恰 3 项，均带目标粒度 id。
- 未通过项：无。

## 重跑

```powershell
cd mock
python -B .tutor/core/scripts/refresh-status.py --today 2026-10-01
python -B .tutor/core/scripts/validate-study.py --today 2026-10-01
python -B ../tools/validate_attempts.py --root .
python -B ../tools/derive_state.py --root .
python -B ../tools/plan-week.py --inputs plan-inputs.yml --root . --out plan-output.md
```

## 未验证项

- 作业照片解读：当前模型（deepseek-v4-pro）不支持图像输入；本机无 OCR 工具。
  照片文件通道（放进 作业/ 目录）已验证存在，读图解读未验证。
