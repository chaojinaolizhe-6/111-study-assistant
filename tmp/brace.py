import re, sys
p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
src = open(p, encoding="utf-8").read().splitlines()
bal = 0
for i, line in enumerate(src, 1):
    # strip comments (unescaped %)
    s = re.sub(r"(?<!\\)%.*$", "", line)
    s = s.replace(r"\{", "").replace(r"\}", "")
    opens = s.count("{"); closes = s.count("}")
    if opens != closes:
        print(f"line {i}: +{opens} -{closes} net {opens-closes} balance {bal} :: {line[:70]}")
    bal += opens - closes
print("final balance", bal)
