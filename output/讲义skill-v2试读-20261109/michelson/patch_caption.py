from pathlib import Path
p=Path(r'output/讲义skill-v2试读-20261109/michelson/michelson-excerpt-v2.tex')
t=p.read_text(encoding='utf-8')
old='\\caption{Q II-1 的作答光路图（自绘，俯视示意；角度放大）。光束 I 去 \\(M_1\\)，光束 II 经 \\(G_2\\) 去 \\(M_2\\)；两束回到 \\(G_1\\) 合束后向下到 \\(E\\)。虚线 \\(M_2\'\\) 是 \\(M_2\\) 经 \\(G_1\\) 的虚像，\\(d=|M_1M_2\'|\\)。}'
new='\\caption{Q II-1 的作答光路图（自绘，俯视示意；角度放大）。输入端的扩束镜（BE）把细激光变成球面波；光束 I 去 \\(M_1\\)，光束 II 经 \\(G_2\\) 去 \\(M_2\\)；两束回到 \\(G_1\\) 合束后向下到 \\(E\\)。虚线 \\(M_2\'\\) 是 \\(M_2\\) 经 \\(G_1\\) 的虚像，\\(d=|M_1M_2\'|\\)。}'
assert old in t
p.write_text(t.replace(old,new,1),encoding='utf-8')
print('ok')
