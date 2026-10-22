# -*- coding: utf-8 -*-
"""Extract per-page text but keep only lines that carry Chinese wording (drop scrambled glyph rows)."""
import re

import fitz

PDF = r"subjects\04-数学物理方法1\课件\第五章+傅里叶变换+-+上传课件.pdf"
CJK = re.compile(r"[\u4e00-\u9fff]")

doc = fitz.open(PDF)
out = []
for i, page in enumerate(doc, start=1):
    out.append("\n===== p%d =====" % i)
    for line in page.get_text().splitlines():
        s = line.strip()
        if s and CJK.search(s):
            out.append(s)
doc.close()

with open(r"tmp\lec-fourier\cn_only.txt", "w", encoding="utf-8") as fh:
    fh.write("\n".join(out))
print("lines:", len(out))
