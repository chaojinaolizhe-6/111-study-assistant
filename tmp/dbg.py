import re
p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
src = open(p, encoding="utf-8").read()
print("count noindent:", src.count("\\noindent"))
print("count begin{tabular}:", src.count("\\begin{tabular}"))
i = src.find("\\begin{tabular}")
print(repr(src[i-30:i+80]))
