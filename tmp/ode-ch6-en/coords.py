# -*- coding: utf-8 -*-
import fitz
pdf = r'subjects/03-微分方程/讲义/ODE-期中之后-完整讲义-L13-L23-20261118.pdf'
d = fitz.open(pdf)
p = d[112]  # page 113
words = p.get_text('words')
rows = {}
for w in words:
    x0, y0, x1, y1, txt = w[0], w[1], w[2], w[3], w[4]
    if 150 < y0 < 420:
        rows.setdefault(round(y0, 1), []).append((round(x0, 1), txt))
for y in sorted(rows):
    print(y, rows[y])
