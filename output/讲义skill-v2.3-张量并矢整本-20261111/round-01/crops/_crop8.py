import sys
from PIL import Image
src = sys.argv[1]; out = sys.argv[2]
jobs = [
 ("p38_fig8", "page-038.png", (340, 250, 560, 400), 5),
 ("p33_bullets", "page-033.png", (75, 660, 700, 740), 3),
 ("p35_head5", "page-035.png", (60, 470, 850, 560), 3),
 ("p35_tail", "page-035.png", (60, 830, 850, 900), 3),
 ("p36_mid", "page-036.png", (60, 880, 850, 960), 3),
]
for name, f, box, scale in jobs:
    im = Image.open(f"{src}/{f}").convert("RGB")
    c = im.crop(box)
    c = c.resize((c.width*scale, c.height*scale), Image.LANCZOS)
    c.save(f"{out}/{name}.png")
    print(name, c.size)
