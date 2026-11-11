import sys
from PIL import Image
src = sys.argv[1]; out = sys.argv[2]
jobs = [
 ("p21_tab", "page-021.png", (60, 845, 850, 1000), 2),
 ("p29_sums", "page-029.png", (120, 330, 800, 480), 2),
 ("p34_para", "page-034.png", (60, 360, 850, 560), 2),
 ("p36_top", "page-036.png", (60, 95, 850, 300), 2),
 ("p37_top", "page-037.png", (60, 95, 850, 260), 2),
]
for name, f, box, scale in jobs:
    im = Image.open(f"{src}/{f}").convert("RGB")
    c = im.crop(box)
    c = c.resize((c.width*scale, c.height*scale), Image.LANCZOS)
    c.save(f"{out}/{name}.png")
    print(name, c.size)
