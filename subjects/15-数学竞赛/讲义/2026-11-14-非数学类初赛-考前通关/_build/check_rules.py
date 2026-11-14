import fitz
d = fitz.open("数学竞赛初赛-考前通关手册-20261114.pdf")
H = d[0].rect.height
flag = []
for i, pg in enumerate(d, start=1):
    for dr in pg.get_drawings():
        r = dr["rect"]
        if r.height < 3 and r.width > 250 and r.y1 > H - 90:
            flag.append((i, round(r.y1,1), round(r.width,1)))
print("page height", H)
print("suspect bottom rules:", flag)
