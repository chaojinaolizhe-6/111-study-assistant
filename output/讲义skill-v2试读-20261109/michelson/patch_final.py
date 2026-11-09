from pathlib import Path
p=Path(r'output/讲义skill-v2试读-20261109/michelson/michelson-excerpt-v2.tex')
t=p.read_text(encoding='utf-8')
t=t.replace('\\enlargethispage{4\\baselineskip}\n','',1)
t=t.replace('\\flowerrule\n\n\\textbf{本文件的边界。}','\\par\\medskip\n\n\\textbf{本文件的边界。}',1)
old1='''\\item \\textbf{II-6 的方向。}讲义 p5 说“增大 \\(d\\)，\\(r\\) 增大，环吐出”，所以本文件把“小半径调大”解释为“增大 \\(d\\)”。但“从中心数第 \\(m\\) 环”的 \\(r_m\\approx z\\sqrt{m\\lambda/d}\\) 在 \\(d\\) 增大时会让同一个 \\(m\\) 的半径变小；这是编号重排，不是矛盾。审校时请确认课程对“小半径调大”的预期方向，以及是否需要在答案里同时说明两种读法。'''
new1='''\\item \\textbf{II-6 的方向。}讲义 p5 说“增大 \\(d\\)，\\(r\\) 增大，环吐出”，本文件因此把“小半径调大”解释为“增大 \\(d\\)”。但 \\(r_m\\approx z\\sqrt{m\\lambda/d}\\) 在 \\(d\\) 增大时让同一个 \\(m\\) 的半径变小；这是编号重排，不是矛盾。请审校课程预期方向，以及是否要同时说明两种读法。'''
if old1 in t: t=t.replace(old1,new1,1)
else: print('item1 not found')
old2='''\\textbf{本文件的边界。}到这里只覆盖了实验目的、仪器、等效空气膜与 \\(\\Delta L=2d\\cos\\theta\\)、\\(d/\\theta\\) 的教学小例，以及 9 个直接相关的预习问答。完整操作步骤、定域/等厚/白光/F-P 的全部内容、空气折射率测量、数据处理全表、其余预习问答、9 道思考题、4 道扩展题和报告模板，仍看 2026-11-06 旧稿（28 页）与两份原始 PDF。本节选不声称覆盖全部实验内容，也不代表实验已完成或已掌握。'''
new2='''\\textbf{本文件的边界。}只到实验目的、仪器、等效空气膜与 \\(\\Delta L=2d\\cos\\theta\\)、\\(d/\\theta\\) 小例及 9 个相关问答。完整操作、定域/等厚/白光/F-P、空气折射率、数据全表、其余问答与思考/扩展题仍看 2026-11-06 旧稿（28 页）与原始 PDF；本节选不声称全覆盖，也不代表已掌握。'''
if old2 in t: t=t.replace(old2,new2,1)
else: print('final not found')
p.write_text(t,encoding='utf-8')
print('done')
