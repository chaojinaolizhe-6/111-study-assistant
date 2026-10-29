p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
s = open(p, encoding="utf-8").read()
R = ">{\\raggedright\\arraybackslash}"
old = f"@{{}}{R}m{{2.1cm}}{R}m{{3.3cm}}{R}m{{4.7cm}}{R}m{{4.9cm}}@{{}}"
new = f"@{{}}{R}m{{2.1cm}}{R}m{{3.2cm}}{R}m{{5.2cm}}{R}m{{4.8cm}}@{{}}"
print("found:", s.count(old))
s = s.replace(old, new)
# 第 4 张表（2.8/5.0/7.6）稍宽，给“明纹（constructive）”留位置
old4 = f"@{{}}{R}m{{2.8cm}}{R}m{{5.0cm}}{R}m{{7.6cm}}@{{}}"
new4 = f"@{{}}{R}m{{3.6cm}}{R}m{{4.8cm}}{R}m{{7.0cm}}@{{}}"
print("found4:", s.count(old4))
s = s.replace(old4, new4)
open(p, "w", encoding="utf-8", newline="\n").write(s)
