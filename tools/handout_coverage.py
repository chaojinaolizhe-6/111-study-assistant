#!/usr/bin/env python3
"""讲义台账：扫 `subjects/*/讲义/` 里的 PDF，生成 `learning/handout-coverage.md`。

为什么要有这个文件（2026-10-29）：
学习者把学习方式改成"讲义驱动"后，讲义成了讲授的唯一通道，但 `subjects/*/progress.md`
的三态表（未讲 / 已讲 / 已测）里没有"讲义已交付"这一维，于是出现两处失真：
  - 讲义已覆盖的章节，三态表仍标"未讲"→ 助手可能重复从零讲；
  - 讲义数量暴涨，但没有任何一处能回答"哪几门课已经有讲义、最近一份是什么时候"。

本脚本只做**事实登记**，不做覆盖判断（文件名与章次的对应关系不足以自动判定覆盖）：
它输出每门课的讲义清单、份数、日期区间，并把"讲义已交付"与"已讲/已学/已测"明确分开。
覆盖对账仍由 `subjects/*/progress.md` 与人工判断负责。

用法：
    python -B tools/handout_coverage.py            # 写 learning/handout-coverage.md
    python -B tools/handout_coverage.py --check     # 只打印摘要，不写文件
"""
from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

DATE_RE = re.compile(r"(20\d{6})")
STAMP_RE = re.compile(r"20\d{6}")


def collect(root: Path) -> dict[str, list[dict]]:
    by_course: dict[str, list[dict]] = {}
    for path in sorted((root / "subjects").glob("*/讲义/*.pdf")):
        course = path.parent.parent.name
        match = DATE_RE.search(path.name)
        stamp = match.group(1) if match else ""
        date = f"{stamp[:4]}-{stamp[4:6]}-{stamp[6:]}" if stamp else ""
        title = STAMP_RE.sub("", path.stem).strip("-_ ")
        by_course.setdefault(course, []).append(
            {
                "title": title or path.stem,
                "date": date or "（文件名无日期）",
                "file": path.relative_to(root).as_posix(),
                "mtime": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d"),
            }
        )
    for rows in by_course.values():
        rows.sort(key=lambda r: (r["date"], r["title"]), reverse=True)
    return by_course


def render(by_course: dict[str, list[dict]], root: Path) -> str:
    total = sum(len(v) for v in by_course.values())
    all_dates = sorted(r["date"] for v in by_course.values() for r in v if r["date"].startswith("20"))
    lines = [
        "# 讲义台账（handout-coverage.md）",
        "",
        "> **本文件由 `python -B tools/handout_coverage.py` 生成，勿手工编辑。**",
        f"> 生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}；讲义合计 **{total}** 份，"
        f"日期区间 {all_dates[0] if all_dates else '—'} ~ {all_dates[-1] if all_dates else '—'}。",
        "",
        "## 口径（先读这三行）",
        "",
        "1. **讲义已交付 ≠ 已讲 ≠ 已学 ≠ 已验收。** 本表只证明「这门课有这份材料」，不证明学习者掌握。",
        "2. 当前学习模式为**讲义驱动、考前集中验收**（`.tutor/config/study-mode.yml`）——"
        "在验收发生之前，`state/current.md` 的能力数字不会因为这些讲义而上升。",
        "3. 覆盖判断（哪一节已被讲义覆盖）仍以 `subjects/*/progress.md` 三态表为准；"
        "本表只做清单与对账入口，**不从文件名推断覆盖**。",
        "",
        "## 按课程",
        "",
        "| 课程 | 讲义份数 | 最近一份 |",
        "|---|---|---|",
    ]
    for course in sorted(by_course):
        rows = by_course[course]
        lines.append(f"| {course} | {len(rows)} | {rows[0]['date']} |")

    lines += ["", "## 清单（按课程、日期倒序）", ""]
    for course in sorted(by_course):
        lines.append(f"### {course}（{len(by_course[course])} 份）")
        lines.append("")
        lines.append("| 日期 | 讲义 | 文件 |")
        lines.append("|---|---|---|")
        for row in by_course[course]:
            lines.append(f"| {row['date']} | {row['title']} | `{row['file']}` |")
        lines.append("")

    lines += [
        "## 缺口（没有讲义的课程）",
        "",
    ]
    subjects_dir = root / "subjects"
    missing = [
        p.name
        for p in sorted(subjects_dir.glob("*"))
        if p.is_dir() and p.name not in by_course
    ]
    if subjects_dir.is_dir():
        lines.append("下列课程目录里还没有讲义 PDF（不代表没学，只代表没有可自学的讲义）：")
        lines.append("")
        if missing:
            lines.extend(f"- {name}" for name in missing)
        else:
            lines.append("- 无（每门课都至少有一份讲义）")
    else:
        lines.append("- 未找到 subjects 目录（请在工作区根目录运行）")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--check", action="store_true", help="只打印摘要，不写文件")
    parser.add_argument("--out", default="learning/handout-coverage.md")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    by_course = collect(root)
    total = sum(len(v) for v in by_course.values())
    print(f"[handout] {len(by_course)} 门课，讲义 {total} 份")
    for course in sorted(by_course):
        rows = by_course[course]
        print(f"  - {course}: {len(rows)} 份，最近 {rows[0]['date']}")
    if args.check:
        return 0

    out = root / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(by_course, root), encoding="utf-8")
    print(f"[handout] 写入 {out.relative_to(root).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
