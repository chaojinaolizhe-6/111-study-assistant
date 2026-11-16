# -*- coding: utf-8 -*-
"""把 round-02 的 handout.pdf 逐页渲染为 PNG，供协调器复核。

渲染不等于目视验收：本脚本只保证每页都生成非空图像并输出清单；
第 1 页另存 220dpi 高清版，便于查看图 0 的小字与连线。
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
    if count < 1:
        print(f"[E] PDF 没有页面：{count}", file=sys.stderr)
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
    hi = doc[0].get_pixmap(dpi=220)
    hi_path = OUT / "page-001-hi.png"
    hi.save(hi_path)
    if not hi_path.exists() or hi_path.stat().st_size == 0:
        print(f"[E] 高清页渲染为空：{hi_path}", file=sys.stderr)
        return 1
    index.append(f"{hi_path.name}\t{hi_path.stat().st_size}\t{hi.width}x{hi.height}\t(第 1 页 220dpi)")
    (OUT / "index.txt").write_text(
        f"handout.pdf\t{count} pages\n" + "\n".join(index) + "\n",
        encoding="utf-8",
    )
    print(f"[ok] 已渲染 {count} 页到 {OUT}（另含 page-001-hi.png）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
