import fitz, os
from PIL import Image, ImageDraw, ImageFont
pdf = r"tmp\texbuild-optics\第五章-杨氏双缝与云母片-精讲-20261027.pdf"
out = r"tmp\lec_preview2"
os.makedirs(out, exist_ok=True)
d = fitz.open(pdf)
for n in [2,3,5,7,13,14]:
    d[n-1].get_pixmap(dpi=130).save(os.path.join(out, f"p{n:02d}.png"))
font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 24)
ims = []
for n in [2,3,5,7,13,14]:
    im = Image.open(os.path.join(out, f"p{n:02d}.png"))
    r = 740/im.width
    ims.append((f"p{n:02d}", im.resize((740, int(im.height*r)), Image.LANCZOS)))
ch = max(im.height for _, im in ims)
sheet = Image.new("RGB", (740*2, (ch+28)*3), "white")
dr = ImageDraw.Draw(sheet)
for k, (name, im) in enumerate(ims):
    cx, cy = (k % 2)*740, (k // 2)*(ch+28)
    dr.text((cx+4, cy+2), name, fill="red", font=font)
    sheet.paste(im, (cx, cy+28))
sheet.save(os.path.join(out, "check.png"))
print(sheet.size)
