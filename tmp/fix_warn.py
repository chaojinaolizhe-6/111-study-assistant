p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
src = open(p, encoding="utf-8").read()
lines = [i for i, l in enumerate(src.splitlines(), 1) if "\u26a0" in l]
print("lines with glyph:", lines)
src = src.replace("p25 的 \u26a0 框", "p25 的红色警示框")
print("remaining:", src.count("\u26a0"))
open(p, "w", encoding="utf-8", newline="\n").write(src)
