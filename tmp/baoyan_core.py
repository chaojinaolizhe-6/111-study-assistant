import os
from docx import Document

out_dir = r"D:\aaa_D_usual\DSH\111学习助手\tmp\baoyan"
path = r"C:\Users\M\Desktop\在办\评奖学金\附件3：2025-2026学年中白学院奖学金评审细则（2024级及以下）\附件1：中白学院学业成绩认定课程清单（核心课程清单）.docx"

d = Document(path)
lines = []
for p in d.paragraphs:
    if p.text.strip():
        lines.append(p.text)
for ti, tbl in enumerate(d.tables):
    lines.append(f"\n--- TABLE {ti+1} ---")
    for row in tbl.rows:
        lines.append(" | ".join(c.text.replace("\n", " ").strip() for c in row.cells))
txt = "\n".join(lines)
dst = os.path.join(out_dir, "core-course-list.txt")
open(dst, "w", encoding="utf-8").write(txt)
print("paras=", len(d.paragraphs), "tables=", len(d.tables), "chars=", len(txt))
print(txt[:3000])
