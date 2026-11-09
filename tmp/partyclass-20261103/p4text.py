import fitz
d=fitz.open(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\final3.pdf")
print("pages",len(d))
pg=d[3]
print("page4 text:")
print(pg.get_text()[:300])
