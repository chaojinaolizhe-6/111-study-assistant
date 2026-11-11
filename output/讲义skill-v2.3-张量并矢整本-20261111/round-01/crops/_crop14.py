import sys
from PIL import Image
src = sys.argv[1]; out = sys.argv[2]
im = Image.open(f"{src}/page-023.png").convert("RGB")
c = im.crop((405, 725, 465, 775)).resize((60*20,50*20), Image.LANCZOS)
c.save(f"{out}/p23_tip.png"); print(c.size)
