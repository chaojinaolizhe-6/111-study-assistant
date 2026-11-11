# -*- coding: utf-8 -*-
"""把最终 handout.pdf 逐页渲染为 PNG，供页面复核。

渲染不等于目视验收；本脚本只保证每一页都实际生成了非空图像，
并输出页数与文件清单。任何一页渲染失败或文件为空，以非零退出码报告。
"""
from __future__ import annotations

import sys
from pathlib import Path

import fitz

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
PDF = ROOT / "handout.pdf"
OUT = ROOT / "rendered"


def main() -> int:
    if not PDF.exists():
        print(f"[E] 找不到 {PDF}", file=sys.stderr)
        return 1
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("page-*.png"):
        old.unlink()
    doc = fitz.open(PDF)
    count = doc.page_count
    if count < 50:
        print(f"[E] 页数异常：{count} < 50", file=sys.stderr)
        return 1
    index = []
    for i, page in enumerate(doc, 1):
        pix = page.get_pixmap(dpi=110)
        path = OUT / f"page-{i:03d}.png"
        pix.save(path)
        if not path.exists() or path.stat().st_size == 0:
            print(f"[E] 渲染为空：{path}", file=sys.stderr)
            return 1
        index.append(f"{path.name}\t{path.stat().st_size}\t{pix.width}x{pix.height}")
    (OUT / "index.txt").write_text(
        f"handout.pdf\t{count} pages\n" + "\n".join(index) + "\n",
        encoding="utf-8",
    )
    print(f"[ok] 已渲染 {count} 页到 {OUT}")
    print(f"[ok] 清单：{OUT / 'index.txt'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
