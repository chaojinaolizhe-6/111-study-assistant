#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按页打印 handout.pdf 的文字层（用于核对实际断页与续页上下文）。"""
from __future__ import annotations

import sys
from pathlib import Path

import fitz

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "handout.pdf"

pages = sys.argv[1:] or ["1"]
doc = fitz.open(PDF)
for spec in pages:
    for part in spec.split(","):
        n = int(part)
        page = doc[n - 1]
        print(f"\n===== p{n} =====")
        print(page.get_text("text"))
