#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Dump the extracted text of every page in sample.pdf for text-level checks.

This is a searchable dump, not a substitute for visual inspection.
"""
from __future__ import annotations

from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent
PDF = ROOT / "sample.pdf"
OUT = ROOT / "page-text.txt"


def main() -> int:
    if not PDF.exists():
        print(f"missing {PDF}")
        return 1
    doc = fitz.open(PDF)
    chunks: list[str] = []
    for index, page in enumerate(doc, 1):
        chunks.append(f"===== PAGE {index} =====")
        chunks.append(page.get_text("text").strip())
        chunks.append("")
    OUT.write_text("\n".join(chunks), encoding="utf-8")
    print(f"wrote {OUT.name}: {doc.page_count} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
