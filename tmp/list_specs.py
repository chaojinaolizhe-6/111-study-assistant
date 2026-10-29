import re
p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
s = open(p, encoding="utf-8").read()
for sp in re.findall(r"\\begin\{tabular\}(\{[^\n]*\})", s):
    print(sp.replace(">{\\raggedright\\arraybackslash}", "|"))
