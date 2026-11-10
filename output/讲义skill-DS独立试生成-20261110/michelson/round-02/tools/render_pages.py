# -*- coding: utf-8 -*-
r"""把 round-02 的 handout.pdf 每页渲染为 PNG，供外部支持看图的审核者只读验收。

用法：python -B michelson/round-02/tools/render_pages.py
输出：michelson/round-02/renders/handout-pNN.png（150 dpi）
本脚本只渲染，不代替目视验收；执行模型无图像输入。
"""
from __future__ import annotations

import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "handout.pdf"
OUT = ROOT / "renders"
DPI = 150


def main() -> int:
    if not PDF.exists():
        print(f"[E] 找不到 {PDF}")
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF)
    for i, page in enumerate(doc, 1):
        pix = page.get_pixmap(dpi=DPI)
        path = OUT / f"handout-p{i:02d}.png"
        pix.save(path)
        print(f"{path.name}  {pix.width}x{pix.height}")
    print(f"共渲染 {doc.page_count} 页，{DPI} dpi；执行模型无图像输入，目视验收待外部审核。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
