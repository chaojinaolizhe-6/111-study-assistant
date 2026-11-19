# -*- coding: utf-8 -*-
"""核对 §13 表里的英文是否都在正文注过一次。"""
import re, os

p = os.path.join('subjects', '03-微分方程', '讲义',
                 'ODE-期中之后-完整讲义-L13-L23-20261118.tex')
s = open(p, encoding='utf-8').read()

start = s.index(r'\hdr{§13}{名词中英对照（考前查用）}')
end = s.index(r'\hdr{附录 A}{全部题目详解')
gloss = s[start:end]
body = s[:start]

terms = re.findall(r'\\EN\{([^}]*)\}', gloss)
seen = []
for t in terms:
    if t not in seen:
        seen.append(t)

only_gloss = []
for t in seen:
    n_body = body.count('\\EN{%s}' % t)
    if n_body == 0:
        only_gloss.append(t)

print('§13 里的英文条目：%d 条（去重 %d）' % (len(terms), len(seen)))
print('正文没有用 \\EN 标注过的：')
for t in only_gloss:
    print('   -', t)
