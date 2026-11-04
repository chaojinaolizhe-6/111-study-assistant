import fitz
src=r"D:\aaa_D_usual\DSH\111学习助手\subjects\06-电工电子技术\实验\教材-电工学实验教程-刘凤春-第2版.pdf"
doc=fitz.open(src)
p=doc[163]
pix=p.get_pixmap(dpi=300, clip=fitz.Rect(135,470,540,762))
pix.save(r"D:\aaa_D_usual\DSH\111学习助手\subjects\06-电工电子技术\实验\图-实验5-教材图524-裁剪.png")
print(pix.width, pix.height)
doc.close()
