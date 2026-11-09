from pathlib import Path
p=Path(r'output/讲义skill-v2试读-20261109/michelson/michelson-excerpt-v2.tex')
t=p.read_text(encoding='utf-8')
heads=[
'§3.5 用到的式子、条件与用途',
'§4.2 II-1（预习 p1）光路图与部件作用',
'§4.4 II-3（预习 p1）成环条件与两镜位置',
'§4.5 II-6（预习 p1）把小半径环调成大半径环',
'§4.6 II-7（预习 p1）为什么环会吐或吞',
'§4.7 II-8（预习 p1）测波长的公式与步骤',
'§4.8 II-9（预习 p1）鼓轮转角与动镜位移',
'§5.2 材料冲突与不编造',
]
for s in heads:
    old='\\subhdr{'+s+'}'
    new='\\needspace{7\\baselineskip}\n\\subhdr{'+s+'}'
    if old in t:
        t=t.replace(old,new,1)
    else:
        print('NOT FOUND',s)
old='\\subhdr{§5.3 未知参数与示例的边界}'
new='\\enlargethispage{4\\baselineskip}\n\\subhdr{§5.3 未知参数与示例的边界}'
if old in t: t=t.replace(old,new,1)
else: print('NOT FOUND 5.3')
p.write_text(t,encoding='utf-8')
print('done')
