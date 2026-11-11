import sys
from PIL import Image
src = sys.argv[1]; out = sys.argv[2]
jobs = [
 ("p23_fig3", "page-023.png", (330, 600, 600, 800), 3),
 ("p25_fig4", "page-025.png", (330, 210, 600, 350), 3),
 ("p29_fig5", "page-029.png", (240, 60, 640, 260), 3),
 ("p33_fig6", "page-033.png", (240, 700, 640, 830), 3),
 ("p35_fig7", "page-035.png", (150, 730, 780, 910), 2),
 ("p34_cos", "page-034.png", (150, 1120, 780, 1210), 3),
 ("p27_top", "page-027.png", (60, 60, 850, 130), 3),
 ("p27_bottom", "page-027.png", (60, 800, 850, 900), 2),
 ("p21_table", "page-021.png", (60, 840, 850, 990), 2),
]
for name, f, box, scale in jobs:
    im = Image.open(f"{src}/{f}").convert("RGB")
    c = im.crop(box)
    c = c.resize((c.width*scale, c.height*scale), Image.LANCZOS)
    c.save(f"{out}/{name}.png")
    print(name, c.size)
