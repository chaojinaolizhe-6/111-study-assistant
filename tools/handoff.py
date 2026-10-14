#!/usr/bin/env python3
"""生成 `plan/handoff-CURRENT.md` —— 跨窗口续学的**唯一入口文件**（派生自动 + 人工意图）。

解决的问题（本轮改进要求 P0-A）：
- 旧 handoff 是**手写快照**，实测已经过期到自相矛盾：孤立奇点已有 `attempt-27～31`，
  交接却还写「完全未开始」；STATUS 还留着「今天 09-29」「判据二复测已欠一天」。
- 人工维护"我读到哪了"这件事本身不可靠 → 改为：
  **静态部分**（协议、读文件顺序、规则提醒）写在本脚本的模板里（长期稳定，不随进度变）；
  **动态部分**（现在到哪、最近证据、帮助史、卡点、下一步）全部**引用 `state/current.md`**，
  由 `tools/current_state.py` 从 `learning/` 重算；
  **人工意图**（今天做什么、为什么暂缓）只从两处取：`.tutor/config/status-narrative.yml` 的叙述行
  和 `plan/today-<中国日期>.md`（不存在则显式写「今天清单尚未建立」，不编造）。

用法:
  python -B tools/handoff.py --root . --today 2026-09-30
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from learninglib import parse_yaml  # noqa: E402
from timebase import learning_today, uk_date_now  # noqa: E402
from workspace_lock import LockTimeout, WorkspaceLock, atomic_write_text  # noqa: E402

NARRATIVE_KEYS = ("current_subject", "current_topic", "next", "note")

TEMPLATE = """# 当前续学入口（CURRENT）

> ✅ **这是唯一应当复制到新对话的交接文件**（由 `python -B tools/handoff.py` 生成）。
> 📌 **当前事实不在本文件里** —— 全部在 **`state/current.md`**（由 `learning/` 重算，含指纹可核）。
> 本文件只负责：①告诉你按什么顺序读；②把当前事实与人工意图**引用**过来；③给规则提醒。
> ⚠ 旧文件 `plan/handoff-prompt-2026-09-28.md` 已标为**历史、勿用**（它是 09-28 上午的快照，会把进度倒退）。
> 生成时间：**{today}**（中国时间；系统英国日期 {uk}）。若与 `state/current.md` 不一致，**以 `state/current.md` 为准**。

---

```
请按本工作区的 tutor 规则继续带我学习（AGENTS.md / CLAUDE.md 会自动注入）。

【时间基准】系统时钟是英国时间，我的真实时间是中国大陆（UTC+8）。
所有「今天/明天/截止日/时间窗」一律按中国时间判断。今天是 {today}（{weekday}）。

【先读这些（按顺序）】
1. state/current.md —— **当前状态的唯一事实来源**（覆盖表、最近证据、帮助史、卡点、可数事实）
2. plan/today-{today}.md —— 当天时间窗与清单（人工安排的权威；若不存在见下）
3. learning/curriculum-coverage.md —— 课程范围与证据对账（未登记目标/无题/无独立证据；目录未核全则覆盖未知）
4. plan/schedule.md —— 复习与再测的**日期化**排期（含「未来才开放、不得提前安排」的项）
5. .tutor/core/protocol.md —— 当前协议；learning/README.md 在入账或核对帮助史时按需读
6. .tutor/config/teaching-conventions.md —— 教学约定（三种模式、批改、讲解范围）
7. tools/observations.py --list —— 待处理学习者反馈；历史系统问题仅在维护时读

【当前状态（引用 state/current.md 的汇总）】
{subject_line}

{next_line}

{note_line}

【今天清单】
{today_line}

【回来先做什么】
{next_steps}

【规则提醒】
- 默认教学式：先让我短暂独立尝试 → 卡住给最小提示 → 收尾用无提示新题检查
- **讲「为什么」要带上下文**：不要只给结论口诀
- **课件原文与教学归纳分开标**：教学归纳请标 `[教学归纳，非课件原文]`
- 批改三层：**看见了什么** → **可能是什么原因**（假设）→ **怎样确认**（一个短问题或一步计算）
  ⚠ 不要把简短回答扩写成具体机制；⚠ 手写读不准标 `[待确认]` 问我，**不得据此改判**
- **作答默认闭卷**：用户会特别说明开卷，不逐题重复追问；未知帮助史不能由照片推断
- 曝光与提示**只能由会话记录或我确认**，不得由作业照片推断；依据不足用 `unknown`（unknown 阻断升级）
- **两条会话线可能并发写同一套文件**：入账一律用 `python -B tools/append_attempt.py --event-id auto`
  （锁内取号，不再靠人读文本预留 attempt-N）；收尾一律跑 `python -B tools/session-close.py --today <中国日期>`
- 公式用纯 Unicode（ẋ ẍ ½ ² √ Σ ∂ ≠ ⟹ Ω θ），**不用 $...$**（实测显示为字面美元符号）
```

