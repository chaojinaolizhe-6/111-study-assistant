# -*- coding: utf-8 -*-
import fitz, pathlib

src = pathlib.Path(r"subjects\01-理论力学\课件\TM2026-Topic8-P1.pdf")
out = pathlib.Path(r"tmp\tm8")
out.mkdir(parents=True, exist_ok=True)
doc = fitz.open(str(src))
for n in (16, 17, 18):
    page = doc[n - 1]
    pix = page.get_pixmap(dpi=150)
    p = out / f"p{n}.png"
    pix.save(str(p))
    print(p, pix.width, pix.height)
