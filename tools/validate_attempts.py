#!/usr/bin/env python3
"""校验学习事件日志 learning/attempts.jsonl。

工程约束（来自架构约定）：
- 事件由程序验证后才能写入/计分：本脚本是唯一入口校验器
- event_id 唯一（attempt-N），重试不得重复计分
- task_id 必须引用 learning/tasks/ 中存在的题目
- target_ids 必须是该题目**在事件所引版本**下声明目标(target_ids)的非空子集：
  一道题不能给无关能力计分；升版换目标时按历史版本元数据（learning/tasks/history/）校验
- task_version 不一致 → 警告不阻断：
  - 有历史版本元数据 → 按该版本元数据解释（警告提示成绩不与当前版本直接比较）
  - 无历史版本元数据 → 保留记录但暂不用于升级（跳过目标校验，警告提示）
- 辅导后做对（final_result=correct 且 max_hint_level>0）必须保留提示级别，不得降级记录
- 测验模式只允许 max_hint_level 0/null；示例学习模式必须 solution_seen=true
- artifact_ref 若给出，对应文件必须存在

用法:
  python -B tools/validate_attempts.py --root .
"""
from __future__ import annotations

import argparse
import datetime as dt
import math
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path

from learninglib import (
    EXPOSURE_TIMING,
    PER_TARGET_KEYS,
    SOLUTION_EXPOSURE,
    TIME_SOURCES,
    apply_corrections,
    check_corrections,
    help_record_inconsistencies,
    load_attempts,
    load_corrections,
    load_task_history,
    load_tasks,
    resolve_task_meta,
)

MODES = {"practice", "quiz", "worked-example"}
INITIAL_RESULTS = {"correct", "partial", "blocked", "not_attempted"}
FINAL_RESULTS = {"correct", "partial", "incorrect", "abandoned"}
TARGET_FINAL_RESULTS = FINAL_RESULTS | {"blocked", "not_attempted"}
DIAGNOSIS_STATUS = {"none", "pending_probe", "confirmed", "repaired"}
REQUIRED = [
    "event_id", "task_id", "task_version", "target_ids", "mode", "closed_book",
    "initial_result", "max_hint_level", "final_result", "predicted_confidence",
    "active_minutes", "error_hypothesis", "diagnosis_status", "solution_seen",
    "artifact_ref", "ts",
]


