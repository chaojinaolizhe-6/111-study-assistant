from PIL import Image
im = Image.open(r'subjects\02-光学\偏振光-数据页3.jpg')
print(im.size)
# crop main data region and upscale
box = (40, 230, 1040, 1000)
c = im.crop(box).resize(((box[2]-box[0])*2, (box[3]-box[1])*2), Image.LANCZOS)
c.save(r'_scratch\data3-main.png')
box2 = (40, 760, 1040, 1200)
c2 = im.crop(box2).resize(((box2[2]-box2[0])*2, (box2[3]-box2[1])*2), Image.LANCZOS)
c2.save(r'_scratch\data3-bottom.png')
print('ok')
