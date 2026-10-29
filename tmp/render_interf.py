import fitz, os
from PIL import Image
src = r"subjects\02-光学\课件\第五章 光的干涉.pdf"
outdir = r"_scratch\interf-pages"
os.makedirs(outdir, exist_ok=True)
doc = fitz.open(src)
n = doc.page_count
for i, page in enumerate(doc, start=1):
    pix = page.get_pixmap(dpi=110)
    pix.save(os.path.join(outdir, f"p{i:02d}.png"))
print("rendered", n)
