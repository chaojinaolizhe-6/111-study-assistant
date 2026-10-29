import fitz
from PIL import Image
d = fitz.open(r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.pdf")
print("pages", d.page_count)
d[8].get_pixmap(dpi=140).save(r"tmp\lec_final2\f09.png")
d[12].get_pixmap(dpi=140).save(r"tmp\lec_final2\f13.png")
a = Image.open(r"tmp\lec_final2\f09.png"); b = Image.open(r"tmp\lec_final2\f13.png")
w = 760
a = a.resize((w, int(a.height*w/a.width)), Image.LANCZOS); b = b.resize((w, int(b.height*w/b.width)), Image.LANCZOS)
s = Image.new("RGB", (w*2, max(a.height,b.height)), "white"); s.paste(a,(0,0)); s.paste(b,(w,0))
s.save(r"tmp\lec_final2\f.png"); print(s.size)
