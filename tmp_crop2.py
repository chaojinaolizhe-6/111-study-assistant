from PIL import Image
im = Image.open(r'subjects\02-光学\偏振光-数据页3.jpg')
crops = {
 'data3-topright': (600, 180, 1080, 420),
 'data3-rows': (40, 380, 1080, 700),
 'data3-bottom2': (40, 880, 1080, 1300),
}
for name,box in crops.items():
    c = im.crop(box)
    c = c.resize((c.width*3, c.height*3), Image.LANCZOS)
    c.save(fr'_scratch\{name}.png'); print(name, c.size)
im1 = Image.open(r'subjects\02-光学\偏振光-数据页1.jpg')
print(im1.size)
c = im1.crop((0, 0, 1080, 900)).resize((2160,1800), Image.LANCZOS)
c.save(r'_scratch\data1-top.png'); print('data1-top', c.size)
