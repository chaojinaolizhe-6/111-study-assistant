# -*- coding: utf-8 -*-
"""Extract small text snippets from round-01 for provenance checks."""
import fitz, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
doc = fitz.open(os.path.join(ROOT, "round-01", "handout.pdf"))
needles = ["-e1 + e2", "e1 + e2", "最短主线", "六个动作", "前两块", "等角方向", "体对角线"]
for n in needles:
    pages = []
    for i, pg in enumerate(doc):
        if n in pg.get_text().replace("\x00", ""):
            pages.append(i + 1)
    print(n, pages)

print("=== round-01 p2 ===")
print(doc[1].get_text().replace("\x00", ""))
print("=== round-01 P1 appendix pages ===")
for i in [37, 38, 39]:
    print("--- p", i + 1)
    print(doc[i].get_text().replace("\x00", ""))
