import fitz, os
src=r"D:\aaa_D_usual\DSH\111学习助手\subjects\06-电工电子技术\实验\实验5-单管放大电路-实验讲义-20261104.pdf"
out=r"D:\aaa_D_usual\DSH\111学习助手\tmp\lab5-preview"
os.makedirs(out, exist_ok=True)
doc=fitz.open(src)
print("pages", doc.page_count)
for i in range(doc.page_count):
    pix=doc[i].get_pixmap(dpi=100)
    pix.save(os.path.join(out, f"p{i+1:02d}.png"))
doc.close()
print("ok")
