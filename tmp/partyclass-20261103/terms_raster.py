import fitz, os
d=fitz.open(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\terms.pdf")
print("pages",len(d), d[0].rect)
os.makedirs(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\tpv",exist_ok=True)
for i in [0,1]:
    d[i].get_pixmap(dpi=110).save(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\tpv\p%d.png"%(i+1))
