# -*- coding: utf-8 -*-
"""Crop a region of a rendered page and upscale it, for reading small symbols."""
import sys

import fitz

# usage: zoom.py <page> <x0> <y0> <x1> <y1> <zoom>
page_no = int(sys.argv[1])
x0, y0, x1, y1 = (float(v) for v in sys.argv[2:6])
zoom = float(sys.argv[6]) if len(sys.argv) > 6 else 4.0

PDF = r"subjects\04-数学物理方法1\课件\第五章+傅里叶变换+-+上传课件.pdf"
doc = fitz.open(PDF)
page = doc[page_no - 1]
clip = fitz.Rect(x0, y0, x1, y1)
pix = page.get_pixmap(clip=clip, matrix=fitz.Matrix(zoom, zoom))
out = r"tmp\lec-fourier\crop.png"
pix.save(out)
print(out, pix.width, "x", pix.height)
doc.close()
