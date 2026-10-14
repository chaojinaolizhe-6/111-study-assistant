#!/usr/bin/env python3
"""复习/再测的**到期扫描**（记忆维护队列 + 能力再测队列），单一实现。

消费者：`tools/schedule_reviews.py`（排成有日期的任务）、`tools/sync_status.py`（due_today 计数）。
此前 `sync_status.due_count()` 只去正则匹配 `state/due.md` 里的一句话——
而那份文件是"生成产物"，一旦没重跑就永远是 0，学习者"要有计划地定期复习"落不了地。

两个队列，**语义不同、不混用同一个分数**（`learning/README.md`）：
- **记忆维护**（SM-2，`state/`）：已经理解了、需要保持 → 到 `due` 就复习。
  来源：`subjects/**/*.md` frontmatter 的 `due` 字段。
- **能力再测**（`learning/`）：还没独立通过、或独立通过但延迟不够 → 换题重测。
  来源：`learning/learner-state.json`（派生自 attempts）+ `learning/tasks/` 的 `due` + `learning/hurdles.jsonl`。
"""
from __future__ import annotations

import re
from pathlib import Path

from learninglib import parse_frontmatter
from timebase import add_days, days_between

CONCEPT_GLOBS = ("subjects/*/topics/*.md", "subjects/*/topics/**/*.md")
# 只认 YYYY-MM-DD 前缀，允许后面跟行内注释（`due: 2026-10-10  # 口述`）。
# 为什么不能要求整串匹配（2026-09-30 实测踩到）：`parse_frontmatter` 不做行内注释剥离，
# `due: 2026-10-08   # 窗口才开` 会整串返回 → 严格匹配直接判定"无 due"，
# 任务就从排期里**静默消失**（正是本轮要消灭的那类问题）。
DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")


def date_prefix(value) -> str | None:
    """从 frontmatter 值里取 YYYY-MM-DD 前缀；没有则 None（不猜）。"""
    match = DATE_RE.match(str(value or "").strip())
    return match.group(1) if match else None


def load_concept_reviews(root: Path) -> list[dict]:
    """扫描概念笔记 frontmatter 的 `due` → 记忆维护队列（到期即复习）。"""
    rows: list[dict] = []
    seen: set[Path] = set()
    for pattern in CONCEPT_GLOBS:
        for path in sorted(Path(root).glob(pattern)):
            if path in seen or not path.is_file():
                continue
            seen.add(path)
            fm = parse_frontmatter(path.read_text(encoding="utf-8"))
            due = date_prefix(fm.get("due"))
            if not due:
                continue
            rows.append(
                {
                    "queue": "记忆维护",
                    "id": fm.get("id") or path.stem,
                    "subject": fm.get("subject") or path.parent.parent.name,
                    "kind": fm.get("kind", "concept"),
                    "due": due,
                    "minutes": _minutes(fm.get("est_minutes"), 15),
                    "device": fm.get("device", "any"),
                    "source": str(path.relative_to(root)).replace("\\", "/"),
                    "note": (fm.get("title") or path.stem).strip(),
                }
            )
    return rows


def _minutes(raw, default: int) -> int:
    try:
        value = int(str(raw).strip())
        return value if value > 0 else default
    except (TypeError, ValueError):
        return default


