import re
p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
src = open(p, encoding="utf-8").read()
pat = re.compile(r"\\noindent\\begin\{tabular\}(\{[^\n]*\})\n(.*?)\\end\{tabular\}", re.S)
m = pat.search(src)
print("found:", m)
if not m:
    pat3 = re.compile(r"\\end\{tabular\}")
    k = src.find("\\end{tabular}")
    print("first end at", k, repr(src[k-40:k+40]))
