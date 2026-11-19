# -*- coding: utf-8 -*-
import fitz, os
pdf = r'subjects/03-微分方程/讲义/ODE-期中之后-完整讲义-L13-L23-20261118.pdf'
d = fitz.open(pdf)
os.makedirs(r'tmp/ode-ch6-en/png2', exist_ok=True)
for i, p in enumerate(d):
    t = p.get_text()
    if "Lyapunov\u2019s second method" in t or "Lyapunov's second method" in t:
        p.get_pixmap(dpi=130).save(r'tmp/ode-ch6-en/png2/p%d.png' % (i + 1))
        print('hit', i + 1)
