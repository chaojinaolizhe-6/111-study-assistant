# -*- coding: utf-8 -*-
"""用同一份数据生成《党的常用名词规范表》阅读版 DOCX（横向 A4，便于手机看）。"""
import importlib.util
import os

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

spec = importlib.util.spec_from_file_location(
    "terms", r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\build_terms.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

OUT = r"D:\aaa_D_usual\DSH\111学习助手\入党\党的常用名词规范表-阅读版-20261104.docx"

doc = Document()
sec = doc.sections[0]
sec.orientation = WD_ORIENT.LANDSCAPE
sec.page_width, sec.page_height = Cm(29.7), Cm(21.0)
sec.top_margin = Cm(1.6)
sec.bottom_margin = Cm(1.4)
sec.left_margin = Cm(1.6)
sec.right_margin = Cm(1.6)

style = doc.styles["Normal"]
style.font.name = "微软雅黑"
style.font.size = Pt(8.5)
style.element.rPr.rFonts.set(qn("w:eastAsia"), "微软雅黑")


def para(text, size=8.5, bold=False, align=None, space_after=0):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.bold = bold
    r.font.name = "微软雅黑"
    r._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "微软雅黑")
    return p


para("党的常用名词规范表", 16, True, WD_ALIGN_PARAGRAPH.CENTER, 2)
para("第36期入党积极分子培训配套 · 2026年11月4日编制 · 依据党章与中央文件原文", 8,
     False, WD_ALIGN_PARAGRAPH.CENTER, 8)

cats = []
for row in mod.ROWS:
    if row[0] not in cats:
        cats.append(row[0])

for cat in cats:
    para(cat, 10, True, None, 2)
    table = doc.add_table(rows=1, cols=4)
    table.style = "Table Grid"
    table.autofit = False
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths = [Cm(4.0), Cm(7.0), Cm(10.0), Cm(5.5)]
    hdr = ["规范表述", "常见错误写法", "用法要点（压缩）", "依据"]
    for i, h in enumerate(hdr):
        cell = table.rows[0].cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(8)
        r.font.name = "微软雅黑"
        r._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "微软雅黑")
    for row in [r for r in mod.ROWS if r[0] == cat]:
        cells = table.add_row().cells
        short = row[2] if len(row[2]) <= 88 else row[2][:86] + "…"
        for i, val in enumerate([row[1], row[3], short, row[4]]):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(7.5)
            r.font.name = "微软雅黑"
            r._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "微软雅黑")
    for i, w in enumerate(widths):
        table.columns[i].width = w
    for row in table.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = w
    para("", 6)

para("易错速查：把左边换成右边", 10, True, None, 2)
t2 = doc.add_table(rows=1, cols=3)
t2.style = "Table Grid"
for i, h in enumerate(["错误写法", "正确写法", "说明"]):
    c = t2.rows[0].cells[i]
    c.text = ""
    r = c.paragraphs[0].add_run(h)
    r.bold = True
    r.font.size = Pt(8)
    r.font.name = "微软雅黑"
for bad, good, note in mod.WRONG_ROWS:
    cells = t2.add_row().cells
    for i, v in enumerate([bad, good, note]):
        cells[i].text = ""
        r = cells[i].paragraphs[0].add_run(v)
        r.font.size = Pt(7.5)
        r.font.name = "微软雅黑"

doc.save(OUT)
print("saved", OUT)



