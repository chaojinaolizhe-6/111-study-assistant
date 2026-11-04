# -*- coding: utf-8 -*-
"""Build the 党课心得体会 DOCX from the plain-text draft."""
import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Pt, Cm

SRC = r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\xinde.txt"
OUT = r"D:\aaa_D_usual\DSH\111学习助手\入党\第36期入党积极分子培训-心得体会-马泽宇-20251091006.docx"

text = open(SRC, encoding="utf-8").read().lstrip("\ufeff")
lines = text.split("\n")
title = lines[0].strip()
subtitle = lines[1].strip()
rest = "\n".join(lines[2:])
body = [p.strip() for p in rest.split("\n\n") if p.strip()]

doc = Document()
sec = doc.sections[0]
sec.page_height = Cm(29.7)
sec.page_width = Cm(21.0)
sec.top_margin = Cm(2.8)
sec.bottom_margin = Cm(2.4)
sec.left_margin = Cm(3.0)
sec.right_margin = Cm(2.6)

# base style
style = doc.styles["Normal"]
style.font.name = "宋体"
style.font.size = Pt(12)
style.element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")


def set_run_font(run, name="宋体", size=12, bold=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = rpr.makeelement(qn("w:rFonts"), {})
        rpr.append(rfonts)
    rfonts.set(qn("w:ascii"), name)
    rfonts.set(qn("w:hAnsi"), name)
    rfonts.set(qn("w:eastAsia"), name)


# title
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(6)
p.paragraph_format.space_after = Pt(4)
p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
set_run_font(p.add_run(title), "黑体", 20, True)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(14)
set_run_font(p.add_run(subtitle), "楷体", 14, False)

for block in body:
    lines = [l.strip() for l in block.split("\n") if l.strip()]
    if not lines:
        continue
    head = lines[0]
    is_heading = bool(re.match(r"^[一二三四五六七八九十]、", head))
    if is_heading:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(9)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.5
        set_run_font(p.add_run(head), "黑体", 14, True)
        for l in lines[1:]:
            p = doc.add_paragraph()
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.first_line_indent = Pt(24)
            p.paragraph_format.space_after = Pt(0)
            set_run_font(p.add_run(l), "宋体", 12)
        continue

    is_sig = block is body[-1]
    for l in lines:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(0)
        if is_sig:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p.paragraph_format.right_indent = Pt(24)
        else:
            p.paragraph_format.first_line_indent = Pt(24)
        set_run_font(p.add_run(l), "宋体", 12)

doc.save(OUT)
print("saved", OUT)

# count
body_text = "".join(p.text for p in doc.paragraphs)
cn = len(re.findall(r"[\u4e00-\u9fff]", body_text))
print("全文字符（不含空白）:", len(re.sub(r"\s", "", body_text)), "汉字:", cn, "段落:", len(doc.paragraphs))


