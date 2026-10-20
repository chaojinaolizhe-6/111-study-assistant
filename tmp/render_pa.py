import fitz
doc = fitz.open(r"tmp\texbuild3\pa.pdf")
print("pages:", doc.page_count)
for i, page in enumerate(doc):
    page.get_pixmap(dpi=105).save(rf"tmp\texbuild3\q{i+1}.png")
print("ok")
