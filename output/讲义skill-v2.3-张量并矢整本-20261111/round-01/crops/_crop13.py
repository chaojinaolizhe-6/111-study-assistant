import sys
from PIL import Image
src = sys.argv[1]; out = sys.argv[2]
im = Image.open(f"{src}/page-025.png").convert("RGB")
c = im.crop((430, 270, 520, 330)).resize((90*14,60*14), Image.LANCZOS)
c.save(f"{out}/p25_foot.png"); print(c.size)
im2 = Image.open(f"{src}/page-023.png").convert("RGB")
c2 = im2.crop((420, 690, 500, 740)).resize((80*14,50*14), Image.LANCZOS)
c2.save(f"{out}/p23_purple_end.png"); print(c2.size)
