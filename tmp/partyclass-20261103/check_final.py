import re, csv
text=open(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\final_text.txt",encoding="utf-8").read()
rows=list(csv.reader(open(r"D:\aaa_D_usual\DSH\111学习助手\入党\党的名词规范\易错对照.csv",encoding="utf-8-sig")))[1:]
print("=== 易错词（整词匹配，排除“全面从严治党”“党的二十届…”子串误报）===")
for r in rows:
    bad=r[1]
    for m in re.finditer(re.escape(bad), text):
        s=max(0,m.start()-2); ctx=text[s:m.end()+2]
        if bad=="从严治党" and ctx.endswith("全面从严治党"): continue
        if bad=="二十届五中全会" and "党的二十届五中全会" in text[max(0,m.start()-1):m.end()+1]: continue
        print("  HIT:", bad, "|", ctx)
print("done")
print()
sents=[s for s in re.split(r"[。！？；]", text) if len(s.strip())>0]
print("平均句长:", round(sum(len(s) for s in sents)/len(sents),1), "句数:", len(sents), "最长:", max(len(s) for s in sents))
for s in sorted(sents,key=len,reverse=True)[:5]:
    print("  ", len(s), s[:40])
