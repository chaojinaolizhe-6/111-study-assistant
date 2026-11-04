import fitz
src=r"D:\aaa_D_usual\DSH\111学习助手\subjects\06-电工电子技术\实验\教材-电工学实验教程-刘凤春-第2版.pdf"
doc=fitz.open(src)
p=doc[163]
pix=p.get_pixmap(dpi=420, clip=fitz.Rect(150, 440, 330, 640))
pix.save(r"D:\aaa_D_usual\DSH\111学习助手\tmp\ee-textbook\fig524-left.png")
print(pix.width, pix.height)
doc.close()
