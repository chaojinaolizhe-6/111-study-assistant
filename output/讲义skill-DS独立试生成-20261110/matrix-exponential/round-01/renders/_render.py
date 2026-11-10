import fitz, pathlib
pdf = pathlib.Path(r"inputs/16_17_matrix_exponential.pdf")
out = pathlib.Path(r"matrix-exponential/round-01/renders")
doc = fitz.open(pdf)
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=170)
    pix.save(out / f"src-p{i+1:02d}.png")
print("pages", doc.page_count)
