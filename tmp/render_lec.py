import fitz
doc = fitz.open(r"tmp\texbuild2\lec.pdf")
print("pages:", doc.page_count)
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=105)
    pix.save(rf"tmp\texbuild2\p{i+1}.png")
print("rendered")
