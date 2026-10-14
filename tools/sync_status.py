#!/usr/bin/env python3
"""同步 AGENTS.md / CLAUDE.md 的 TUTOR-STATUS 块：**可数事实由程序生成**，叙述行由人维护。

分工（见 learning/README.md）：
- 作答/困难观察 = 事实来源（learning/attempts.jsonl、learning/hurdles.jsonl）
- 能力状态 = 程序派生（learning/learner-state.json）
- STATUS 块 = 派生视图：`last_session` / `due_today` / `mastered` / `open_hurdles` / `attempts`
  由本脚本重算；`current_subject` / `current_topic` / `next` / `note` 保留现有文本（人工叙述）。
- 两个文件必须**逐字一致**（AGENTS.md 与 CLAUDE.md 互为镜像）。

用法: python -B tools/sync-status.py [--root .] [--today YYYY-MM-DD] [--dry-run]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from learninglib import load_attempts, load_hurdles, parse_yaml  # noqa: E402
from timebase import learning_today
from workspace_lock import LockTimeout, WorkspaceLock, atomic_write_text  # noqa: E402

NARRATIVE_KEYS = ("current_subject", "current_topic", "next", "note")
GENERATED_KEYS = ("last_session", "due_today", "mastered", "open_hurdles", "attempts")
BLOCK_RE = re.compile(r"<!-- TUTOR-STATUS:START -->\n(.*?)\n<!-- TUTOR-STATUS:END -->", re.S)
# 文件名（含 `AGENTS.md/CLAUDE.md` 这种连写形式）：两个文件必然各自写着不同的名字
# （标题行、"本文件"说明，以及"必须镜像对方"那句）——这些**必然**不同（ISSUES B6）。
# 镜像规则因此是"**除文件名外**逐字一致"；本函数就是这条规则的可执行检查：
# 把两个文件名（任意出现形式）都归一化成一个占位符，再逐字比较。
# ⚠ 需要把"名字/名字"整体吃掉：否则 `/` 两侧各剩一个名字，归一化结果仍不对称
# （2026-09-30 实测：`AGENTS.md/CLAUDE.md` 会漏掉).
MIRROR_NAME_RE = re.compile(r"\b(?:AGENTS|CLAUDE)\.md\b(?:\s*/\s*\b(?:AGENTS|CLAUDE)\.md\b)?")


def mirrored_except_names(a: Path, b: Path) -> bool:
    """除文件名外，两文件是否逐字一致（ISSUES B6 的可执行验收）。"""
    try:
        ta = a.read_text(encoding="utf-8")
        tb = b.read_text(encoding="utf-8")
    except OSError:
        return False
    return MIRROR_NAME_RE.sub("<MIRROR>", ta) == MIRROR_NAME_RE.sub("<MIRROR>", tb)


def read_block(path: Path) -> dict[str, str] | None:
    if not path.is_file():
        return None
    match = BLOCK_RE.search(path.read_text(encoding="utf-8"))
    if not match:
        return None
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields


def write_block(path: Path, body: str) -> None:
    text = path.read_text(encoding="utf-8")
    block = f"<!-- TUTOR-STATUS:START -->\n{body}\n<!-- TUTOR-STATUS:END -->"
    if BLOCK_RE.search(text):
        text = BLOCK_RE.sub(block, text)
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    atomic_write_text(path, text)


def due_count(root: Path, today: str) -> tuple[int, str]:
    """到期复习条数 + 来源说明。

    2026-09-30 修（学习者 2026-09-26 明确要求「有计划地定期复习」，而 `due_today` 长期为 0）：
    旧实现只正则匹配 `state/due.md` 里那句「共 N 个概念已到期」——那是**生成产物**，
    没人重跑就永远是 0，复习队列从未真正运行。
    现在直接扫描事实源：`subjects/**/topics/*.md` frontmatter 的 `due`（记忆维护队列），
    与 `tools/schedule_reviews.py` 共用 `tools/reviews.py`，避免两处实现漂移。
    """
    try:
        from reviews import overdue_concepts

        items = overdue_concepts(root, today)
    except Exception as exc:  # noqa: BLE001 - 读取失败要报「未知」，不猜
        return -1, f"到期数未知（扫描概念笔记失败：{exc}）"
    return len(items), f"{len(items)} 个到期复习概念（扫 subjects/**/topics 的 frontmatter，截至 {today}）"


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync TUTOR-STATUS block in AGENTS.md and CLAUDE.md.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--today", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    today = learning_today(args.today)

    state_path = root / "learning" / "learner-state.json"
    if not state_path.is_file():
        print("ERROR: 缺少 learning/learner-state.json（先运行 tools/derive_state.py）", file=sys.stderr)
        return 2
    state = json.loads(state_path.read_text(encoding="utf-8"))

    attempts = [r["data"] for r in load_attempts(root) if r.get("data")]
    hurdles = [r["data"] for r in load_hurdles(root) if r.get("data")]
    open_hurdles = [h for h in hurdles if h.get("status") in ("open", "teaching", "awaiting_retest")]
    last_ts = max((str(a.get("ts", "")) for a in attempts), default="无")

    agents = root / "AGENTS.md"
    claude = root / "CLAUDE.md"
    current = read_block(agents) or read_block(claude)
    if current is None:
        print("ERROR: 两个文件都找不到 TUTOR-STATUS 块", file=sys.stderr)
        return 2

    # 叙述行来源优先级：.tutor/config/status-narrative.yml（唯一来源）→ 现有 STATUS 块
    narrative_path = root / ".tutor" / "config" / "status-narrative.yml"
    narrative: dict[str, str] = {}
    # Narrative is retained as a human-readable source, including legacy unquoted Markdown.
    # It is no longer parsed or copied into the generated compact navigation block.
    for key in NARRATIVE_KEYS:
        narrative.setdefault(key, current.get(key, "(未填写)"))

    levels = state["summary"]["by_level"]
    mastered = levels.get("迁移通过", 0)
    total = state["summary"]["targets"]
    due, due_note = due_count(root, today)

    fields: dict[str, str] = {}
    for key in NARRATIVE_KEYS:
        fields[key] = narrative.get(key, current.get(key, "(未填写)"))
    # Preserve full current intent in its original source; keep cold-start navigation small.
    fields.update({
        'current_subject':'见 state/current.md 按项目的有效证据；课程顺序见 .tutor/config/status-narrative.yml',
        'current_topic':'维护刷新不代表新学习；具体续学点见 state/current.md',
        'next':'见 plan/schedule.md、当天清单与原 status-narrative.yml；先尊重学习者当次选择',
        'note':'默认闭卷；Unicode 公式；中国日期；保留当前项目协议和个人偏好',
    })
    fields["last_session"] = f"{last_ts}（作答 {len(attempts)} 条；未解决困难 {len(open_hurdles)} 条）"
    fields["due_today"] = due_note
    fields["mastered"] = f"迁移通过 {mastered}/{total}（稳定证据 {state['summary']['stable_evidence']}；截至 {today}）"
    fields["open_hurdles"] = (
        "；".join(f"{h.get('hurdle_id')}({h.get('status')})→{','.join(h.get('target_ids') or [])}" for h in open_hurdles)
        or "无"
    )
    fields["attempts"] = f"{len(attempts)} 条（实测时长 {state['summary']['measured_minutes_global']} 分钟；估计 {state['summary']['estimated_minutes_global']} 分钟单列）"

    order = list(NARRATIVE_KEYS) + ["last_session", "due_today", "mastered", "open_hurdles", "attempts"]
    body = "\n".join(f"{key}: {fields[key]}" for key in order)

    if args.dry_run:
        print(body)
        return 0

    # 2026-09-30（ISSUES D4）：叙述行曾被并发编辑回退过一次（后写者用旧副本覆盖）。
    # 现在：锁内校验"进入时读到的一致状态"仍在 → 否则拒绝写入并显式报错，
    # 而不是把另一条会话线刚写的 STATUS 覆盖掉。写入本身走原子替换。
    try:
        with WorkspaceLock(root, label="sync_status"):
            if read_block(agents) != current or read_block(claude) != current:
                print(
                    "REFUSED: 等锁期间 AGENTS.md/CLAUDE.md 的 STATUS 被其他会话修改 → 本次**未写入**。"
                    "请重跑本脚本（重新读取最新叙述行）后再同步。",
                    file=sys.stderr,
                )
                return 4
            write_block(agents, body)
            write_block(claude, body)
    except LockTimeout as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 4

    same = read_block(agents) == read_block(claude)
    mirrored = mirrored_except_names(agents, claude)
    print("STATUS 已同步（叙述行保留，可数事实重算）")
    print(f"- 生成字段：{', '.join(GENERATED_KEYS)}")
    print(f"- STATUS 块两文件一致：{same}")
    print(f"- 两文件除互指文件名外逐字一致：{mirrored}")
    if not same or not mirrored:
        print("WARN 镜像规则未满足（见上）——不要只更新计数就宣称状态已同步", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
