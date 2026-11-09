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

默认读全文；显式 --max-chars N 才截断，并标明省略长度。
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
    if total < 1:
        raise ValueError("PDF 没有可读取的页面")
    out: set[int] = set()
    for chunk in spec.split(","):
        chunk = chunk.strip()
        match = re.fullmatch(r"(\d+)(?:\s*-\s*(\d+))?", chunk)
        if not match:
            raise ValueError(f"无效页码片段：{chunk!r}；请使用 1-3,5 这样的格式")
        lo, hi = int(match.group(1)), int(match.group(2) or match.group(1))
        if lo > hi:
            raise ValueError(f"页码范围倒置：{chunk}")
        if lo < 1 or hi > total:
            raise ValueError(f"页码越界：{chunk}；本文件有效页码为 1-{total}")
        out.update(range(lo - 1, hi))
    return sorted(out)


def _clean(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(description="课件 PDF 逐页取文字 / 页码速查表")
    ap.add_argument("pdf")
    ap.add_argument("--pages", help="页码区间（1 起）：28-38,50；省略则全书")
    ap.add_argument("--map", action="store_true", help="只输出「页号 → 首行」速查表")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--max-chars", type=int, default=None, help="显式限制每页字符数；默认全文，限长时报告省略长度")
    args = ap.parse_args(argv)
    if args.max_chars is not None and args.max_chars < 1:
        ap.error("--max-chars 必须为正整数；省略此参数即读取全文")

    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("需要 PyMuPDF：python -m pip install pymupdf", file=sys.stderr)
        return 2

    path = Path(args.pdf)
    if not path.is_file():
        print(f"找不到文件：{path}", file=sys.stderr)
        return 2

    rows = []
    try:
        with fitz.open(path) as doc:
            total = doc.page_count
            if total < 1:
                raise ValueError("PDF 没有可读取的页面")
            pages = _parse_pages(args.pages, total) if args.pages is not None else list(range(total))
            for idx in pages:
                raw = _clean(doc[idx].get_text())
                first = next((ln.strip() for ln in raw.splitlines() if ln.strip()), "")
                selected = raw if args.max_chars is None else raw[:args.max_chars]
                rows.append({"page": idx + 1, "chars": len(raw), "first_line": first[:90],
                             "text": selected, "returned_chars": len(selected),
                             "truncated": len(selected) < len(raw),
                             "omitted_chars": len(raw) - len(selected), "image_only": len(raw) < 20})
    except Exception as exc:
        print(f"读取失败：{path}：{exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps({"file": str(path), "total_pages": total, "max_chars": args.max_chars, "pages": rows}, ensure_ascii=False, indent=1))
        return 0

    print(f"# {path.name}（共 {total} 页，本次取 {len(rows)} 页）\n")

    if args.map:
        print("| 页 | 首行 |")
        print("| --- | --- |")
        for r in rows:
            flag = " ⚠️无文字层" if r["image_only"] else ""
            if r["truncated"]:
                flag += f" [正文截断：省略 {r['omitted_chars']} 字符]"
            print(f"| p{r['page']} | {r['first_line']}{flag} |")
        return 0

    for r in rows:
        head = f"—— p{r['page']} · {r['chars']} 字符 ——"
        print(f"\n{head}")
        if r["image_only"]:
            print("（本页几乎无文字层：可能是纯图片页，需 OCR 或多模态直读；引用页码前先确认）")
        print(r["text"])
        if r["truncated"]:
            print(f"[已截断：返回 {r['returned_chars']}/{r['chars']} 字符，省略 {r['omitted_chars']} 字符；去掉 --max-chars 读取全文。]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
