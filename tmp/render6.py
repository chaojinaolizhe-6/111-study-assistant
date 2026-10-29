import fitz
from PIL import Image
d = fitz.open(r"tmp\texbuild-optics\第五章-杨氏双缝与云母片-精讲-20261027.pdf")
d[0].get_pixmap(dpi=135).save(r"tmp\lec_final2\p01b.png")
d[2].get_pixmap(dpi=135).save(r"tmp\lec_final2\p03b.png")
a = Image.open(r"tmp\lec_final2\p01b.png"); b = Image.open(r"tmp\lec_final2\p03b.png")
w = 760
a = a.resize((w, int(a.height*w/a.width)), Image.LANCZOS)
b = b.resize((w, int(b.height*w/b.width)), Image.LANCZOS)
sheet = Image.new("RGB", (w*2, max(a.height, b.height)), "white")
sheet.paste(a, (0,0)); sheet.paste(b, (w,0))
sheet.save(r"tmp\lec_final2\p1p3.png")
print(sheet.size)
