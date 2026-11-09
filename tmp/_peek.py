import json, re
p = r"D:\aaa_D_usual\DSH\111学习助手\tmp\_sess_606c.jsonl"
rows = [json.loads(l) for l in open(p, encoding='utf-8') if l.strip()]
print("records:", len(rows))
from collections import Counter
print(Counter(r.get("type") for r in rows))
for r in rows[:8]:
    s = json.dumps(r, ensure_ascii=False)
    print("----", r.get("type"), len(s))
    print(s[:1200])
