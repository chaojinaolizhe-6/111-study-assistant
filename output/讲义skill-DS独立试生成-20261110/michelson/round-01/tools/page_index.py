# -*- coding: utf-8 -*-
"""生成 source-map.json 用的页码索引：在 handout.pdf 中按行定位各节、各图、各题所在页。"""
import json
import re
import sys
from pathlib import Path

import fitz

PDF = Path(__file__).resolve().parents[1] / "handout.pdf"

PATTERNS = {
    "§1": r"实验目的与仪器：中英对照$",
    "§2": r"原理：分振幅、等效空气膜与光程差$",
    "§3": r"教学小例：膜厚、角度与条纹计数$",
    "§4": r"预习问答节选（中英对照）$",
    "§5": r"覆盖台账、源资料问题与未覆盖项$",
    "图1": r"^图1$",
    "图2": r"^图2$",
    "图3": r"^图3$",
    "图4": r"^图4$",
    "图A1": r"^图A1$",
    "II-1": r"^II-1$",
    "II-2": r"^II-2$",
    "II-3": r"^II-3$",
    "II-6": r"^II-6$",
    "II-7": r"^II-7$",
    "II-8": r"^II-8$",
    "II-9": r"^II-9$",
    "附加(1)": r"^附加\s?\(1\)$",
    "附加(2)": r"^附加\s?\(2\)$",
}


def lines_of(page):
    out = []
    for block in page.get_text("dict")["blocks"]:
        if block.get("type") != 0:
            continue
        for ln in block["lines"]:
            t = "".join(s["text"] for s in ln["spans"]).strip()
            if t:
                out.append(t)
    return out


def main() -> int:
    doc = fitz.open(PDF)
    pages = {}
    for name, pat in PATTERNS.items():
        pages[name] = None
        for p in range(1, doc.page_count + 1):
            if any(re.search(pat, t) for t in lines_of(doc[p - 1])):
                pages[name] = p
                break
    print(json.dumps(pages, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