def check(root: Path) -> tuple[list[str], list[str], list[dict], dict[str, dict]]:
    """返回 (errors, warnings, attempts, tasks)。仅 errors 非空时计分无效。

    **`attempts` 返回的是"应用订正后的记录"**（learning/corrections.jsonl）：
    校验、能力派生（derive_state）与排期（plan-week）因此同源，
    不会出现"订正只对其中一个消费者生效"。原始 attempts.jsonl 仍只增不改。
    """
    errors: list[str] = []
    warnings: list[str] = []
    tasks = load_tasks(root)
    history = load_task_history(root)
    rows = load_attempts(root)

    # ① 先解析原始事件（保留行号）——坏行照旧报错
    parsed: list[tuple[int, dict]] = []
    for row in rows:
        if row["data"] is None:
            errors.append(f"line {row['line']}: {row.get('error', 'invalid json')}")
            continue
        parsed.append((row["line"], row["data"]))

    # ② 应用结构化订正（校验订正本身 → 在拷贝上应用），③ 之后所有判定都基于应用订正后的记录
    correction_rows = load_corrections(root)
    errors.extend(check_corrections(correction_rows, [d for _line, d in parsed]))
    effective = apply_corrections([d for _line, d in parsed], correction_rows)

    seen_ids: set[str] = set()
    seen_submissions: set[str] = set()
    attempts: list[dict] = []
    for (line_no, _raw), data in zip(parsed, effective):
        label = f"line {line_no}"
        for key in REQUIRED:
            if key not in data:
                errors.append(f"{label}: missing field {key}")
        event_id = data.get("event_id")
        if not isinstance(event_id, str) or not event_id.startswith("attempt-") or not event_id[8:].isdigit():
            errors.append(f"{label}: event_id must be attempt-N, got {event_id!r}")
        elif event_id in seen_ids:
            errors.append(f"{label}: duplicate event_id {event_id} (重试不得重复计分)")
        else:
            seen_ids.add(event_id)
        target_ids = data.get("target_ids")
        submission=data.get('submission_id')
        if submission is not None:
            if not isinstance(submission,str) or not submission.strip() or len(submission)>200:
                errors.append(f'{label}: invalid submission_id')
            elif submission in seen_submissions:
                errors.append(f'{label}: duplicate submission_id')
            else:
                seen_submissions.add(submission)
        if 'task_completed' in data and type(data['task_completed']) is not bool:
            errors.append(f'{label}: task_completed must be boolean')
        if not isinstance(target_ids, list) or not all(isinstance(x, str) for x in target_ids):
            errors.append(f"{label}: target_ids must be a list of strings")
        if data.get("mode") not in MODES:
            errors.append(f"{label}: bad mode {data.get('mode')!r}")
        if data.get("initial_result") not in INITIAL_RESULTS:
            errors.append(f"{label}: bad initial_result {data.get('initial_result')!r}")
        if data.get("final_result") not in FINAL_RESULTS:
            errors.append(f"{label}: bad final_result {data.get('final_result')!r}")
        if data.get("diagnosis_status") not in DIAGNOSIS_STATUS:
            errors.append(f"{label}: bad diagnosis_status {data.get('diagnosis_status')!r}")
        hint = data.get("max_hint_level")
        if hint is not None and (type(hint) is not int or not 0 <= hint <= 4):
            errors.append(f"{label}: max_hint_level must be 0-4 or null, got {hint!r}")
        if data.get("mode") == "quiz" and hint != 0:
            errors.append(
                f"{label}: quiz mode requires explicit max_hint_level=0（null=未知，不等于无提示）: {hint!r}"
            )
        if data.get("mode") == "worked-example" and data.get("solution_seen") is not True:
            errors.append(f"{label}: worked-example mode must record solution_seen=true")
        # --- 可选字段（2026-09-27 新增；缺失时按旧语义回退，不报错）---
        exposure = data.get("solution_exposure")
        if exposure is not None and exposure not in SOLUTION_EXPOSURE:
            errors.append(f"{label}: bad solution_exposure {exposure!r}（应为 {SOLUTION_EXPOSURE} 之一）")
        timing = data.get("exposure_timing")
        if timing is not None and timing not in EXPOSURE_TIMING:
            errors.append(f"{label}: bad exposure_timing {timing!r}（应为 {EXPOSURE_TIMING} 之一）")
        tsrc = data.get("time_source")
        if tsrc is not None and tsrc not in TIME_SOURCES:
            errors.append(f"{label}: bad time_source {tsrc!r}（应为 {TIME_SOURCES} 之一）")
        target_results = data.get("target_results")
        if target_results is not None:
            if not isinstance(target_results, dict) or not target_results:
                errors.append(f"{label}: target_results must be a non-empty object")
            else:
                for tkey, tval in target_results.items():
                    if isinstance(target_ids, list) and tkey not in target_ids:
                        errors.append(f"{label}: target_results 含未声明目标 {tkey!r}")
                    if not isinstance(tval, dict):
                        errors.append(f"{label}: target_results[{tkey}] must be an object")
                        continue
                    for rkey, rval in tval.items():
                        if rkey not in PER_TARGET_KEYS:
                            errors.append(f"{label}: target_results[{tkey}] 未知字段 {rkey!r}")
                        elif rkey == 'hint_level' and rval is not None and (type(rval) is not int or not 0 <= rval <= 4):
                            errors.append(f'{label}: target hint_level must be integer 0..4 or null')
                        elif rkey == 'final' and rval is not None and rval not in TARGET_FINAL_RESULTS:
                            errors.append(f'{label}: invalid target final result')
                        elif rkey == 'initial' and rval is not None and rval not in INITIAL_RESULTS:
                            errors.append(f'{label}: invalid target initial result')
                        elif rkey == "exposure" and rval is not None and rval not in SOLUTION_EXPOSURE:
                            errors.append(
                                f"{label}: target_results[{tkey}].exposure 非法 {rval!r}（应为 {SOLUTION_EXPOSURE} 之一）"
                            )
                        elif rkey == "exposure_timing" and rval is not None and rval not in EXPOSURE_TIMING:
                            errors.append(
                                f"{label}: target_results[{tkey}].exposure_timing 非法 {rval!r}（应为 {EXPOSURE_TIMING} 之一）"
                            )
                        elif rkey == "needs_verify" and not isinstance(rval, bool):
                            errors.append(f"{label}: target_results[{tkey}].needs_verify must be boolean")
        for key in ("closed_book", "solution_seen"):
            if not isinstance(data.get(key), bool):
                errors.append(f"{label}: {key} must be boolean")
        conf = data.get("predicted_confidence")
        if conf is not None and (not isinstance(conf, (int, float)) or isinstance(conf, bool) or not 0 <= conf <= 1):
            errors.append(f"{label}: predicted_confidence must be 0-1 or null")
        if not isinstance(data.get("active_minutes"), (int, float)) or isinstance(data.get("active_minutes"), bool) or not math.isfinite(data.get('active_minutes',0)) or data.get("active_minutes", -1) < 0:
            errors.append(f"{label}: active_minutes must be a non-negative number")
        try:
            dt.date.fromisoformat(str(data.get("ts", "")))
        except ValueError:
            errors.append(f"{label}: ts must be YYYY-MM-DD")
        task_id = data.get("task_id")
        current_task = tasks.get(task_id)
        if current_task is None:
            errors.append(f"{label}: task_id {task_id!r} not found in learning/tasks/")
        else:
            version = str(data.get("task_version", ""))
            meta = resolve_task_meta(tasks, history, task_id, version)
            if meta is None:
                warnings.append(
                    f"{label}: 版本元数据缺失（{task_id} v{version}）：不校验目标、该事件保留但不用于升级"
                )
            else:
                if version != current_task["version"]:
                    warnings.append(
                        f"{label}: task_version mismatch for {task_id}: {version} != {current_task['version']} "
                        f"（按 v{version} 历史元数据解释，成绩不与当前版本直接比较）"
                    )
                declared = set(meta["target_ids"])
                if not declared:
                    errors.append(f"{label}: task {task_id} v{version} declares no target_ids")
                elif not isinstance(target_ids, list) or not target_ids:
                    errors.append(f"{label}: attempt must list at least one target")
                else:
                    for tid in target_ids:
                        if tid not in declared:
                            errors.append(
                                f"{label}: target_ids 越界：{tid} 未由题目 {task_id} v{version} 声明，不能计分"
                            )
        ref = data.get("artifact_ref")
        if ref:
            if not isinstance(ref, str) or not (root / ref).is_file():
                errors.append(f"{label}: artifact_ref missing file: {ref!r}")
        # 帮助史一致性（2026-09-30 加）：事件级声称 H0+无曝光、目标级却记着帮助 → 展示与判定不一致。
        # 报 WARN 而不是 ERROR：判定本身按目标级走（不会错误升级），但记录会误导读者，
        # 必须显式提示去订正目标级字段（本轮 attempt-28 就踩在这里）。
        for problem in help_record_inconsistencies(data):
            warnings.append(f"{label}（{data.get('event_id')}）: {problem}")
        attempts.append(data)
    return errors, warnings, attempts, tasks


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate learning attempt events.")
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors, warnings, attempts, tasks = check(root)
    for warning in warnings:
        print(f"WARN {warning}")
    if errors:
        print("ATTEMPT VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("ATTEMPT VALIDATION OK")
    print(f"- attempts: {len(attempts)}")
    print(f"- tasks: {len(tasks)}")
    print(f"- warnings: {len(warnings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
