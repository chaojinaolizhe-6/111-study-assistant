# -*- coding: utf-8 -*-
"""勘察源 PDF：页面图文结构、图形范围与文字坐标，用于核对图与正文描述。

只读 inputs/ 下两份 PDF；输出到 stdout。
运行：python -B michelson/round-01/tools/inspect_source.py
"""
import sys
from pathlib import Path

import fitz

BASE = str(Path(__file__).resolve().parents[3] / "inputs") + "/"
FILES = [
    "Exp.11TheAdjustmentofMichelsonInterferometer.pdf",
    "PreviewforMichelsoninterferometer-2025.pdf",
]


def main() -> int:
    for name in FILES:
        doc = fitz.open(BASE + name)
        print("==", name, "pages:", doc.page_count)
        for i, page in enumerate(doc):
            imgs = page.get_images(full=True)
            drawings = page.get_drawings()
            blocks = page.get_text("blocks")
            print(f"  p{i+1}: images={len(imgs)} vector_drawings={len(drawings)} text_blocks={len(blocks)}")
            if drawings:
                xs = [r["rect"] for r in drawings if r.get("rect") is not None]
                if xs:
                    print("      draw bbox x0..x1 / y0..y1:",
                          round(min(b.x0 for b in xs), 1), round(max(b.x1 for b in xs), 1),
                          round(min(b.y0 for b in xs), 1), round(max(b.y1 for b in xs), 1))
            for b in blocks:
                txt = " ".join(b[4].split())
                if len(txt) <= 60:  # 图注、标签一类短文本
                    print(f"      [{b[0]:.0f},{b[1]:.0f},{b[2]:.0f},{b[3]:.0f}] {txt}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
