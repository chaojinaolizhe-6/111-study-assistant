# -*- coding: utf-8 -*-
"""诊断：量出实际文本区边界、每页首末行、图注与题号所在页，用于校准版面检查阈值。"""
import sys
from pathlib import Path

import fitz

PDF = Path(__file__).resolve().parents[1] / "handout.pdf"


def main() -> int:
    doc = fitz.open(PDF)
    p0 = doc[0].rect
    print(f"页面 {p0.width:.2f} x {p0.height:.2f} pt")
    for i in range(1, doc.page_count + 1):
        page = doc[i - 1]
        lines = []
        for block in page.get_text("dict")["blocks"]:
            if block.get("type") != 0:
                continue
            for ln in block["lines"]:
                txt = "".join(s["text"] for s in ln["spans"]).strip()
                if txt:
                    lines.append((ln["bbox"], txt))
        if not lines:
            continue
        x0 = min(b[0] for b, _ in lines)
        x1 = max(b[2] for b, _ in lines)
        body = [(b, t) for b, t in lines if 60 < b[1] < 780]
        by0 = min(b[1] for b, _ in body) if body else float("nan")
        by1 = max(b[3] for b, _ in body) if body else float("nan")
        print(f"p{i:2d} 行数 {len(lines):3d} x=[{x0:.1f},{x1:.1f}] 正文 y=[{by0:.1f},{by1:.1f}]")
    # 校准：取正文最靠边的一行
    print("\n--- 最靠左/右的行 ---")
    worst_l, worst_r = [], []
    for i in range(1, doc.page_count + 1):
        for block in doc[i - 1].get_text("dict")["blocks"]:
            if block.get("type") != 0:
                continue
            for ln in block["lines"]:
                txt = "".join(s["text"] for s in ln["spans"]).strip()
                if txt:
                    worst_l.append((ln["bbox"][0], i, txt[:30]))
                    worst_r.append((ln["bbox"][2], i, txt[-30:]))
    worst_l.sort(); worst_r.sort(reverse=True)
    for x, p, t in worst_l[:5]:
        print(f"  左 {x:.1f} p{p} {t!r}")
    for x, p, t in worst_r[:5]:
        print(f"  右 {x:.1f} p{p} {t!r}")
    print("\n--- 图注/题号所在页 ---")
    for key in ("图 1", "图 2", "图 3", "图 4", "图 A1", "II-1", "II-2", "II-3", "II-6",
                "II-7", "II-8", "II-9", "附加 (1)", "附加 (2)", "Answer (English)"):
        pages = [i for i in range(1, doc.page_count + 1) if key in doc[i - 1].get_text()]
        print(f"  {key!r}: {pages}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
