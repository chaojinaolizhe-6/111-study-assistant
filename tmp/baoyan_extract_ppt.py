import os
from pptx import Presentation

out_dir = r"D:\aaa_D_usual\DSH\111学习助手\tmp\baoyan"
os.makedirs(out_dir, exist_ok=True)

def dump(path, tag):
    prs = Presentation(path)
    lines = []
    for i, slide in enumerate(prs.slides, 1):
        texts = []
        for shape in slide.shapes:
            if shape.has_text_frame:
                t = shape.text_frame.text.strip()
                if t:
                    texts.append(t)
            if getattr(shape, "has_table", False) and shape.has_table:
                for row in shape.table.rows:
                    texts.append(" | ".join(c.text.strip().replace("\n", " ") for c in row.cells))
        lines.append(f"\n===== [slide {i}] =====\n" + "\n".join(texts))
    txt = "\n".join(lines)
    dst = os.path.join(out_dir, tag + ".txt")
    open(dst, "w", encoding="utf-8").write(txt)
    print(tag, "slides=", len(prs.slides), "chars=", len(txt), "->", dst)

dump(r"C:\Users\M\Downloads\2025.09.09_中白学院教学事务说明.pptx", "jiaoxue-shiwu")
dump(r"C:\Users\M\Downloads\选课相关问题解读.pptx", "xuanke-jiedu")
