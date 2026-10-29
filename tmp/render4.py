import fitz, os
from PIL import Image, ImageDraw, ImageFont
pdf = r"tmp\texbuild-optics\第五章-杨氏双缝与云母片-精讲-20261027.pdf"
out = r"tmp\lec_preview4"
os.makedirs(out, exist_ok=True)
d = fitz.open(pdf)
for n in [15, 16]:
    d[n-1].get_pixmap(dpi=140).save(os.path.join(out, f"p{n:02d}.png"))
font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 22)
ims = [(f"p{n:02d}", Image.open(os.path.join(out, f"p{n:02d}.png"))) for n in [15,16]]
w = 700
ims = [(nm, im.resize((w, int(im.height*w/im.width)), Image.LANCZOS)) for nm, im in ims]
ch = max(im.height for _, im in ims)
sheet = Image.new("RGB", (w*2, ch+26), "white")
dr = ImageDraw.Draw(sheet)
for k, (nm, im) in enumerate(ims):
    dr.text((k*w+4, 2), nm, fill="red", font=font)
    sheet.paste(im, (k*w, 26))
sheet.save(os.path.join(out, "last.png"))
print(sheet.size)
