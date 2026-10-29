import re
p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
lines = open(p, encoding="utf-8").read().splitlines()
count = 0
for i, line in enumerate(lines, 1):
    s = re.sub(r"(?<!\\)%.*$", "", line)
    s = s.replace(r"\$", "")
    n = s.count("$")
    count += n
    if n % 2 == 1:
        print(f"line {i}: odd $ ({n}) :: {line[:90]}")
print("total $:", count, "even" if count % 2 == 0 else "ODD")
