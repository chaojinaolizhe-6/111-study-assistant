import sys
from PIL import Image
src = sys.argv[1]; out = sys.argv[2]
im = Image.open(f"{src}/page-034.png").convert("RGB")
c = im.crop((330,1178,420,1204)).resize((90*20,26*20), Image.LANCZOS)
c.save(f"{out}/p34_den_big.png"); print(c.size)
im2 = Image.open(f"{src}/page-035.png").convert("RGB")
c2 = im2.crop((285,100,520,140)).resize((235*8,40*8), Image.LANCZOS)
c2.save(f"{out}/p35_absL.png"); print(c2.size)
