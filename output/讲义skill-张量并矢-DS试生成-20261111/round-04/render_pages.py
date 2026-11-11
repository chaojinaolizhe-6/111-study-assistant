# -*- coding: utf-8 -*-
"""把 handout.pdf 逐页渲染成 PNG，并生成 4 张联系表（供支持看图的审核者目视）。

当前模型不支持图像输入；本脚本只负责生成渲染，不声称已目视通过。
输出：render/page-XX.png、render/contact-1..4.png
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PDF = HERE / "handout.pdf"
OUT = HERE / "render"


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    import fitz
    from PIL import Image

    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("page-*.png"):
        old.unlink()
    for old in OUT.glob("contact-*.png"):
        old.unlink()

    doc = fitz.open(PDF)
    paths: list[Path] = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=150)
        path = OUT / f"page-{i + 1:02d}.png"
        pix.save(path)
        paths.append(path)
    doc.close()
    print(f"rendered {len(paths)} pages at 150 dpi -> {OUT}")

    # 每张联系表放 12 页（4 列 x 3 行），缩略图宽 360 px
    thumb_w = 360
    per_sheet = 12
    cols, rows = 4, 3
    for s in range(0, len(paths), per_sheet):
        chunk = paths[s:s + per_sheet]
        thumbs = []
        for p in chunk:
            im = Image.open(p).convert("RGB")
            ratio = thumb_w / im.width
            thumbs.append(im.resize((thumb_w, max(1, int(im.height * ratio))), Image.LANCZOS))
        if not thumbs:
            continue
        cell_h = max(im.height for im in thumbs) + 24
        sheet = Image.new("RGB", (cols * thumb_w, rows * cell_h), "white")
        for k, im in enumerate(thumbs):
            r, c = divmod(k, cols)
            sheet.paste(im, (c * thumb_w, r * cell_h + 18))
        sheet_path = OUT / f"contact-{s // per_sheet + 1}.png"
        sheet.save(sheet_path)
        print(f"contact sheet -> {sheet_path.name} ({len(chunk)} pages)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
