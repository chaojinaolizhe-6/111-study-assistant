import re
t=open(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\xinde.txt",encoding="utf-8").read()
body="\n".join(l for l in t.splitlines() if l.strip())
cn=len(re.findall(r"[\u4e00-\u9fff]", body))
allc=len(re.sub(r"\s","",body))
paras=[p for p in t.split("\n\n") if p.strip()]
print("汉字数:", cn, "含标点字符数:", allc, "段落:", len(paras))
for p in paras: print(len(p), p[:20])
