import os
from PIL import Image, ImageDraw, ImageFont
src = r"_scratch\interf-pages"
files = sorted(f for f in os.listdir(src) if f.endswith(".png"))
cell_w = 640
cols, rows = 3, 3
per = cols*rows
try:
    font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 28)
except Exception:
    font = ImageFont.load_default()
for s in range(0, len(files), per):
    chunk = files[s:s+per]
    ims = []
    for f in chunk:
        im = Image.open(os.path.join(src, f))
        r = cell_w / im.width
        im = im.resize((cell_w, int(im.height*r)), Image.LANCZOS)
        ims.append((f, im))
    ch = max(im.height for _, im in ims)
    sheet = Image.new("RGB", (cols*cell_w, rows*(ch+34)), "white")
    d = ImageDraw.Draw(sheet)
    for k, (f, im) in enumerate(ims):
        cx = (k % cols)*cell_w
        cy = (k // cols)*(ch+34)
        d.text((cx+6, cy+2), f.replace(".png",""), fill="red", font=font)
        sheet.paste(im, (cx, cy+34))
    out = os.path.join("tmp", f"sheet_{s//per+1:02d}.png")
    sheet.save(out)
    print(out, sheet.size)
