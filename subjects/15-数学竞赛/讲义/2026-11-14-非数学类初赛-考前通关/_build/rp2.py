import fitz, os
d = fitz.open("数学竞赛初赛-考前通关手册-20261114.pdf")
os.makedirs("_build/_pages", exist_ok=True)
for p in (10, 11, 25):
    pix = d[p-1].get_pixmap(dpi=115)
    pix.save(f"_build/_pages/p{p:02d}.png")
print("ok", d.page_count)
