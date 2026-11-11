# -*- coding: utf-8 -*-
"""Print layout blocks (bbox + first chars) for pages of interest."""
import fitz, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

def show(rel, pages):
    d = fitz.open(os.path.join(ROOT, rel))
    print("#####", rel, "pages", d.page_count, "size", d[0].rect)
    for p in pages:
        pg = d[p - 1]
        print(f"--- p{p} rect={pg.rect}")
        for b in pg.get_text("blocks"):
            x0, y0, x1, y1, txt, bno, btype = b
            t = txt.replace("\x00", "").replace("\n", " ").strip()
            if t:
                print(f"  y={y0:6.1f}-{y1:6.1f} x={x0:5.1f}-{x1:5.1f} | {t[:70]}")

if __name__ == "__main__":
    which = sys.argv[1]
    pages = [int(x) for x in sys.argv[2:]]
    show(os.path.join("inputs", "old-handout.pdf") if which == "old" else os.path.join("round-04", "handout.pdf"), pages)
