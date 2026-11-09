from pathlib import Path
p=Path(r'output/讲义skill-v2试读-20261109/michelson/michelson-excerpt-v2.tex')
t=p.read_text(encoding='utf-8')
t=t.replace('\\textbf{English short answer.}','\\textbf{English short answer.} ')
t=t.replace('centre','center').replace('colours','colors').replace('coloured','colored')
p.write_text(t,encoding='utf-8')
print('replaced')