def load_capability_retests(root: Path, today: str) -> list[dict]:
    """由能力状态派生"需要重测/补练"的条目（**只看派生状态，不重复实现判定**）。"""
    import json

    state_path = Path(root) / "learning" / "learner-state.json"
    if not state_path.is_file():
        return []
    state = json.loads(state_path.read_text(encoding="utf-8"))
    rows: list[dict] = []
    for tid, target in sorted(state.get("targets", {}).items()):
        dims = target.get("status_dimensions") or {}
        delay = dims.get("delayed_retest") or {}
        perf = dims.get("independent_performance") or {}
        open_hurdles = [h for h in target.get("open_hurdles", []) if h.get("status") in ("open", "teaching", "awaiting_retest")]
        has_independent = bool(perf.get("pass_dates"))
        needs_verify = bool(target.get("needs_verify_events"))
        tasks = target.get("tasks") or []
        est = max((_minutes(t.get("est_minutes"), 0) for t in tasks), default=0) or 20

        if not tasks:
            kind, reason, not_before = "建题", "目标已声明但**一道题都没有**（纸面目标）→ 先出题", today
        elif has_independent and not delay.get("satisfied"):
            # 已经独立通过过，但延迟跨度不够 → 必须在**未来**某天做变式（不得排进过去）
            last = perf["pass_dates"][-1]
            need = int(delay.get("required_delay_days") or 2)
            not_before = add_days(last, need)
            kind, reason = "延迟检验", f"已有独立通过（{last}）；已验证通过日期跨度 {delay.get('achieved_delay_days')}d < {need}d；最早 {not_before} 可换题复测（等待本身不算通过）"
        elif target.get("variant_passes", 0) < 1 and has_independent:
            kind, reason, not_before = "未见变式", "独立通过过但还没有一次「未见变式」通过 → 换形态的新题", today
        elif open_hurdles:
            ids = "、".join(h.get("hurdle_id", "?") for h in open_hurdles)
            status = open_hurdles[0].get("status")
            kind = "补讲/补练" if status in ("open", "teaching") else "修复后再测"
            reason = f"未解决困难 {ids}（状态 {status}）"
            not_before = today
        elif needs_verify:
            kind, reason, not_before = "撤去帮助再测", "历史作答全部 needs_verify（受助/曝光）→ 需要无提示新题", today
        else:
            kind, reason, not_before = "补练", f"覆盖状态「{target.get('coverage')}」→ 继续练到能独立", today

        rows.append(
            {
                "queue": "能力再测",
                "id": tid,
                "subject": (target.get("goal") or {}).get("subject") or "（未归入能力目标）",
                "kind": kind,
                "due": not_before,
                "minutes": est,
                "device": "any",
                "source": f"learning/learner-state.json#{tid}",
                "note": reason,
            }
        )
    return rows


def load_task_due_dates(root: Path, today: str) -> list[dict]:
    """`learning/tasks/*.md` 里带 `due` 且**还没作答过**的题目 → 按截止日期进入排期。

    2026-09-30：加两条过滤/字段。
    ① 已作答过就不再当待办：此前只看 `status != done`，而作答后题目 frontmatter 的
       `status` 往往没人改 → 已做完的题会一直在"已逾期"里刷屏，把真正该做的事埋掉
       （"未完成事项静默消失"的反面：**已完成事项赖着不走**）。
       已作答的题若仍需重测，由**能力再测队列**按目标给出条目（那里才看得到"延迟够不够"）。
    ② `not_before`（frontmatter 可选）：**窗口/最早开始日期**——
       例如"形势与政策选课窗口 2026-10-08 12:30 才开"，在窗口开启前**不得**排进今天。
       没有这个字段时，只有 `due` 的题一律今天可做（保持旧行为）。
    """
    from learninglib import completed_task_ids, load_tasks

    answered = completed_task_ids(root)
    rows = []
    for task in load_tasks(root).values():
        due = date_prefix(task.get("due"))
        if not due or task.get("status") == "done":
            continue
        if task["id"] in answered:
            continue
        not_before = date_prefix(task.get("not_before"))
        note = f"题目截止 {due}"
        if days_between(due, today) > 0:
            note += "（已逾期）"
        if not_before and days_between(today, not_before) > 0:
            note += f"；窗口 {not_before} 才开 → 到日期前不得提前做"
        rows.append(
            {
                "queue": "题目截止",
                "id": task["id"],
                "subject": task.get("subject", "—"),
                "kind": task.get("kind", "practice"),
                "due": not_before or due,
                "deadline": due,
                "not_before": not_before,
                "minutes": _minutes(task.get("est_minutes"), 20),
                "device": task.get("device", "any"),
                "source": task.get("path", ""),
                "note": note,
                "targets": task.get("target_ids") or [],
            }
        )
    return rows


