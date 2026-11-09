import fitz, os
d=fitz.open(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\final.pdf")
print("pages",len(d),d[0].rect)
os.makedirs(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\fpv",exist_ok=True)
for i,pg in enumerate(d):
    pg.get_pixmap(dpi=110).save(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\fpv\p%d.png"%(i+1))
