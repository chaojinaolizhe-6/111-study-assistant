#!/usr/bin/env python3
"""周计划排期脚本（跨课程 + 截止日期 + 设备时段 + 三条队列 + 容量约束）。

这是对 tutor 模板确认缺失功能的唯一补充。三队列竞争同一时间预算：
- 记忆维护队列：到期概念复习（扫描 subjects 概念笔记 frontmatter 的 due，与 state/due.md 同源）
- 能力建设队列：learning/tasks/ 中未完成的题目（独立手推/方法选择）
- 修复与再测队列：attempts.jsonl 中错因待确认/待修复的作答（诊断状态 pending_probe|confirmed）

规则：
- 截止日期优先；白天平板 / 晚上电脑设备约束；每天每时段最多用 可用时间 × slack
- 可选"阶段时间比例"：每个类别的每日配额 = 当日总容量 × 比例，防止到期复习挤占独立解题
- 可选"周容量约束"：Σ承诺任务 ≤ (1-buffer) × 周专注预算；超了显式告警（延期不靠平摊制造可行性）
- 排不下的任务显式告警；大任务可跨天拆分

用法:
  python -B tools/plan-week.py --inputs plan/inputs.yml --root . --out plan/week-plan.md
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path

from learninglib import (  # noqa: E402
    apply_corrections,
    is_independent_pass_for,
    load_corrections,
    parse_yaml,
    parse_frontmatter,
    parse_list,
)

WEEKDAY_CN = {1: "周一", 2: "周二", 3: "周三", 4: "周四", 5: "周五", 6: "周六", 7: "周日"}
CATEGORY_LABEL = {"recall": "复习", "independent": "能力", "concept": "概念", "planning": "规划"}


def scan_due_concepts(root: Path, today: dt.date, horizon: dt.date) -> list[dict]:
    """记忆维护队列：到期概念复习。

    2026-09-30（统一队列来源）：改为调用 `tools/reviews.py` 的**同一实现**，
    不再在这里自己写一份 glob + frontmatter 解析。
    旧实现用 `subjects/*/topics/*/*.md`（要求 topics 下还有一层子目录），
    而当前的概念笔记是 `subjects/<课>/topics/<主题>.md` → **一条都扫不到**，
    于是 `plan-week` 与 `schedule_reviews` 会给出**不一致**的复习队列。
    """
    from reviews import load_concept_reviews

    tasks = []
    for item in load_concept_reviews(root):
        due = dt.date.fromisoformat(item["due"])
        if due > horizon:
            continue
        tasks.append(
            {
                "id": item["id"],
                "course": item["subject"],
                "title": f"概念复习：{item['id']}",
                "due": due,
                "overdue_days": max((today - due).days, 0),
                "est_minutes": item["minutes"],
                "device": item["device"],
                "category": "recall",
                "kind": "review",
            }
        )
    return tasks


def load_learning_tasks(root: Path, horizon: dt.date) -> list[dict]:
    """能力建设队列：learning/tasks/ 中**未作答**的题目。

    2026-09-30：加"已作答即出队"的过滤（与 `reviews.load_task_due_dates` 同口径）。
    理由：作答后 frontmatter 的 `status` 往往没人改，已做完的题会一直占着能力建设队列；
    仍需重测的由**修复/再测队列**按目标给出（那里才看得到"延迟够不够"）。
    """
    from learninglib import completed_task_ids, current_task_metadata

    answered = completed_task_ids(root)
    tasks = []
    base = root / "learning" / "tasks"
    if not base.is_dir():
        return tasks
    for path in sorted(base.glob("*.md")):
        if path.name.startswith("_"):
            continue
        fm = current_task_metadata(root,path)
        task_id = fm.get("id")
        if not task_id:
            continue
        if fm.get("status") == "done" or task_id in answered:
            continue
        kind = fm.get("kind", "practice")
        due_text = fm.get("due", "")
        from reviews import date_prefix
        placeholder = False
        try:
            due = dt.date.fromisoformat(date_prefix(due_text) or '')
        except ValueError:
            due = horizon + dt.timedelta(days=1)
            placeholder = True  # 程序默认视界，不是真实截止日期
        gate_text = fm.get('not_before')
        not_before = dt.date.fromisoformat(date_prefix(gate_text) or '') if gate_text else None
        gate_time = None
        due_time = None
        for value, which in ((gate_text, 'gate'), (due_text, 'due')):
            if value and len(str(value).strip()) > 10:
                parsed = dt.datetime.fromisoformat(str(value).strip())
                if which == 'gate':
                    gate_time = parsed.strftime('%H:%M')
                else:
                    due_time = parsed.strftime('%H:%M')
        try:
            est = int(fm.get("est_minutes", "30"))
        except ValueError:
            est = 30
        tasks.append(
            {
                "id": task_id,
                "course": fm.get("subject", "（未标课程）"),
                "title": fm.get("title", task_id),
                "due": due,
                "not_before": not_before,
                "not_before_time": gate_time,
                "due_time": due_time,
                "est_minutes": est,
                "device": fm.get("device", "any"),
                "category": "concept" if kind == "worked-example" else "independent",
                "kind": kind,
                "due_is_placeholder": placeholder,
            }
        )
    return tasks


def declared_targets(root: Path) -> dict[tuple[str, str], list[str]]:
    """题目各版本声明的目标：{(task_id, version): [target...]}（当前版本 + learning/tasks/history/）。"""
    registry: dict[tuple[str, str], list[str]] = {}
    base = root / "learning" / "tasks"
    if base.is_dir():
        for path in sorted(base.glob("*.md")):
            if path.name.startswith("_"):
                continue
            fm = parse_frontmatter(path.read_text(encoding="utf-8"))
            task_id = fm.get("id")
            if not task_id:
                continue
            version = fm.get("version", "1")
            targets = parse_list(fm.get("target_ids", "[]"))
            registry[(task_id, version)] = targets if isinstance(targets, list) else []
    history_dir = base / "history"
    if history_dir.is_dir():
        for path in sorted(history_dir.glob("*.md")):
            if path.name.startswith("_"):
                continue
            fm = parse_frontmatter(path.read_text(encoding="utf-8"))
            task_id = fm.get("id")
            version = fm.get("version")
            if not task_id or not version:
                continue
            targets = parse_list(fm.get("target_ids", "[]"))
            registry[(task_id, version)] = targets if isinstance(targets, list) else []
    return registry


def load_repair_tasks(
    root: Path, today: dt.date, horizon: dt.date, write_queue: bool = True
) -> tuple[list[dict], set[str]]:
    """修复与再测队列：按 (题目, 目标) 粒度追踪，一次通过只关闭它实际覆盖的问题。

    - 对每个 (task_id, target)，取**最后一条包含该目标**的作答事件（追加式日志：行序即时间序）。
    - 该事件是独立通过 → 该目标已闭环，不入队。
    - 该事件诊断状态 ∈ {pending_probe, confirmed} 且不是独立通过 → 该目标入队
      （含"提示后做对但错因待确认"：辅导后做对≠问题解决）。
    - 同一道题：目标 A 失败待修复、随后只针对目标 B 独立通过 → A 仍入队，不被 B 关闭。
    - 事件版本元数据缺失 → 不参与修复推断（保守）。
    返回 (repair_tasks, source_task_ids)：source_task_ids 用于从能力建设队列中剔除
    同一道题，避免"原题 + 修复任务"被重复安排。
    """
    tasks = []
    source_ids: set[str] = set()
    path = root / "learning" / "attempts.jsonl"
    if not path.is_file():
        return tasks, source_ids
    registry = declared_targets(root)
    repair_registry = load_repair_registry(root)
    last_by_pair: dict[tuple[str, str], dict] = {}
    raw_events: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            raw_events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    # 与 validate_attempts / derive_state 同源：排期也在"应用订正后的记录"上做
    for row in apply_corrections(raw_events, load_corrections(root)):
        task_id = row.get("task_id", "")
        version = str(row.get("task_version", ""))
        declared = registry.get((task_id, version))
        if not declared:
            continue  # 版本元数据缺失：保留记录，但不据此推断修复
        for target in row.get("target_ids", []):
            if target in declared:
                last_by_pair[(task_id, target)] = row
    # 第一遍：判定哪些 (题目, 目标) 需要进修复队列，并维护 first_seen 登记（历史保留）
    queued: dict[str, list[tuple[str, dt.date, int]]] = {}   # target -> [(task_id, due, overdue_days)]
    from learninglib import resumable_attempts
    unfinished_ids = {e['task_id'] for e in resumable_attempts(root)}
    for (task_id, target), last in sorted(last_by_pair.items()):
        if task_id in unfinished_ids:
            continue  # Continue the unfinished concrete task; preserve its original deadline.
        # 判定与 derive_state 共用同一实现（2026-09-27 修规则漂移：此前此处仍是旧的 hint in (0, None)）
        # 2026-09-28：改为**逐目标**判定，与下方 target_results 的按目标闭环口径统一
        if is_independent_pass_for(last, target, require_closed_book=True):
            continue
        # 按目标闭环：target_results 里明确"已订正且无需核验"的目标不再入队；
        # 明确 needs_verify 的目标即使同题其它目标已订正，也仍入队（不互相连带关闭）。
        per_target = last.get("target_results")
        if isinstance(per_target, dict) and isinstance(per_target.get(target), dict):
            detail = per_target[target]
            if detail.get("needs_verify"):
                pass
            elif detail.get("final") == "correct":
                continue
        if last.get("diagnosis_status") not in {"pending_probe", "confirmed"}:
            continue
        source_ids.add(task_id)
        # 修复任务日期：**首次建立时固定**，之后保持原日期；到期未做显示逾期，不再每天自动后移
        repair_key = f"repair-{task_id}-{target}"
        entry = repair_registry.get(repair_key)
        if not isinstance(entry, dict) or "target_process_date" not in entry:
            entry = {
                "first_seen": today.isoformat(),
                "target_process_date": (today + dt.timedelta(days=2)).isoformat(),
                "reason": "首次建立（默认给 2 天窗口）；延期需人工在本文件写延期理由",
            }
            repair_registry[repair_key] = entry
        try:
            due = dt.date.fromisoformat(str(entry["target_process_date"]))
        except ValueError:
            due = today + dt.timedelta(days=2)
        queued.setdefault(target, []).append((task_id, due, max((today - due).days, 0)))

    # 第二遍：**按目标合并成一次覆盖性复测**（2026-09-28）。
    # 此前每个 (题目, 目标) 各排一条 → 同一个目标被拆成多轮旧题重做
    # （判据二曾被 tm-t4-criteria-01/02/03 排成 3×20 分钟 = 60 分钟，而实际状态是
    #  "补讲完成、待延迟复测"）。修复队列的口径本来就是**按目标闭环**，所以下一步应当是
    #  **一次覆盖该目标的未见变式复测**，而不是重放旧题。
    # 历史的 first_seen 仍按 (题目, 目标) 记在 repair-queue.json 里，不丢。
    #
    # 2026-09-30：加 `not_before`（**最早可做日期**）——取自 `tools/reviews.py` 的同一判定。
    # 典型情形：某目标已有独立通过，但日期跨度不足 `min_delay_days` → 必须等到
    # 最后一次独立通过 + 2 天才能做换题复测。旧实现只看截止日，会把这种任务排进**今天**，
    # 与 `plan/schedule.md`（"未来才开放，不得提前安排"）直接矛盾。
    from reviews import load_capability_retests

    retest_gate = {item["id"]: item["due"] for item in load_capability_retests(root, today.isoformat())}
    for target, items in sorted(queued.items()):
        task_ids = [t for t, _d, _o in items]
        due = min(d for _t, d, _o in items)                 # 取最紧的那个窗口
        overdue_days = max(o for _t, _d, o in items)
        shown = "、".join(task_ids[:3]) + ("…" if len(task_ids) > 3 else "")
        gate_text = retest_gate.get(target)
        not_before = None
        if gate_text:
            try:
                not_before = dt.date.fromisoformat(gate_text)
            except ValueError:
                not_before = None
        if not_before and not_before > due:
            due = not_before  # 不得早于"最早可做日期"
        tasks.append(
            {
                "id": f"repair-{target}",
                "course": "修复",
                "title": (
                    f"错因覆盖复测：{target}（覆盖 {len(task_ids)} 个历史题目：{shown}）"
                    "—— 用一道**未见变式**一次覆盖，不重放旧题"
                ),
                "due": due,
                "not_before": not_before,
                "overdue_days": overdue_days,
                "est_minutes": 20,
                "device": "any",
                "category": "independent",
                "kind": "repair",
            }
        )
    # 2026-09-28（ISSUES B4）：原先**无条件**重写 repair-queue.json —— 跑一次"验证"就改了数据。
    # 现在由调用方决定；--dry-run / --no-write-queue 时只读不写。
    if write_queue:
        save_repair_registry(root, repair_registry)
    else:
        print(
            "NOTE: --dry-run/--no-write-queue 生效：未写 learning/repair-queue.json（队列变更未持久化）",
            file=sys.stderr,
        )
    return tasks, source_ids


def load_repair_registry(root: Path) -> dict:
    """修复队列的**首次建立日期**登记（learning/repair-queue.json）。

    存在这里的原因：修复任务日期必须在首次建立时固定，之后每次排期保持不变；
    到期未做应显示逾期，而不是每天自动顺延到 today+2。
    """
    path = root / "learning" / "repair-queue.json"
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def save_repair_registry(root: Path, registry: dict) -> None:
    path = root / "learning" / "repair-queue.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_inputs(path: Path) -> dict:
    if not path.is_file():
        print(f"ERROR: inputs file not found: {path}", file=sys.stderr)
        sys.exit(2)
    data = parse_yaml(path.read_text(encoding="utf-8"))
    for key in ["today", "days", "slack", "windows", "assignments"]:
        if key not in data:
            print(f"ERROR: inputs file missing key: {key}", file=sys.stderr)
            sys.exit(2)
    return data


def minute(value: str) -> int:
    hour, minutes = map(int, value.split(':'))
    if not 0 <= hour <= 24 or not 0 <= minutes < 60 or (hour == 24 and minutes):
        raise ValueError('Invalid time: '+value)
    return hour * 60 + minutes


def build_slots(data: dict, today: dt.date) -> list[dict]:
    slack = float(data.get("slack", 0.7))
    slots = []
    for day_index in range(int(data.get("days", 7))):
        day = today + dt.timedelta(days=day_index)
        for window in data.get("windows", []):
            if not isinstance(window, dict):
                continue
            days = window.get("days", [1, 2, 3, 4, 5, 6, 7])
            if not isinstance(days, list):
                days = [days]
            if day.isoweekday() not in days:
                continue
            start = str(window.get("start", "09:00"))
            end = str(window.get("end", "18:00"))
            start_min = minute(start)
            end_min = minute(end)
            start = f'{start_min//60:02d}:{start_min%60:02d}'
            end = f'{end_min//60:02d}:{end_min%60:02d}'
            window_capacity = max(end_min - start_min, 0)
            cap = int(window.get("max_minutes", window_capacity))
            capacity = int(min(cap, window_capacity) * slack)
            slots.append(
                {
                    "day": day,
                    "device": window.get("device", "any"),
                    "window_id": window.get("id", "?"),
                    "start": start,
                    "end": end,
                    "raw_capacity": cap,
                    "capacity": capacity,
                    "used": 0,
                    "tasks": [],
                    "allocated_minutes": set(),
                }
            )
    return slots


def phase_ratios(data: dict) -> dict[str, float]:
    """返回 {category: ratio}；未配置阶段比例时返回空 dict（不设配额）。"""
    ratios = data.get("ratios")
    if not isinstance(ratios, dict):
        return {}
    capacity = data.get("capacity") or {}
    phase = capacity.get("phase", "常规巩固期")
    phase_map = ratios.get(phase) or ratios.get("常规巩固期") or {}
    if not isinstance(phase_map, dict):
        return {}
    out: dict[str, float] = {}
    for key in ("concept", "independent", "recall", "planning"):
        value = phase_map.get(key)
        if isinstance(value, (int, float)):
            out[key] = float(value)
    return out


def day_budgets(slots: list[dict], ratios: dict[str, float]) -> dict[tuple, int]:
    """每天每类别的分钟配额（当日总容量 × 比例）。ratios 为空 → 返回空 dict（不限配额）。"""
    budgets: dict[tuple, int] = {}
    if not ratios:
        return budgets
    per_day: dict[dt.date, int] = {}
    for slot in slots:
        per_day[slot["day"]] = per_day.get(slot["day"], 0) + slot["capacity"]
    for day, total in per_day.items():
        for category, ratio in ratios.items():
            budgets[(day, category)] = int(total * ratio)
    return budgets


def compatible(slot: dict, device: str) -> bool:
    if device == "any":
        return True
    return slot["device"] == device


def slot_priority(slot: dict, device: str) -> tuple:
    if device == "any":
        return (0 if slot["device"] == "tablet" else 1, slot["day"], slot["start"])
    return (0, slot["day"], slot["start"])


def place_task(slot: dict, task: dict, minutes: int) -> None:
    slot["used"] += minutes
    slot["capacity"] -= minutes
    slot["tasks"].append({**task, "chunk": minutes})


def schedule(tasks: list[dict], slots: list[dict], budgets: dict[tuple, int], today: dt.date) -> tuple[list[dict], list[dict]]:
    ordered = sorted(tasks, key=lambda t: (t["due"], -t["est_minutes"], t["course"], t["id"]))
    placed: list[dict] = []
    warnings: list[dict] = []
    for task in ordered:
        remaining = int(task["est_minutes"])
        assignment: dict = {"task": task, "parts": []}
        # 到期日=截止日：当天仍可安排；已逾期任务从今天起安排（不因"截止已过"被丢弃）
        effective_due = max(task["due"], today)
        # 2026-09-30（本轮改进要求："未来才开放的任务不提前安排"）：
        # 有些任务有**最早开始日**（如"已有独立通过 + 2 天延迟"才能做换题复测，
        # 或"选课窗口 10-08 12:30 才开"）。这类任务不得排到 not_before 之前——
        # 旧实现只看截止日，会把它们排进**今天**，与 `plan/schedule.md` 的日期互相矛盾。
        not_before = task.get("not_before")
        if isinstance(not_before, dt.date) and not_before > today:
            effective_start = not_before
        else:
            effective_start = today
        candidate_slots = sorted(
            (
                s
                for s in slots
                if compatible(s, task["device"])
                and s["day"] <= effective_due
                and s["day"] >= effective_start
            ),
            key=lambda s: slot_priority(s, task["device"]),
        )
        for slot in candidate_slots:
            if remaining <= 0:
                break
            if slot["capacity"] <= 0:
                continue
            lower = minute(slot['start'])
            upper = minute(slot['end'])
            if slot['day'] == not_before and task.get('not_before_time'):
                lower = max(lower, minute(task['not_before_time']))
            if slot['day'] == task['due'] and task.get('due_time'):
                upper = min(upper, minute(task['due_time']))
            used_minutes = slot.setdefault('allocated_minutes',set())
            free_minutes = [n for n in range(lower,upper) if n not in used_minutes]
            if not free_minutes:
                continue
            budget_key = (slot["day"], task["category"])
            if budget_key in budgets:
                if budgets[budget_key] <= 0:
                    continue
                chunk = min(remaining, slot["capacity"], budgets[budget_key],len(free_minutes))
            else:
                chunk = min(remaining, slot["capacity"],len(free_minutes))
            place_task(slot, task, chunk)
            chosen = free_minutes[:chunk]
            used_minutes.update(chosen)
            slot['tasks'][-1]['scheduled_time'] = f'{chosen[0]//60:02d}:{chosen[0]%60:02d}–{(chosen[-1]+1)//60:02d}:{(chosen[-1]+1)%60:02d}'
            if budget_key in budgets:
                budgets[budget_key] -= chunk
            assignment["parts"].append((slot["day"], slot["window_id"], chunk))
            remaining -= chunk
        if remaining > 0:
            overdue = task.get("overdue_days", 0)
            overdue_note = f"；已逾期 {overdue} 天" if overdue else ""
            gate_note = ""
            if isinstance(not_before, dt.date) and not_before > effective_due:
                gate_note = f"；最早可做 {not_before}（晚于截止 {task['due']}）→ 需先与学习者确认"
            warnings.append(
                {
                    "id": task["id"],
                    "title": task["title"],
                    "course": task["course"],
                    "due": task["due"],
                    "unplaced_minutes": remaining,
                    "reason": f"截止 {task['due']}（含当天）前可排的兼容时段/类别配额不足{overdue_note}{gate_note}",
                }
            )
        if assignment["parts"]:
            placed.append(assignment)
    return placed, warnings


def render(placed: list[dict], warnings: list[dict], slots: list[dict], data: dict, inputs_path: Path, root: Path, ratios: dict[str, float]) -> str:
    today = dt.date.fromisoformat(str(data["today"]))
    days = int(data.get("days", 7))
    slack = float(data.get("slack", 0.7))
    capacity = data.get("capacity") or {}
    weekly = capacity.get("weekly_minutes")
    buffer_ratio = float(capacity.get("buffer_ratio", 0.3)) if weekly else None
    lines = [
        f"# 周计划（{today.isoformat()} 起 {days} 天）",
        "",
        f"> 生成产物，勿手工编辑。生成器：tools/plan-week.py；输入：{inputs_path}；复习来源：{root}/subjects 概念笔记 frontmatter。",
        f"> 余量系数：每天每时段最多排 {slack:.0%} 的可用时间。",
    ]
    if ratios:
        ratio_text = "、".join(f"{CATEGORY_LABEL.get(k, k)} {v:.0%}" for k, v in ratios.items())
        lines.append(f"> 阶段时间比例（每日配额）：{ratio_text}。")
    lines.append("")
    for day_index in range(days):
        day = today + dt.timedelta(days=day_index)
        lines.append(f"## {day.isoformat()} {WEEKDAY_CN[day.isoweekday()]}")
        lines.append("")
        day_slots = [s for s in slots if s["day"] == day]
        if not day_slots:
            lines.append("（当日无可用时段）")
            lines.append("")
            continue
        for slot in sorted(day_slots, key=lambda s: s["start"]):
            label = "平板（白天）" if slot["device"] == "tablet" else ("电脑（晚上）" if slot["device"] == "pc" else "通用")
            lines.append(
                f"- {label} {slot['start']}-{slot['end']}：已排 {slot['used']} 分钟，余 {slot['capacity']} 分钟"
            )
            for item in slot["tasks"]:
                due = item["due"]
                cat = CATEGORY_LABEL.get(item["category"], item["category"])
                overdue_mark = f"（已逾期 {item['overdue_days']} 天）" if item.get("overdue_days") else ""
                if item.get("due_is_placeholder"):
                    note = f"（**无真实截止日期**；排期占位 {due}；{item['chunk']} 分钟）{overdue_mark}[{cat}]"
                else:
                    note = f"（截止 {due}；{item['chunk']} 分钟）{overdue_mark}[{cat}]"
                lines.append(f"  - [{item['course']}] {item['title']} {note}；安排 {item.get('scheduled_time','按时段分配')}")
        lines.append("")
    committed = sum(minutes for assignment in placed for _day, _w, minutes in assignment["parts"])
    lines.append("## 排期报告")
    lines.append("")
    if weekly:
        effective = int(weekly * (1 - buffer_ratio))
        lines.append(f"- 周容量：承诺 {committed} 分钟；可用 {weekly} 分钟；缓冲 {buffer_ratio:.0%}；上限 {effective} 分钟。")
        if committed > effective:
            lines.append(f"- ⚠ 容量不足：承诺超出上限 {committed - effective} 分钟。请移出低价值任务或缩减目标范围，不要给每天加任务。")
    else:
        lines.append(f"- 承诺任务总时长：{committed} 分钟（未配置周容量，不做容量检查）。")
    if warnings:
        lines.append("## ⚠ 排期告警")
        lines.append("")
        for warn in warnings:
            lines.append(f"- {warn['course']} / {warn['title']}：{warn['reason']}，剩余 {warn['unplaced_minutes']} 分钟未排。")
        lines.append("")
    lines.append("## 说明")
    lines.append("")
    lines.append("- 排序规则：截止日期优先，同截止日期时预估耗时长的优先；复习任务（any）优先放白天平板时段。")
    lines.append("- 三队列：记忆维护（到期概念）/ 能力建设（learning/tasks）/ 修复再测（attempts 中待修复错因）竞争同一时间预算。")
    lines.append("- 检查点建议：独立推导块 35~45 分钟后判断\"仍在产生新推理 / 原地打转 / 缺前置 / 疲劳\"，再决定延长、诊断、修复或换低负荷任务。")
    lines.append("- 标「**无真实截止日期**；排期占位」的日期是脚本默认视界（today+days），**不是真实作业截止日期**；拿到真实截止后写入 plan/inputs.yml 的 assignments。")
    lines.append("- **脚本不支持当日临时时间窗**（如\"今天学到 13:00\"）：临时窗口写在 `plan/today-YYYY-MM-DD.md`，当天以该文件为准；临时窗口不跨天沿用。")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a cross-course weekly plan.")
    parser.add_argument("--inputs", default="plan/inputs.yml")
    parser.add_argument("--root", default=".")
    parser.add_argument("--out", default="plan/week-plan.md")
    parser.add_argument("--review-minutes", type=int, default=15, help="每个到期概念复习的预估分钟")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="**不写任何文件**（既不写 --out，也不写 learning/repair-queue.json）；只把预览打到屏幕",
    )
    parser.add_argument(
        "--no-write-queue", action="store_true",
        help="仍生成计划（照常写 --out），但**不写** learning/repair-queue.json",
    )
    args = parser.parse_args()
    write_queue = not (args.dry_run or args.no_write_queue)
    write_plan = not args.dry_run

    root = Path(args.root).resolve()
    inputs_path = Path(args.inputs).resolve()
    out_path = Path(args.out).resolve()

    data = load_inputs(inputs_path)
    today = dt.date.fromisoformat(str(data["today"]))
    horizon = today + dt.timedelta(days=int(data.get("days", 7)) - 1)

    tasks = [a for a in data.get("assignments", []) if a.get("status", "未开始") != "已提交"]
    for idx, task in enumerate(tasks, 1):
        task.setdefault("id", f"assignment-{idx}")  # 手写 inputs 漏 id 时不再整体崩溃
        task["due"] = dt.date.fromisoformat(str(task["due"]))
        task["category"] = "independent"
        task["kind"] = "assignment"
    if data.get("reviews", {}).get("enabled", True):
        review_tasks = scan_due_concepts(root, today, horizon)
        for task in review_tasks:
            task["est_minutes"] = int(data.get("reviews", {}).get("minutes_per_concept", args.review_minutes))
        tasks.extend(review_tasks)
    repair_tasks, repair_source_ids = load_repair_tasks(root, today, horizon, write_queue=write_queue)
    learning_tasks = [t for t in load_learning_tasks(root, horizon) if t["id"] not in repair_source_ids]
    tasks.extend(learning_tasks)
    tasks.extend(repair_tasks)

    slots = build_slots(data, today)
    ratios = phase_ratios(data)
    budgets = day_budgets(slots, ratios)
    placed, warnings = schedule(tasks, slots, budgets, today)
    text = render(placed, warnings, slots, data, inputs_path, root, ratios)
    if write_plan:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
        print(f"wrote {out_path} ({len(tasks)} tasks, {len(warnings)} warnings)")
    else:
        print(f"[dry-run] **未写任何文件**（--out 已忽略）：tasks={len(tasks)} warnings={len(warnings)}")
        print(f"[dry-run] 目标输出路径本应是：{out_path}")
        print("[dry-run] 渲染预览（前 40 行）：")
        for line in text.splitlines()[:40]:
            print("  " + line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
