from pathlib import Path
p=Path(r'output/讲义skill-v2试读-20261109/michelson/michelson-excerpt-v2.tex')
t=p.read_text(encoding='utf-8')
old='''\\item \\textbf{II-6 的方向。}讲义 p5 说“增大 \\(d\\)，\\(r\\) 增大，环吐出”，本文件因此把“小半径调大”解释为“增大 \\(d\\)”。但 \\(r_m\\approx z\\sqrt{m\\lambda/d}\\) 在 \\(d\\) 增大时让同一个 \\(m\\) 的半径变小；这是编号重排，不是矛盾。请审校课程预期方向，以及是否要同时说明两种读法。'''
new='''\\item \\textbf{II-6 的方向。}讲义 p5 说“增大 \\(d\\)，\\(r\\) 增大，环吐出”，本文件因此把“小半径调大”解释为“增大 \\(d\\)”。但 \\(r_m\\approx z\\sqrt{m\\lambda/d}\\) 在 \\(d\\) 增大时让同一个 \\(m\\) 的半径变小；这是编号重排。请审校预期方向。'''
assert old in t
p.write_text(t.replace(old,new,1),encoding='utf-8')
print('ok')
