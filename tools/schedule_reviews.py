#!/usr/bin/env python3
"""把复习与再测**排成有日期的任务**（`plan/schedule.md`）——让"两天后再测"真的落到日历上。

解决的问题（本轮改进要求 P1-E）：
1. **"两天后再测"只留在聊天里** → 现在落成带目标、带**具体日期**的任务；
2. **未来才开放的任务被提前安排** → 每条都有 `最早开始`（`not_before`），
   早于该日期不进入"到期/今天"清单，只出现在"未来"区；
3. **过期计划起始日把新任务排进过去** → 日期基准是**中国时间的今天**（`tools/timebase.py`），
   且 `not_before` 由"上次独立通过日期 + min_delay_days"算出，**必然 ≥ 通过日期**；
4. **设备可用 ≠ 全时段能专注** → 每条带设备需求；每日只呈现**少量主任务**（默认 2 条），
   其余进候选队列；"专注预算"未知时**不编造分钟数**（只按条数与已知 est_minutes 汇总，并标注未知）。
5. **当天未完成事项不静默消失** → `--carry-over` 读取昨日清单里未完成的行，显式标"结转/延期/取消"。

用法:
  python -B tools/schedule_reviews.py --root . --today 2026-09-30
  python -B tools/schedule_reviews.py --root . --today 2026-09-30 --today-only   # 只看今天
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reviews import all_review_items, overdue_concepts  # noqa: E402
from timebase import days_between, learning_today, uk_date_now  # noqa: E402
from workspace_lock import LockTimeout, WorkspaceLock, atomic_write_text  # noqa: E402

PLAN_FILE = "plan/schedule.md"
MAIN_TASKS_PER_DAY = 2          # 每日只呈现少量主任务（其余进候选队列）
DEADLINE_LOOKAHEAD = 7          # 截止日期进入"到期"区的提前量（天）


def categorize(item: dict, today: str) -> str:
    delta = days_between(today, item["due"])      # 距今天数（正=未来）
    if delta <= 0:
        return "已到期"
    if delta <= DEADLINE_LOOKAHEAD:
        return "本周内"
    return "未来"


def blocked_reason(item: dict, today: str) -> str:
    if item.get("queue") == "能力再测" and days_between(today, item["due"]) > 0:
        return f"最早 {item['due']} 才能做（不得提前：未到延迟间隔）"
    if item.get("queue") == "目标节点" and days_between(today, item["due"]) > 0:
        return f"截止/里程碑尚未到（{item['due']}）"
    if item.get("queue") == "题目截止":
        gate = item.get("not_before")
        if gate and days_between(today, gate) > 0:
            return f"窗口/最早开始 {gate} 才开（截止 {item.get('deadline') or item['due']}）→ 提前做没有意义"
        if days_between(today, item["due"]) > 0:
            return f"题目 {item['due']} 到期"
    if item.get("queue") == "外部截止" and days_between(today, item["due"]) > 0:
        return f"外部截止 {item['due']} 尚未到"
    return ""


def build(root: Path, today: str, carry_over: list[dict] | None = None) -> str:
    items = all_review_items(root, today)
    buckets: dict[str, list[dict]] = {"已到期": [], "本周内": [], "未来": []}
    for item in items:
        buckets[categorize(item, today)].append(item)

    lines: list[str] = []
    lines.append("# 复习与再测排期（schedule.md）")
    lines.append("")
    lines.append("> **本文件由 `python -B tools/schedule_reviews.py` 生成，勿手工编辑**（派生视图）。")
    lines.append(f"> 学习日（**中国时间**）：**{today}**（系统英国日期 {uk_date_now()}；排期一律按中国日期）。")
    lines.append("> 三个队列合排：**记忆维护**（SM-2 到期概念）／**能力再测**（独立通过但延迟不足、未解决困难、受助待重测）／**题目截止**。")
    lines.append("> 记忆与能力**不混用同一个分数**：前者管「何时再测」，后者管「无帮助下通过了什么」。")
    lines.append(">")
    lines.append("> 每条任务都带 **①最早开始 ②截止 ③设备 ④预计时长**；")
    lines.append("> 早于「最早开始」的任务**不会**被排进今天（未来才开放的任务不提前安排）。")
    lines.append("> ⚠ **设备可用 ≠ 全时段能专注**：`device` 只说明「用什么设备」，不代表那段时间一定空闲；")
    lines.append("> 每周专注预算（`plan/inputs.yml` 的 `capacity.weekly_minutes`）**未知**时本文件不编造总量。")
    lines.append("")

    # ---- ① 今天做（已到期）----
    lines.append(f"## ① 今天做（已到期，共 {len(buckets['已到期'])} 条）")
    lines.append("")
    due = buckets["已到期"]
    if due:
        lines.append(f"**每日主任务上限 {MAIN_TASKS_PER_DAY} 条**；其余进候选队列，不硬塞。")
        lines.append("")
        lines.append("| # | 队列 | 任务 | 课程 | 性质 | 最早开始 | 截止 | 设备 | 预计 | 为什么现在做 |")
        lines.append("|---|---|---|---|---|---|---|---|---|---|")
        for i, item in enumerate(due, 1):
            mark = "**主任务**" if i <= MAIN_TASKS_PER_DAY else "候选"
            lines.append(
                f"| {i} | {item['queue']} | `{item['id']}` {mark} | {item['subject']} | {item['kind']} | "
                f"{item['due']} | {'—' if item.get('reminder_only') else item['due']} | {item['device']} | "
                f"{'—' if item.get('reminder_only') else str(item['minutes']) + ' min'} | {item['note']} |"
            )
    else:
        lines.append("无到期项。")
    lines.append("")
    overdue_mem = overdue_concepts(root, today)
    lines.append(f"**记忆维护（SM-2）到期概念：{len(overdue_mem)} 个**")
    if overdue_mem:
        for item in overdue_mem:
            lines.append(f"- `{item['id']}`（{item['subject']}）due {item['due']} — {item['note']}")
    else:
        lines.append("- 无（概念笔记 frontmatter 里没有 `due ≤ 今天` 的条目）。")
        lines.append("- ⚠ 这**不等于**「没有要复习的东西」：能力再测队列里的项是另一回事（见上表）。")
    lines.append("")

    # ---- ② 本周内 ----
    lines.append(f"## ② 本周内到期（{DEADLINE_LOOKAHEAD} 天内，共 {len(buckets['本周内'])} 条）")
    lines.append("")
    if buckets["本周内"]:
        lines.append("| 最早开始 | 队列 | 任务 | 课程 | 性质 | 设备 | 预计 | 说明 |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for item in buckets["本周内"]:
            lines.append(
                f"| {item['due']} | {item['queue']} | `{item['id']}` | {item['subject']} | {item['kind']} | "
                f"{item['device']} | {'—' if item.get('reminder_only') else str(item['minutes']) + ' min'} | {item['note']} |"
            )
    else:
        lines.append("无。")
    lines.append("")

    # ---- ③ 未来（不得提前安排）----
    lines.append(f"## ③ 未来才开放（**不提前安排**，共 {len(buckets['未来'])} 条）")
    lines.append("")
    if buckets["未来"]:
        lines.append("| 最早开始 | 距今 | 队列 | 任务 | 性质 | 为什么不现在做 |")
        lines.append("|---|---|---|---|---|---|")
        for item in buckets["未来"]:
            reason = blocked_reason(item, today) or "未到排期窗口"
            lines.append(
                f"| {item['due']} | +{days_between(today, item['due'])}d | {item['queue']} | `{item['id']}` | "
                f"{item['kind']} | {reason} |"
            )
    else:
        lines.append("无。")
    lines.append("")

    # ---- ④ 结转（当天未完成事项不静默消失）----
    lines.append("## ④ 结转：昨日清单里未完成的项（**不静默消失**）")
    lines.append("")
    if carry_over:
        lines.append("每项必须显式给一个处置：**结转**（今天继续）／**延期**（给出新日期）／**取消**（说明理由）。")
        lines.append("")
        lines.append("| 原项 | 原日期 | 处置 | 新日期 / 理由 |")
        lines.append("|---|---|---|---|")
        for row in carry_over:
            lines.append(f"| {row['item']} | {row['from']} | {row['action']} | {row['detail']} |")
    else:
        lines.append("无待处置项（没有提供昨日清单，或昨日清单里已无未完成项）。")
        lines.append("")
        lines.append("> 用法：`python -B tools/schedule_reviews.py --carry-over plan/today-<昨天>.md`")
        lines.append("> 脚本会扫描该文件里**未勾选**的行（`[ ]`），逐条要求处置，而不是让它们消失。")
    lines.append("")

    # ---- ⑤ 汇总 ----
    total_min = sum(i["minutes"] for i in items if not i.get("reminder_only"))
    lines.append("## ⑤ 汇总")
    lines.append("")
    lines.append(f"- 条目合计 **{len(items)}** 条（已到期 {len(buckets['已到期'])}／本周内 {len(buckets['本周内'])}／未来 {len(buckets['未来'])}）")
    lines.append(f"- 已知预计时长合计 **{total_min} min**（**只累加题目里写明的 est_minutes**；未写明的按 0 计，不编造）")
    lines.append(f"- 每日主任务上限 {MAIN_TASKS_PER_DAY} 条；其余为候选队列")
    lines.append("- 每周专注预算：见 `plan/inputs.yml` 的 `capacity.weekly_minutes`（`null` = 未知 → 不做容量校验）")
    lines.append("")
    return "\n".join(lines)


def parse_carry_over(path: Path, today: str) -> list[dict]:
    """从昨日清单里找出未完成行（`[ ]`），逐条给出处置建议（不自动删除）。"""
    if not path.is_file():
        return []
    rows = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line.startswith("|") or "[ ]" not in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        label = " / ".join(c for c in cells[:3] if c) or line[:60]
        rows.append(
            {
                "item": label[:80],
                "from": path.stem.replace("today-", ""),
                "action": "待学习者决定：结转 / 延期 / 取消",
                "detail": f"**必须显式处置**——原日期早于 {today} 且未完成；不得静默消失",
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate plan/schedule.md (dated review/retest plan).")
    parser.add_argument("--root", default=".")
    parser.add_argument("--today", default=None, help="中国日期；默认取系统换算后的中国日期")
    parser.add_argument("--out", default=None)
    parser.add_argument("--carry-over", default=None, help="昨日清单路径（扫描未完成行）")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--today-only", action="store_true", help="只打印今天该做的（终端速览）")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    today = learning_today(args.today)
    carry = parse_carry_over(Path(args.carry_over), today) if args.carry_over else None
    text = build(root, today, carry)

    if args.today_only:
        print(f"学习日（中国时间）：{today}")
        items = all_review_items(root, today)
        due = [i for i in items if days_between(today, i["due"]) <= 0]
        if not due:
            print("- 今天没有到期项")
        for i, item in enumerate(due, 1):
            tag = "主任务" if i <= MAIN_TASKS_PER_DAY else "候选"
            print(f"- [{tag}] {item['queue']}｜{item['id']}｜{item['kind']}｜{item['minutes']}min｜{item['note']}")
        return 0

    if args.dry_run:
        print(text)
        return 0

    out = Path(args.out) if args.out else root / PLAN_FILE
    try:
        with WorkspaceLock(root / "plan", label="schedule_reviews"):
            atomic_write_text(out, text)
    except LockTimeout as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 4
    print(f"wrote {out}")
    items = all_review_items(root, today)
    due = [i for i in items if days_between(today, i["due"]) <= 0]
    future = [i for i in items if days_between(today, i["due"]) > 0]
    print(f"- 学习日（中国时间）：{today}（英国 {uk_date_now()}）")
    print(f"- 已到期 {len(due)} 条；未来才开放 {len(future)} 条（不提前安排）")
    for i, item in enumerate(due, 1):
        print(f"  {i}. [{'主任务' if i <= MAIN_TASKS_PER_DAY else '候选'}] {item['queue']}｜{item['id']}｜{item['note'][:70]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
