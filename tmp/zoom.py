import fitz
doc = fitz.open(r"subjects\04-数学物理方法1\讲义\第二章-精讲-复变函数的积分-20261101.pdf")
pg = doc[1]
# clip the table region
clip = fitz.Rect(60, 220, 420, 340)
pg.get_pixmap(dpi=300, clip=clip).save(r"tmp\zoom_table.png")
print("ok")
