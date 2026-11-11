import sys
from PIL import Image
src = sys.argv[1]; out = sys.argv[2]
jobs = [
 ("p20_a", "page-020.png", (60, 95, 850, 400), 2),
 ("p20_b", "page-020.png", (60, 400, 850, 700), 2),
 ("p20_c", "page-020.png", (60, 700, 850, 1000), 2),
 ("p20_d", "page-020.png", (60, 1000, 850, 1180), 2),
]
for name, f, box, scale in jobs:
    im = Image.open(f"{src}/{f}").convert("RGB")
    c = im.crop(box)
    c = c.resize((c.width*scale, c.height*scale), Image.LANCZOS)
    c.save(f"{out}/{name}.png")
    print(name, c.size)
