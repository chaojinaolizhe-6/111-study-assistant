from pathlib import Path
p=Path(r'output/讲义skill-v2试读-20261109/michelson/michelson-excerpt-v2.tex')
t=p.read_text(encoding='utf-8')
t=t.replace('& 必做\\\\','& 非选做\\\\')
# only two occurrences in purpose table; check
old='空气的 \\(n\\approx1\\)，所以本实验里“几何路程差”和“光程差”数值相同。'
new='空气的 \\(n\\) 只比 1 大万分之几，所以本实验里“几何路程差”和“光程差”在实验精度内近似相同。'
assert old in t
t=t.replace(old,new,1)
old='\\node[left] at (0.72,2.35) {$d$};'
new='\\node[left] at (0.66,2.35) {$d$};'
assert old in t
t=t.replace(old,new,1)
p.write_text(t,encoding='utf-8')
print('ok')
