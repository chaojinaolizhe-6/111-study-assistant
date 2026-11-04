import fitz
src=r"D:\aaa_D_usual\DSH\111学习助手\subjects\06-电工电子技术\实验\实验5-单管放大电路-实验讲义-20261104.pdf"
doc=fitz.open(src)
txt=[]
for i in range(doc.page_count):
    txt.append(f"===== p{i+1} =====\n"+doc[i].get_text())
open(r"D:\aaa_D_usual\DSH\111学习助手\tmp\lab5-text.txt","w",encoding="utf-8").write("\n".join(txt))
print("chars", sum(len(t) for t in txt))
doc.close()
