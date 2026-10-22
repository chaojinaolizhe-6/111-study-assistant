# -*- coding: utf-8 -*-
"""把生成的 PDF 逐页渲染成 PNG，便于目视检查版式。"""
import sys
from pathlib import Path
import fitz

base = Path(__file__).resolve().parent
pdf = base / "大工学生医保办理指南.pdf"
doc = fitz.open(pdf)
print("pages:", doc.page_count)
print("size(mm):", round(doc[0].rect.width / 72 * 25.4, 1), "x", round(doc[0].rect.height / 72 * 25.4, 1))

out = base / "preview"
out.mkdir(exist_ok=True)
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=110)
    p = out / f"p{i + 1}.png"
    pix.save(p)
    print(p.name, pix.width, "x", pix.height)
doc.close()
