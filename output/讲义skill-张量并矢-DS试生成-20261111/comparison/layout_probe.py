# -*- coding: utf-8 -*-
"""Print a page-by-page layout summary of comparison.pdf (text-layer only)."""
import fitz
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
doc = fitz.open(os.path.join(HERE, "comparison.pdf"))
print("pages:", doc.page_count)
for i, pg in enumerate(doc):
    blocks = [b for b in pg.get_text("blocks") if b[6] == 0 and b[4].strip("\x00\r\n ")]
    text = pg.get_text().replace("\x00", "")
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    ymax = max((b[3] for b in blocks), default=0)
    ymin = min((b[1] for b in blocks), default=0)
    imgs = pg.get_images(full=True)
    iboxes = []
    for info in imgs:
        for r in pg.get_image_rects(info[0]):
            if r.width > 100:
                iboxes.append(r)
    ih = sum(r.height for r in iboxes)
    print(f"p{i+1:02d}: text y {ymin:.0f}..{ymax:.0f}, imgs={len(iboxes)} (h={ih:.0f}), "
          f"first={lines[1][:32] if len(lines)>1 else ''!r} last={lines[-2][:32] if len(lines)>2 else ''!r}")
    # headings on the page
    heads = [l for l in lines if re.match(r"^(一|二|三|A|B|C|D|E|F|G|附录)", l) and len(l) < 40]
    if heads:
        print("      heads:", " | ".join(heads[:4]))
