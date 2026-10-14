#!/usr/bin/env python3
"""订正影响面：列出"有生效订正的目标"关联到的题目文件，供**人工核对**说明是否已更新。

为什么不做关键词匹配：自由文本里的"相反结论"无法可靠自动判定——会漏（换个说法就匹配不到）
也会误报（同一个词在别的语境里出现）。所以本工具**只做确定性关联**：

  订正 → event_id → 事件的 task_id → 该题文件（确定）
  订正涉及的 target_id → 所有 frontmatter 里声明该目标的 learning/tasks/*.md（确定）

判定"说明里的旧结论是否已撤"仍然交给人；工具只保证**不会被忽略**。

用法: python -B tools/correction_impact.py [--root .]
"""
from __future__ import annotations

import argparse
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from learninglib import load_attempts, load_corrections, load_tasks  # noqa: E402

# 这些文件是自由文本，无法可靠关联到单个目标 → 一律列为人工核对项
MANUAL_FILES = [
    "state/mistakes.md",
    "learning/attempts/corrections.md",
    "ISSUES-待改进.md",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Report which task files are touched by active corrections.")
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    corrections = [r["data"] for r in load_corrections(root) if r.get("data") and r["data"].get("kind") != "narrative"]
    attempts = {r["data"].get("event_id"): r["data"] for r in load_attempts(root) if r.get("data")}
    tasks = load_tasks(root)

    if not corrections:
        print("订正影响面：无字段订正（corrections.jsonl 为空）")
        return 0

    # target_id -> 声明了它的题目文件
    by_target: dict[str, list[str]] = {}
    for task in tasks.values():
        for tid in task["target_ids"]:
            by_target.setdefault(tid, []).append(task["path"])

    affected_tasks: set[str] = set()
    affected_targets: set[str] = set()
    print(f"== 生效字段订正：{len(corrections)} 条 ==")
    for c in corrections:
        event = attempts.get(c.get("event_id")) or {}
        target = c.get("target_id") or "(事件级)"
        if c.get("target_id"):
            affected_targets.add(c["target_id"])
        own_task = tasks.get(event.get("task_id", ""))
        if own_task:
            affected_tasks.add(own_task["path"])
        print(f"  {c['correction_id']:<20} {c.get('event_id','?'):<11} {target:<28} {c.get('field')}")

    print("\n== 该订正直接涉及的题目文件（请核对说明是否已更新）==")
    if affected_tasks:
        for path in sorted(affected_tasks):
            print(f"  [ ] {path}")
    else:
        print("  （无）")

    print("\n== 声明了同一目标的其他题目文件（同一目标可能被多题引用）==")
    others: set[str] = set()
    for tid in sorted(affected_targets):
        for path in by_target.get(tid, []):
            if path not in affected_tasks:
                others.add(path)
                print(f"  [ ] {path}　（目标 {tid}）")
    if not others:
        print("  （无）")

    print("\n== 人工核对清单（自由文本，工具不做内容判定）==")
    for rel in MANUAL_FILES:
        print(f"  [ ] {rel}　{'（存在）' if (root / rel).is_file() else '（不存在）'}")
    for pattern in ("plan/handoff-*.md", "plan/today-*.md", "subjects/*/progress.md"):
        hits = sorted(root.glob(pattern))
        if hits:
            print(f"  [ ] {pattern}　→ {len(hits)} 个文件")

    print("\n提示：本工具只列**关联**，不判断文字内容；'旧结论是否已撤'由人工确认。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
