# -*- coding: utf-8 -*-
"""Compare structural markers across rounds 1-4 to attribute changes honestly."""
import fitz, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

MARKERS = [
    "六个动作", "矢量、基与分量", "求和约定", "六个排列", "选读",
    "最短主线", "最短路径", "等角方向", "体对角线", "续解", "答案详解",
    "线性泛函", "度规", "瞬时轴", "准静态", "偏斜", "单位并矢与投影并矢",
]

def pages_of(doc, needle):
    out = []
    for i, pg in enumerate(doc):
        t = pg.get_text().replace("\x00", "")
        if needle in t:
            out.append(i + 1)
    return out

for r in ["round-01", "round-02", "round-03", "round-04"]:
    p = os.path.join(ROOT, r, "handout.pdf")
    doc = fitz.open(p)
    print(f"--- {r}: {doc.page_count} pages")
    for m in MARKERS:
        ps = pages_of(doc, m)
        if ps:
            print(f"   {m}: {ps[:8]}{'...' if len(ps) > 8 else ''}")
