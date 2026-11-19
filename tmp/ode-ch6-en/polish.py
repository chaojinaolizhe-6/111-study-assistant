# -*- coding: utf-8 -*-
import os, sys

p = os.path.join('subjects', '03-微分方程', '讲义',
                 'ODE-期中之后-完整讲义-L13-L23-20261118.tex')
s = open(p, encoding='utf-8').read()

pairs = [
    # 鞍点全称与课件一致
    (r'\subhdr{（2）鞍点（saddle）}',
     r'\subhdr{（2）鞍点（saddle point）}'),
    # 定理 7.1 与定理 6.1 的英文写法对齐
    (r'\textbf{定理 7.1（李雅普诺夫第二方法）}',
     "\\textbf{定理 7.1（李雅普诺夫第二方法，Lyapunov's second method）}"),
    # 邻域首次出现处标注（定理 6.2 是唯一带"某邻域"的定理表述）
    (r'则在 $\mathbf{0}$ 的某个邻域内，非线性系统 (6.3) 的相图',
     r'则在 $\mathbf{0}$ 的某个邻域（\EN{neighborhood}）内，非线性系统 (6.3) 的相图'),
    # 13.2 表后补一句：未扰解/受扰解是课件用语
    (r'\subhdr{13.3 矩阵与判据}',
     '{\\small\\color{inkgray}末两行的\\EN{unperturbed solution}与\\EN{perturbed solution}是课件定义稳定性时的用语'
     '（要研究的那个解叫未扰解，从附近初值出发的解叫受扰解）；本书 §4.2 直接用 $\\X^{*}$ 与 $\\X(t)$ 写，'
     '没有引入这两个词，认词即可。\\par}\n\n'
     r'\subhdr{13.3 矩阵与判据}'),
]

bad = False
for a, b in pairs:
    n = s.count(a)
    print('count=%d  %s' % (n, a[:50]))
    if n != 1:
        bad = True
if bad:
    sys.exit(2)

for a, b in pairs:
    s = s.replace(a, b, 1)

open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('written')
