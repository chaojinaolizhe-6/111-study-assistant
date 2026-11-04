import fitz, os
src=r"D:\aaa_D_usual\DSH\111学习助手\subjects\06-电工电子技术\实验\教材-电工学实验教程-刘凤春-第2版.pdf"
out=r"D:\aaa_D_usual\DSH\111学习助手\tmp\ee-textbook"
os.makedirs(out, exist_ok=True)
doc=fitz.open(src)
print("pages", doc.page_count, "size", doc[0].rect)
for n in (8,9,10):
    p=doc[n-1]
    pix=p.get_pixmap(dpi=150)
    f=os.path.join(out, f"toc-p{n:03d}.png")
    pix.save(f)
    print(f, pix.width, pix.height)
doc.close()
