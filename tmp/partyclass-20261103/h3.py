import fitz, os
d=fitz.open(r"D:\aaa_D_usual\DSH\111学习助手\入党\马泽宇-20251091006-党课心得体会-定稿.pdf")
os.makedirs(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\h3",exist_ok=True)
for i in (1,2):
    d[i].get_pixmap(dpi=110).save(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\h3\p%d.png"%(i+1))
print("ok")
