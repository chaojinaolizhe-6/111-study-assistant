#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 handout.pdf 渲染为 PNG，并做像素墨迹/裁切检查。

本会话模型不能读取图像；这里只做“有墨迹、未触边、非空白页”的程序化检查，
不等于目视验收。外部审核者需只读查看 renders/ 下的 PNG。
"""
import sys
from pathlib import Path

import fitz
import numpy as np
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
pdf = ROOT / "handout.pdf"
out = ROOT / "renders"
out.mkdir(exist_ok=True)

doc = fitz.open(pdf)
fails = []
print(f"PDF: {pdf.name}, {doc.page_count} pages, output: {out}")
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    png = out / f"handout-p{i+1:02d}.png"
    pix.save(png)
    im = Image.open(png).convert("L")
    a = np.asarray(im)
    ink = a < 245
    frac = ink.mean()
    ys, xs = np.where(ink)
    if len(xs) == 0:
        fails.append(f"p{i+1} 空白渲染")
        print(f"p{i+1}: BLANK")
        continue
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    h, w = a.shape
    border = ink[:6, :].any() or ink[-6:, :].any() or ink[:, :6].any() or ink[:, -6:].any()
    print(f"p{i+1:02d}: ink={frac*100:.2f}% bbox=({x0},{y0})-({x1},{y1}) page={w}x{h} border={border}")
    if frac < 0.005:
        fails.append(f"p{i+1} 墨迹过少 {frac*100:.2f}%")
    if border:
        fails.append(f"p{i+1} 墨迹触及页面边缘（可能裁切）")
print(f"\n渲染页数 {doc.page_count}, 像素检查失败 {len(fails)}")
if fails:
    print("\n".join(fails))
    sys.exit(1)
print("PIXEL CHECKS PASSED（只查墨迹与裁切，不代表目视版面验收）")
