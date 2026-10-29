import fitz
d = fitz.open(r"tmp\modex\diag.pdf")
print("pages", d.page_count)
for i in range(min(3, d.page_count)):
    p = d[i]
    pix = p.get_pixmap(dpi=110)
    pix.save(rf"tmp\modex\pg{i+1}.png")
print("ok")
