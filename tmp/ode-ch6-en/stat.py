# -*- coding: utf-8 -*-
import os, re
p = os.path.join('subjects', '03-微分方程', '讲义',
                 'ODE-期中之后-完整讲义-L13-L23-20261118.tex')
s = open(p, encoding='utf-8').read()
i13 = s.index(r'\hdr{§13}{名词中英对照')
body, gloss = s[:i13], s[i13:]
print('全文 \\EN 次数', len(re.findall(r'\\EN\{', s)))
print('正文（§0–§12 + 附录）\\EN 次数', len(re.findall(r'\\EN\{', body)))
print('§13 内 \\EN 次数', len(re.findall(r'\\EN\{', gloss)))
print('总行数', s.count('\n') + 1)
