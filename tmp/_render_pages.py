import os, fitz
os.makedirs(r"tmp\pages", exist_ok=True)
jobs = [
    (r"subjects\07-俄语\课件\УРОК 1. Алфавит(3).pdf", [28, 29, 30], "u1"),
    (r"subjects\07-俄语\课件\УРОК 2. Твердые и мягкие согласные звуки. Оглушение. Озвончение. Диалоги.pdf", [19, 20, 26], "u2"),
    (r"subjects\07-俄语\课件\УРОК 3. Глухие и звонкие согласные звуки. Ритмика. ИК-3.pdf", [16], "u3"),
    (r"subjects\07-俄语\课件\УРОК 4. Имя существительное. Род.pdf", [7, 13, 17], "u4"),
    (r"subjects\07-俄语\课件\УРОК 6. Личные и притяжательные местоимения.pdf", [6], "u6"),
]
for path, pages, tag in jobs:
    doc = fitz.open(path)
    for p in pages:
        if p < 1 or p > doc.page_count: continue
        pix = doc[p-1].get_pixmap(matrix=fitz.Matrix(1.6, 1.6))
        out = rf"tmp\pages\{tag}_p{p}.png"
        pix.save(out)
        print(out, pix.width, pix.height)
