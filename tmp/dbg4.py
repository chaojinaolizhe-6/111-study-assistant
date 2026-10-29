p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
src = open(p, encoding="utf-8").read()
idx = 0
while True:
    k = src.find("end{tabular", idx)
    if k < 0: break
    print(k, repr(src[k-12:k+30]))
    idx = k + 1
print("tabtop count", src.count("\\tabtop"), "tabbot", src.count("\\tabbot"))
