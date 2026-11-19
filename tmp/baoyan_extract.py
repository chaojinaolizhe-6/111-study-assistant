import sys, os, json
import fitz
from docx import Document

out_dir = r"D:\aaa_D_usual\DSH\111学习助手\tmp\baoyan"

def dump_pdf(path, tag):
    doc = fitz.open(path)
    parts = []
    for i, page in enumerate(doc):
        t = page.get_text("text")
        parts.append(f"\n===== [PDF p{i+1}] =====\n{t}")
    txt = "".join(parts)
    dst = os.path.join(out_dir, tag + ".txt")
    with open(dst, "w", encoding="utf-8") as f:
        f.write(txt)
    print(f"{tag}: pages={doc.page_count} chars={len(txt)} -> {dst}")

def dump_docx(path, tag):
    d = Document(path)
    lines = []
    for p in d.paragraphs:
        if p.text.strip():
            lines.append(p.text)
    for ti, tbl in enumerate(d.tables):
        lines.append(f"\n--- TABLE {ti+1} ---")
        for row in tbl.rows:
            cells = [c.text.replace("\n", " ").strip() for c in row.cells]
            lines.append(" | ".join(cells))
    txt = "\n".join(lines)
    dst = os.path.join(out_dir, tag + ".txt")
    with open(dst, "w", encoding="utf-8") as f:
        f.write(txt)
    print(f"{tag}: paras={len(d.paragraphs)} tables={len(d.tables)} chars={len(txt)} -> {dst}")

os.makedirs(out_dir, exist_ok=True)

dump_docx(r"C:\Users\M\Desktop\保研政策.docx", "desktop-baoyan-policy")
dump_pdf(r"C:\Users\M\Desktop\MMM DAILY\DELVING\政策\保研\附件1：中白学院2022级、2023级推荐优秀应届毕业生免试攻读研究生工作实施办法(2).pdf", "zhongbai-2022-2023")
