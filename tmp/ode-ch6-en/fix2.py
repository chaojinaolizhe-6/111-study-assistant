# -*- coding: utf-8 -*-
import os, sys

p = os.path.join('subjects', '03-微分方程', '讲义',
                 'ODE-期中之后-完整讲义-L13-L23-20261118.tex')
s = open(p, encoding='utf-8').read()

pairs = [
    ('{\\small\\color{inkgray}末两行的\\EN{unperturbed solution}',
     '{\\small\\color{inkgray}最后一行的\\EN{unperturbed solution}'),
    (r'\subhdr{13.4 六组容易混的词}',
     '\\needspace{4\\baselineskip}\n' + r'\subhdr{13.4 六组容易混的词}'),
]
for a, b in pairs:
    n = s.count(a)
    print('count=%d  %s' % (n, a[:40]))
    if n != 1:
        sys.exit(2)
for a, b in pairs:
    s = s.replace(a, b, 1)

open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
