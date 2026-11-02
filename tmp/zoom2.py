import fitz
doc = fitz.open(r"subjects\04-数学物理方法1\讲义\第二章-精讲-复变函数的积分-20261101.pdf")
pg = doc[20]
pg.get_pixmap(dpi=250, clip=fitz.Rect(120, 700, 560, 930)).save(r"tmp\zoom_fig3.png")
doc2 = fitz.open(r"subjects\04-数学物理方法1\讲义\第二章-精讲-复变函数的积分-20261101.pdf")
pg2 = doc2[11]
pg2.get_pixmap(dpi=200, clip=fitz.Rect(60, 60, 560, 620)).save(r"tmp\zoom_fig2.png")
print("ok")
