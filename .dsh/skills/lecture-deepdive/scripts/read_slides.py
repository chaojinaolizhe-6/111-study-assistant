#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""read_slides.py —— 把课件 PDF 的指定页读成可核对的文字，用来建「课件页 → 知识点」映射。

为什么不用现成的 PDF 技能：本工作区只需要三件事——
  (1) 逐页文字层；(2) 每页首行，用来快速定位「老师在哪一页讲了什么」；
  (3) 纯图片页的警告（无文字层 = 要么 OCR，要么别引用页码）。

用法：
  python read_slides.py <课件.pdf> --pages 28-38              # 逐页正文
  python read_slides.py <课件.pdf> --pages 28-38 --map        # 只出「页号 → 首行」速查表
  python read_slides.py <课件.pdf> --map --json                # 机器可读

输出默认 UTF-8，Windows 控制台不会因中文报错。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def _parse_pages(spec: str, total: int) -> list[int]:
    """'28-38,50,53-55' → [27,28,...,37,49,52,53,54]（0-based）"""
    out: list[int] = []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            a, b = chunk.split("-", 1)
            lo, hi = int(a), int(b)
        else:
            lo = hi = int(chunk)
        for p in range(lo, hi + 1):
            idx = p - 1
            if 0 <= idx < total:
                out.append(idx)
    return sorted(set(out))


def _clean(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(description="课件 PDF 逐页取文字 / 页码速查表")
    ap.add_argument("pdf")
    ap.add_argument("--pages", help="页码区间（1 起）：28-38,50；省略则全书")
    ap.add_argument("--map", action="store_true", help="只输出「页号 → 首行」速查表")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--max-chars", type=int, default=1200, help="每页最多输出多少字符")
    args = ap.parse_args()

    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("需要 PyMuPDF：python -m pip install pymupdf", file=sys.stderr)
        return 2

    path = Path(args.pdf)
    if not path.exists():
        print(f"找不到文件：{path}", file=sys.stderr)
        return 2

    doc = fitz.open(path)
    pages = _parse_pages(args.pages, doc.page_count) if args.pages else list(range(doc.page_count))

    rows = []
    for idx in pages:
        page = doc[idx]
        raw = _clean(page.get_text())
        first = next((ln.strip() for ln in raw.splitlines() if ln.strip()), "")
        rows.append({
            "page": idx + 1,
            "chars": len(raw),
            "first_line": first[:90],
            "text": raw[: args.max_chars],
            "image_only": len(raw) < 20,
        })

    if args.json:
        print(json.dumps({"file": str(path), "pages": rows}, ensure_ascii=False, indent=1))
        return 0

    print(f"# {path.name}（共 {doc.page_count} 页，本次取 {len(rows)} 页）\n")

    if args.map:
        print("| 页 | 首行 |")
        print("| --- | --- |")
        for r in rows:
            flag = " ⚠️无文字层" if r["image_only"] else ""
            print(f"| p{r['page']} | {r['first_line']}{flag} |")
        return 0

    for r in rows:
        head = f"—— p{r['page']} · {r['chars']} 字符 ——"
        print(f"\n{head}")
        if r["image_only"]:
            print("（本页几乎无文字层：可能是纯图片页，需 OCR 或多模态直读；引用页码前先确认）")
            continue
        print(r["text"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
