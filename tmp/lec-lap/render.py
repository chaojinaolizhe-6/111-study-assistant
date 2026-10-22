# -*- coding: utf-8 -*-
import os
import fitz

pdf_path = r"subjects\04-数学物理方法1\课件\第六章+拉普拉斯变换+-+上传课件.pdf"
out_dir = r"tmp\lec-lap\png"
os.makedirs(out_dir, exist_ok=True)

doc = fitz.open(pdf_path)
print("pages:", doc.page_count)

zoom = 110.0 / 72.0
mat = fitz.Matrix(zoom, zoom)

for i, page in enumerate(doc, start=1):
    pix = page.get_pixmap(matrix=mat, alpha=False)
    name = os.path.join(out_dir, "p%02d.png" % i)
    pix.save(name)
    print(i, pix.width, pix.height, os.path.getsize(name))

doc.close()
print("DONE")
