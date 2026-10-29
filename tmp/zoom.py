import fitz, os
src = r"subjects\02-光学\课件\第五章 光的干涉.pdf"
outdir = r"tmp\zoom"
os.makedirs(outdir, exist_ok=True)
doc = fitz.open(src)
for p in [15,16,17,18,19,20,22,24,25,26,27,28]:
    page = doc[p-1]
    pix = page.get_pixmap(dpi=170)
    pix.save(os.path.join(outdir, f"p{p:02d}.png"))
print("ok")
