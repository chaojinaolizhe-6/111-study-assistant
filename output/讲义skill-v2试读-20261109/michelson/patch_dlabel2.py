from pathlib import Path
p=Path(r'output/讲义skill-v2试读-20261109/michelson/michelson-excerpt-v2.tex')
t=p.read_text(encoding='utf-8')
old='\\node[left] at (0.92,2.35) {$d$};'
new='\\node[left] at (0.72,2.35) {$d$};'
assert old in t
p.write_text(t.replace(old,new,1),encoding='utf-8')
print('ok')
