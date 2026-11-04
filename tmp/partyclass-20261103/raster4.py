import fitz, os
d=fitz.open(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\xinde4.pdf")
print("pages",len(d))
os.makedirs(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\pv4",exist_ok=True)
for i,pg in enumerate(d):
    pg.get_pixmap(dpi=110).save(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\pv4\p%d.png"%(i+1))
