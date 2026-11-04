import fitz
p=r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\xinde.pdf"
d=fitz.open(p)
print("pages", len(d), "size", d[0].rect)
pg=d[0]
bl=pg.get_text("dict")
for b in bl["blocks"][:3]:
    for l in b.get("lines", [])[:2]:
        for s in l["spans"][:2]:
            print(round(s["size"],1), s["font"], s["bbox"], s["text"][:20])
