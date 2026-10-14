#!/usr/bin/env python3
"""读取 learning/goals.yaml —— 能力目标（含**尚没有题目**的目标）。

**为什么单独一个模块**（ISSUES A7 根因）：
`goals.yaml` 此前只有 `validate_hurdles.py` 读，`derive_state.py` / `plan-week.py` 都不读。
而目标集合在 `derive_state` 里是"扫题目 frontmatter + 历史版本 + 事件"拼出来的 ——
于是**只在 goals.yaml 里声明、还没出过题的目标根本不进派生状态**，从系统里静默消失。
这正是学习者 2026-09-30 提的现象（"角动量、力学相似连目标都没有"；
`tm.t3.lagrangian-construction` 有目标 0 题）。

修法：目标集合 = goals.yaml ∪ 题目声明 ∪ 历史版本 ∪ 事件引用；
derive_state 对"有目标、无题目"的目标给出 `level = 未测` + `coverage = 未安排（0 题）`，
并在 `learning/coverage.md` 里显式列出——**没有题目不等于从系统消失**。

本模块是 goals.yaml 的**唯一**解析入口（validate_hurdles / derive_state / coverage 共用），
避免同一份文件出现两种读法。
"""
from __future__ import annotations

from pathlib import Path

from learninglib import parse_yaml


def load_goals(root: Path) -> list[dict]:
    """返回 [{id, title, subject, targets[], acceptance[], deadline, milestone, status, note}]。"""
    path = Path(root) / "learning" / "goals.yaml"
    if not path.is_file():
        return []
    raw = parse_yaml(path.read_text(encoding="utf-8"))
    goals: list[dict] = []
    for item in raw.get("goals") or []:
        if not isinstance(item, dict):
            continue
        targets = item.get("targets") or []
        if not isinstance(targets, list):
            targets = [targets]
        acceptance = item.get("acceptance") or []
        if not isinstance(acceptance, list):
            acceptance = [acceptance]
        goals.append(
            {
                "id": item.get("id"),
                "title": item.get("title"),
                "subject": item.get("subject"),
                "targets": [str(t) for t in targets],
                "acceptance": [str(a) for a in acceptance],
                "deadline": item.get("deadline"),
                "milestone": item.get("milestone"),
                "status": item.get("status", "active"),
                "note": item.get("note", ""),
            }
        )
    return goals


def declared_goal_targets(root: Path) -> dict[str, dict]:
    """{target_id: {goal_id, goal_title, subject, goal_status}} —— 目标 → 所属能力目标。"""
    index: dict[str, dict] = {}
    for goal in load_goals(root):
        for tid in goal["targets"]:
            index.setdefault(
                tid,
                {
                    "goal_id": goal["id"],
                    "goal_title": goal["title"],
                    "subject": goal["subject"],
                    "goal_status": goal["status"],
                },
            )
    return index


__all__ = ["load_goals", "declared_goal_targets"]
