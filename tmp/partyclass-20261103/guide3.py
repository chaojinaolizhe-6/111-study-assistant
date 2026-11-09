import fitz
d=fitz.open(r"D:\aaa_D_usual\DSH\111学习助手\入党\党课心得体会-审稿清单-20261105.pdf")
print("pages",len(d))
for i,pg in enumerate(d):
    pg.get_pixmap(dpi=105).save(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\guide\q%d.png"%(i+1))
