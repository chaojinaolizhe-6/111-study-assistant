import fitz, os
p=r"D:\aaa_D_usual\DSH\111学习助手\入党\第36期入党积极分子培训-心得体会-马泽宇-20251091006.pdf"
d=fitz.open(p); print("pages",len(d))
os.makedirs(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\final_pv",exist_ok=True)
for i,pg in enumerate(d):
    pg.get_pixmap(dpi=110).save(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\final_pv\p%d.png"%(i+1))
print("ok")
