import sys
from PIL import Image
src = sys.argv[1]; out = sys.argv[2]
jobs = [
 ("p33_fig6_big", "page-033.png", (250, 715, 620, 830), 5),
 ("p35_fig7_left", "page-035.png", (180, 760, 470, 900), 4),
 ("p35_fig7_right", "page-035.png", (480, 760, 760, 900), 4),
 ("p34_cos2", "page-034.png", (200, 1145, 760, 1195), 5),
 ("p27_top2", "page-027.png", (60, 62, 850, 120), 4),
 ("p25_fig4_big", "page-025.png", (350, 235, 560, 340), 6),
 ("p23_fig3_big", "page-023.png", (360, 630, 560, 760), 6),
]
for name, f, box, scale in jobs:
    im = Image.open(f"{src}/{f}").convert("RGB")
    c = im.crop(box)
    c = c.resize((c.width*scale, c.height*scale), Image.LANCZOS)
    c.save(f"{out}/{name}.png")
    print(name, c.size)
