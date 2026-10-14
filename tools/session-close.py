#!/usr/bin/env python3
"""会话收尾**唯一入口**：逐步执行、逐步报告；任何一步失败都显式报出。

为什么统一成一个入口（本轮改进要求 P0-A 第 5 条）：
此前「更新状态」散在多个脚本里（`derive_state` / `sync_status` / 手写 STATUS 叙述行 / 手写 handoff），
收尾时只跑了其中一两个，于是出现「计数更新了、状态其实没同步」——
实测：孤立奇点已有 `attempt-27～31`，交接文件仍写「完全未开始」。

步骤（事实 → 派生 → 视图 → 一致性核对）：
  1. 作答事件校验（learning/attempts.jsonl，含订正层）
  1b. 帮助史一致性（事件级「H0+无曝光」不得与目标级记录矛盾）
  2. 困难观察校验（learning/hurdles.jsonl）
  3. 重建能力状态（learning/learner-state.json；锁内 + 原子写 + 事实源指纹）
  4. 生成课程覆盖台账（learning/coverage.md）
  5. 生成当前状态事实卡（state/current.md）——**跨窗口续学的唯一事实来源**
  6. 同步 AGENTS.md / CLAUDE.md 的 TUTOR-STATUS（可数事实重算；锁内；镜像规则可执行检查）
  7. 生成续学入口（plan/handoff-CURRENT.md；动态部分引用 state/current.md）
  8. 生成复习/再测排期（plan/schedule.md；带最早开始日期，未来项不提前安排）
  9. 订正影响面（列出被订正波及、需人工核对的文件）
 10. **一致性核对**：STATUS 的计数必须等于派生状态；镜像必须成立；事实源指纹必须与库一致。
     **不一致 → 本步 FAIL，不允许「只更新计数就宣称已同步」。**

用法:
  python -B tools/session-close.py --today 2026-09-30 [--root .] [--carry-over plan/today-<昨天>.md]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync_status  # noqa: E402
import validate_hurdles  # noqa: E402
from derive_state import derive_and_write, source_fingerprint  # noqa: E402
from learninglib import load_hurdles  # noqa: E402
from timebase import learning_today, uk_date_now  # noqa: E402
from validate_attempts import check  # noqa: E402
from observations import pending  # noqa: E402

BLOCK_RE = re.compile(r"<!-- TUTOR-STATUS:START -->\n(.*?)\n<!-- TUTOR-STATUS:END -->", re.S)


def read_status_fields(root: Path) -> dict[str, str]:
    for name in ("AGENTS.md", "CLAUDE.md"):
        path = root / name
        if not path.is_file():
            continue
        match = BLOCK_RE.search(path.read_text(encoding="utf-8"))
        if not match:
            continue
        fields = {}
        for line in match.group(1).splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                fields[key.strip()] = value.strip()
        return fields
    return {}


def consistency_check(root: Path, today: str) -> tuple[bool, list[str], list[str]]:
    """STATUS 视图 vs 事实源：计数必须一致，镜像必须成立，指纹必须匹配。"""
    errors: list[str] = []
    notes: list[str] = []
    state_path = root / "learning" / "learner-state.json"
    if not state_path.is_file():
        return False, ["learning/learner-state.json 不存在"], []
    state = json.loads(state_path.read_text(encoding="utf-8"))

    # ① 指纹：派生状态必须来自**当前** attempts/corrections
    live = source_fingerprint(root)
    recorded = state.get("source", {})
    for key in live:
        if recorded.get(key) != live.get(key):
            errors.append(
                f"事实源指纹不一致：{key} 记 {recorded.get(key)!r}，实际 {live.get(key)!r}"
                f" → learner-state.json 不是从当前事实源派生的（并发写入或未重建）"
            )

    # ② STATUS 计数 vs 派生状态
    status = read_status_fields(root)
    summary = state["summary"]
    attempts_field = status.get("attempts", "")
    match = re.search(r"(\d+)\s*条", attempts_field)
    if not match:
        errors.append(f"STATUS.attempts 无法解析条数：{attempts_field!r}")
    elif int(match.group(1)) != live["attempts_events"]:
        errors.append(f"STATUS.attempts={match.group(1)}，事实源 {live['attempts_events']} 条")

    mastered_field = status.get("mastered", "")
    match = re.search(r"迁移通过\s*(\d+)/(\d+)", mastered_field)
    if not match:
        errors.append(f"STATUS.mastered 无法解析：{mastered_field!r}")
    else:
        if int(match.group(1)) != summary["by_level"].get("迁移通过", 0):
            errors.append(f"STATUS.mastered 分子={match.group(1)}，派生 {summary['by_level'].get('迁移通过', 0)}")
        if int(match.group(2)) != summary["targets"]:
            errors.append(f"STATUS.mastered 分母={match.group(2)}，派生目标数 {summary['targets']}")

    hurdles_field = status.get("open_hurdles", "")
    if summary["open_hurdles"] == 0:
        ok_h = hurdles_field.strip() in ("无", "")
    else:
        ok_h = bool(hurdles_field.strip()) and hurdles_field.count("；") + 1 == summary["open_hurdles"]
    if not ok_h:
        errors.append(f"STATUS.open_hurdles={hurdles_field[:60]!r} 与实际未解决困难 {summary['open_hurdles']} 条不符")

    # ③ 镜像规则（除互指文件名外逐字一致）
    if not sync_status.mirrored_except_names(root / "AGENTS.md", root / "CLAUDE.md"):
        errors.append("AGENTS.md / CLAUDE.md 除互指文件名外**不**逐字一致（镜像规则未满足）")

    # ④ 续学入口必须与事实卡同源
    handoff = root / "plan" / "handoff-CURRENT.md"
    if not handoff.is_file():
        errors.append("plan/handoff-CURRENT.md 不存在")
    else:
        text = handoff.read_text(encoding="utf-8")
        if "state/current.md" not in text:
            errors.append("plan/handoff-CURRENT.md 没有引用 state/current.md（不再是同源入口）")
        if today not in text:
            errors.append(f"plan/handoff-CURRENT.md 里的日期不是 {today}（可能是旧快照）")

    # ⑤ 事实卡必须与派生状态同源
    current = root / "state" / "current.md"
    if not current.is_file():
        errors.append("state/current.md 不存在")
    else:
        text = current.read_text(encoding="utf-8")
        if str(live["attempts_sha256"])[:12] not in text:
            errors.append("state/current.md 的指纹与当前 attempts.jsonl 不一致（未重算）")
        if today not in text:
            errors.append(f"state/current.md 里的生成日期不是 {today}")

    notes.append(f"中国日期 {today}／系统英国日期 {uk_date_now()}（排期一律用中国日期）")
    return (not errors), errors, notes


def main() -> int:
    parser = argparse.ArgumentParser(description="Unified session close pipeline with per-step reporting.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--today", default=None, help="中国日期；默认由 tools/timebase.py 换算")
    parser.add_argument("--carry-over", default=None, help="昨日清单路径（结转未完成项，不静默消失）")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    today = learning_today(args.today)

    results: list[tuple[str, bool, str]] = []

    # 1) 作答事件校验
    errors, warnings, attempts, _tasks = check(root)
    results.append((
        "1 作答事件校验", not errors,
        f"attempts={len(attempts)}, warnings={len(warnings)}" + ("" if not errors else f", errors={len(errors)}"),
    ))
    for error in errors:
        print(f"  - ERROR {error}")
    for warning in warnings:
        print(f"  - WARN {warning}")
    # 帮助史一致性（2026-09-30 加）：事件级声称「H0+无曝光」而目标级记着帮助 → 展示与判定不一致。
    # 判定本身按目标级走（不会错误升级），但**看记录的窗口会被误导**，因此这里单独列为一步。
    inconsistent = [line for line in warnings if "展示与判定不一致" in line]
    results.append((
        "1b 帮助史一致性（事件级 vs 目标级）", not inconsistent,
        "事件级与目标级一致" if not inconsistent else f"{len(inconsistent)} 条需订正目标级字段",
    ))

    # 2) 困难观察校验
    sys.argv = ["validate_hurdles", "--root", str(root)]
    rc_hurdle = validate_hurdles.main()
    try:
        observations_count = len(pending(root))
        observations_note = f"待处理反馈={observations_count}"
    except (ValueError, OSError, KeyError, TypeError) as exc:
        rc_hurdle = 1
        observations_note = f"反馈队列校验失败：{exc}"
    hurdles = [r["data"] for r in load_hurdles(root) if r.get("data")]
    open_hurdles = [h for h in hurdles if h.get("status") in ("open", "teaching", "awaiting_retest")]
    results.append(("2 困难与反馈队列校验", rc_hurdle == 0, f"hurdles={len(hurdles)}, 未解决={len(open_hurdles)}；{observations_note}"))

    # 3) 重建能力状态
    state = None
    if not errors and not inconsistent and rc_hurdle == 0:
        try:
            state = derive_and_write(root)
            results.append(("3 重建能力状态", True, f"targets={state['summary']['targets']}（锁内派生，含事实源指纹）"))
        except Exception as exc:  # noqa: BLE001 - 必须显式报失败
            results.append(("3 重建能力状态", False, f"失败：{exc}"))
    else:
        results.append(("3 重建能力状态", False, "跳过：作答/帮助史/困难校验未通过"))

    # 4) 覆盖台账
    if state is not None:
        sys.argv = ["coverage", "--root", str(root), "--today", today]
        import coverage  # noqa: E402

        rc_cov = coverage.main()
        results.append(("4 课程覆盖台账", rc_cov == 0, "learning/coverage.md"))
    else:
        results.append(("4 课程覆盖台账", False, "跳过：能力状态未重建"))

    # Independent course scope must be reconciled before generating summaries.
    if state is not None:
        try:
            import curriculum
            sys.argv = ['curriculum', '--root', str(root), '--today', today]
            rc_curriculum = curriculum.main()
            results.append(('4b 课程范围对账', rc_curriculum == 0, 'learning/curriculum-coverage.md'))
        except Exception as exc:
            results.append(('4b 课程范围对账', False, str(exc)))
    else:
        results.append(('4b 课程范围对账', False, '跳过：能力状态未重建'))

    # 5) 当前状态事实卡
    if state is not None:
        sys.argv = ["current_state", "--root", str(root), "--today", today]
        import current_state  # noqa: E402

        rc_cur = current_state.main()
        results.append(("5 当前状态事实卡", rc_cur == 0, "state/current.md（续学唯一事实来源）"))
    else:
        results.append(("5 当前状态事实卡", False, "跳过：能力状态未重建"))

    # 6) 同步 STATUS
    if state is not None:
        sys.argv = ["sync_status", "--root", str(root), "--today", today]
        rc_sync = sync_status.main()
        results.append(("6 同步 TUTOR-STATUS", rc_sync == 0, "可数事实重算 + 镜像规则检查"))
    else:
        results.append(("6 同步 TUTOR-STATUS", False, "跳过：能力状态未重建"))

    # 7) 续学入口
    if state is not None:
        sys.argv = ["handoff", "--root", str(root), "--today", today]
        import handoff  # noqa: E402

        rc_hand = handoff.main()
        results.append(("7 续学入口 handoff", rc_hand == 0, "plan/handoff-CURRENT.md"))
    else:
        results.append(("7 续学入口 handoff", False, "跳过：能力状态未重建"))

    # 8) 复习/再测排期
    if state is not None:
        argv = ["schedule_reviews", "--root", str(root), "--today", today]
        if args.carry_over:
            argv += ["--carry-over", args.carry_over]
        sys.argv = argv
        import schedule_reviews  # noqa: E402

        rc_sched = schedule_reviews.main()
        results.append(("8 复习/再测排期", rc_sched == 0, "plan/schedule.md（含最早开始日期）"))
    else:
        results.append(("8 复习/再测排期", False, "跳过：能力状态未重建"))

    # 9) 订正影响面
    sys.argv = ["correction_impact", "--root", str(root)]
    import correction_impact  # noqa: E402

    print()
    correction_impact.main()
    results.append(("9 订正影响面", True, "已列出（需人工核对说明是否更新）"))
    print()

    # 10) 一致性核对
    ok_cons, cons_errors, cons_notes = consistency_check(root, today)
    for note in cons_notes:
        print(f"  - {note}")
    for error in cons_errors:
        print(f"  - ERROR {error}")
    results.append((
        "10 一致性核对（STATUS vs 事实源）", ok_cons,
        "计数/镜像/指纹三者一致" if ok_cons else f"{len(cons_errors)} 项不符",
    ))

    # ---- 汇总 ----
    print("\n== 会话收尾汇总 ==")
    for name, ok, detail in results:
        print(f"[{'OK  ' if ok else 'FAIL'}] {name}：{detail}")
    if state:
        blocked_rows = []
        for tid, target in sorted(state["targets"].items()):
            blocked = target.get("upgrade_blocked") or []
            if blocked:
                reasons = sorted({reason for item in blocked for reason in item["why"]})
                blocked_rows.append(f"{tid}×{len(blocked)}（{', '.join(reasons)}）")
        needs_verify = [
            f"{tid}（{a.get('event_id')}）"
            for a in attempts
            for tid, val in (a.get("target_results") or {}).items()
            if isinstance(val, dict) and val.get("needs_verify")
        ]
        print(f"- 需要核验的目标：{', '.join(needs_verify) if needs_verify else '无'}")
        print(f"- 未升级事件（逐目标判定不构成独立通过）：{'；'.join(blocked_rows) if blocked_rows else '无'}")
        print(f"- 实测时长合计 {state['summary']['measured_minutes_global']} 分钟；"
              f"估计 {state['summary']['estimated_minutes_global']} 分钟（单列，不混算）")
        print(f"- 有目标但无题目（纸面目标）：{state['summary'].get('targets_without_tasks') or '无'}")
    print(f"- 未解决困难：{'; '.join(h.get('hurdle_id','?') + '→' + ','.join(h.get('target_ids') or []) for h in open_hurdles) if open_hurdles else '无'}")
    print(f"- 学习日（中国时间）：{today}；系统英国日期：{uk_date_now()}")
    print("- 生成物：learning/learner-state.json · learning/coverage.md · state/current.md · "
          "AGENTS.md+CLAUDE.md 的 STATUS · plan/handoff-CURRENT.md · plan/schedule.md")

    failed = [name for name, ok, _ in results if not ok]
    if failed:
        print(f"\n结论：有步骤失败 → {', '.join(failed)}（**不声称已保存完整**）")
        return 1
    print(f"\n结论：{len(results)} 步全部通过（含课程范围对账、帮助史一致性与一致性核对）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
