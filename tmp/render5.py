import fitz, os
from PIL import Image, ImageDraw, ImageFont
pdf = r"tmp\texbuild-optics\第五章-杨氏双缝与云母片-精讲-20261027.pdf"
out = r"tmp\lec_final2"
os.makedirs(out, exist_ok=True)
d = fitz.open(pdf)
font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 22)
ims = []
for n in [1, 2, 12, 13]:
    f = os.path.join(out, f"p{n:02d}.png")
    d[n-1].get_pixmap(dpi=120).save(f)
    im = Image.open(f)
    w = 720
    ims.append((f"p{n:02d}", im.resize((w, int(im.height*w/im.width)), Image.LANCZOS)))
ch = max(im.height for _, im in ims)
sheet = Image.new("RGB", (720*2, (ch+26)*2), "white")
dr = ImageDraw.Draw(sheet)
for k, (nm, im) in enumerate(ims):
    cx, cy = (k % 2)*720, (k // 2)*(ch+26)
    dr.text((cx+4, cy+2), nm, fill="red", font=font)
    sheet.paste(im, (cx, cy+26))
sheet.save(os.path.join(out, "check2.png"))
print(sheet.size)
