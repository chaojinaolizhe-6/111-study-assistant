# -*- coding: utf-8 -*-
import fitz, os
pdf = r'subjects/03-微分方程/讲义/ODE-期中之后-完整讲义-L13-L23-20261118.pdf'
d = fitz.open(pdf)
targets = {
    'BRIDGE': '第一近似系统（',
    'NOTE132': 'unperturbed solution 与',
    'SADDLE': '（2）鞍点（saddle point）',
    'LYAP2': 'Lyapunov',
    'G33NOTE': 'not-exist-xyz',
}
res = {}
for i, p in enumerate(d):
    t = p.get_text()
    for k, v in targets.items():
        if v in t and k not in res:
            res[k] = i + 1
lines = ['%s -> %s' % (k, v) for k, v in res.items()]
open(r'tmp/ode-ch6-en/pages.txt', 'w', encoding='utf-8').write('\n'.join(lines))
print('ok')
