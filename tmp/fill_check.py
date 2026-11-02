import fitz
doc = fitz.open(r"subjects\04-数学物理方法1\讲义\第二章-精讲-复变函数的积分-20261101.pdf")
low = []
for i, pg in enumerate(doc, 1):
    blocks = [b for b in pg.get_text("blocks") if b[4].strip()]
    ys = [b[3] for b in blocks]
    # ignore footer (page number) near bottom
    ys = [y for y in ys if y < 1050]
    bottom = max(ys) if ys else 0
    if bottom < 700:
        low.append((i, int(bottom)))
print("pages:", doc.page_count)
print("underfilled (last text y<700 of 1170):", low)
