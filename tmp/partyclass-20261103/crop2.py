from PIL import Image
p=r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\final\e7412b1fc4ede3dc1d712cc8c985772d.jpg"
im=Image.open(p); print(im.size)
box=(280,470,900,960)
c=im.crop(box).resize(((box[2]-box[0])*3,(box[3]-box[1])*3), Image.LANCZOS)
c.save(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\crop08.png")
print(c.size)
