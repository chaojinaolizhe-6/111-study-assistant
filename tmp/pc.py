import fitz, glob
for f in glob.glob(r"subjects\04-数学物理方法1\讲义\*.pdf"):
    d = fitz.open(f)
    print(d.page_count, f)
