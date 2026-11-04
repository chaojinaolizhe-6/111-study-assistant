import csv, io
p=r"D:\aaa_D_usual\DSH\111学习助手\入党\党的名词规范\规范表.csv"
rows=list(csv.reader(open(p,encoding="utf-8-sig")))
print("csv rows:", len(rows), "cols:", len(rows[0]))
print("head:", rows[0])
print("row2:", rows[1][:4])
bad=[r for r in rows[1:] if len(r)!=6]
print("bad rows:", len(bad))
md=open(r"D:\aaa_D_usual\DSH\111学习助手\入党\党的名词规范\规范表.md",encoding="utf-8").read()
print("md chars:", len(md), "tables:", md.count("|---"))
