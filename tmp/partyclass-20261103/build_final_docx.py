# -*- coding: utf-8 -*-
"""按原稿版式生成定稿 DOCX：黑体二号标题、楷体三号副标题、黑体四号小标题、
宋体小四正文、1.5 倍行距、首行缩进 2 字符、落款右对齐。"""
import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

SRC = r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\final_text.txt"
OUT = r"D:\aaa_D_usual\DSH\111学习助手\入党\马泽宇-20251091006-党课心得体会-定稿.docx"

raw = open(SRC, encoding="utf-8").read().lstrip("\ufeff")
lines = raw.split("\n")
title, subtitle = lines[0].strip(), lines[1].strip()
body = [p.strip() for p in "\n".join(lines[2:]).split("\n\n") if p.strip()]

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
sec.top_margin, sec.bottom_margin = Cm(2.0), Cm(2.0)
sec.left_margin, sec.right_margin = Cm(3.0), Cm(3.0)

style = doc.styles["Normal"]
style.font.name = "Times New Roman"
style.font.size = Pt(12)
style.element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")


def run_font(run, ea, size, bold=False):
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)
    run.bold = bold
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = rpr.makeelement(qn("w:rFonts"), {})
        rpr.append(rf)
    rf.set(qn("w:ascii"), "Times New Roman")
    rf.set(qn("w:hAnsi"), "Times New Roman")
    rf.set(qn("w:eastAsia"), ea)


def para(text, ea, size, bold=False, align=None, indent=False, sa=0.0, ls=1.5, sb=0.0):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    p.paragraph_format.line_spacing = ls
    p.paragraph_format.space_before = Pt(sb)
    p.paragraph_format.space_after = Pt(sa)
    if indent:
        p.paragraph_format.first_line_indent = Pt(24)
    run_font(p.add_run(text), ea, size, bold)
    return p


para(title, "黑体", 22, True, WD_ALIGN_PARAGRAPH.CENTER)
para(subtitle, "楷体", 16, False, WD_ALIGN_PARAGRAPH.CENTER, sa=8)

for block in body:
    blines = [x.strip() for x in block.split("\n") if x.strip()]
    if re.match(r"^[一二三四五六七八九十]、", blines[0]):
        hp = para(blines[0], "黑体", 14, True, WD_ALIGN_PARAGRAPH.LEFT, sa=4)
        hp.paragraph_format.space_before = Pt(4)
        hp.paragraph_format.keep_with_next = True
        for x in blines[1:]:
            para(x, "宋体", 12, False, WD_ALIGN_PARAGRAPH.JUSTIFY, indent=True)
        continue
    if block is body[-1]:
        for i, x in enumerate(blines):
            para(x, "宋体", 12, False, WD_ALIGN_PARAGRAPH.RIGHT, ls=1.15, sb=4 if i == 0 else 0)
        continue
    for x in blines:
        para(x, "宋体", 12, False, WD_ALIGN_PARAGRAPH.JUSTIFY, indent=True)

doc.save(OUT)

text = "\n".join(p.text for p in doc.paragraphs)
cn = len(re.findall(r"[\u4e00-\u9fff]", text))
print("saved", OUT)
print("字符（不含空白）:", len(re.sub(r"\s", "", text)), "汉字:", cn)





