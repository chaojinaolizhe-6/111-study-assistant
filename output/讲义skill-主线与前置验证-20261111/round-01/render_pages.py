#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Render every page of sample.pdf to PNG for external visual review."""
from __future__ import annotations

from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent
PDF = ROOT / "sample.pdf"
OUT = ROOT / "render"


def main() -> int:
    if not PDF.exists():
        print(f"missing {PDF}")
        return 1
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("page-*.png"):
        old.unlink()
    doc = fitz.open(PDF)
    for index, page in enumerate(doc, 1):
        pix = page.get_pixmap(dpi=110, alpha=False)
        path = OUT / f"page-{index:02d}.png"
        pix.save(path)
        print(f"{path.name}: {pix.width}x{pix.height}")
    print(f"rendered {doc.page_count} pages at 110 dpi into {OUT.name}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
