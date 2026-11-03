import fitz
d = fitz.open("t2.pdf"); p = d[0]
p.get_pixmap(dpi=170, clip=fitz.Rect(30,30,560,300)).save("t2.png")
