#!/usr/bin/env python3
"""记录 attempt-3（H4.2）与 attempt-4（H4.3）。用 append_attempt 做校验+回滚保护。"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

events = [
    {
        "event_id": "attempt-3",
        "task_id": "tm-t4-criteria-01",
        "task_version": "3",
        "target_ids": ["tm.t4.energy-integral", "tm.t4.energy-criteria", "tm.t4.direct-check"],
        "mode": "practice",
        "closed_book": True,
        "initial_result": "partial",
        "max_hint_level": 3,
        "final_result": "partial",
        "predicted_confidence": None,
        "active_minutes": 25,
        "time_source": "estimated",
        "solution_exposure": "partial",
        "exposure_timing": "after_attempt",
        "target_results": {
            "tm.t4.energy-integral": {"initial": "correct", "hint_level": 0, "final": "correct", "needs_verify": False,
                                      "note": "E = ½mR²θ̇² − ½mR²Ω²sin²θ − mgR cosθ（即 T2 − T0 + U），独立写出"},
            "tm.t4.direct-check": {"initial": "correct", "hint_level": 0, "final": "correct", "needs_verify": False,
                                   "note": "dE/dt 展开 + 拉格朗日方程 ⇒ dE/dt = 0，独立完成"},
            "tm.t4.energy-criteria": {"initial": "blocked", "hint_level": 3, "final": "partial", "needs_verify": True,
                                      "note": "criteria 2 留空；反馈中已给出 T2/T0 写法（曝光）→ 待课后补讲后重测"}
        },
        "error_hypothesis": "判据二（T=T2+T1+T0 与欧拉定理的应用）仍写不出；E 表达式与直接计算两项独立正确",
        "diagnosis_status": "pending_probe",
        "solution_seen": False,
        "artifact_ref": "learning/attempts/tm-t4-criteria-01-attempt1.png",
        "ts": "2026-09-28"
    },
    {
        "event_id": "attempt-4",
        "task_id": "tm-h4-03",
        "task_version": "1",
        "target_ids": ["tm.t4.energy-integral", "tm.t4.cyclic-momentum"],
        "mode": "practice",
        "closed_book": True,
        "initial_result": "partial",
        "max_hint_level": 0,
        "final_result": "partial",
        "predicted_confidence": None,
        "active_minutes": 20,
        "time_source": "estimated",
        "solution_exposure": "full",
        "exposure_timing": "before_attempt",
        "target_results": {
            "tm.t4.energy-integral": {"initial": "correct", "hint_level": 0, "final": "correct", "needs_verify": False,
                                      "note": "能量积分 ½m₁ẋ₁²+½m₂ẋ₂²+½k(x₂−x₁−l)² = C，正确"},
            "tm.t4.cyclic-momentum": {"initial": "partial", "hint_level": 0, "final": "partial", "needs_verify": True,
                                      "note": "写成 dP/dt=0 ⇒ m₁ẍ₁+m₂ẍ₂=0（推导正确）；题目要的是积分式，缺 P = m₁ẋ₁+m₂ẋ₂ = const"}
        },
        "error_hypothesis": "把运动积分写成时间导数形式，未再积一步给出守恒量表达式；两条积分的表达式此前已在反馈中展示（全曝光，不计独立）",
        "diagnosis_status": "confirmed",
        "solution_seen": True,
        "artifact_ref": "learning/attempts/tm-h4-03-attempt1.png",
        "ts": "2026-09-28"
    },
]

for ev in events:
    tmp = ROOT / "learning" / "attempts" / f"_new_{ev['event_id']}.json"
    tmp.write_text(json.dumps(ev, ensure_ascii=False), encoding="utf-8")
    rc = subprocess.run([sys.executable, "-B", "tools/append_attempt.py", "--file", str(tmp)],
                        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(f"[{ev['event_id']}] rc={rc.returncode}")
    print((rc.stdout or "").strip())
    if rc.stderr and rc.stderr.strip():
        print("STDERR:", rc.stderr.strip())
    tmp.unlink(missing_ok=True)
