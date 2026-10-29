import fitz, os
from PIL import Image, ImageDraw, ImageFont
pdf = r"tmp\texbuild-optics\第五章-杨氏双缝与云母片-精讲-20261027.pdf"
out = r"tmp\lec_preview3"
os.makedirs(out, exist_ok=True)
d = fitz.open(pdf)
for n in [9, 15, 16]:
    d[n-1].get_pixmap(dpi=150).save(os.path.join(out, f"p{n:02d}.png"))
print("ok")
