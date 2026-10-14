#!/usr/bin/env python3
"""生成学习状态事实卡（learning/coverage.md）——**课程覆盖 + 当前状态**的唯一派生视图。

解决的问题（学习者 2026-09-30 提出，见 `ISSUES-待改进.md` A7 + 本轮改进要求）：
1. **没被出过题的考点会静默消失**：目标集合此前只由"题目 frontmatter + 历史版本 + 事件"拼出，
   `learning/goals.yaml` 里声明、但还没有题目的目标（角动量、力学相似）根本不进状态。
2. **一个"等级"挤掉了四件事**：作业是否交了、概念困难是否解决、独立作答表现、延迟检验结果
   —— 这四件事必须分开看（困难结案 ≠ 目标升级，交了作业 ≠ 会做）。
3. **"未学/已讲未测/需补练/独立通过/待延迟复测"没有统一台账**，
   于是"暂缓"和"遗漏"看起来一样。

本文件是**纯派生**（没有任何手写内容），由 `tools/derive_state.py` 的数据生成；
手写意图（今天做什么、为什么暂缓）在 `plan/today-<日期>.md`、
`.tutor/config/status-narrative.yml` 与 `plan/gaps.md` 里，**不写进本文件**。

用法:
  python -B tools/coverage.py --root . [--today 2026-09-30] [--out learning/coverage.md]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from goallib import load_goals  # noqa: E402
from learninglib import load_attempts, load_corrections, load_hurdles, load_tasks  # noqa: E402
from workspace_lock import LockTimeout, WorkspaceLock, atomic_write_text  # noqa: E402
from timebase import learning_today

COVERAGE_ORDER = [
    "未安排（无题目）",
    "已安排·未作答",
    "已作答·需补练",
    "已作答·开卷/受助通过",
    "已独立通过·待延迟复测",
    "独立通过",
]


def build(root: Path, today: str) -> str:
    state_path = root / "learning" / "learner-state.json"
    if not state_path.is_file():
        raise SystemExit("ERROR: 缺少 learning/learner-state.json，先运行 tools/derive_state.py")
    state = json.loads(state_path.read_text(encoding="utf-8"))
    goals = load_goals(root)
    tasks = load_tasks(root)
    attempts = [r["data"] for r in load_attempts(root) if r.get("data")]
    hurdles = [r["data"] for r in load_hurdles(root) if r.get("data")]
    corrections = [r["data"] for r in load_corrections(root) if r.get("data")]

    targets = state["targets"]
    src = state.get("source", {})

    lines: list[str] = []
    lines.append("# 学习状态事实卡（coverage.md）")
    lines.append("")
    lines.append("> **本文件由 `python -B tools/coverage.py` 生成，勿手工编辑**（派生视图）。")
    lines.append("> 事实源：`learning/attempts.jsonl`（不改不删）+ `learning/corrections.jsonl`（订正）+ `learning/goals.yaml`（目标）+ 题目 frontmatter。")
    lines.append(f"> 生成日期：{today} ｜ 事件 {src.get('attempts_events', '?')} 条 ｜ 订正 {src.get('corrections_events', '?')} 条 "
                 f"｜ attempts.jsonl sha256 `{str(src.get('attempts_sha256', '?'))[:16]}…`")
    lines.append("> 手写意图（今天做什么、为什么暂缓）不在这里：见 `plan/today-<日期>.md`、`plan/gaps.md`、`.tutor/config/status-narrative.yml`。")
    lines.append("")

    # ---- ① 覆盖总览：每个能力目标一行 ----
    lines.append("## ① 能力目标覆盖（含**尚未出题**的考点）")
    lines.append("")
    lines.append("`覆盖状态` 的六个取值，语义互斥：")
    lines.append("")
    lines.append("| 覆盖状态 | 含义 | 下一步该做什么 |")
    lines.append("|---|---|---|")
    lines.append("| 未安排（无题目） | 目标已声明，但**一道题都没有** | 先建题（不建题它就永远是纸面目标）|")
    lines.append("| 已安排·未作答 | 有题、还没做过 | 排进当天清单，做无提示基线 |")
    lines.append("| 已作答·需补练 | 做过，但没有一次无提示独立通过 | 补讲/补练 → 撤去帮助再测 |")
    lines.append("| 已作答·开卷/受助通过 | 通过过，但开卷或受助 | 换题、闭卷、无提示重测 |")
    lines.append("| 已独立通过·待延迟复测 | 有独立通过，但日期跨度不足或未见变式不足 | 排**具体日期**的延迟变式 |")
    lines.append("| 独立通过 | 日期跨度与未见变式都达标（= 迁移通过）| 进入记忆维护队列 |")
    lines.append("")

    by_goal: dict[str, list[str]] = {}
    for tid, tgt in sorted(targets.items()):
        gid = (tgt.get("goal") or {}).get("id") or "（未归入任何能力目标）"
        by_goal.setdefault(gid, []).append(tid)

    for goal in goals:
        tid_list = by_goal.pop(goal["id"], [])
        if not tid_list:
            continue
        lines.append(f"### {goal['id']} — {goal['title']}")
        lines.append("")
        subj = goal.get("subject") or "?"
        meta = [f"课程 `{subj}`", f"状态 `{goal.get('status')}`"]
        if goal.get("deadline"):
            meta.append(f"截止 `{goal['deadline']}`")
        if goal.get("milestone"):
            meta.append(f"里程碑 `{goal['milestone']}`")
        lines.append("　".join(meta))
        lines.append("")
        lines.append("| 目标 | 覆盖状态 | 等级 | 题数 | 独立通过日期 | 未解决困难 | 延迟检验 |")
        lines.append("|---|---|---|---|---|---|---|")
        for tid in sorted(tid_list):
            tgt = targets[tid]
            hids = [h.get("hurdle_id") for h in tgt.get("open_hurdles", [])]
            delay = tgt["status_dimensions"]["delayed_retest"]
            delay_txt = (
                f"已满足（跨度 {delay['achieved_delay_days']}d ≥ {delay['required_delay_days']}d）"
                if delay["satisfied"]
                else f"未满足（跨度 {delay['achieved_delay_days']}d < {delay['required_delay_days']}d）"
            )
            dates = "、".join(tgt["independent_pass_dates"]) or "—"
            lines.append(
                f"| `{tid}` | {tgt['coverage']} | {tgt['level']} | {tgt['task_count']} | {dates} | "
                f"{'、'.join(hids) if hids else '—'} | {delay_txt} |"
            )
        lines.append("")

    leftovers = {g: t for g, t in by_goal.items() if t}
    if leftovers:
        lines.append("### 未归入任何能力目标的目标（`goals.yaml` 缺声明）")
        lines.append("")
        lines.append("| 目标 | 覆盖状态 | 等级 | 题数 |")
        lines.append("|---|---|---|---|")
        for gid, tids in sorted(leftovers.items()):
            for tid in sorted(tids):
                tgt = targets[tid]
                lines.append(f"| `{tid}` | {tgt['coverage']} | {tgt['level']} | {tgt['task_count']} |")
        lines.append("")

    # ---- ② 未安排的目标（本轮重点）----
    no_task = [t for t, v in targets.items() if not v["tasks"]]
    lines.append("## ② 已声明但**一道题都没有**的考点（不会因为没有题目而从系统消失）")
    lines.append("")
    if no_task:
        lines.append("| 目标 | 所属能力目标 | 等级 | 说明 |")
        lines.append("|---|---|---|---|")
        for tid in sorted(no_task):
            tgt = targets[tid]
            g = (tgt.get("goal") or {}).get("id") or "—"
            reason = "目标已声明、从未出题 → 目前没有任何能力证据"
            lines.append(f"| `{tid}` | {g} | {tgt['level']} | {reason} |")
        lines.append("")
        lines.append("> ⚠ 「没有题目」既**不等于**已掌握，也**不等于**没学过——它表示**系统里没有任何证据**。")
        lines.append("> 处理方式必须由学习者指定（见 `plan/gaps.md` / `ISSUES-待改进.md` A7），本文件不自动建题。")
    else:
        lines.append("无：每个已声明目标至少有一道题。")
    lines.append("")

    # ---- ③ 覆盖状态分布 ----
    lines.append("## ③ 覆盖状态分布")
    lines.append("")
    counts = state["summary"].get("coverage", {})
    lines.append("| 覆盖状态 | 目标数 |")
    lines.append("|---|---|")
    for key in COVERAGE_ORDER:
        lines.append(f"| {key} | {counts.get(key, 0)} |")
    lines.append(f"| **合计** | **{state['summary']['targets']}** |")
    lines.append("")

    # ---- ④ 分开表示的四个维度（困难结案 ≠ 目标升级）----
    lines.append("## ④ 四个维度分开看（**不要挤成一个「等级」**）")
    lines.append("")
    lines.append("| 目标 | ① 作业完成 | ② 概念困难已解决 | ③ 独立作答表现 | ④ 延迟检验 |")
    lines.append("|---|---|---|---|---|")
    for tid, tgt in sorted(targets.items()):
        d = tgt["status_dimensions"]
        hw = "✅" if d["assignment_done"] else ("—（无题目）" if not tgt["tasks"] else "进行中")
        ch = d["concept_hurdles"]
        if not ch["open"] and not ch["resolved"]:
            concept = "无困难记录"
        elif ch["open"]:
            concept = f"❌ 未解决 {('、'.join(ch['open']))}"
        else:
            concept = f"✅ 已结案 {('、'.join(ch['resolved']))}"
        perf = d["independent_performance"]
        if perf["pass_dates"]:
            perf_txt = f"独立通过 {len(perf['pass_dates'])} 次（{'、'.join(perf['pass_dates'])}）"
        elif perf["open_book_only"]:
            perf_txt = f"仅开卷/受助通过（{len(perf['open_book_only'])} 次）"
        elif tgt["attempts"]:
            perf_txt = f"0 次独立通过（{tgt['attempts']} 次作答，其中 {perf['helped_or_exposed_events']} 次受助/曝光）"
        else:
            perf_txt = "无作答"
        lines.append(f"| `{tid}` | {hw} | {concept} | {perf_txt} | {'✅' if d['delayed_retest']['satisfied'] else '❌'} |")
    lines.append("")
    lines.append("> **困难结案 ≠ 目标升级**：`hurdle` 结案只说明「那个卡点讲通了」，")
    lines.append("> 目标等级只看「有没有在无提示、闭卷、未见变式的条件下独立答对」。")
    lines.append("> **交了作业 ≠ 会做**：作业完成是事务状态，不进入等级判定。")
    lines.append("")

    # ---- ⑤ 未升级事件（凭什么没升级）----
    lines.append("## ⑤ 未升级的作答事件与原因（可复查）")
    lines.append("")
    rows = []
    for tid, tgt in sorted(targets.items()):
        for item in tgt.get("upgrade_blocked", []):
            rows.append((tid, item.get("event_id"), item.get("ts"), "；".join(item.get("why") or [])))
    if rows:
        lines.append("| 目标 | 事件 | 日期 | 未升级原因 |")
        lines.append("|---|---|---|---|")
        for tid, eid, ts, why in rows:
            lines.append(f"| `{tid}` | `{eid}` | {ts} | {why} |")
    else:
        lines.append("无。")
    lines.append("")

    # ---- ⑥ 订正台账（可追溯）----
    lines.append("## ⑥ 订正台账（原始事件不改不删，订正单独成条）")
    lines.append("")
    if corrections:
        lines.append(f"共 {len(corrections)} 条，全文见 `learning/corrections.jsonl`；人读渲染见 `learning/attempts/corrections.md`。")
        lines.append("")
        lines.append("| 订正 | 事件 | 字段 | from → to | 证据 |")
        lines.append("|---|---|---|---|---|")
        for c in corrections:
            if c.get("kind") == "narrative":
                lines.append(f"| `{c.get('correction_id')}` | —（叙述） | — | — | {str(c.get('text',''))[:60]}… |")
                continue
            field = c.get("field")
            if c.get("scope") == "target":
                field = f"{c.get('target_id')}.{field}"
            lines.append(
                f"| `{c.get('correction_id')}` | `{c.get('event_id')}` | `{field}` | "
                f"`{c.get('from')!r}` → `{c.get('to')!r}` | {str(c.get('evidence_ref',''))[:70]} |"
            )
    else:
        lines.append("无。")
    lines.append("")

    # ---- ⑦ 困难台账 ----
    lines.append("## ⑦ 困难观察（没有作答的「不会/不理解」，不伪装成做错的题）")
    lines.append("")
    if hurdles:
        lines.append("| 困难 | 状态 | 目标 | 观察到 | 证据 |")
        lines.append("|---|---|---|---|---|")
        for h in hurdles:
            lines.append(
                f"| `{h.get('hurdle_id')}` | {h.get('status')} | {', '.join(h.get('target_ids') or [])} | "
                f"{h.get('observed_at')} | {str(h.get('evidence_ref',''))[:60]} |"
            )
    else:
        lines.append("无。")
    lines.append("")

    # ---- ⑧ 题目清单 ----
    lines.append("## ⑧ 题目清单（`learning/tasks/`）")
    lines.append("")
    lines.append("| 题目 | 课程 | 类别 | 状态 | 目标 | 截止 |")
    lines.append("|---|---|---|---|---|---|")
    for task in sorted(tasks.values(), key=lambda t: t["id"]):
        lines.append(
            f"| `{task['id']}` | — | {task.get('kind')} | {task.get('status')} | "
            f"{', '.join(task['target_ids']) or '—'} | {task.get('due') or '—'} |"
        )
    lines.append("")
    lines.append(f"（题目 {len(tasks)} 道；作答事件 {len(attempts)} 条；以上均由脚本重算，不含手写内容。）")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate learning/coverage.md (derived).")
    parser.add_argument("--root", default=".")
    parser.add_argument("--today", default=None)
    parser.add_argument("--out", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    today = learning_today(args.today)
    text = build(root, today)
    out = Path(args.out) if args.out else root / "learning" / "coverage.md"
    if args.dry_run:
        print(text)
        return 0
    try:
        with WorkspaceLock(root / "learning", label="coverage"):
            atomic_write_text(out, text)
    except LockTimeout as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 4
    print(f"wrote {out}")
    state = json.loads((root / "learning" / "learner-state.json").read_text(encoding="utf-8"))
    print(f"- 目标 {state['summary']['targets']} 个；覆盖分布 {state['summary'].get('coverage')}")
    no_task = state["summary"].get("targets_without_tasks") or []
    print(f"- 已声明但无题目：{no_task or '无'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
