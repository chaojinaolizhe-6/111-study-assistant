# -*- coding: utf-8 -*-
"""比较 round-02 PDF 与字节锁定快照 PDF 的正文文本（忽略页眉页脚、页码与换行）。"""
from __future__ import annotations
import re
import sys
from pathlib import Path
import fitz

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
NEW = fitz.open(ROOT / "handout.pdf")
OLD = fitz.open(Path("D:/aaa_D_usual/CODEX/AI-SKILL/output/lecture-overview-20261114/"
                     "author-r1-working-snapshot/handout.pdf"))


def body_text(doc):
    pages = []
    for page in doc:
        t = page.get_text()
        lines = [ln for ln in t.split("\n") if ln.strip()]
        # 去掉书眉与页脚
        lines = [ln for ln in lines if not ln.startswith("专题·从张量到并矢")
                 and ln.strip() != "理论力学"
                 and not re.fullmatch(r":\s*\d+\s*:", ln.strip())]
        pages.append("\n".join(lines))
    full = "\n".join(pages)
    i = full.find("起点：矢量、矩阵与换基")
    return re.sub(r"\s+", "", full[i:])


a = body_text(NEW)
b = body_text(OLD)
print("new len", len(a), "old len", len(b), "equal", a == b)
if a != b:
    n = min(len(a), len(b))
    k = next((i for i in range(n) if a[i] != b[i]), n)
    print("first diff at", k)
    print("new context:", a[max(0, k - 40):k + 60])
    print("old context:", b[max(0, k - 40):k + 60])
    # 找出差异数量
    diffs = [(i, a[i], b[i]) for i in range(min(len(a), len(b))) if a[i] != b[i]]
    print("diff count", len(diffs), diffs[:10])
print("new pages", NEW.page_count, "old pages", OLD.page_count)
