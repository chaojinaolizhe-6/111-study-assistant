# -*- coding: utf-8 -*-
import difflib, os

a = open(os.path.join('tmp', 'ode-ch6-en', 'before.tex'), encoding='utf-8').read().split('\n')
b = open(os.path.join('subjects', '03-微分方程', '讲义',
                      'ODE-期中之后-完整讲义-L13-L23-20261118.tex'), encoding='utf-8').read().split('\n')

out = []
for line in difflib.unified_diff(a, b, 'before', 'after', n=0, lineterm=''):
    out.append(line)

open(os.path.join('tmp', 'ode-ch6-en', 'diff.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('diff lines', len(out))

# 统计
add = [l for l in out if l.startswith('+') and not l.startswith('+++')]
rem = [l for l in out if l.startswith('-') and not l.startswith('---')]
print('added', len(add), 'removed', len(rem))
print('EN 宏出现次数', sum(l.count('\\EN{') for l in b))
