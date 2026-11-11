import sys
from PIL import Image
src = sys.argv[1]; out = sys.argv[2]
jobs = [
 ("p22_a", "page-022.png", (60, 360, 850, 620), 2),
 ("p23_a", "page-023.png", (60, 380, 850, 620), 2),
 ("p24_a", "page-024.png", (60, 240, 850, 440), 2),
 ("p26_a", "page-026.png", (60, 300, 850, 520), 2),
]
for name, f, box, scale in jobs:
    im = Image.open(f"{src}/{f}").convert("RGB")
    c = im.crop(box)
    c = c.resize((c.width*scale, c.height*scale), Image.LANCZOS)
    c.save(f"{out}/{name}.png")
    print(name, c.size)
