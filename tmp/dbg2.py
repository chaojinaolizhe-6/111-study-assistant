import re
p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
src = open(p, encoding="utf-8").read()
i = src.find("\\noindent")
seg = src[i:i+120]
print(repr(seg))
pat = re.compile(r"\\noindent\\begin\{tabular\}(\{[^\n]*\})\n", re.S)
print("match head:", pat.match(seg))
pat2 = re.compile(r"\\noindent")
print("find noindent:", bool(pat2.search(src)))
