import sys
from PIL import Image
src = sys.argv[1]; out = sys.argv[2]
jobs = [
 ("p32_Jmatrix", "page-032.png", (150, 380, 760, 570), 3),
 ("p33_rod", "page-033.png", (150, 1010, 760, 1090), 3),
 ("p36_box", "page-036.png", (150, 390, 760, 460), 3),
 ("p37_euler", "page-037.png", (280, 320, 640, 430), 3),
 ("p30_box", "page-030.png", (280, 820, 640, 880), 3),
 ("p24_small", "page-024.png", (430, 540, 760, 610), 3),
]
for name, f, box, scale in jobs:
    im = Image.open(f"{src}/{f}").convert("RGB")
    c = im.crop(box)
    c = c.resize((c.width*scale, c.height*scale), Image.LANCZOS)
    c.save(f"{out}/{name}.png")
    print(name, c.size)
