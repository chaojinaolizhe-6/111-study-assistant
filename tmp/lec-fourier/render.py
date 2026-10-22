# -*- coding: utf-8 -*-
"""Render every page of the Fourier-transform lecture PDF to PNG at dpi=110."""
import os
import sys

import fitz

PDF = r"subjects\04-数学物理方法1\课件\第五章+傅里叶变换+-+上传课件.pdf"
OUT = os.path.join("tmp", "lec-fourier", "png")
DPI = 110


def main() -> int:
    doc = fitz.open(PDF)
    print("pages:", doc.page_count)
    os.makedirs(OUT, exist_ok=True)
    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(dpi=DPI)
        name = "p%02d.png" % i
        path = os.path.join(OUT, name)
        pix.save(path)
        print(name, pix.width, "x", pix.height, os.path.getsize(path))
    doc.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
