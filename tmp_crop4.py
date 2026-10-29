from PIL import Image
im = Image.open(r'subjects\02-光学\偏振光-数据页3.jpg')
# region around middle row right end and bottom row left end
c = im.crop((600, 400, 1080, 640)).resize((1920, 960), Image.LANCZOS)
c.save(r'_scratch\data3-mid.png')
c = im.crop((30, 560, 500, 720)).resize((1880, 640), Image.LANCZOS)
c.save(r'_scratch\data3-lowleft.png')
print('ok')
