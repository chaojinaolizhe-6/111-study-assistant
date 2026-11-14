import fitz
d = fitz.open("数学竞赛初赛-考前通关手册-20261114.pdf")
for p in (19,):
    d[p-1].get_pixmap(dpi=110).save(f"_build/_pages/p{p:02d}.png")
print("ok")
