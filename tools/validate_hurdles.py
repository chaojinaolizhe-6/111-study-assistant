#!/usr/bin/env python3
"""校验 learning/hurdles.jsonl —— 困难观察（不是作答事件，不产生分数）。

必填字段：hurdle_id、target_ids（非空）、observed_at(YYYY-MM-DD)、source、status、evidence_ref
取值：source ∈ {learner_statement, tutor_observation, review_feedback}
      status ∈ {open, teaching, awaiting_retest, verified, closed}
target_ids 必须是**已声明**的目标（来自 learning/tasks/ 或 learning/goals.yaml），
防止把困难挂到不存在的目标上（否则修复队列会漏掉它）。

用法: python -B tools/validate_hurdles.py [--root .]
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path

from learninglib import load_hurdles, load_tasks, parse_yaml

SOURCES = {"learner_statement", "tutor_observation", "review_feedback"}
STATUSES = {"open", "teaching", "awaiting_retest", "verified", "closed"}
REQUIRED = ["hurdle_id", "target_ids", "observed_at", "source", "status", "evidence_ref"]


def declared_targets(root: Path) -> set[str]:
    targets: set[str] = set()
    for task in load_tasks(root).values():
        targets.update(task["target_ids"])
    goals_path = root / "learning" / "goals.yaml"
    if goals_path.is_file():
        raw = parse_yaml(goals_path.read_text(encoding="utf-8"))
        for goal in raw.get("goals") or []:
            if isinstance(goal, dict):
                targets.update(goal.get("targets") or [])
    return targets


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate learning/hurdles.jsonl")
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    rows = load_hurdles(root)
    errors: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()
    known = declared_targets(root)
    count = 0
    for row in rows:
        label = f"line {row['line']}"
        data = row.get("data")
        if data is None:
            errors.append(f"{label}: {row.get('error', 'invalid json')}")
            continue
        for key in REQUIRED:
            if key not in data:
                errors.append(f"{label}: missing field {key}")
        hid = data.get("hurdle_id")
        if not isinstance(hid, str) or not hid:
            errors.append(f"{label}: hurdle_id must be a non-empty string")
        elif hid in seen:
            errors.append(f"{label}: duplicate hurdle_id {hid!r}")
        else:
            seen.add(hid)
        tids = data.get("target_ids")
        if not isinstance(tids, list) or not tids or not all(isinstance(x, str) for x in tids):
            errors.append(f"{label}: target_ids must be a non-empty list of strings")
        else:
            for tid in tids:
                if known and tid not in known:
                    errors.append(f"{label}: target_ids 越界：{tid} 未在任何题目/目标中声明")
        try:
            dt.date.fromisoformat(str(data.get("observed_at", "")))
        except ValueError:
            errors.append(f"{label}: observed_at must be YYYY-MM-DD")
        if data.get("source") not in SOURCES:
            errors.append(f"{label}: bad source {data.get('source')!r}（应为 {sorted(SOURCES)} 之一）")
        if data.get("status") not in STATUSES:
            errors.append(f"{label}: bad status {data.get('status')!r}（应为 {sorted(STATUSES)} 之一）")
        ref = data.get("evidence_ref")
        if ref and not isinstance(ref, str):
            errors.append(f"{label}: evidence_ref must be a string")
        count += 1

    for warning in warnings:
        print(f"WARN {warning}")
    if errors:
        print("HURDLE VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("HURDLE VALIDATION OK")
    print(f"- hurdles: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
