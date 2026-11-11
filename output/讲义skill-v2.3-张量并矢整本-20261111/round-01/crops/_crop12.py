import sys, numpy as np
from PIL import Image, ImageEnhance
src = sys.argv[1]; out = sys.argv[2]
im = Image.open(f"{src}/page-038.png").convert("RGB")
c = im.crop((330, 250, 580, 420))
# strong contrast stretch on the light end to reveal faint strokes
a = np.array(c).astype(np.float32)/255.0
a = np.clip((a-0.94)/(1.0-0.94), 0, 1)  # anything darker than 0.94 -> visible
Image.fromarray((a*255).astype(np.uint8)).resize((250*5,170*5), Image.LANCZOS).save(f"{out}/p38_faint.png")
print("ok")
