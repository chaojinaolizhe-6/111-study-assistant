import fitz, re
d = fitz.open("tmp_cr.pdf")
txt = "\n".join(p.get_text() for p in d)
print("pages:", len(d))
for bad in ["??", "**", "Missing", "undefined", "§§"]:
    n = txt.count(bad)
    if n: print("FOUND", repr(bad), n)
# 检查公式编号连续性
nums = sorted({int(m) for m in re.findall(r"\((\d{1,2})\)\s*$", txt, re.M)})
print("eq numbers:", nums)
d.close()
