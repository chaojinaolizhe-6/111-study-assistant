p=r"D:\aaa_D_usual\DSH\111学习助手\入党\党的名词规范\规范表.md"
bad=[]
for i,l in enumerate(open(p,encoding="utf-8"),1):
    l=l.rstrip("\n")
    if l.startswith("|"):
        n=l.count("|")
        if n not in (5,6):
            bad.append((i,n,l[:60]))
print("bad table lines:", len(bad))
for b in bad[:10]: print(b)
