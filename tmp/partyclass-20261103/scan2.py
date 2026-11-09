import re, csv
text=open(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\final_text.txt",encoding="utf-8").read()
rows=list(csv.reader(open(r"D:\aaa_D_usual\DSH\111学习助手\入党\党的名词规范\易错对照.csv",encoding="utf-8-sig")))[1:]
issues=[]
for r in rows:
    bad=r[1]
    for m in re.finditer(re.escape(bad), text):
        pre=text[max(0,m.start()-1):m.start()]
        if bad=="从严治党" and pre=="面": continue
        if bad=="二十届五中全会" and pre=="的": continue
        if bad=="政治占位" and text[m.end():m.end()+1]=="”": continue
        issues.append((bad, text[max(0,m.start()-8):m.end()+6]))
print("真实问题:", len(issues), issues)
sents=[s for s in re.split(r"[。！？；\n]", text) if len(s.strip())>2]
print("平均句长", round(sum(len(s) for s in sents)/len(sents),1), "最长", max(len(s) for s in sents))
