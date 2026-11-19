# -*- coding: utf-8 -*-
p = r'subjects/03-微分方程/讲义/ODE-期中之后-完整讲义-L13-L23-20261118.tex'
s = open(p, encoding='utf-8').read()
old = '本书正文写作不稳定结点稳定结点，同义。'
new = '本书正文写作“不稳定结点”“稳定结点”，同义。'
print('count', s.count(old))
s = s.replace(old, new, 1)
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
