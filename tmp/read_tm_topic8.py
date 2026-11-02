# -*- coding: utf-8 -*-
import fitz, pathlib, sys

p = pathlib.Path(r"subjects\01-理论力学\课件\TM2026-Topic8-P1.pdf")
doc = fitz.open(str(p))
print("pages:", doc.page_count)
for i in range(doc.page_count):
    t = doc[i].get_text().strip()
    print("\n" + "=" * 30, "PAGE", i + 1, "len", len(t), "=" * 30)
    print(t[:2000] if t else "[NO TEXT LAYER]")
    imgs = doc[i].get_images(full=True)
    print("[images on page:", len(imgs), "]")
