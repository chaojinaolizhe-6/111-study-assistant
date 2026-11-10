# -*- coding: utf-8 -*-
"""导出源 PDF 指定页的图形线段与图片位置，用于核对装置图布局（模型无图像输入时的替代）。"""
import sys
from pathlib import Path

import fitz

BASE = Path(__file__).resolve().parents[3] / "inputs"


def dump(page_no: int, path: Path) -> None:
    doc = fitz.open(path)
    page = doc[page_no - 1]
    print(f"--- {path.name} p{page_no} ---")
    for img in page.get_images(full=True):
        xref = img[0]
        rects = page.get_image_rects(xref)
        info = doc.extract_image(xref)
        print(f"  image xref={xref} {info['width']}x{info['height']} ext={info['ext']} "
              f"rects={[tuple(round(v, 1) for v in r) for r in rects]}")
    for i, d in enumerate(page.get_drawings()):
        items = d["items"]
        print(f"  drawing[{i}] items={len(items)} rect={tuple(round(v, 1) for v in d['rect'])}")
        for it in items[:40]:
            kind = it[0]
            if kind == "l":
                p1, p2 = it[1], it[2]
                print(f"     line ({p1.x:.1f},{p1.y:.1f})-({p2.x:.1f},{p2.y:.1f})")
            elif kind == "re":
                r = it[1]
                print(f"     rect {tuple(round(v, 1) for v in r)}")
            elif kind in ("qu", "c"):
                pts = [f"({p.x:.1f},{p.y:.1f})" for p in it[1:]]
                print(f"     {kind} {' '.join(pts)}")
            else:
                print(f"     {kind}")


if __name__ == "__main__":
    for no in (2, 3, 4):
        dump(no, BASE / "Exp.11TheAdjustmentofMichelsonInterferometer.pdf")
