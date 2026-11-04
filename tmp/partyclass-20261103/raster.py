import fitz
d=fitz.open(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\xinde2.pdf")
print("pages",len(d),d[0].rect)
for i,pg in enumerate(d):
    pix=pg.get_pixmap(dpi=120)
    pix.save(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\pv\p%d.png"%(i+1))
print("ok")
