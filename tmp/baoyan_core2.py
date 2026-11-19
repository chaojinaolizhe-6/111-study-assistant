# -*- coding: utf-8 -*-
import io, sys
from docx import Document

path = r"C:\Users\M\Desktop\在办\评奖学金\附件3：2025-2026学年中白学院奖学金评审细则（2024级及以下）\附件1：中白学院学业成绩认定课程清单（核心课程清单）.docx"
d = Document(path)
out = []
for ti, tbl in enumerate(d.tables):
    out.append(f"\n########## TABLE {ti+1}: rows={len(tbl.rows)} cols={len(tbl.columns)} ##########")
    for ri, row in enumerate(tbl.rows):
        cells = [c.text.replace("\n", " ").strip() for c in row.cells]
        # dedupe horizontally merged repeats
        dedup = []
        for c in cells:
            if not dedup or dedup[-1] != c:
                dedup.append(c)
        line = " | ".join(dedup)
        if any(k in line for k in ("思政", "选修", "Required 16", "学分")) or ri < 4:
            out.append(f"[r{ri}] {line}")
txt = "\n".join(out)
open(r"D:\aaa_D_usual\DSH\111学习助手\tmp\baoyan\core-rows.txt", "w", encoding="utf-8").write(txt)
print(txt)
