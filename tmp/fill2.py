import fitz
doc = fitz.open(r"subjects\04-数学物理方法1\讲义\第二章-精讲-复变函数的积分-20261101.pdf")
rows = []
for i, pg in enumerate(doc, 1):
    H = pg.rect.height
    blocks = [b for b in pg.get_text("blocks") if b[4].strip()]
    ys = [b[3] for b in blocks if b[3] < H*0.9]   # drop footer
    bottom = max(ys) if ys else 0
    rows.append((i, round(bottom/H, 2)))
print("pages:", doc.page_count, "height", doc[0].rect.height)
print("fill ratio per page:")
print(rows)
low = [r for r in rows if r[1] < 0.6]
print("under 60%:", low)
