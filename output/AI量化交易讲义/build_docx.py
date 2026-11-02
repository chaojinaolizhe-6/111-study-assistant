# -*- coding: utf-8 -*-
"""Build a styled DOCX lecture note from the Markdown source."""
import re
import sys
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC = sys.argv[1]
OUT = sys.argv[2]

BODY_EA = "宋体"
HEAD_EA = "黑体"
LATIN = "Times New Roman"
ACCENT = RGBColor(0x1F, 0x38, 0x64)
GREY = RGBColor(0x59, 0x59, 0x59)
DARK = RGBColor(0x1A, 0x1A, 0x1A)

TOC = [
    ("导言", "这份讲义回答什么问题，三条判据与三种读法"),
    ("第 1 章", "alpha 从哪里来：五类收益来源与套利限制"),
    ("第 2 章", "技术地图总览：十层结构 + 证据分级总表"),
    ("第 3 章", "数据与微观结构：订单流、VPIN、做市、冲击、成本"),
    ("第 4 章", "统计套利：配对、协整、O-U、PCA 残差、为何失效"),
    ("第 5 章", "横截面因子：FF5、因子动物园、动量崩溃、基本定律"),
    ("第 6 章", "机器学习选股：标签、特征、GBDT、网络、失败模式"),
    ("第 7 章", "强化学习：执行可行，端到端选股不可行"),
    ("第 8 章", "NLP 与另类数据：词典、FinBERT、LLM 的三个陷阱"),
    ("第 9 章", "组合与风险：MVO、收缩、BL、ERC、HRP、凯利"),
    ("第 10 章", "回测方法论：七宗罪、Purged CV、DSR、PBO"),
    ("第 11 章", "执行：Almgren-Chriss、VWAP/POV、冲击估计"),
    ("第 12 章", "工程与组织：研究栈、生产栈、监控、归因"),
    ("第 13 章", "中国 A 股特化：T+1、涨跌停、做空约束、新规"),
    ("第 14 章", "反清单：十种薄弱说法与六个识别红旗"),
    ("第 15 章", "12 周学习与实践路径"),
    ("第 16 章", "参考文献与资源总表"),
    ("附录 A–D", "公式速查、术语、自检清单、两路意见核对"),
]


def set_run(run, size=10.5, bold=False, color=None, ea=BODY_EA, latin=LATIN):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = latin
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    rFonts.set(qn("w:ascii"), latin)
    rFonts.set(qn("w:hAnsi"), latin)
    rFonts.set(qn("w:eastAsia"), ea)
    if color is not None:
        run.font.color.rgb = color


def shade(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tcPr.append(shd)


def cell_margins(table, top=40, bottom=40, left=80, right=80):
    tblPr = table._tbl.tblPr
    mar = OxmlElement("w:tblCellMar")
    for side, val in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:w"), str(val))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tblPr.append(mar)


def table_borders(table, color="BFBFBF"):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), color)
        borders.append(el)
    tblPr.append(borders)


def repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    trPr.append(el)


def keep_with_next(p):
    pPr = p._p.get_or_add_pPr()
    el = OxmlElement("w:keepNext")
    pPr.append(el)


def left_border(p, color="1F3864", size=18):
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), str(size))
    left.set(qn("w:space"), "8")
    left.set(qn("w:color"), color)
    pbdr.append(left)
    pPr.append(pbdr)


def add_field(paragraph, instr, size=9):
    run = paragraph.add_run()
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr_el = OxmlElement("w:instrText")
    instr_el.set(qn("xml:space"), "preserve")
    instr_el.text = instr
    fld_sep = OxmlElement("w:fldChar")
    fld_sep.set(qn("w:fldCharType"), "separate")
    txt = OxmlElement("w:t")
    txt.text = "1"
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run._r.append(fld_begin)
    run._r.append(instr_el)
    run._r.append(fld_sep)
    run._r.append(txt)
    run._r.append(fld_end)
    set_run(run, size=size, color=GREY)


INLINE = re.compile(r"(\*\*.+?\*\*|\*[^*\n]+?\*|`.+?`)")


def smart_quotes(text):
    out = []
    opening = True
    for ch in text:
        if ch == '"':
            out.append("\u201c" if opening else "\u201d")
            opening = not opening
        else:
            out.append(ch)
    return "".join(out)


def add_inline(paragraph, text, size=10.5, color=None, ea=BODY_EA):
    text = smart_quotes(text)
    pos = 0
    for m in INLINE.finditer(text):
        if m.start() > pos:
            r = paragraph.add_run(text[pos:m.start()])
            set_run(r, size=size, color=color, ea=ea)
        token = m.group(0)
        if token.startswith("**"):
            r = paragraph.add_run(token[2:-2])
            set_run(r, size=size, bold=True, color=color, ea=ea)
        elif token.startswith("*"):
            r = paragraph.add_run(token[1:-1])
            set_run(r, size=size, color=color, ea=ea)
            r.font.italic = True
        else:
            r = paragraph.add_run(token[1:-1])
            r.font.name = "Consolas"
            set_run(r, size=size - 1, color=color, ea="宋体", latin="Consolas")
        pos = m.end()
    if pos < len(text):
        r = paragraph.add_run(text[pos:])
        set_run(r, size=size, color=color, ea=ea)


