import fitz, sys
doc = fitz.open(r"tmp\texbuild\ode_hw.pdf")
print("pages:", doc.page_count)
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=110)
    out = rf"tmp\texbuild\page{i+1}.png"
    pix.save(out)
    print(out, pix.width, "x", pix.height)
