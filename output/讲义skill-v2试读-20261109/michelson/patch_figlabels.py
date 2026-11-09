from pathlib import Path
p=Path(r'output/讲义skill-v2试读-20261109/michelson/michelson-excerpt-v2.tex')
t=p.read_text(encoding='utf-8')
# Figure 1 theta label
old='\\node at (0.38,1.22) {$\\theta$};'
new='\\node at (0.18,1.38) {$\\theta$};'
assert old in t; t=t.replace(old,new,1)
# Figure 1 C label
old='\\fill (C) circle (1.5pt) node[above right] {$C$};'
new='\\fill (C) circle (1.5pt) node[below right] {$C$};'
assert old in t; t=t.replace(old,new,1)
# Figure 1 projection label shift up slightly
old='\\node[right,smalllab,align=left] at (0.78,2.50) {投影段 $AD$\\\\$=2d\\tan\\theta\\sin\\theta$};'
new='\\node[right,smalllab,align=left] at (0.80,2.56) {投影段 $AD$\\\\$=2d\\tan\\theta\\sin\\theta$};'
if old in t: t=t.replace(old,new,1)
else: print('projection label not found')
# Figure 3 M1 label below left
old='\\node[left] at (1.15,2.2) {$M_1$};'
new='\\node[below left] at (1.18,2.2) {$M_1$};'
assert old in t; t=t.replace(old,new,1)
p.write_text(t,encoding='utf-8')
print('ok')
