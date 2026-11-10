#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""对生成的 handout.pdf 做版面/字体/结构的程序化检查。

模型无图像输入，不能做像素级目视检查；本脚本用文字层坐标代替：
  * 正文是否越出左右页边距或正文上下界；
  * 是否有页面几乎空白、标题落在页底而正文在下一页；
  * 字体是否嵌入、是否有图片对象、是否有缺失字形（另见编译日志）；
  * 例题/练习/附录标题是否都在 PDF 中。
任一硬性检查失败则非零退出。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import fitz

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PDF = Path(__file__).resolve().parents[1] / "handout.pdf"
MM = 72 / 25.4
LEFT = 20 * MM
RIGHT_MARGIN = 20 * MM
TOP = 21 * MM
BOTTOM_MARGIN = 23 * MM

doc = fitz.open(PDF)
W, H = doc[0].rect.width, doc[0].rect.height
fails: list[str] = []
warns: list[str] = []


def fail(msg: str) -> None:
    fails.append(msg)
    print("[FAIL]", msg)


def warn(msg: str) -> None:
    warns.append(msg)
    print("[WARN]", msg)


print(f"PDF: {PDF.name}, {doc.page_count} pages, {W:.1f}x{H:.1f} pt")

# ---------- 1. 正文边界 ----------
for i, page in enumerate(doc):
    body = []
    for block in page.get_text("dict")["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                if not span["text"].strip():
                    continue
                x0, y0, x1, y1 = span["bbox"]
                if y1 < 52 or y0 > 784:  # 页眉/页脚（页脚基线约 805pt）
                    continue
                body.append((x0, y0, x1, y1, span["text"]))
    if not body:
        fail(f"p{i+1} 正文为空")
        continue
    xmin = min(b[0] for b in body)
    xmax = max(b[2] for b in body)
    ymin = min(b[1] for b in body)
    ymax = max(b[3] for b in body)
    tol = 12.0  # ctex 标点悬挂可伸出边界约 8pt
    if xmin < LEFT - tol or xmax > W - RIGHT_MARGIN + tol:
        fail(f"p{i+1} 正文越界：x=[{xmin:.1f},{xmax:.1f}]，允许 [{LEFT:.1f},{W-RIGHT_MARGIN:.1f}]")
    if ymin < TOP - tol or ymax > H - BOTTOM_MARGIN + tol:
        fail(f"p{i+1} 正文纵向越界：y=[{ymin:.1f},{ymax:.1f}]，允许 [{TOP:.1f},{H-BOTTOM_MARGIN:.1f}]")
    # 页底孤立标题：按行合并后，最后两行若以节号开头且很短，则提示
    lines = []
    for block in page.get_text("dict")["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block["lines"]:
            spans = [s for s in line["spans"] if s["text"].strip()]
            if not spans:
                continue
            text = "".join(s["text"] for s in spans).strip()
            y0 = min(s["bbox"][1] for s in spans)
            if y0 > 784:
                continue
            lines.append((y0, text))
    for y0, text in sorted(lines)[-2:]:
        if y0 > H - 150 and len(text) < 42 and re.match(r"^(§|附录|[0-9]+\.[0-9]+\s|B\.[0-9])", text):
            fail(f"p{i+1} 页底疑似孤立标题：{text!r}")

# ---------- 2. 稀疏页 ----------
body_counts = []
for i, page in enumerate(doc):
    n = sum(1 for b in page.get_text("dict")["blocks"] if b.get("type") == 0)
    body_counts.append(n)
for i, n in enumerate(body_counts):
    print(f"  p{i+1}: {n} text blocks, {len(doc[i].get_text())} chars")
    if n < 3:
        fail(f"p{i+1} 文本块过少（{n}），疑似空白页")

# ---------- 3. 图片与字体 ----------
images = sum(len(page.get_images(full=True)) for page in doc)
if images:
    warn(f"PDF 含 {images} 个位图对象（本讲义源为纯文字，预期 0）")
else:
    print("图片对象：0（预期）")

font_xrefs = set()
for page in doc:
    for f in page.get_fonts(full=True):
        font_xrefs.add(f[0])
bad_fonts = []
for xref in sorted(font_xrefs):
    try:
        info = doc.extract_font(xref)
        if not info or not info[3]:
            bad_fonts.append(xref)
    except Exception:
        bad_fonts.append(xref)
if bad_fonts:
    fail(f"存在未嵌入或无法提取的字体 xref：{bad_fonts}")
else:
    print(f"字体：{len(font_xrefs)} 个 xref，均可提取（嵌入）")

# ---------- 4. 结构要素 ----------
full = "\n".join(page.get_text() for page in doc)
expect = [f"课件例题{i}" for i in range(1, 9)] + [
    "练习H1", "练习H2", "练习H3",
    "附录A", "附录B", "B.3 勘误", "B.4 没有改动的内容",
    "H1\n续解", "H3\n续解",
]
for item in expect:
    if item not in full:
        fail(f"PDF 中找不到结构要素：{item!r}")
    else:
        print(f"  找到：{item!r}")

# 三个练习的附录页码引用应与实际答案页一致（从 PDF 实际页读取）
def answer_page(hid: str) -> int | None:
    for i, page in enumerate(doc, 1):
        t = page.get_text()
        if f"{hid}\n详解" in t or f"{hid} 详解" in t:
            return i
    return None


for hid in ("H1", "H2", "H3"):
    # 找“详解见附录第N页”
    m = re.search(rf"练习\s*{hid}.*?详解见附录第\s*(\d+)\s*页", full, re.S)
    expected_page = answer_page(hid)
    if not m:
        fail(f"{hid} 的详解页码引用未找到")
    elif expected_page is None:
        fail(f"{hid} 的详解页未在 PDF 中找到")
    else:
        got = int(m.group(1))
        print(f"  {hid} 详解引用页：{got}（PDF 实际答案页：{expected_page}）")
        if got != expected_page:
            fail(f"{hid} 详解引用页 {got} 与 PDF 实际页 {expected_page} 不同")

print(f"\n硬性失败 {len(fails)} 条，提示 {len(warns)} 条。")
if fails:
    sys.exit(1)
print("LAYOUT CHECKS PASSED（不代表像素级目视验收）")
