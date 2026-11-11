import sys
from PIL import Image
src = sys.argv[1]; out = sys.argv[2]
im = Image.open(f"{src}/page-034.png").convert("RGB")
print(im.size)
# find the vertical extent: crop wide band
for i,(box,scale) in enumerate([((300,1175,430,1210),14), ((430,1175,570,1210),14)]):
    c = im.crop(box); c = c.resize((c.width*scale, c.height*scale), Image.LANCZOS)
    c.save(f"{out}/p34_den{i}.png"); print(c.size)
