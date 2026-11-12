import fitz, os
pdf = r"subjects\07-俄语\讲义\俄语-УРОК1-8-总复习课件-审校版-20261112.pdf"
doc = fitz.open(pdf)
print("pages:", doc.page_count)
os.makedirs(r"tmp\new", exist_ok=True)
for p in [3,4,6,8,9,12,13,16]:
    pix = doc[p-1].get_pixmap(matrix=fitz.Matrix(1.5,1.5))
    out = rf"tmp\new\n_p{p}.png"
    pix.save(out); print(out, pix.width, pix.height)
