# -*- coding: utf-8 -*-
import os
p = os.path.join('subjects', '03-微分方程', '讲义',
                 'ODE-期中之后-完整讲义-L13-L23-20261118.tex')
s = open(p, encoding='utf-8').read()
a = s.index(r'\hdr{§13}{名词中英对照')
b = s.index(r'\hdr{附录 A}{全部题目详解')
gloss = s[a:b]
rows = [l for l in gloss.split('\n') if l.count(' & ') == 3 and l.rstrip().endswith('\\\\')]
hdr = [l for l in rows if '\\thead' in l]
body = [l for l in rows if '\\thead' not in l]
print('表头行', len(hdr), '词表行', len(body), '词条', len(body) * 2)