def load_goals_with_deadlines(root: Path) -> list[dict]:
    """带截止日期或里程碑的能力目标 → 反向排一个复习块（截止前留缓冲）。"""
    from goallib import load_goals

    rows = []
    for goal in load_goals(root):
        for key in ("deadline", "milestone"):
            value = date_prefix(goal.get(key))
            if not value:
                continue
            rows.append(
                {
                    "queue": "目标节点",
                    "id": f"{goal['id']}:{key}",
                    "subject": goal.get("subject") or "—",
                    "kind": "里程碑复核",
                    "due": value,
                    "minutes": 0,  # 只做提醒，不占预算（不编造课时）
                    "device": "any",
                    "source": "learning/goals.yaml",
                    "note": f"{goal.get('title')} 的 {key} = {value}",
                    "reminder_only": True,
                }
            )
    return rows


def load_assignment_items(root: Path) -> list[dict]:
    """`plan/inputs.yml` 的 assignments（**外部截止**，如作业/考试）→ 按截止进入排期。

    `plan/inputs.yml` 是这些截止的权威（来源标注 `[口述]`/`[变更留痕]`）；
    `learning/tasks/` 里的题目是另一类身份，两者**不重复排**（2026-09-28 `ee-lab1-prep` 教训）。
    仅收录 `status` 不是「已提交/已完成/已取消」的条目。
    """
    from learninglib import parse_yaml

    path = Path(root) / "plan" / "inputs.yml"
    if not path.is_file():
        return []
    raw = parse_yaml(path.read_text(encoding="utf-8"))
    done_words = ("已提交", "已完成", "已取消", "done", "closed")
    rows = []
    for item in raw.get("assignments") or []:
        if not isinstance(item, dict):
            continue
        due = date_prefix(item.get("due"))
        status = str(item.get("status") or "")
        if not due or any(w in status for w in done_words):
            continue
        rows.append(
            {
                "queue": "外部截止",
                "id": str(item.get("id")),
                "subject": str(item.get("course") or "—"),
                "kind": "作业/考试截止",
                "due": due,
                "minutes": _minutes(item.get("est_minutes"), 0),
                "device": item.get("device", "any"),
                "source": "plan/inputs.yml",
                "note": f"{item.get('title')}（截止 {due}，状态 {status or '未标注'}）",
            }
        )
    return rows


def all_review_items(root: Path, today: str) -> list[dict]:
    """各来源合并（记忆维护 / 能力再测 / 题目截止 / 外部截止 / 目标节点）。"""
    items = (
        load_concept_reviews(root)
        + load_capability_retests(root, today)
        + load_task_due_dates(root, today)
        + load_assignment_items(root)
        + load_goals_with_deadlines(root)
    )
    # 同一 target 既在 learner-state 又在 tasks 里出现时，按 id 去重（题目截止优先）
    by_id: dict[str, dict] = {}
    for item in items:
        by_id.setdefault(item["id"], item)
    return sorted(by_id.values(), key=lambda r: (r["due"], r["queue"], r["id"]))


def overdue_concepts(root: Path, today: str) -> list[dict]:
    """到期的记忆维护条目（due ≤ today）——`sync_status.due_today` 的真实来源。"""
    return [r for r in load_concept_reviews(root) if days_between(r["due"], today) >= 0]


def capability_due_today(root: Path, today: str) -> list[dict]:
    """今天可以动手的能力再测/补练条目（not_before ≤ today）。"""
    return [r for r in load_capability_retests(root, today) if days_between(r["due"], today) >= 0]


__all__ = [
    "all_review_items",
    "capability_due_today",
    "load_assignment_items",
    "load_capability_retests",
    "load_concept_reviews",
    "load_goals_with_deadlines",
    "load_task_due_dates",
    "overdue_concepts",
]
