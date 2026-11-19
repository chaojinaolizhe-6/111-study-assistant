# -*- coding: utf-8 -*-
import os, re
p = os.path.join('subjects', '03-微分方程', '讲义',
                 'ODE-期中之后-完整讲义-L13-L23-20261118.tex')
s = open(p, encoding='utf-8').read()
i13 = s.index(r'\hdr{§13}{名词中英对照')
gloss = s[i13:]
rows = [l for l in gloss.split('\n') if l.count(' & ') == 3 and l.rstrip().endswith('\\\\')]
print('词表行数', len(rows), '=> 词条', len(rows) * 2)
for l in rows[:2]:
    print(l[:60])
