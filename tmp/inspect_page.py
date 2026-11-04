import fitz
src=r"D:\aaa_D_usual\DSH\111学习助手\subjects\06-电工电子技术\实验\教材-电工学实验教程-刘凤春-第2版.pdf"
doc=fitz.open(src)
p=doc[164]
for b in p.get_text("blocks"):
    print("TEXT", [round(v,1) for v in b[:4]], b[4][:40].replace("\n"," "))
print("images:")
for img in p.get_images(full=True):
    print(img)
print("drawings count", len(p.get_drawings()))
# bbox of largest image via get_image_bbox
for img in p.get_images(full=True):
    try:
        print("bbox", img[0], p.get_image_bbox(img))
    except Exception as e:
        print("err", e)
doc.close()
