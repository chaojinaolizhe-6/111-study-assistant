import re
p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
src = open(p, encoding="utf-8").read()
src = re.sub(r"^\{% -", "% -", src, flags=re.M)
src = src.replace("\\flowerrule}", "\\flowerrule")
open(p, "w", encoding="utf-8", newline="\n").write(src)
print(src.count("{%"), src.count("\\flowerrule}"))
