from PIL import Image
p=r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\final\8635c96bd6edc3c305b0c977fe7322f3.jpg"
im=Image.open(p); print(im.size)
# slide occupies roughly x 620-1110, y 320-750 in 1706x1280
box=(620,300,1120,760)
c=im.crop(box).resize(((box[2]-box[0])*3,(box[3]-box[1])*3), Image.LANCZOS)
c.save(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\crop11.png")
print(c.size)