def is_table_row(line):
    return line.strip().startswith("|") and line.strip().endswith("|")


def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def main():
    with open(SRC, encoding="utf-8-sig") as f:
        lines = f.read().split("\n")

    # drop the markdown front matter (title / subtitle / date) because the
    # DOCX has a dedicated title page for it
    for idx, ln in enumerate(lines):
        if ln.strip() == "---":
            lines = lines[idx + 1:]
            break

    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(2.4)
    sec.bottom_margin = Cm(2.2)
    sec.left_margin = Cm(2.5)
    sec.right_margin = Cm(2.3)
    sec.different_first_page_header_footer = True

    # base style
    normal = doc.styles["Normal"]
    normal.font.name = LATIN
    normal.font.size = Pt(10.5)
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), BODY_EA)
    pf = normal.paragraph_format
    pf.line_spacing = 1.35
    pf.space_after = Pt(6)

    # header / footer
    hp = sec.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = hp.add_run("AI 炒股与量化交易：成熟技术讲义")
    set_run(r, size=8.5, color=RGBColor(0x8C, 0x8C, 0x8C))

    fp = sec.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = fp.add_run("— ")
    set_run(r, size=9, color=GREY)
    add_field(fp, " PAGE ")
    r = fp.add_run(" / ")
    set_run(r, size=9, color=GREY)
    add_field(fp, " NUMPAGES ")
    r = fp.add_run(" —")
    set_run(r, size=9, color=GREY)

    # ---------- title page ----------
    for _ in range(4):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("AI 炒股与量化交易")
    set_run(r, size=30, bold=True, color=ACCENT, ea=HEAD_EA, latin="Cambria")

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("成熟技术讲义")
    set_run(r, size=26, bold=True, color=ACCENT, ea=HEAD_EA, latin="Cambria")

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(14)
    r = p.add_run("一份带证据等级、公式与失效条件的技术清单")
    set_run(r, size=12.5, color=GREY, ea="楷体", latin="Cambria")

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(60)
    r = p.add_run("整理日期：2026 年 10 月 31 日")
    set_run(r, size=10.5, color=DARK)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("适用对象：具备基础统计与编程能力、希望系统进入量化与 AI 选股的学习者")
    set_run(r, size=10, color=GREY)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(80)
    r = p.add_run("本讲义为教学材料，不构成投资建议")
    set_run(r, size=9, color=RGBColor(0x8C, 0x8C, 0x8C))

    doc.add_page_break()

    # ---------- TOC ----------
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run("目　录")
    set_run(r, size=18, bold=True, color=ACCENT, ea=HEAD_EA)

    tbl = doc.add_table(rows=0, cols=2)
    tbl.autofit = False
    table_borders(tbl, color="E6E6E6")
    cell_margins(tbl)
    for name, desc in TOC:
        row = tbl.add_row()
        c0, c1 = row.cells
        c0.width = Cm(3.4)
        c1.width = Cm(12.6)
        pp = c0.paragraphs[0]
        pp.paragraph_format.space_after = Pt(2)
        rr = pp.add_run(name)
        set_run(rr, size=10, bold=True, color=ACCENT, ea=HEAD_EA)
        pp2 = c1.paragraphs[0]
        pp2.paragraph_format.space_after = Pt(2)
        add_inline(pp2, desc, size=10, color=DARK)

    # ---------- body ----------
    i = 0
    n = len(lines)
    chapter_count = 0
    while i < n:
        line = lines[i]
        s = line.strip()

        if not s:
            i += 1
            continue

        # code fence
        if s == "```":
            block = []
            i += 1
            while i < n and lines[i].strip() != "```":
                block.append(lines[i])
                i += 1
            i += 1
            for bl in block:
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Cm(0.8)
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.1
                r = p.add_run(bl)
                set_run(r, size=8.5, ea="宋体", latin="Consolas",
                        color=RGBColor(0x33, 0x33, 0x33))
            doc.add_paragraph().paragraph_format.space_after = Pt(2)
            continue

        # horizontal rule
        if s in ("---", "***", "___"):
            i += 1
            continue

        # title
        if s.startswith("# ") and not s.startswith("## "):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(s[2:])
            set_run(r, size=20, bold=True, color=ACCENT, ea=HEAD_EA)
            i += 1
            continue

        # chapter
        if s.startswith("## "):
            chapter_count += 1
            if chapter_count == 1:
                doc.add_page_break()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(26) if chapter_count > 1 else Pt(0)
            p.paragraph_format.space_after = Pt(10)
            keep_with_next(p)
            r = p.add_run(s[3:])
            set_run(r, size=17, bold=True, color=ACCENT, ea=HEAD_EA)
            # underline rule
            pPr = p._p.get_or_add_pPr()
            pbdr = OxmlElement("w:pBdr")
            bottom = OxmlElement("w:bottom")
            bottom.set(qn("w:val"), "single")
            bottom.set(qn("w:sz"), "10")
            bottom.set(qn("w:space"), "4")
            bottom.set(qn("w:color"), "1F3864")
            pbdr.append(bottom)
            pPr.append(pbdr)
            i += 1
            continue

        # section
        if s.startswith("### "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(5)
            keep_with_next(p)
            r = p.add_run(smart_quotes(s[4:]))
            set_run(r, size=12.5, bold=True, color=RGBColor(0x2E, 0x54, 0x8C), ea=HEAD_EA)
            i += 1
            continue

        # table
        if is_table_row(line):
            rows = []
            while i < n and is_table_row(lines[i]):
                rows.append(split_row(lines[i]))
                i += 1
            # drop separator row
            rows = [r for r in rows if not all(re.fullmatch(r":?-{2,}:?", c) for c in r if c)]
            if not rows:
                continue
            ncol = max(len(r) for r in rows)
            tbl = doc.add_table(rows=0, cols=ncol)
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            table_borders(tbl)
            cell_margins(tbl)
            # widths
            content_w = 16.2
            lengths = []
            for c in range(ncol):
                mx = max((len(r[c]) for r in rows if c < len(r)), default=4)
                lengths.append(max(4, min(mx, 60)))
            total = sum(lengths)
            widths = [max(1.8, content_w * L / total) for L in lengths]
            for ridx, row in enumerate(rows):
                tr = tbl.add_row()
                trPr = tr._tr.get_or_add_trPr()
                cant = OxmlElement("w:cantSplit")
                cant.set(qn("w:val"), "true")
                trPr.append(cant)
                if ridx == 0:
                    repeat_header(tr)
                for c in range(ncol):
                    cell = tr.cells[c]
                    cell.width = Cm(widths[c])
                    txt = row[c] if c < len(row) else ""
                    para = cell.paragraphs[0]
                    para.paragraph_format.space_after = Pt(1)
                    para.paragraph_format.line_spacing = 1.15
                    if ridx == 0:
                        shade(cell, "1F3864")
                        add_inline(para, txt, size=9, color=RGBColor(0xFF, 0xFF, 0xFF), ea=HEAD_EA)
                        for r_ in para.runs:
                            r_.font.bold = True
                    else:
                        if ridx % 2 == 0:
                            shade(cell, "F2F4F8")
                        add_inline(para, txt, size=9, color=DARK)
            doc.add_paragraph().paragraph_format.space_after = Pt(2)
            continue

        # blockquote
        if s.startswith(">"):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.9)
            p.paragraph_format.right_indent = Cm(0.6)
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(8)
            left_border(p, color="B08D57", size=18)
            add_inline(p, s.lstrip("> ").strip(), size=9.5, color=RGBColor(0x44, 0x44, 0x44))
            i += 1
            continue

        # bullets
        if s.startswith("- "):
            txt = s[2:].strip()
            marker = "▪  "
            size_marker = 9
            if txt.startswith("[ ]"):
                txt = txt[3:].strip()
                marker = "☐  "
                size_marker = 11
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.9)
            p.paragraph_format.first_line_indent = Cm(-0.45)
            p.paragraph_format.space_after = Pt(3)
            r = p.add_run(marker)
            set_run(r, size=size_marker, color=ACCENT)
            add_inline(p, txt)
            i += 1
            continue

        # numbered list
        m = re.match(r"^(\d+)[.、]\s+(.*)$", s)
        if m:
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.95)
            p.paragraph_format.first_line_indent = Cm(-0.55)
            p.paragraph_format.space_after = Pt(3)
            r = p.add_run(m.group(1) + ". ")
            set_run(r, size=10.5, bold=True, color=ACCENT)
            add_inline(p, m.group(2))
            i += 1
            continue

        # checkboxes
        if s.startswith("- [ ]"):
            txt = s[5:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.9)
            p.paragraph_format.first_line_indent = Cm(-0.45)
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run("☐  ")
            set_run(r, size=11, color=ACCENT)
            add_inline(p, txt)
            i += 1
            continue

        # formula / indented line (starts with ideographic space)
        if line.startswith("　") or line.startswith(" "):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(1.0)
            p.paragraph_format.right_indent = Cm(0.6)
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.3
            pPr = p._p.get_or_add_pPr()
            shd = OxmlElement("w:shd")
            shd.set(qn("w:val"), "clear")
            shd.set(qn("w:color"), "auto")
            shd.set(qn("w:fill"), "F2F5FA")
            pPr.append(shd)
            left_border(p, color="7F9BC4", size=12)
            add_inline(p, s, size=11, color=RGBColor(0x0F, 0x2A, 0x4A))
            i += 1
            continue

        # normal paragraph
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.first_line_indent = Pt(21)
        add_inline(p, s)
        i += 1

    doc.save(OUT)
    print("saved", OUT, "chapters:", chapter_count)


if __name__ == "__main__":
    main()

