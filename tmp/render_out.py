import fitz, os
src = r"subjects\04-数学物理方法1\讲义\第二章-精讲-复变函数的积分-20261101.pdf"
out = r"tmp\ch2out"
os.makedirs(out, exist_ok=True)
doc = fitz.open(src)
print("pages:", doc.page_count)
for i, page in enumerate(doc, start=1):
    page.get_pixmap(dpi=100).save(os.path.join(out, f"p{i:02d}.png"))
