import sys
from PIL import Image
src = sys.argv[1]; out = sys.argv[2]
im = Image.open(f"{src}/page-021.png").convert("RGB")
c = im.crop((60, 935, 850, 1060)).resize((790*2,125*2), Image.LANCZOS)
c.save(f"{out}/p21_rows.png"); print(c.size)
