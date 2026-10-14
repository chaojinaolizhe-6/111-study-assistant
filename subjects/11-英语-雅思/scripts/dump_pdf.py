"""导出 PDF 文字到控制台或文件（只读）。

用法：
    python -B subjects/11-英语-雅思/scripts/dump_pdf.py <路径关键词> [--pages a-b] [--max 4000]
    python -B subjects/11-英语-雅思/scripts/dump_pdf.py <关键词> --save 输出名.txt
"""
from __future__ import annotations

import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[3]
MAT = ROOT / "subjects" / "11-英语-雅思" / "资料"


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1
    key = args[0]
    pages = None
    mx = 4000
    save = None
    i = 1
    while i < len(args):
        if args[i] == "--pages":
            part = args[i + 1]
            if "-" in part:
                a, b = part.split("-")
                pages = (int(a), int(b))
            else:
                pages = (int(part), int(part))
            i += 2
        elif args[i] == "--max":
            mx = int(args[i + 1])
            i += 2
        elif args[i] == "--save":
            save = args[i + 1]
            i += 2
        else:
            i += 1

    hits = [p for p in MAT.rglob("*.pdf") if key.lower() in p.name.lower()]
    if not hits:
        print("no match for", key)
        print("available:")
        for p in sorted(MAT.rglob("*.pdf")):
            print("   ", p.name[:90])
        return 1
    p = hits[0]
    print(f"### {p.relative_to(ROOT)}")
    with fitz.open(p) as doc:
        rng = range(pages[0] - 1, min(pages[1], doc.page_count)) if pages else range(doc.page_count)
        out = []
        for n in rng:
            out.append(f"\n----- page {n + 1} -----")
            out.append(doc[n].get_text())
        text = "\n".join(out)
    if save:
        (MAT / save).write_text(text, encoding="utf-8")
        print(f"saved {len(text)} chars -> {save}")
    else:
        print(text[:mx])
        if len(text) > mx:
            print(f"\n... [{len(text)} chars total, truncated]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
