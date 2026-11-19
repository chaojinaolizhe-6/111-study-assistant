# -*- coding: utf-8 -*-
import os, sys
p = os.path.join('subjects', '03-微分方程', '讲义', 'INDEX.md')
s = open(p, encoding='utf-8').read()
pairs = [
    ('第 6 章正文 71 处专业名词在首次出现处补', '第 6 章正文与附录详解共 71 处专业名词在首次出现处补'),
    ('三张四栏表（共 76 词，', '三张四栏表（34 行、共 68 词，'),
]
for a, b in pairs:
    n = s.count(a)
    print('count=%d %s' % (n, a[:30]))
    if n != 1:
        sys.exit(2)
for a, b in pairs:
    s = s.replace(a, b, 1)
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
