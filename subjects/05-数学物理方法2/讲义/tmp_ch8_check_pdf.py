import fitz, sys, re
sys.stdout.reconfigure(encoding="utf-8")
p = r"第八章作业四题-分步详解-20261113.pdf"
d = fitz.open(p)
txt = "\n".join(pg.get_text() for pg in d)
print("pages:", d.page_count, "chars:", len(txt))
print("unresolved ??:", txt.count("??"))
print("has 4 answers:", txt.count("4h"), txt.count("16b"), txt.count("8b"), txt.count("2A"))
