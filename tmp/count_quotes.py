p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
s = open(p, encoding="utf-8").read()
print("ascii quotes:", s.count('"'))
import re
for m in re.finditer(r'"[^"\n]{0,40}"', s):
    pass
print("pairs guess:", len(re.findall(r'"[^"\n]*"', s)))
