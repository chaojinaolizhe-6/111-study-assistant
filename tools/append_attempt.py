#!/usr/bin/env python3
"""安全追加作答事件：**锁内**取号 → 校验 → 写入 → 复核；重试不重复计分、失败不覆盖别人的新增行。

与旧实现的区别（ISSUES B8 / D4）：
- 旧：`读全文件 → 重写全文件`，靠人读文本"预留"下一个 attempt-N。两条会话线同时写时，
  后写者会用自己读到的旧快照覆盖先写者的新行；且预留号只写在人读文本里，程序看不见。
- 新：`learning/.write.lock` 互斥（跨进程）→ 锁内**机器取号**（`learning/attempts/_ids.json`
  与 attempts.jsonl 实际最大号取较大值 +1）→ 写入走 **append 模式**（只追加一行，
  不再重写整个文件，因此不可能覆盖别人的行）→ 写后跑全量校验，失败则**只回滚自己追加的那一行**。

用法:
  python -B tools/append_attempt.py --file learning/attempts/_new_event.json
  python -B tools/append_attempt.py --file ev.json --event-id auto   # 自动取号（推荐）
  python -B tools/append_attempt.py --file ev.json --dry-run         # 只看将要写入什么
"""
from __future__ import annotations

import argparse
import json
import os
import hashlib
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from workspace_lock import (  # noqa: E402
    LockTimeout,
    WorkspaceLock,
    atomic_write_text,
    bump_counter,
    max_suffix_event_id,
    next_counter,
)
from validate_attempts import check  # noqa: E402

ID_PREFIX = "attempt-"


def payload(event):
    return {k:v for k,v in event.items() if k not in ('event_id','submission_id')}


def load_event(args) -> dict:
    raw = args.event if args.event else Path(args.file).read_text(encoding="utf-8")
    event = json.loads(raw)
    if not isinstance(event, dict):
        raise ValueError("事件必须是 JSON 对象")
    return event


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate-then-append one attempt event (lock-protected).")
    parser.add_argument("--root", default=".")
    parser.add_argument("--event", help="事件 JSON 字符串")
    parser.add_argument("--file", help="事件 JSON 文件路径")
    parser.add_argument(
        "--event-id",
        default=None,
        help="'auto' = 在锁内自动取号（推荐）；或显式给出 attempt-N（撞号会被拒绝）",
    )
    parser.add_argument("--dry-run", action="store_true", help="只显示将要写入的内容，不写任何文件")
    parser.add_argument('--submission-id', help='稳定的真实作答提交ID；重试复用，新作答换新ID')
    parser.add_argument("--lock-timeout", type=float, default=30.0)
    args = parser.parse_args()

    if bool(args.event) == bool(args.file):
        print("ERROR: 需要且只需要 --event 或 --file 之一", file=sys.stderr)
        return 2

    root = Path(args.root).resolve()
    path = root / "learning" / "attempts.jsonl"
    counter_path = root / "learning" / "attempts" / "_ids.json"

    try:
        event = load_event(args)
        submission=args.submission_id or event.get('submission_id')
        if submission is None:
            identity=json.dumps(payload(event),ensure_ascii=False,sort_keys=True,allow_nan=False)
            submission='auto-'+hashlib.sha256(identity.encode('utf-8')).hexdigest()
        if not isinstance(submission,str) or not submission.strip() or len(submission)>200:
            raise ValueError('submission_id must be a nonempty string up to 200 characters')
        event['submission_id']=submission
    except json.JSONDecodeError as exc:
        print(f"ERROR: 事件不是合法 JSON：{exc}", file=sys.stderr)
        print("提示：中文文本里的引号请用「」，半角引号会让事件成为非法 JSON。", file=sys.stderr)
        return 2
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    # ---- 锁内完成"取号 + 查重 + 追加"（整个读-校验-写过程受保护）----
    try:
        with WorkspaceLock(root / "learning", label="append_attempt", timeout=args.lock_timeout):
            original = path.read_bytes().decode("utf-8") if path.is_file() else ""
            bad_lines = []
            existing: set[str] = set()
            for line_no, line in enumerate(original.splitlines(), 1):
                if not line.strip():
                    continue
                try:
                    previous=json.loads(line)
                    if not isinstance(previous,dict):
                        raise ValueError('Existing event is not an object')
                    if previous.get('submission_id') == submission:
                        if payload(previous) != payload(event):
                            print('REFUSED: submission_id reused with different content',file=sys.stderr)
                            return 3
                        print(f"ALREADY SAVED: event_id={previous['event_id']}; no duplicate event or time")
                        return 0
                    existing.add(previous.get("event_id", ""))
                except json.JSONDecodeError:
                    bad_lines.append(line_no)
            if bad_lines:
                print(f"ERROR: 现有 attempts.jsonl 有坏行 {bad_lines}，先修复再追加（未写入任何内容）", file=sys.stderr)
                return 2

            auto = args.event_id in (None, "auto")
            if args.event_id == "auto":
                floor = max(max_suffix_event_id(original, ID_PREFIX), next_counter(counter_path, ID_PREFIX) - 1)
                event_id = f"{ID_PREFIX}{floor + 1}"
            elif args.event_id:
                event_id = args.event_id
            else:
                event_id = event.get("event_id")

            if not isinstance(event_id, str) or not event_id.startswith(ID_PREFIX) or not event_id[len(ID_PREFIX):].isdigit():
                print(f"ERROR: event_id 必须是 attempt-N，得到 {event_id!r}", file=sys.stderr)
                return 2
            if event_id in existing:
                nxt = max(max_suffix_event_id(original, ID_PREFIX), next_counter(counter_path, ID_PREFIX) - 1) + 1
                print(
                    f"REFUSED: event_id {event_id!r} 已存在 —— 不重复计分，未写入。"
                    f"下一个可用号 = {ID_PREFIX}{nxt}",
                    file=sys.stderr,
                )
                return 3

            event = dict(event)
            event["event_id"] = event_id
            line = json.dumps(event, ensure_ascii=False) + "\n"
            if args.dry_run:
                print(f"[dry-run] event_id={event_id}; no files or counters changed")
                print(line.rstrip())
                return 0
            original_size = len(original.encode('utf-8'))
            prefix = '\n' if original and not original.endswith('\n') else ''
            try:
                with open(path, 'ab') as handle:
                    handle.write((prefix+line).encode('utf-8'))
                    handle.flush()
                    os.fsync(handle.fileno())
                errors, warnings, attempts, _tasks = check(root)
            except Exception as exc:
                with open(path, 'r+b') as handle:
                    handle.truncate(original_size)
                    handle.flush()
                    os.fsync(handle.fileno())
                print(f'REFUSED: validation/write exception {type(exc).__name__}; original bytes preserved',file=sys.stderr)
                return 1
            for warning in warnings:
                print(f'WARN {warning}')
            if errors:
                with open(path, 'r+b') as handle:
                    handle.truncate(original_size)
                    handle.flush()
                    os.fsync(handle.fileno())
                print('REFUSED: invalid event; original bytes preserved', file=sys.stderr)
                for error in errors:
                    print(f'- {error}', file=sys.stderr)
                return 1
            if auto:
                try:
                    bump_counter(counter_path, ID_PREFIX, int(event_id[len(ID_PREFIX):]))
                except OSError:
                    print('WARN: event committed; counter cache not updated, next ID derives from the log')
    except LockTimeout as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 4

    print(f"step 2/2 校验通过：attempts={len(attempts)}，event_id={event_id}")
    print("提示：接着运行 python -B tools/session-close.py --today <中国日期>（会重建能力状态并同步入口）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
