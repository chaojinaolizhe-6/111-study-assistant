p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
s = open(p, encoding="utf-8").read()
old = "{第五章 \\S5.5--5.7 \\ 双缝干涉与分波前装置 · 精讲讲义}"
new = "{第五章 \\S5.5--5.6 \\ 双缝干涉与分波前装置 · 精讲讲义}"
print("subtitle:", s.count(old))
s = s.replace(old, new)
open(p, "w", encoding="utf-8", newline="\n").write(s)
