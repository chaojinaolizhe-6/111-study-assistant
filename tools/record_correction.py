#!/usr/bin/env python3
"""写入一条**可追溯**的事实订正（learning/corrections.jsonl）。

为什么需要单独的工具（ISSUES B7 + 本次维护）：
- 原始作答事件 `attempts.jsonl` **只增不改**，订正写在 `corrections.jsonl`；
- 但"怎么写一条合法订正"此前没有入口：要手写 JSON，容易漏 `reason`/`evidence_ref`，
  也容易把 `from` 写错——而 `from` 写错在过去会被**静默接受**（ISSUES B2，本次已修）。
- 本工具在**锁内**完成"校验 → 追加 → 全量复核"，并强制要求：
  `reason`（为什么改）、`source`（证据种类）、`evidence_ref`（证据在哪，如会话 id + seq）。
  **没有证据就不给订正**——这是"不能靠改写原始事件绕过"的落地方式。

用法:
  python -B tools/record_correction.py --event-id attempt-28 --field max_hint_level \
      --from-json 0 --to-json 2 --reason "测验前导师已就第 4 题给出方法提示" \
      --source record_audit --evidence-ref "session-a46ca69d seq387"

  # 目标级字段；--from/--to 用 --from-json/--to-json 传非字符串
  python -B tools/record_correction.py --event-id attempt-28 --scope target \
      --target-id mp.isolated-singularity --field exposure --from-json '"none"' --to-json '"partial"' ...
"""
from __future__ import annotations

import argparse
import json
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from learninglib import (  # noqa: E402
    ALLOWED_EVENT_FIELDS,
    CORRECTION_SOURCES,
    PER_TARGET_KEYS,
    apply_corrections,
    check_corrections,
    load_attempts,
    load_corrections,
)
from timebase import learning_today
from validate_attempts import check  # noqa: E402
from workspace_lock import LockTimeout, WorkspaceLock, atomic_write_text  # noqa: E402


def parse_value(raw: str | None, raw_json: str | None, label: str):
    if raw_json is not None:
        return json.loads(raw_json)
    return raw


def main() -> int:
    parser = argparse.ArgumentParser(description="Append one traceable correction to learning/corrections.jsonl")
    parser.add_argument("--root", default=".")
    parser.add_argument("--correction-id", required=True)
    parser.add_argument("--event-id", required=True)
    parser.add_argument("--scope", choices=("event", "target"), default="event")
    parser.add_argument("--target-id", default=None)
    parser.add_argument("--field", required=True)
    parser.add_argument("--from", dest="from_raw", default=None, help="字符串值；非字符串请用 --from-json")
    parser.add_argument("--to", dest="to_raw", default=None, help="字符串值；非字符串请用 --to-json")
    parser.add_argument("--from-json", default=None, help='JSON 字面量，如 \'"none"\'、true、2、null')
    parser.add_argument("--to-json", default=None)
    parser.add_argument("--reason", required=True)
    parser.add_argument("--source", required=True, choices=CORRECTION_SOURCES)
    parser.add_argument("--evidence-ref", required=True)
    parser.add_argument("--at", default=None, help="日期（默认中国 UTC+8）")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    path = root / "learning" / "corrections.jsonl"
    try:
        today = learning_today(args.at)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.scope == "target" and not args.target_id:
        print("ERROR: scope=target 必须给 --target-id", file=sys.stderr)
        return 2
    if args.scope == "event" and args.target_id:
        print("ERROR: scope=event 不应带 --target-id", file=sys.stderr)
        return 2
    if args.scope == "event" and args.field not in ALLOWED_EVENT_FIELDS:
        print(f"ERROR: 事件级字段 {args.field!r} 不允许订正（仅 {ALLOWED_EVENT_FIELDS}）", file=sys.stderr)
        return 2
    if args.scope == "target" and args.field not in PER_TARGET_KEYS:
        print(f"ERROR: 目标级字段 {args.field!r} 不在 {PER_TARGET_KEYS}", file=sys.stderr)
        return 2

    try:
        value_from = parse_value(args.from_raw, args.from_json, "from")
        value_to = parse_value(args.to_raw, args.to_json, "to")
    except json.JSONDecodeError as exc:
        print(f"ERROR: --from-json/--to-json 不是合法 JSON：{exc}", file=sys.stderr)
        return 2
    if value_from is None and args.from_json is None and args.from_raw is None:
        print("ERROR: 必须给 --from 或 --from-json", file=sys.stderr)
        return 2
    if value_to is None and args.to_json is None and args.to_raw is None:
        print("ERROR: 必须给 --to 或 --to-json", file=sys.stderr)
        return 2

    entry = {
        "correction_id": args.correction_id,
        "event_id": args.event_id,
        "scope": args.scope,
        "field": args.field,
        "from": value_from,
        "to": value_to,
        "reason": args.reason,
        "source": args.source,
        "evidence_ref": args.evidence_ref,
        "at": today,
    }
    if args.target_id:
        entry["target_id"] = args.target_id

    try:
        with WorkspaceLock(root / "learning", label="record_correction"):
            rows = load_corrections(root)
            existing_ids = {r["data"].get("correction_id") for r in rows if r.get("data")}
            if args.correction_id in existing_ids:
                print(f"REFUSED: correction_id {args.correction_id!r} 已存在，未写入", file=sys.stderr)
                return 3

            # 在"应用此前订正后的记录"上校验 from —— 避免同一字段两条订正互相掩盖
            parsed = [r["data"] for r in load_attempts(root) if r.get("data")]
            effective = {a.get("event_id"): a for a in apply_corrections(parsed, rows)}
            event = effective.get(args.event_id)
            if event is None:
                print(f"ERROR: event_id {args.event_id!r} 不在 attempts.jsonl 中", file=sys.stderr)
                return 2
            if args.scope == "target":
                tr = (event.get("target_results") or {}).get(args.target_id)
                if not isinstance(tr, dict):
                    print(f"ERROR: target_results[{args.target_id!r}] 不存在", file=sys.stderr)
                    return 2
                current = tr.get(args.field)
            else:
                current = event.get(args.field)
            if current != value_from:
                print(
                    f"ERROR: --from 与当前（应用此前订正后）的值不一致：记录 {value_from!r}，实际 {current!r}。"
                    "请先核对，不要凭印象写 from。",
                    file=sys.stderr,
                )
                return 2

            line = json.dumps(entry, ensure_ascii=False) + "\n"
            if args.dry_run:
                print("[dry-run] 将要追加订正（未写入）：")
                print(line.rstrip())
                return 0

            original = path.read_bytes().decode('utf-8') if path.is_file() else ''
            prefix = '\n' if original and not original.endswith('\n') else ''
            atomic_write_text(path, original + prefix + line)
            try:
                errors, warnings, attempts, _tasks = check(root)
            except Exception as exc:
                atomic_write_text(path, original)
                print(f'REFUSED: validation exception {type(exc).__name__}; original bytes preserved',file=sys.stderr)
                return 1
            for warning in warnings:
                print(f'WARN {warning}')
            if errors:
                atomic_write_text(path, original)
                print('REFUSED: invalid correction; original bytes preserved', file=sys.stderr)
                for error in errors:
                    print(f'- {error}', file=sys.stderr)
                return 1
    except LockTimeout as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 4

    print(f"step 2/2 校验通过：attempts={len(attempts)}，corrections={len(load_corrections(root))}")
    print("提示：接着运行 python -B tools/session-close.py --today <中国日期>（重建能力状态并同步入口）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
