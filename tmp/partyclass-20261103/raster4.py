import fitz
d=fitz.open(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\terms4.pdf")
print("pages",len(d))
d[len(d)-1].get_pixmap(dpi=110).save(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\tpv\s_last.png")
