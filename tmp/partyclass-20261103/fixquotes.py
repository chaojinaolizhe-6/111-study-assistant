import re, io
p=r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\xinde.txt"
t=open(p,encoding="utf-8").read()
def fix(s):
    out=[]; dq=0; sq=0
    for ch in s:
        if ch=='"':
            out.append("“" if dq%2==0 else "”"); dq+=1
        elif ch=="'":
            out.append("‘" if sq%2==0 else "’"); sq+=1
        else:
            out.append(ch)
    return "".join(out)
lines=t.split("\n")
lines=[fix(l) for l in lines]
t="\n".join(lines)
# simplify signature block
t=t.replace("汇报人：马泽宇\n学号：20251091006\n中白学院\n2026年11月3日","马泽宇\n中白学院　20251091006\n2026年11月3日")
open(p,"w",encoding="utf-8").write(t)
print(t[-120:])
