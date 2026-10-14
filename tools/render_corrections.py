#!/usr/bin/env python3
"""从 learning/corrections.jsonl 生成 learning/attempts/corrections.md（人读视图）。

背景：旧做法是"事件不改不删，订正写 corrections.md"，但 corrections.md 是自由文本，
`validate_attempts` / `derive_state` / `plan-week` 都读不到它 —— 订正对能力判定实际上
零影响，同一件事留下两种状态。现在 `corrections.jsonl` 是唯一事实源，本脚本只负责
把它渲染成人读文档，**不再人工维护结论**。

用法:
  python -B tools/render_corrections.py [--root .]
"""
from __future__ import annotations

import argparse
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from learninglib import load_corrections  # noqa: E402

SHORT = 60


def short(value) -> str:
    if value is None:
        return "(无)"
    text = str(value)
    if len(text) <= SHORT:
        return text
    head = text[:SHORT].replace("|", "\\|")
    return f"{head}…（共 {len(text)} 字，全文见 corrections.jsonl）"


def render(root: Path) -> str:
    rows = [r for r in load_corrections(root) if r.get("data")]
    field_rows = [r["data"] for r in rows if r["data"].get("kind") != "narrative"]
    narrative_rows = [r["data"] for r in rows if r["data"].get("kind") == "narrative"]

    out: list[str] = []
    out.append("# 记录订正（Corrections Log）")
    out.append("")
    out.append("> ⚠ **本文件由 `python -B tools/render_corrections.py` 从 `learning/corrections.jsonl` 自动生成，请勿手工编辑。**")
    out.append(">")
    out.append("> `learning/corrections.jsonl` 是订正的**唯一事实源**。`tools/validate_attempts.py`、")
    out.append("> `tools/derive_state.py`、`tools/plan-week.py` 三处消费者统一：**先应用订正，再在应用订正后的记录上判定**。")
    out.append("> 原始事件 `learning/attempts.jsonl` 与手写照片只增不改、不删。")
    out.append("")

    out.append(f"## 字段订正（{len(field_rows)} 条，已进入判定链路）")
    out.append("")
    if not field_rows:
        out.append("（无）")
    else:
        by_event: dict[str, list[dict]] = {}
        for data in field_rows:
            by_event.setdefault(str(data.get("event_id")), []).append(data)
        for event_id in sorted(by_event, key=lambda e: (len(e), e)):
            items = by_event[event_id]
            out.append(f"### {event_id}")
            out.append("")
            out.append("| 范围 | 目标 | 字段 | 原值 | 修正值 | 来源 | 日期 |")
            out.append("|---|---|---|---|---|---|---|")
            for data in items:
                scope = "事件级" if data.get("scope") == "event" else "目标级"
                target = data.get("target_id") or "—"
                out.append(
                    "| {scope} | `{target}` | `{field}` | {old} | {new} | {source} | {at} |".format(
                        scope=scope,
                        target=target,
                        field=data.get("field"),
                        old=short(data.get("from")),
                        new=short(data.get("to")),
                        source=data.get("source", "?"),
                        at=data.get("at", "?"),
                    )
                )
            out.append("")
            out.append("**理由与证据**")
            out.append("")
            for data in items:
                target = data.get("target_id") or "(事件级)"
                out.append(f"- `{data.get('correction_id')}` / {target} / `{data.get('field')}`：{data.get('reason', '')}")
                out.append(f"  - 证据：{data.get('evidence_ref', '')}")
            out.append("")

    out.append(f"## 叙述与作废声明（{len(narrative_rows)} 条，不改字段、仅供阅读）")
    out.append("")
    if not narrative_rows:
        out.append("（无）")
    else:
        for data in sorted(narrative_rows, key=lambda d: str(d.get("at", ""))):
            out.append(f"### {data.get('at', '?')} — {data.get('correction_id')}")
            out.append("")
            out.append(str(data.get("text", "")))
            out.append("")

    out.append("---")
    out.append("")
    out.append("生成命令：`python -B tools/render_corrections.py`")
    out.append("")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render learning/attempts/corrections.md from corrections.jsonl.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--check", action="store_true", help="只检查是否已是最新，不写文件")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    out_path = root / "learning" / "attempts" / "corrections.md"
    text = render(root)
    if args.check:
        current = out_path.read_text(encoding="utf-8") if out_path.is_file() else ""
        if current == text:
            print(f"OK: {out_path.relative_to(root)} 已是最新")
            return 0
        print(f"STALE: {out_path.relative_to(root)} 与 corrections.jsonl 不一致（跑 render_corrections.py 重新生成）")
        return 1
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    print(f"wrote {out_path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