---

## 仍需学习者确认的

{open_questions}

## 相关文件

| 用途 | 文件 |
|---|---|
| **当前状态（唯一事实源）** | `state/current.md` |
| 课程覆盖台账 | `learning/coverage.md` |
| 复习/再测排期 | `plan/schedule.md` |
| 当天清单（人工权威） | `plan/today-{today}.md` |
| 答题与订正事实源 | `learning/attempts.jsonl` · `learning/corrections.jsonl` |
| 订正人读视图 | `learning/attempts/corrections.md` |
| 缺口台账 | `plan/gaps.md` |
| 系统问题清单 | `ISSUES-待改进.md` |
| 人工意图（叙述行唯一来源） | `.tutor/config/status-narrative.yml` |
| 历史交接（勿用） | `plan/handoff-prompt-2026-09-28.md` |
"""


def narrative(root: Path) -> dict[str, str]:
    path = root / ".tutor" / "config" / "status-narrative.yml"
    if not path.is_file():
        return {}
    text=path.read_text(encoding='utf-8')
    try:
        raw = parse_yaml(text)
    except ValueError:
        # The original workspace used four single-line Markdown values, not full YAML.
        # Keep that one legacy format readable without weakening structural YAML elsewhere.
        raw={}
        for line in text.splitlines():
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            key,separator,value=line.partition(':')
            if not separator or key not in NARRATIVE_KEYS or key in raw:
                raise ValueError('Invalid or duplicate legacy narrative field')
            raw[key]=value.strip()
    return {k: str(v).strip() for k, v in raw.items() if k in NARRATIVE_KEYS} if isinstance(raw, dict) else {}


def today_items(root: Path, today: str) -> tuple[str, list[str]]:
    """当天清单：文件存在就引用它（权威）；不存在就显式说"尚未建立"，不编造。"""
    path = root / "plan" / f"today-{today}.md"
    if path.is_file():
        return (
            f"**`plan/today-{today}.md` 已存在** —— 当天时间窗与清单以它为准（人工安排，不经脚本生成）。",
            [],
        )
    return (
        f"⚠ **`plan/today-{today}.md` 尚未建立** —— 本轮没有人安排过今天；"
        f"请先按下面的「回来先做什么」+ `plan/schedule.md` 的到期项，与学习者确认后再建。**不要凭空补一份。**",
        [],
    )


def next_steps(root: Path, today: str, narr: dict[str, str]) -> str:
    """下一步：以叙述行的 `next` 行文字为准（人工判断），并附机械候选供核对。"""
    lines: list[str] = []
    next_line = narr.get("next", "").strip()
    if next_line:
        lines.append("**人工指定的下一步（权威）** —— 见上方 `next:` 行；要点摘录：")
        lines.append("")
        # 把 ①②③ 之类的编号项拆成条目，便于阅读（不改变原文）
        for chunk in next_line.replace("；", "\n").split("\n"):
            chunk = chunk.strip()
            if chunk:
                lines.append(f"- {chunk}")
        lines.append("")
    else:
        lines.append("⚠ 叙述行没有 `next`（人工下一步缺失）——请补 `.tutor/config/status-narrative.yml` 的 `next` 行。")
        lines.append("")
    lines.append("**机械候选（来自 `plan/schedule.md`，仅供核对，不等于安排）**：")
    lines.append("")
    try:
        from reviews import all_review_items
        from timebase import days_between

        items = all_review_items(root, today)
        due = [i for i in items if days_between(today, i["due"]) <= 0]
        if due:
            for i, item in enumerate(due[:6], 1):
                lines.append(f"{i}. `{item['id']}`（{item['queue']}｜{item['kind']}）— {item['note']}")
        else:
            lines.append("（无到期项）")
        upcoming = [i for i in items if days_between(today, i["due"]) > 0]
        if upcoming:
            lines.append("")
            lines.append(f"未来才开放（**不得提前做**）{len(upcoming)} 条，最早一条 = "
                         f"`{upcoming[0]['id']}` @ {upcoming[0]['due']}（{upcoming[0]['note']}）。")
    except Exception as exc:  # noqa: BLE001
        lines.append(f"（排期扫描失败：{exc}）")
    return "\n".join(lines)


def open_questions(root: Path) -> str:
    """待确认清单：从叙述行的 note 里抽 `[待确认]`，加上"没有题目的目标"与"未解决困难"。"""
    import json

    bullets: list[str] = []
    narr = narrative(root)
    note = narr.get("note", "")
    if "[待确认]" in note or "待确认" in note:
        bullets.append("叙述行 `note` 里标了 `[待确认]` 的事项（见 AGENTS.md 的 STATUS，逐条列出）。")
    state_path = root / "learning" / "learner-state.json"
    if state_path.is_file():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        no_task = state["summary"].get("targets_without_tasks") or []
        if no_task:
            bullets.append(
                "**已声明但没有任何题目的考点**：" + "、".join(f"`{t}`" for t in no_task)
                + " —— 要不要出题、什么时候出，需要你指定（系统不自动建题）。"
            )
    hurdles_path = root / "learning" / "hurdles.jsonl"
    if hurdles_path.is_file():
        open_h = []
        for line in hurdles_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            if data.get("status") in ("open", "teaching", "awaiting_retest"):
                open_h.append(f"`{data.get('hurdle_id')}`（{data.get('status')}）")
        if open_h:
            bullets.append("**未解决困难**：" + "、".join(open_h) + " —— 处置方式（补讲/补练/再测）需要你确认。")
    bullets.append("**并发写约定**（ISSUES D4 已由本轮实现落地：锁 + 机器取号 + 原子写；若你另有偏好请说明）。")
    return "\n".join(f"- {b}" for b in bullets) if bullets else "- （暂无）"


WEEKDAY_CN = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def build(root: Path, today: str) -> str:
    import datetime as dt

    narr = narrative(root)
    weekday = WEEKDAY_CN[dt.date.fromisoformat(today).weekday()]
    today_line, _ = today_items(root, today)
    return TEMPLATE.format(
        today=today,
        uk=uk_date_now(),
        weekday=weekday,
        subject_line="**当前课程/主线**：" + (narr.get("current_subject") or "（叙述行未填 `current_subject`）"),
        next_line="**最近一次收尾**：" + (narr.get("current_topic") or "（叙述行未填 `current_topic`）"),
        note_line="**必须遵守的提醒**：" + (narr.get("note") or "（叙述行未填 `note`）"),
        today_line=today_line,
        next_steps=next_steps(root, today, narr),
        open_questions=open_questions(root),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate plan/handoff-CURRENT.md from live facts.")
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
    out = Path(args.out) if args.out else root / "plan" / "handoff-CURRENT.md"
    try:
        with WorkspaceLock(root / "plan", label="handoff"):
            atomic_write_text(out, text)
    except LockTimeout as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 4
    print(f"wrote {out}")
    print("- 动态部分全部引用 state/current.md；人工意图取自 .tutor/config/status-narrative.yml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
