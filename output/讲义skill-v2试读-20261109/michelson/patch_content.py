from pathlib import Path
p=Path(r'output/讲义skill-v2试读-20261109/michelson/michelson-excerpt-v2.tex')
t=p.read_text(encoding='utf-8')
t=t.replace('与鼓轮读数差差 20 倍','与鼓轮读数差 20:1',1)
# BE lens in figure 3
old='\\draw[ray] (-0.9,0) -- (1.9,0);\n% G1'
new='''\\draw[ray] (-0.9,0) -- (1.9,0);
% 扩束镜 BE
\\draw[thick] (0.55,-0.22) .. controls (0.67,0) .. (0.55,0.22);
\\draw[thick] (0.67,-0.22) .. controls (0.55,0) .. (0.67,0.22);
\\node[above,smalllab] at (0.61,0.25) {扩束镜};
% G1'''
assert old in t
t=t.replace(old,new,1)
# k0 integer approximation
old='从中心往外数第 \\(m\\) 个环（\\(m=1,2,\\dots\\)）对应 \\(k=k_0-m\\)。代入上式：'
new='从中心往外数第 \\(m\\) 个环（\\(m=1,2,\\dots\\)），在 \\(k_0=2d/\\lambda\\gg1\\) 时把 \\(k_0\\) 近似看成整数，对应 \\(k=k_0-m\\)。代入上式：'
assert old in t
t=t.replace(old,new,1)
# 2d << z condition and central order note
old='由几何，\\(S_2\'P-S_1P\\approx -2d\\cos\\theta\\)，取大小就是 \\(2d\\cos\\theta\\)，与式~\\eqref{eq:dl} 同形。代入小角近似'
new='在 \\(2d\\ll z\\)、\\(r\\ll z\\) 时，由几何（把 \\(S_2\'P\\) 对 \\(2d/z\\) 展开），\\(S_2\'P-S_1P\\approx -2d\\cos\\theta\\)，取大小就是 \\(2d\\cos\\theta\\)，与式~\\eqref{eq:dl} 同形。代入小角近似'
assert old in t
t=t.replace(old,new,1)
old='中心 \\(r=0\\) 处 \\(2d=k_0\\lambda\\)，级次最高；往外'
new='中心 \\(r=0\\) 处 \\(2d=k_0\\lambda\\)（\\(k_0=2d/\\lambda\\)，不一定是整数），级次最高；往外'
assert old in t
t=t.replace(old,new,1)
p.write_text(t,encoding='utf-8')
print('ok')
