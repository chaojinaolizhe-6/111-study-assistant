import fitz, os
from PIL import Image, ImageDraw, ImageFont
pdf = r"tmp\texbuild-optics\第五章-杨氏双缝与云母片-精讲-20261027.pdf"
out = r"tmp\lec_final"
os.makedirs(out, exist_ok=True)
d = fitz.open(pdf)
font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 20)
files = []
for i in range(d.page_count):
    f = os.path.join(out, f"p{i+1:02d}.png")
    d[i].get_pixmap(dpi=110).save(f)
    files.append(f)
w = 520
for s in range(0, len(files), 8):
    chunk = files[s:s+8]
    ims = [(os.path.basename(f), Image.open(f)) for f in chunk]
    ims = [(nm, im.resize((w, int(im.height*w/im.width)), Image.LANCZOS)) for nm, im in ims]
    ch = max(im.height for _, im in ims)
    sheet = Image.new("RGB", (w*4, (ch+24)*2), "white")
    dr = ImageDraw.Draw(sheet)
    for k, (nm, im) in enumerate(ims):
        cx, cy = (k % 4)*w, (k // 4)*(ch+24)
        dr.text((cx+2, cy), nm, fill="red", font=font)
        sheet.paste(im, (cx, cy+20))
    sheet.save(os.path.join(out, f"all{s//8+1}.png"))
print("ok", d.page_count)
