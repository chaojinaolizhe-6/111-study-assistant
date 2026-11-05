import re, csv
text=open(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\gemini_draft.txt",encoding="utf-8").read()
rows=list(csv.reader(open(r"D:\aaa_D_usual\DSH\111学习助手\入党\党的名词规范\易错对照.csv",encoding="utf-8-sig")))[1:]
print("=== 易错词扫描 ===")
hits=0
for r in rows:
    bad,good,note=r[1],r[2],r[3]
    if bad in text:
        hits+=1
        print("  HIT:", bad, "->", good, "|", note)
print("hits:", hits)
print()
print("=== 套话扫描 ===")
banned=["作为新时代青年","深刻认识到","精神洗礼","思想升华","赓续红色血脉","筑牢信仰之基","汲取奋进力量",
        "扣好人生第一粒扣子","众所周知","不难看出","受益匪浅","首先","其次","最后，","让青春在"]
for b in banned:
    if b in text: print("  HIT:", b, text.count(b))
print()
print("=== 句长 ===")
sents=[s for s in re.split(r"[。！？；]", text) if len(s.strip())>0]
for s in sorted(sents,key=len,reverse=True)[:8]:
    print(len(s), s[:70])
print("平均句长:", round(sum(len(s) for s in sents)/len(sents),1), "句子数:", len(sents))
print()
print("=== 段落字数 ===")
for p in [x for x in text.split("\n") if x.strip()]:
    print(len(p), p[:24])
