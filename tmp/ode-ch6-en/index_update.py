# -*- coding: utf-8 -*-
import os, sys

p = os.path.join('subjects', '03-微分方程', '讲义', 'INDEX.md')
s = open(p, encoding='utf-8').read()

old_pages = '| [`ODE-期中之后-完整讲义-L13-L23-20261118.pdf`](ODE-期中之后-完整讲义-L13-L23-20261118.pdf)（＋同名 `.tex`） | **155** |'
new_pages = '| [`ODE-期中之后-完整讲义-L13-L23-20261118.pdf`](ODE-期中之后-完整讲义-L13-L23-20261118.pdf)（＋同名 `.tex`） | **157** |'

add_anchor = '图 1–4 编号正确）。 |'
add_text = (
    '图 1–4 编号正确）。'
    '<br>**2026-11-19 修订（第 6 章名词附英文）**：第 6 章正文 71 处专业名词在首次出现处补“（灰色斜体英文）”'
    '（`\\EN` 宏，样式同《L21-L23 作业答案-名词附英文》）；新增 §13《名词中英对照（考前查用）》——'
    '13.1 相图与点型、13.2 稳定性·线性化·方法、13.3 矩阵与判据三张四栏表（共 76 词，含源/汇、未扰/受扰解等课件用语），'
    '13.4 六组易混词，13.5 两道作业题干原句及译法；§12.4 页码对照表补 §13 一行；章题副标题补 English。'
    '同时改正 §3.3 表与表下注解：原稿把 `improper node` 当成普通结点，与课件 L22 定义相反（`improper/degenerate node` 是 $g=1$ 的退化结点，普通结点只叫 `node`）。'
    '修订后 155→157 页，两遍 xelatex 全部通过，0 错误、0 Overfull、0 缺字、0 未解析引用；`check_handout.py --mode appendix` 仍为同一批 8 条 [E]（旧问题，无新增），13.5 的题干已补课件出处。 |'
)

n1 = s.count(old_pages)
n2 = s.count(add_anchor)
print('pages anchor', n1, ' add anchor', n2)
if n1 != 1 or n2 != 1:
    sys.exit(2)

s = s.replace(old_pages, new_pages, 1)
s = s.replace(add_anchor, add_text, 1)
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok', len(s))
