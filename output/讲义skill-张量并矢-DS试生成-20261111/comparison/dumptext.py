# -*- coding: utf-8 -*-
"""Dump per-page text of the two PDFs for comparison work."""
import fitz, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

def dump(rel, outname):
    src = os.path.join(ROOT, rel)
    d = fitz.open(src)
    print(rel, "pages=", d.page_count, "creation=", d.metadata.get("creationDate"))
    with open(os.path.join(HERE, outname), "w", encoding="utf-8") as f:
        for i, pg in enumerate(d):
            f.write(f"\n===== PAGE {i+1} =====\n")
            f.write(pg.get_text())

if __name__ == "__main__":
    dump(os.path.join("inputs", "old-handout.pdf"), "old-text.txt")
    dump(os.path.join("round-04", "handout.pdf"), "new-text.txt")
