import fitz
for name, pgs in [(r'subjects\02-光学\课件\第3章光的偏振.pdf',[1,2,3]), (r'subjects\02-光学\课件\第一章 几何光学 第一课.pdf',[1,2,3])]:
    d=fitz.open(name)
    base = name.split('\\')[-1].replace('.pdf','')
    for i in pgs:
        pix=d[i-1].get_pixmap(dpi=110)
        out=fr'_scratch\optics-sample\{base}-p{i}.png'
        import os; os.makedirs('_scratch\\optics-sample',exist_ok=True)
        pix.save(out); print(out, pix.width, pix.height)
