#!/usr/bin/env python3
"""隔离验收测试（不触碰真实学习记录）：在 mock/acceptance-20260927/ 下自建用例目录，
对 tools/derive_state.py 的新判定语义做断言。

运行：python -B mock/acceptance-20260927/run_acceptance.py
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from derive_state import derive  # noqa: E402

BASE = ROOT / "mock" / "acceptance-20260927"
TASK = """---
id: t-demo
subject: 99-测试
title: 验收用例题
target_ids: [demo.a, demo.b]
version: 1
kind: practice
status: open
est_minutes: 10
device: any
---

测试用题（隔离目录，不进真实记录）
"""


def make_case(name: str, events: list[dict], kind: str = "practice") -> Path:
    case = BASE / name
    if case.exists():
        shutil.rmtree(case)
    (case / "learning" / "tasks").mkdir(parents=True)
    (case / "state").mkdir(parents=True)
    (case / "learning" / "tasks" / "t-demo.md").write_text(TASK.replace("kind: practice", f"kind: {kind}"), encoding="utf-8")
    (case / "learning" / "policy.yml").write_text(
        "independent_pass:\n  require_closed_book: true\n  min_dates: 2\n  min_variant_passes: 1\n  min_delay_days: 2\n",
        encoding="utf-8",
    )
    with (case / "learning" / "attempts.jsonl").open("w", encoding="utf-8") as fh:
        for event in events:
            fh.write(json.dumps(event, ensure_ascii=False) + "\n")
    return case


def event(eid: str, ts: str, *, hint=0, final="correct", closed=True, targets=("demo.a",), minutes=15, extra=None):
    base = {
        "event_id": eid,
        "task_id": "t-demo",
        "task_version": "1",
        "target_ids": list(targets),
        "mode": "practice",
        "closed_book": closed,
        "initial_result": "partial",
        "max_hint_level": hint,
        "final_result": final,
        "predicted_confidence": None,
        "active_minutes": minutes,
        "error_hypothesis": "（测试）",
        "diagnosis_status": "none",
        "solution_seen": False,
        "artifact_ref": "",
        "ts": ts,
    }
    if extra:
        base.update(extra)
    return base


CASES = []


def check(name: str, cond: bool, detail: str) -> None:
    CASES.append((name, cond, detail))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}：{detail}")


def main() -> int:
    # 1) max_hint_level=null（未知）不得计独立通过
    case = make_case("case1-null-hint", [event("attempt-1", "2026-09-01", hint=None)])
    state = derive(case)
    lv = state["targets"]["demo.a"]["level"]
    check("null 提示级别不算独立通过", lv == "需支持", f"level={lv}（期望 需支持）")

    # 2) 见过局部答案后订正，不得算该目标独立通过
    case = make_case("case2-exposure", [event("attempt-1", "2026-09-01", extra={"solution_exposure": "partial", "exposure_timing": "after_attempt"})])
    state = derive(case)
    check("曝光 partial 不算独立通过", state["targets"]["demo.a"]["level"] == "需支持", f"level={state['targets']['demo.a']['level']}")

    # 3) 同一次作答涉及两个目标：全局时长不重复计算
    case = make_case("case3-time", [event("attempt-1", "2026-09-01", targets=("demo.a", "demo.b"), extra={"time_source": "estimated"})])
    state = derive(case)
    g_est = state["summary"]["estimated_minutes_global"]
    g_mea = state["summary"]["measured_minutes_global"]
    per = state["targets"]["demo.a"]["estimated_minutes"] + state["targets"]["demo.b"]["estimated_minutes"]
    check("跨目标不重复计全局时长", g_est == 15.0 and per == 30.0, f"全局估计={g_est}（期望 15），两目标合计={per}（期望 30）")
    check("估计时长不进实测桶", g_mea == 0.0, f"实测={g_mea}（期望 0）")

    # 4) 相邻两天各一次独立通过：不到 min_delay_days，不算延迟通过
    evs = [
        event("attempt-1", "2026-09-01"),
        event("attempt-2", "2026-09-02"),
    ]
    case = make_case("case4-short-delay", evs)
    state = derive(case)
    t = state["targets"]["demo.a"]
    check("跨午夜/相邻日不算延迟证据", t["level"] == "曾独立完成" and t["delay_days"] == 1, f"level={t['level']}，delay_days={t['delay_days']}")

    # 5) 间隔满足 + 未见变式通过 → 迁移通过（唯一稳定证据）
    evs = [
        event("attempt-1", "2026-09-01"),
        event("attempt-2", "2026-09-05"),
    ]
    case = make_case("case5-stable", evs, kind="delayed-variant")
    state = derive(case)
    t = state["targets"]["demo.a"]
    check("间隔足够+未见变式=迁移通过", t["level"] == "迁移通过" and t["stable_evidence"], f"level={t['level']}，stable={t['stable_evidence']}，delay_days={t['delay_days']}")

    # 6) 开卷通过单独统计，不计等级
    case = make_case("case6-open-book", [event("attempt-1", "2026-09-01", closed=False)])
    state = derive(case)
    t = state["targets"]["demo.a"]
    check("开卷通过单独统计", t["level"] == "需支持" and t["open_book_pass_dates"] == ["2026-09-01"], f"level={t['level']}，open_book={t['open_book_pass_dates']}")

    failed = [n for n, ok, _ in CASES if not ok]
    print(f"\n共 {len(CASES)} 项验收：通过 {len(CASES) - len(failed)}，失败 {len(failed)}")
    if failed:
        print("失败项：" + "；".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
