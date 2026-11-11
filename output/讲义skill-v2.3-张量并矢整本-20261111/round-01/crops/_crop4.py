import sys
from PIL import Image
src = sys.argv[1]; out = sys.argv[2]
jobs = [
 ("p34_cos3", "page-034.png", (300, 1150, 620, 1195), 8),
 ("p27_head", "page-027.png", (50, 40, 860, 200), 3),
 ("p23_fig3_c", "page-023.png", (380, 655, 540, 745), 8),
 ("p25_fig4_c", "page-025.png", (380, 250, 520, 330), 8),
]
for name, f, box, scale in jobs:
    im = Image.open(f"{src}/{f}").convert("RGB")
    c = im.crop(box)
    c = c.resize((c.width*scale, c.height*scale), Image.LANCZOS)
    c.save(f"{out}/{name}.png")
    print(name, c.size)
