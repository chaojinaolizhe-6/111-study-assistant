import fitz, os
from PIL import Image, ImageDraw, ImageFont
pdf = r"tmp\texbuild-optics\第五章-杨氏双缝与云母片-精讲-20261027.pdf"
out = r"tmp\lec_preview"
os.makedirs(out, exist_ok=True)
d = fitz.open(pdf)
files = []
for i in range(d.page_count):
    fn = os.path.join(out, f"p{i+1:02d}.png")
    d[i].get_pixmap(dpi=120).save(fn)
    files.append(fn)
font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 26)
cell_w = 760
for s in range(0, len(files), 4):
    ims = []
    for f in files[s:s+4]:
        im = Image.open(f)
        r = cell_w / im.width
        im = im.resize((cell_w, int(im.height*r)), Image.LANCZOS)
        ims.append((os.path.basename(f), im))
    ch = max(im.height for _, im in ims)
    sheet = Image.new("RGB", (cell_w*2, (ch+30)*2), "white")
    dr = ImageDraw.Draw(sheet)
    for k, (name, im) in enumerate(ims):
        cx, cy = (k % 2)*cell_w, (k // 2)*(ch+30)
        dr.text((cx+4, cy+2), name, fill="red", font=font)
        sheet.paste(im, (cx, cy+30))
    sheet.save(os.path.join(out, f"sheet{s//4+1}.png"))
print("pages", d.page_count)
