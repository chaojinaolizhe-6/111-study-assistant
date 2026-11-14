import fitz, os
doc = fitz.open("main.pdf")
print("pages", doc.page_count)
os.makedirs("_pages", exist_ok=True)
for p in [1,2,3,5,9,13,14,19,24,27,29]:
    pg = doc[p-1]
    pix = pg.get_pixmap(dpi=115)
    fn = f"_pages/p{p:02d}.png"
    pix.save(fn)
    print(fn, pix.width, pix.height)
