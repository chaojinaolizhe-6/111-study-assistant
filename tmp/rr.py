import fitz
d = fitz.open("test-table.pdf"); p = d[0]
p.get_pixmap(dpi=200, clip=fitz.Rect(40,40,560,160)).save("test-table.png")
