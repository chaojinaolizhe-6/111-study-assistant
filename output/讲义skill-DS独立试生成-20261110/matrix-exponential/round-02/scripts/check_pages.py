#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""列出 handout.pdf 每页首行/末行，并标出真实跨页的可疑断点。

本脚本只做文字层与分页位置检查，不代替人眼阅读版面。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import fitz

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "handout.pdf"

# 已知不能出现在页首的残句/孤立成分（按本轮审核 R6 的证据）
BAD_FIRST = [
    "式）。",
    "即",
    "乘开后是",
]
# 页底孤立标题：短行且以节号/小节号开头
HEADING_RE = re.compile(r"^(?:§\s*\d|附录\s*[A-Z]|[0-9]+\.[0-9]+|B\.[0-9]|例\s*\d)")

doc = fitz.open(PDF)
print(f"PDF: {PDF.name}, {doc.page_count} pages")
fails = []
warns = []

for i, page in enumerate(doc, 1):
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
            if y0 < 52 or y0 > 784:  # 页眉/页脚
                continue
            lines.append((y0, text))
    lines.sort()
    first = lines[0][1] if lines else ""
    last = lines[-1][1] if lines else ""
    print(f"p{i:02d}: first={first[:70]!r}")
    if len(lines) > 1:
        print(f"      last ={last[:70]!r}")

    for bad in BAD_FIRST:
        if first.startswith(bad):
            fails.append(f"p{i}: 页首残句/缺上下文：{first!r}")
    if first and first[0] in "，。；）】":
        fails.append(f"p{i}: 页首以标点开头：{first!r}")
    if last and len(last) < 40 and HEADING_RE.match(last):
        fails.append(f"p{i}: 页底孤立标题：{last!r}")

print(f"\n硬性失败 {len(fails)} 条，提示 {len(warns)} 条。")
for msg in fails:
    print("  [FAIL]", msg)
if fails:
    sys.exit(1)
print("PAGE-EDGE CHECKS PASSED（只查文字层首末行，不代表目视版面验收）")
