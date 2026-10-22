# -*- coding: utf-8 -*-
import os
import fitz

pdf_path = r"subjects\04-数学物理方法1\课件\第六章+拉普拉斯变换+-+上传课件.pdf"
out_dir = r"tmp\lec-lap\zoom"
os.makedirs(out_dir, exist_ok=True)
doc = fitz.open(pdf_path)
zoom = 320.0 / 72.0
mat = fitz.Matrix(zoom, zoom)
for pno in (22, 24, 19):
    page = doc[pno - 1]
    pix = page.get_pixmap(matrix=mat, alpha=False)
    name = os.path.join(out_dir, "z%02d.png" % pno)
    pix.save(name)
    print(pno, pix.width, pix.height)
doc.close()
