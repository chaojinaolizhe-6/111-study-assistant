#!/usr/bin/env python3
"""由事件推导能力状态 learning/learner-state.json（派生视图，勿手工编辑）。

能力等级（参数见 learning/policy.yml，工程初值可调）：
- 未测       该目标没有任何作答事件
- 需支持     有作答但无任何"独立通过"
- 曾独立完成 独立通过日期数 < min_dates
- 延迟通过   独立通过日期数 ≥ min_dates（未见变式通过数不足）
- 迁移通过   独立通过日期数 ≥ min_dates 且 未见变式通过数 ≥ min_variant_passes

"独立通过"（默认全部要求；**逐目标判定**，2026-09-28 修）：
  对该目标：结果正确（目标级 final 优先）且 提示级别明确为 0（目标级 hint_level 优先）
  且 needs_verify 不为真 且 答案未曝光（目标级 exposure 优先；after_attempt 的曝光不阻断）
  且 mode!=worked-example 且 closed_book==true（开卷通过单独统计，不计入等级）
  —— 不再用整条事件的汇总总评去逐目标升级：那会把同事件中待核验的目标一起升级，
     也会把同事件中已独立答对的目标一起压掉。

"未见变式通过"（防曝光绕过的三层条件）：
  1. 题目曝光按**整份日志全局**计算：该题此前从未被任何目标下的任何作答引用过
     （先在其他目标下看过完整示例 → 本题已曝光，任何目标都不得再计"未见变式"）；
  2. 题目在事件所引版本的 kind ∈ {delayed-variant, mixed}（按历史版本元数据，不用当前版本顶替）；
  3. 本次为独立通过。
→ 见过答案的旧变式、旧版本事件借用当前版本类别，都不构成迁移证据。

版本处理：
- 有历史版本元数据（learning/tasks/history/）→ 按该版本元数据解释事件；
- 无元数据的版本 → 事件保留在统计中（attempts/时间/提示依赖），但不用于升级。

用法:
  python -B tools/derive_state.py --root .
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path

from learninglib import (
    estimated_minutes,
    hint_level_of,
    independence_blockers,
    is_open_book_pass_for,
    load_attempts,
    load_hurdles,
    load_task_history,
    load_tasks,
    measured_minutes,
    parse_yaml,
    resolve_task_meta,
)
from goallib import declared_goal_targets, load_goals
from validate_attempts import check
from workspace_lock import (
    ConcurrentModification,
    LockTimeout,
    WorkspaceLock,
    atomic_write_text,
    snapshot,
)

DEFAULT_POLICY = {
    "require_closed_book": True,
    "min_dates": 2,
    "min_variant_passes": 1,
    "min_delay_days": 2,  # 两次独立通过之间的最小间隔（工程初值，可调）；防"跨午夜几分钟"冒充延迟检验
}


def load_policy(root: Path) -> dict:
    path = root / "learning" / "policy.yml"
    if not path.is_file():
        return dict(DEFAULT_POLICY)
    raw = parse_yaml(path.read_text(encoding="utf-8"))
    section = raw.get("independent_pass") or {}
    if not isinstance(section, dict):
        return dict(DEFAULT_POLICY)
    policy = dict(DEFAULT_POLICY)
    if "require_closed_book" in section:
        policy["require_closed_book"] = bool(section["require_closed_book"])
    for key in ("min_dates", "min_variant_passes", "min_delay_days"):
        if key in section and isinstance(section[key], int) and section[key] >= 1:
            policy[key] = section[key]
    return policy


def derive(root: Path) -> dict:
    errors, warnings, attempts, tasks = check(root)
    if errors:
        print("attempts 未通过校验，不推导状态：", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        sys.exit(1)
    policy = load_policy(root)
    require_closed_book = policy["require_closed_book"]
    min_dates = policy["min_dates"]
    min_variant = policy["min_variant_passes"]
    min_delay_days = policy["min_delay_days"]
    history = load_task_history(root)

    # 1) 题目曝光：按整份日志（行序）全局计算——任何目标下的任何作答都让该题"曝光"
    global_exposure: dict[str, int] = {}
    attempt_first_seen: dict[str, bool] = {}
    for attempt in attempts:
        task_id = attempt.get("task_id", "")
        first = global_exposure.get(task_id, 0) == 0
        attempt_first_seen[attempt.get("event_id", "")] = first
        global_exposure[task_id] = global_exposure.get(task_id, 0) + 1

    # 2) 逐事件解析版本元数据（kind 按事件所引版本，不用当前版本顶替）
    meta_by_event: dict[str, dict | None] = {}
    for attempt in attempts:
        meta = resolve_task_meta(
            tasks, history, attempt.get("task_id", ""), str(attempt.get("task_version", ""))
        )
        meta_by_event[attempt.get("event_id", "")] = meta

    # 3) 目标集合：**目标声明 ∪ 当前题目 ∪ 历史版本 ∪ 事件引用**（升版换目标后旧目标仍可追踪）
    #    2026-09-30 修（ISSUES A7 根因）：此前**不读 goals.yaml**，
    #    于是"已声明、还没出题"的目标（如 tm.t3.lagrangian-construction）根本不进派生状态，
    #    从系统里静默消失。现在 goals.yaml 是目标的事实源之一。
    goal_index = declared_goal_targets(root)
    target_ids: set[str] = set(goal_index)
    for task in tasks.values():
        target_ids.update(task["target_ids"])
    for meta in history.values():
        target_ids.update(meta["target_ids"])
    for attempt in attempts:
        target_ids.update(attempt.get("target_ids", []))

    # 每个目标有哪些题目（含"没有题目"的情形）——覆盖表用
    tasks_for_target: dict[str, list[dict]] = {tid: [] for tid in target_ids}
    for task in tasks.values():
        for tid in task["target_ids"]:
            tasks_for_target.setdefault(tid, []).append(
                {"id": task["id"], "kind": task.get("kind"), "status": task.get("status"), "due": task.get("due")}
            )

    by_target: dict[str, list[tuple[dict, dict | None]]] = {tid: [] for tid in target_ids}
    for attempt in attempts:
        meta = meta_by_event.get(attempt.get("event_id", ""))
        for tid in attempt.get("target_ids", []):
            by_target.setdefault(tid, []).append((attempt, meta))

    # 2b) 困难观察（hurdles）：没有作答的"明确表示不会/不理解"，不是分数，但必须可被查到
    hurdle_rows = load_hurdles(root)
    hurdle_bad_lines = [r["line"] for r in hurdle_rows if r.get("data") is None]
    hurdles_for_target: dict[str, list[dict]] = {}
    open_hurdle_count = 0
    for row in hurdle_rows:
        data = row.get("data")
        if not data:
            continue
        if data.get("status") in ("open", "teaching", "awaiting_retest"):
            open_hurdle_count += 1
        for tid in data.get("target_ids") or []:
            hurdles_for_target.setdefault(tid, []).append(
                {
                    "hurdle_id": data.get("hurdle_id"),
                    "status": data.get("status"),
                    "observed_at": data.get("observed_at"),
                    "evidence_ref": data.get("evidence_ref"),
                }
            )

    targets: dict[str, dict] = {}
    # 逐目标记录"为什么某些作答没有升级"——让"凭什么算独立完成"可被复查（2026-09-28 加）
    upgrade_blocked: dict[str, list[dict]] = {}
    for tid in sorted(by_target):
        pairs = by_target[tid]
        attempts_for_target = [a for a, _m in pairs]
        independent_dates: set[str] = set()
        open_book_pass_dates: set[str] = set()
        variant_passes = 0
        version_mismatches = 0
        unknown_version_events = 0
        for attempt, meta in pairs:
            task_id = attempt.get("task_id", "")
            version = str(attempt.get("task_version", ""))
            current = tasks.get(task_id)
            if current is not None and version != current.get("version", ""):
                version_mismatches += 1
            if meta is None:
                unknown_version_events += 1
                # 2026-09-28（ISSUES B3）：元数据缺失同样是"未升级"，必须一并列出原因，
                # 否则"每个未升级事件都列出事件号、日期与原因"这句话名不副实。
                upgrade_blocked.setdefault(tid, []).append(
                    {
                        "event_id": attempt.get("event_id"),
                        "ts": attempt.get("ts"),
                        "why": [f"版本元数据缺失（{task_id} v{version}）→ 保留记录但不用于升级"],
                    }
                )
                continue
            # 独立通过 / 开卷通过：**逐目标**判定（2026-09-28 修）
            # 旧实现用整条事件的总评，会把同事件中 needs_verify 的目标一起升级，
            # 也会把同事件中已独立答对的目标一起压掉；判定集中在 learninglib。
            blockers = independence_blockers(attempt, tid, require_closed_book)
            if not blockers:
                independent_dates.add(str(attempt["ts"]))
                first_seen = attempt_first_seen.get(attempt.get("event_id", ""), False)
                if first_seen and meta.get("kind") in ("delayed-variant", "mixed"):
                    variant_passes += 1
            elif is_open_book_pass_for(attempt, tid):
                open_book_pass_dates.add(str(attempt["ts"]))
            else:
                upgrade_blocked.setdefault(tid, []).append(
                    {
                        "event_id": attempt.get("event_id"),
                        "ts": attempt.get("ts"),
                        "why": blockers,
                    }
                )

        dates = sorted(independent_dates)
        # 延迟：只在日期跨度 ≥ min_delay_days 时才承认"延迟通过"（跨午夜几分钟不算）
        delay_days = 0
        if len(dates) >= 2:
            try:
                delay_days = (dt.date.fromisoformat(dates[-1]) - dt.date.fromisoformat(dates[0])).days
            except ValueError:
                delay_days = 0
        delay_ok = delay_days >= min_delay_days
        if not attempts_for_target:
            level = "未测"
        elif not dates:
            level = "需支持"
        elif len(dates) < min_dates or not delay_ok:
            level = "曾独立完成"
        elif variant_passes >= min_variant:
            level = "迁移通过"
        else:
            level = "延迟通过"

        hint_counts: dict[str, int] = {}
        measured = 0.0
        estimated = 0.0
        needs_verify_events = 0
        for attempt in attempts_for_target:
            # 提示依赖按**目标**记（2026-09-28）：与升级判定同源，
            # 否则"同事件里独立答对的目标"会被事件级的最大提示级别带偏
            hint = hint_level_of(attempt, tid)
            key = f"h{hint}" if isinstance(hint, int) and not isinstance(hint, bool) else "unknown"
            hint_counts[key] = hint_counts.get(key, 0) + 1
            measured += measured_minutes(attempt)
            estimated += estimated_minutes(attempt)
            tr = attempt.get("target_results")
            if isinstance(tr, dict) and isinstance(tr.get(tid), dict) and tr[tid].get("needs_verify"):
                needs_verify_events += 1

        # ---- 分开表示的五件事（2026-09-30 新增；勿挤成一个"等级"）----------------
        # ① 作业完成：是否有题目被标记 done（事务性，不等于会做）
        # ② 概念困难是否解决：hurdles 的状态（verified/closed = 已结案）
        # ③ 独立作答表现：无提示独立通过的日期（= level 的依据）
        # ④ 延迟检验结果：日期跨度是否达到 min_delay_days
        # ⑤ 课程覆盖：有没有题（没题 → 未安排，**不等于已掌握也不等于没学**）
        my_tasks = tasks_for_target.get(tid, [])
        my_hurdles = hurdles_for_target.get(tid, [])
        resolved_hurdles = [h for h in my_hurdles if h.get("status") in ("verified", "closed")]
        open_my_hurdles = [h for h in my_hurdles if h.get("status") in ("open", "teaching", "awaiting_retest")]
        if not my_tasks:
            coverage = "未安排（无题目）"
        elif not attempts_for_target:
            coverage = "已安排·未作答"
        elif not dates and not open_book_pass_dates:
            coverage = "已作答·需补练"
        elif level == "迁移通过":
            coverage = "独立通过"
        elif dates:
            coverage = "已独立通过·待延迟复测"
        else:
            coverage = "已作答·开卷/受助通过"
        # 帮助史与曝光史（跨窗口保留）：哪些事件被帮助/曝光挡住了升级
        helped_events = len(upgrade_blocked.get(tid, []))
        target_meta = goal_index.get(tid, {})

        targets[tid] = {
            "level": level,
            # 稳定证据＝≥min_dates 个不同日期独立通过 **且** 含 ≥min_variant 次未见变式通过（＝迁移通过）
            "stable_evidence": level == "迁移通过",
            "attempts": len(attempts_for_target),
            "independent_pass_dates": dates,
            "delay_days": delay_days,
            "delay_requirement_days": min_delay_days,
            "open_book_pass_dates": sorted(open_book_pass_dates),
            "variant_passes": variant_passes,
            "version_mismatch_events": version_mismatches,
            "unknown_version_events": unknown_version_events,
            "hint_dependence": hint_counts,
            "measured_minutes": round(measured, 1),
            "estimated_minutes": round(estimated, 1),
            "needs_verify_events": needs_verify_events,
            # 逐目标列出"未升级的作答事件与原因"——空表示该目标所有作答都已按规则处理
            "upgrade_blocked": upgrade_blocked.get(tid, []),
            "open_hurdles": hurdles_for_target.get(tid, []),
            "last_attempt": max(str(a["ts"]) for a in attempts_for_target) if attempts_for_target else None,
            # ---- 2026-09-30 新增 ----
            "goal": {
                "id": target_meta.get("goal_id"),
                "title": target_meta.get("goal_title"),
                "subject": target_meta.get("subject"),
                "status": target_meta.get("goal_status"),
            },
            "tasks": my_tasks,
            "task_count": len(my_tasks),
            "coverage": coverage,
            "status_dimensions": {
                "assignment_done": bool(my_tasks) and all(t.get("status") == "done" for t in my_tasks),
                "concept_hurdle_resolved": (not my_hurdles) or (not open_my_hurdles),
                "concept_hurdles": {
                    "open": [h.get("hurdle_id") for h in open_my_hurdles],
                    "resolved": [h.get("hurdle_id") for h in resolved_hurdles],
                },
                "independent_performance": {
                    "pass_dates": dates,
                    "open_book_only": sorted(open_book_pass_dates),
                    "helped_or_exposed_events": helped_events,
                },
                "delayed_retest": {
                    "required_delay_days": min_delay_days,
                    "achieved_delay_days": delay_days,
                    "satisfied": delay_ok,
                },
            },
        }

    levels = {"未测": 0, "需支持": 0, "曾独立完成": 0, "延迟通过": 0, "迁移通过": 0}
    for target in targets.values():
        levels[target["level"]] += 1

    coverage_counts: dict[str, int] = {}
    for target in targets.values():
        coverage_counts[target["coverage"]] = coverage_counts.get(target["coverage"], 0) + 1

    return {
        "generated_at": dt.date.today().isoformat(),
        "rule": (
            "独立通过按**目标**判定：该目标结果正确+**明确无提示**+`needs_verify` 不为真+未见解答+非示例学习"
            + ("+闭卷" if require_closed_book else "（不要求闭卷）")
            + "；目标级字段（target_results[tid]）优先，缺失回退事件级；"
            "提示级别未知（null）不计独立通过；needs_verify=true 的目标**不得升级**；"
            "exposure_timing=after_attempt 的曝光不阻断。"
            f"≥{min_dates} 个不同日期且日期跨度 ≥{min_delay_days} 天=延迟通过；"
            f"另含 ≥{min_variant} 次未见变式通过=迁移通过（**仅迁移通过计为稳定证据**）。"
            "未见变式=题目在整份日志中首次被作答（任何目标）+该版本 kind 为变式类。"
            "参数来自 learning/policy.yml，为工程初值。"
        ),
        "warnings": warnings,
        # 事实源指纹（2026-09-30）：证明本文件是从**当前** attempts/corrections 算出来的。
        # 并发会话若用较旧快照覆盖派生状态，指纹就会与库不一致 → 可被检测（ISSUES D4）。
        "source": source_fingerprint(root),
        "summary": {
            "targets": len(targets),
            "by_level": levels,
            "stable_evidence": sum(1 for t in targets.values() if t["stable_evidence"]),
            "open_hurdles": open_hurdle_count,
            "hurdle_bad_lines": hurdle_bad_lines,
            # 课程覆盖：区分"未安排（无题目）/已安排未作答/需补练/独立通过/待延迟复测"
            "coverage": coverage_counts,
            # 有目标但一道题都没有的（纸面目标）——必须能一眼看到，不能静默消失
            "targets_without_tasks": sorted(t for t, v in targets.items() if not v["tasks"]),
            # 全局时长按**不同事件**去重（同一次作答涉及多目标时不重复计入全局）
            "measured_minutes_global": round(sum(measured_minutes(a) for a in attempts), 1),
            "estimated_minutes_global": round(sum(estimated_minutes(a) for a in attempts), 1),
            "time_note": "measured=actual/self_reported；estimated 单独统计；未知不给值",
        },
        "targets": targets,
    }


def source_fingerprint(root: Path) -> dict:
    """事实源指纹：attempts.jsonl 的 sha256 + 事件条数 + corrections 条数。

    用途（2026-09-30，ISSUES D4）：`learner-state.json` 是派生视图，必须能证明
    "我是从**当前**事实源算出来的"。并发会话各跑一次 derive 时，后写者若用的是较旧快照，
    指纹就会与库不一致 → 可被检测出来，而不是靠人眼看等级有没有"倒退"。
    """
    import hashlib

    attempts_path = Path(root) / "learning" / "attempts.jsonl"
    raw = attempts_path.read_bytes() if attempts_path.is_file() else b""
    events = len([l for l in raw.decode("utf-8", "replace").splitlines() if l.strip()])
    corrections_path = Path(root) / "learning" / "corrections.jsonl"
    corrections = 0
    if corrections_path.is_file():
        corrections = len([l for l in corrections_path.read_text(encoding="utf-8").splitlines() if l.strip()])
    result = {
        "attempts_sha256": hashlib.sha256(raw).hexdigest(),
        "attempts_events": events,
        "corrections_events": corrections,
    }
    # Hash every input that can change a capability decision, not just row counts.
    paths = [Path(root) / 'learning' / name for name in
             ('corrections.jsonl', 'hurdles.jsonl', 'goals.yaml', 'policy.yml', 'task-windows.json')]
    paths += sorted((Path(root) / 'learning' / 'tasks').rglob('*.md'))
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.relative_to(root).as_posix().encode('utf-8'))
        digest.update(b'\0')
        digest.update(path.read_bytes() if path.is_file() else b'<missing>')
        digest.update(b'\0')
    result['decision_inputs_sha256'] = digest.hexdigest()
    return result


def write_derived_state(root: Path, state: dict) -> Path:
    """把派生状态**原子**写入 learning/learner-state.json（唯一写入口）。

    2026-09-30（ISSUES D4）：与 attempts 同源的并发风险——两条会话线各跑一次 derive
    会让后写者覆盖先写者，甚至用**较旧**的一次派生结果把等级/独立通过日期写回去。
    现在：写临时文件 + `os.replace` 原子替换（读者永远看不到半写文件），
    并在锁内比对"读到的 attempts.jsonl 快照"是否仍是写锁时的那一份：
    不一致说明期间有人追加了新事件 → 重新派生，而不是把旧结果写下去。
    """
    out = Path(root) / "learning" / "learner-state.json"
    text = json.dumps(state, ensure_ascii=False, indent=2) + "\n"
    atomic_write_text(out, text)
    return out


def derive_and_write(root: Path) -> dict:
    """锁内派生 + 原子写入：拿到锁后确认事实源没变，变了就重算（不允许旧快照覆盖新状态）。"""
    attempts_path = Path(root) / "learning" / "attempts.jsonl"
    corrections_path = Path(root) / "learning" / "corrections.jsonl"
    last_exc: Exception | None = None
    for attempt_no in range(1, 6):
        before = (snapshot(attempts_path), snapshot(corrections_path))
        try:
            with WorkspaceLock(Path(root) / "learning", label="derive_state"):
                after = (snapshot(attempts_path), snapshot(corrections_path))
                if before != after:
                    raise ConcurrentModification(
                        f"等锁期间事实源被改写（attempts/corrections 快照变化）→ 重算（{attempt_no}/5）"
                    )
                state = derive(root)
                write_derived_state(root, state)
                return state
        except (ConcurrentModification, LockTimeout) as exc:
            last_exc = exc
            print(f"WARN {exc}")
    raise RuntimeError(f"连续 5 次未能在稳定快照上派生状态，未写入：{last_exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Derive capability state from attempt events.")
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    state = derive_and_write(root)
    out = root / "learning" / "learner-state.json"
    print(f"wrote {out}")
    print(f"- targets: {state['summary']['targets']}")
    print(f"- by_level: {state['summary']['by_level']}")
    print(f"- stable_evidence: {state['summary']['stable_evidence']}")
    print(f"- 有目标但无题目（纸面目标）：{state['summary']['targets_without_tasks'] or '无'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
