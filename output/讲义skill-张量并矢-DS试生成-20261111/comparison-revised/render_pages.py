# -*- coding: utf-8 -*-
"""Render every page of comparison.pdf to render/page-NN.png for external review."""
import fitz
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, "comparison.pdf")
OUT = os.path.join(HERE, "render")
DPI = 150


def main():
    os.makedirs(OUT, exist_ok=True)
    for old in os.listdir(OUT):
        if old.startswith("page-") and old.endswith(".png"):
            os.remove(os.path.join(OUT, old))
    doc = fitz.open(PDF)
    for i, pg in enumerate(doc):
        pix = pg.get_pixmap(dpi=DPI, alpha=False)
        path = os.path.join(OUT, f"page-{i+1:02d}.png")
        pix.save(path)
        print(f"page {i+1:02d}: {pix.width}x{pix.height} -> {path}")
    print(f"rendered {doc.page_count} pages at {DPI} dpi")
    return 0


if __name__ == "__main__":
    sys.exit(main())
