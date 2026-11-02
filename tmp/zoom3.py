import fitz
doc = fitz.open(r"subjects\04-数学物理方法1\讲义\第二章-精讲-复变函数的积分-20261101.pdf")
pg = doc[3]
H = pg.rect.height
pg.get_pixmap(dpi=200, clip=fitz.Rect(40, H-170, 560, H-20)).save(r"tmp\zoom_p4bottom.png")
print(H)
