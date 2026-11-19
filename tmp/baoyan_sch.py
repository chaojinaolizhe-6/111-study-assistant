# -*- coding: utf-8 -*-
import os
from docx import Document
import fitz

out = r"D:\aaa_D_usual\DSH\111学习助手\tmp\baoyan"

docs = [
    (r"C:\Users\M\Desktop\在办\评奖学金\附件2：2025-2026学年中白学院奖学金评审细则（2023级）\2025-2026学年中白学院优秀学生奖学金评审细则.docx", "scholarship-2023.docx.txt"),
    (r"C:\Users\M\Desktop\在办\评奖学金\附件3：2025-2026学年中白学院奖学金评审细则（2024级及以下）\2025-2026学年中白学院荣誉评选实施细则.docx", "honor-2024.docx.txt"),
]
for path, tag in docs:
    if not os.path.exists(path):
        print("MISSING", path); continue
    d = Document(path)
    lines = [p.text for p in d.paragraphs if p.text.strip()]
    for t in d.tables:
        for row in t.rows:
            lines.append(" | ".join(c.text.replace("\n", " ").strip() for c in row.cells))
    txt = "\n".join(lines)
    open(os.path.join(out, tag), "w", encoding="utf-8").write(txt)
    print(tag, len(txt))
    for ln in lines:
        if any(k in ln for k in ("学习成绩", "必修", "选修", "学分绩", "加权", "智育")):
            print("   >", ln[:200])
