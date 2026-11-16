# -*- coding: utf-8 -*-
"""汇总 round-02 最终文件的页数、页码、哈希，供 verification / manifest 使用。"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import fitz

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
WS = ROOT.parent
SNAP = Path("D:/aaa_D_usual/CODEX/AI-SKILL/output/lecture-overview-20261114/author-r1-working-snapshot")
REVIEW = Path("D:/aaa_D_usual/CODEX/AI-SKILL/output/lecture-overview-20261114")
R04 = Path("D:/aaa_D_usual/DSH/111学习助手/output/讲义skill-v2.3-张量并矢整本-20261111/round-04")


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def info(p: Path) -> dict:
    return {"path": str(p), "bytes": p.stat().st_size, "sha256": sha(p)}


doc = fitz.open(ROOT / "handout.pdf")
pages = doc.page_count


def page_of(needle: str, after: int = 0) -> int | None:
    for i, page in enumerate(doc, 1):
        if i <= after:
            continue
        if needle in re.sub(r"\s+", "", page.get_text()):
            return i
    return None


aux = (ROOT / "handout.aux").read_text(encoding="utf-8", errors="replace")
labels = {k: int(v) for k, v in re.findall(r"\\newlabel\{(ans:P\d+)\}\{\{[^}]*\}\{(\d+)\}", aux)}

# 正文保持区
snap = (SNAP / "handout.tex").read_text(encoding="utf-8")
tex = (ROOT / "handout.tex").read_text(encoding="utf-8")
b0 = snap.find(r"\hdr{§0}{起点：矢量、矩阵与换基}")
b1 = snap.find(r"\callout{\textbf{交付说明。}")
body = snap[b0:b1]

cap = doc[0].search_for("图 0（自绘") or doc[0].search_for("图0（自绘")
caption_bbox = None
if cap:
    top = min(r.y0 for r in cap)
    boxes = [b["bbox"] for b in doc[0].get_text("dict")["blocks"]
             if b["type"] == 0 and top - 2 <= b["bbox"][1] < 795]
    caption_bbox = [round(min(b[0] for b in boxes), 1), round(min(b[1] for b in boxes), 1),
                    round(max(b[2] for b in boxes), 1), round(max(b[3] for b in boxes), 1)]
out = {
    "pages": pages,
    "figure0_page": page_of("图0（自绘"),
    "figure0_caption_bbox": caption_bbox,
    "sec0_page": page_of("起点：矢量、矩阵与换基"),
    "sec4_page": page_of("落点一：转动惯量张量", after=1),
    "sec5_page": page_of("落点二", after=1),
    "sec6_page": page_of("落点三：应力张量", after=1),
    "appendixA_page": page_of("附录A练习详解") or page_of("练习详解"),
    "last_page": pages,
    "answer_pages": {k: labels[k] for k in sorted(labels, key=lambda s: int(s.split("P")[1]))},
    "body_preserved": {"chars": len(body), "sha256": hashlib.sha256(body.encode()).hexdigest()},
    "artifacts": {
        "handout.tex": info(ROOT / "handout.tex"),
        "handout.pdf": info(ROOT / "handout.pdf"),
        "handout.log": info(ROOT / "handout.log"),
        "handout.aux": info(ROOT / "handout.aux"),
    },
    "baselines": {
        "snapshot/handout.tex": info(SNAP / "handout.tex"),
        "snapshot/handout.pdf": info(SNAP / "handout.pdf"),
        "snapshot/handout.log": info(SNAP / "handout.log"),
        "snapshot/handout.aux": info(SNAP / "handout.aux"),
        "snapshot/snapshot.json": info(SNAP / "snapshot.json"),
        "round-01/handout.tex": info(WS / "round-01" / "handout.tex"),
        "round-01/handout.pdf": info(WS / "round-01" / "handout.pdf"),
        "round-04/handout.tex": info(R04 / "handout.tex"),
        "round-04/handout.pdf": info(R04 / "handout.pdf"),
        "rule/SKILL.md": info(WS / ".dsh/skills/lecture-deepdive/SKILL.md"),
        "rule/theme-violet.tex": info(WS / ".dsh/skills/lecture-deepdive/assets/theme-violet.tex"),
        "rule/check_handout.py": info(WS / ".dsh/skills/lecture-deepdive/scripts/check_handout.py"),
        "tools/verify_math.py": info(WS / "tools" / "verify_math.py"),
        "AGENTS.md": info(WS / "AGENTS.md"),
        "review/source-reading-review.json": info(REVIEW / "source-reading-review.json"),
        "review/math-overview-review.json": info(REVIEW / "math-overview-review.json"),
        "review/overview-working-visual-review.json": info(REVIEW / "review-visual" / "overview-working-visual-review.json"),
    },
}
print(json.dumps(out, ensure_ascii=False, indent=2))
