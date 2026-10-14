#!/usr/bin/env python3
"""当前状态事实卡（`state/current.md`）——跨窗口续学的**唯一事实来源**。

解决的问题（本轮改进要求 P0-A）：
1. **同一件事有多个入口、各写一份**：`AGENTS.md/CLAUDE.md` 的 STATUS 叙述行、
   `plan/handoff-CURRENT.md`、`plan/today-<日期>.md`、`learning/learner-state.json`
   各自描述"现在到哪了"，于是互相矛盾（实测：孤立奇点已有 attempt-27～31，
   交接文件却还写"完全未开始"；STATUS 还留着"今天 09-29""判据二复测已欠一天"）。
   → 现在：**事实行全部由程序从 `learning/` 重算**，写进 `state/current.md`；
     各入口（AGENTS/CLAUDE 的指针、handoff）**引用它，不再各写一份**。
2. **四件事挤成一个"进度"**：作业完成 / 概念困难是否解决 / 独立作答表现 / 延迟检验结果
   → 本文件分别列出（数据来自 `learner-state.json` 的 `status_dimensions`）。
3. **续学摘要堆着整个纠错过程**：冷启动入口被历史更正淹没。
   → 本文件只保留：**当前目标、最近有效证据、帮助史、当前卡点、下一步**；
     纠错过程留在 `learning/corrections.jsonl` + `learning/attempts/corrections.md`，
     这里只给一条"最近订正"摘要 + 指针。

手写意图（"我接下来想做什么/为什么暂缓"）**不在**本文件：
在 `.tutor/config/status-narrative.yml`（叙述行唯一来源）、`plan/today-<日期>.md`、`plan/gaps.md`。

用法:
  python -B tools/current_state.py --root . --today 2026-09-30
  python -B tools/current_state.py --root . --today 2026-09-30 --print   # 打印不写
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from goallib import load_goals  # noqa: E402
from learninglib import effective_attempts, resumable_attempts, load_corrections, load_hurdles, load_tasks
from observations import pending  # noqa: E402
from timebase import days_between, learning_today, uk_date_now  # noqa: E402
from workspace_lock import LockTimeout, WorkspaceLock, atomic_write_text  # noqa: E402

LEVEL_ORDER = ["迁移通过", "延迟通过", "曾独立完成", "需支持", "未测"]


def latest_events(attempts: list[dict], n: int = 4) -> list[dict]:
    def key(a):
        eid = str(a.get("event_id", ""))
        num = int(eid.split("-")[-1]) if eid.split("-")[-1].isdigit() else 0
        return (str(a.get("ts", "")), num)

    return sorted(attempts, key=key)[-n:][::-1]


def build(root: Path, today: str) -> str:
    state_path = root / "learning" / "learner-state.json"
    if not state_path.is_file():
        raise SystemExit("ERROR: 缺少 learning/learner-state.json，先运行 tools/derive_state.py")
    state = json.loads(state_path.read_text(encoding="utf-8"))
    src = state.get("source", {})
    targets = state["targets"]
    from derive_state import source_fingerprint
    if state.get('source') != source_fingerprint(root):
        raise ValueError('State is stale; run session-close.py before building the fact card')
    attempts = effective_attempts(root)
    hurdles = [r["data"] for r in load_hurdles(root) if r.get("data")]
    corrections = [r["data"] for r in load_corrections(root) if r.get("data")]
    goals = load_goals(root)
    tasks = load_tasks(root)
    open_hurdles = [h for h in hurdles if h.get("status") in ("open", "teaching", "awaiting_retest")]

    L: list[str] = []
    L.append("# 当前状态事实卡（state/current.md）")
    L.append("")
    L.append("> **本文件由 `python -B tools/current_state.py` 生成，勿手工编辑**（派生视图）。")
    L.append("> 这是**跨窗口续学的唯一事实来源**：`AGENTS.md` / `CLAUDE.md` 的 STATUS 与")
    L.append("> `plan/handoff-CURRENT.md` 都**引用**它，不再各写一份叙述。")
    L.append(f"> 生成于 **{today}**（中国时间；系统英国日期 {uk_date_now()}）。")
    L.append(f"> 事实源指纹：`attempts.jsonl` {src.get('attempts_events', '?')} 条（sha256 `{str(src.get('attempts_sha256','?'))[:12]}…`）"
             f"＋ `corrections.jsonl` {src.get('corrections_events', '?')} 条。")
    L.append("> 手写意图（下一步想做什么、为什么暂缓）不在这里：见 `.tutor/config/status-narrative.yml`、`plan/today-<日期>.md`、`plan/gaps.md`。")
    L.append("")

    # ============ ① 现在到哪了（按课程） ============
    L.append("## ① 现在到哪了（按课程，全部由程序重算）")
    L.append("")
    by_subject: dict[str, list[tuple[str, dict]]] = {}
    for tid, tgt in sorted(targets.items()):
        subj = (tgt.get("goal") or {}).get("subject") or "（未归入能力目标）"
        by_subject.setdefault(subj, []).append((tid, tgt))
    for goal in goals:
        subject = goal.get("subject") or "?"
        rows = by_subject.pop(subject, [])
        if not rows:
            continue
        L.append(f"**{subject}** — {goal['title']}（`{goal['id']}`，状态 {goal.get('status')}"
                 + (f"，截止 {goal['deadline']}" if goal.get("deadline") else "")
                 + (f"，里程碑 {goal['milestone']}" if goal.get("milestone") else "")
                 + "）")
        L.append("")
        L.append("| 目标 | 覆盖 | 等级 | 独立通过 | 未解决困难 |")
        L.append("|---|---|---|---|---|")
        for tid, tgt in rows:
            dates = "、".join(tgt["independent_pass_dates"]) or "—"
            hids = "、".join(h.get("hurdle_id", "?") for h in tgt.get("open_hurdles", [])) or "—"
            L.append(f"| `{tid}` | {tgt['coverage']} | {tgt['level']} | {dates} | {hids} |")
        L.append("")
    for subject, rows in sorted(by_subject.items()):
        if not rows:
            continue
        L.append(f"**{subject}**（未在 goals.yaml 归入能力目标）")
        L.append("")
        L.append("| 目标 | 覆盖 | 等级 | 独立通过 |")
        L.append("|---|---|---|---|")
        for tid, tgt in rows:
            dates = "、".join(tgt["independent_pass_dates"]) or "—"
            L.append(f"| `{tid}` | {tgt['coverage']} | {tgt['level']} | {dates} |")
        L.append("")

    # ============ ② 最近有效证据 ============
    L.append("## ② 最近有效证据（最近 4 条作答事件）")
    L.append("")
    L.append("| 事件 | 日期 | 题目 | 模式 | 提示 | 结果 | 曝光 | 目标 |")
    L.append("|---|---|---|---|---|---|---|---|")
    for a in latest_events(attempts, 4):
        tr = a.get("target_results") or {}
        tid = next(iter(tr), (a.get("target_ids") or ["—"])[0] if a.get("target_ids") else "—")
        entry = tr.get(tid) or {}
        hint = entry.get("hint_level", a.get("max_hint_level"))
        exp = entry.get("exposure", a.get("solution_exposure"))
        timing = entry.get("exposure_timing", a.get("exposure_timing"))
        final = entry.get("final", a.get("final_result"))
        L.append(
            f"| `{a.get('event_id')}` | {a.get('ts')} | `{a.get('task_id')}` | {a.get('mode')} | "
            f"{'H' + str(hint) if isinstance(hint, int) else 'H?'} | {final} | "
            f"{exp}{'@' + str(timing) if timing else ''} | `{tid}` |"
        )
    L.append("")
    L.append("> 「有效证据」= 能支持或推翻「独立掌握」的作答；")
    L.append("> **受助/曝光的作答也算证据**——它证明的是「当时需要帮助」，不是「已经会了」。")
    L.append("")

    L += ['## 暂停与未完成题续学点', '']
    pauses=[r for r in pending(root) if r.get('kind') == 'pause']
    for row in pauses:
        L += [f"- `{row['id']}`（{row['subject']}；来源 {row['evidence_ref']}）：{row['text']}"]
    for event in latest_events(resumable_attempts(root),6):
        notes='；'.join(str(v.get('note')) for v in (event.get('target_results') or {}).values() if v.get('note'))
        L += [f"- `{event['task_id']}` / `{event['event_id']}`：尚未完成；{notes or '续学步骤未提供，按实际草稿核对'}"]
    if not pauses and not resumable_attempts(root):
        L += ['暂无已登记暂停点。']
    L += ['']
    # ============ ③ 帮助史与曝光史（跨窗口保留） ============
    L.append("## ③ 帮助史与曝光史（跨窗口保留，不因换窗口丢失）")
    L.append("")
    L.append(f"共 **{len(attempts)}** 条作答事件；其中 **{sum(1 for a in attempts if (a.get('solution_exposure') or 'none') != 'none' or (a.get('max_hint_level') or 0) > 0)}** 条记录了提示或答案曝光。")
    L.append("")
    helped = [
        a for a in attempts
        if (a.get("solution_exposure") or "none") != "none" or isinstance(a.get("max_hint_level"), int) and a.get("max_hint_level") > 0
    ]
    if helped:
        L.append("| 事件 | 提示 | 曝光 | 时机 | 说明（为何不计独立通过） |")
        L.append("|---|---|---|---|---|")
        for a in sorted(helped, key=lambda x: str(x.get("ts")), reverse=True):
            tr = a.get("target_results") or {}
            entry = next(iter(tr.values()), {}) if tr else {}
            hint = entry.get("hint_level", a.get("max_hint_level"))
            exp = entry.get("exposure", a.get("solution_exposure"))
            timing = entry.get("exposure_timing", a.get("exposure_timing"))
            L.append(
                f"| `{a.get('event_id')}` | {'H' + str(hint) if isinstance(hint, int) else 'H?'} | {exp} | {timing or '—'} | "
                f"{'待核验' if entry.get('needs_verify') else ('提示>0' if isinstance(hint, int) and hint > 0 else '—')} |"
            )
    else:
        L.append("无受助/曝光事件。")
    L.append("")
    L.append("> ⚠ **未知不默认成最有利值**：曝光时机缺失/`unknown` 一律**阻断**独立通过（fail-closed）。")
    L.append("> ⚠ **反馈后的曝光**（`after_attempt`）不污染此前那次独立表现；**作答前/作答中**的曝光都阻断。")
    L.append("")

    # ============ ④ 当前卡点 ============
    L.append("## ④ 当前卡点（未解决困难 + 未升级目标）")
    L.append("")
    if open_hurdles:
        L.append("| 困难 | 状态 | 目标 | 观察到 | 证据 |")
        L.append("|---|---|---|---|---|")
        for h in open_hurdles:
            L.append(
                f"| `{h.get('hurdle_id')}` | {h.get('status')} | {', '.join(h.get('target_ids') or [])} | "
                f"{h.get('observed_at')} | {str(h.get('evidence_ref',''))[:60]} |"
            )
    else:
        L.append("无未解决困难。")
    L.append("")
    retest = [t for t, v in targets.items()
              if v["status_dimensions"]["independent_performance"]["pass_dates"]
              and not v["status_dimensions"]["delayed_retest"]["satisfied"]]
    if retest:
        L.append(f"**已有独立通过、但延迟检验未满足**（下一步应做换题延迟复测）：{'、'.join('`' + t + '`' for t in sorted(retest))}")
        L.append("")
    noskill = [t for t, v in targets.items() if not v["tasks"]]
    if noskill:
        L.append(f"**已声明但一道题都没有（纸面目标）**：{'、'.join('`' + t + '`' for t in sorted(noskill))}")
        L.append("")
        L.append("> 没有题目**不等于**已掌握，也**不等于**没学过——它表示系统里没有任何证据。")
        L.append("")

    # ============ ⑤ 下一步（自动候选；最终由学习者/导师叙述行决定） ============
    L.append("## ⑤ 下一步（机械候选，不是最终安排）")
    L.append("")
    L.append("| 最早开始 | 队列 | 任务 | 性质 | 为什么 |")
    L.append("|---|---|---|---|---|")
    try:
        from reviews import all_review_items

        for item in all_review_items(root, today)[:12]:
            when = item["due"] if days_between(today, item["due"]) <= 0 else f"{item['due']}（+{days_between(today, item['due'])}d）"
            L.append(f"| {when} | {item['queue']} | `{item['id']}` | {item['kind']} | {item['note']} |")
    except Exception as exc:  # noqa: BLE001
        L.append(f"| — | — | — | — | 排期扫描失败：{exc} |")
    L.append("")
    L.append("完整排期（含'未来才开放、不得提前安排'的项）见 `plan/schedule.md`（`tools/schedule_reviews.py` 生成）。")
    L.append("**最终下一步以 `.tutor/config/status-narrative.yml` 的 `next` 行 + `plan/today-<日期>.md` 为准**（那是人工判断，不是机械候选）。")
    L.append("")

    # ============ ⑥ 最近订正（只给摘要与指针，不在入口堆积纠错过程） ============
    L.append("## ⑥ 最近订正（**摘要 + 指针**；纠错全过程不在这里）")
    L.append("")
    if corrections:
        L.append(f"共 **{len(corrections)}** 条订正。最近 5 条：")
        L.append("")
        L.append("| 订正 | 事件 | 字段 | from → to | 证据 |")
        L.append("|---|---|---|---|---|")
        for c in corrections[-5:]:
            if c.get("kind") == "narrative":
                L.append(f"| `{c.get('correction_id')}` | —（叙述） | — | — | {str(c.get('text',''))[:50]}… |")
                continue
            field = c.get("field")
            if c.get("scope") == "target":
                field = f"{c.get('target_id')}.{field}"
            L.append(
                f"| `{c.get('correction_id')}` | `{c.get('event_id')}` | `{field}` | "
                f"`{c.get('from')!r}` → `{c.get('to')!r}` | {str(c.get('evidence_ref',''))[:50]} |"
            )
        L.append("")
        L.append("全文：`learning/corrections.jsonl`（机器可读、唯一事实源）→ 人读视图 `learning/attempts/corrections.md`。")
        L.append("> 历史更正的**可追溯记录保留在那里**，冷启动入口只放这一条摘要。")
    else:
        L.append("无订正记录。")
    L.append("")

    # ============ ⑦ 汇总计数 ============
    L.append("## ⑦ 汇总（可数事实，唯一来源）")
    L.append("")
    summary = state["summary"]
    L.append("| 项 | 值 |")
    L.append("|---|---|")
    L.append(f"| 目标总数 | {summary['targets']} |")
    for level in LEVEL_ORDER:
        L.append(f"| 　等级「{level}」 | {summary['by_level'].get(level, 0)} |")
    L.append(f"| 覆盖分布 | {json.dumps(summary.get('coverage', {}), ensure_ascii=False)} |")
    L.append(f"| 稳定证据（=迁移通过） | {summary['stable_evidence']} |")
    L.append(f"| 未解决困难 | {summary['open_hurdles']} |")
    L.append(f"| 作答事件 | {src.get('attempts_events', '?')} 条 |")
    L.append(f"| 订正 | {src.get('corrections_events', '?')} 条 |")
    L.append(f"| 题目 | {len(tasks)} 道 |")
    L.append(f"| 实测时长 / 估计时长 | {summary['measured_minutes_global']} min / {summary['estimated_minutes_global']} min（**单列，不混算**） |")
    L.append("")
    L.append("> 本表是 STATUS 块里 `mastered` / `open_hurdles` / `attempts` 等字段的来源；")
    L.append("> **不允许**在其它文件再手写一份计数（避免「两处各写一份、对不上」）。")
    L.append("")
    return "\n".join(L)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate state/current.md (single source of current facts).")
    parser.add_argument("--root", default=".")
    parser.add_argument("--today", default=None)
    parser.add_argument("--out", default=None)
    parser.add_argument("--print", dest="do_print", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    today = learning_today(args.today)
    text = build(root, today)
    if args.do_print:
        print(text)
        return 0
    out = Path(args.out) if args.out else root / "state" / "current.md"
    try:
        with WorkspaceLock(root / "learning", label="current_state"):
            atomic_write_text(out, text)
    except LockTimeout as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 4
    print(f"wrote {out}")
    state = json.loads((root / "learning" / "learner-state.json").read_text(encoding="utf-8"))
    print(f"- 目标 {state['summary']['targets']}；未解决困难 {state['summary']['open_hurdles']}；"
          f"作答 {state['source']['attempts_events']} 条")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
