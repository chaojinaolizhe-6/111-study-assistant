import fitz
d = fitz.open("t3.pdf"); p = d[0]
p.get_pixmap(dpi=170, clip=fitz.Rect(30,30,500,330)).save("t3.png")
