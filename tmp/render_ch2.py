import fitz, os
src = r"subjects\04-数学物理方法1\课件\第二章+复变函数的积分+-+上传课件.pdf"
out = r"tmp\ch2png"
os.makedirs(out, exist_ok=True)
doc = fitz.open(src)
for i, page in enumerate(doc, start=1):
    pix = page.get_pixmap(dpi=100)
    pix.save(os.path.join(out, f"p{i:02d}.png"))
print("pages:", doc.page_count, "->", out)
