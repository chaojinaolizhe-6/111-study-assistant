import json, datetime, collections
p = r"C:\Users\M\AppData\Roaming\dsh-desktop\harness\llm-deepseek\files-v3.json"
d = json.load(open(p, encoding='utf-8'))
recs = d["records"]
recs.sort(key=lambda r: r.get("createdAt",0), reverse=True)
def ts(ms):
    return datetime.datetime.fromtimestamp(ms/1000).strftime('%m-%d %H:%M:%S')
for r in recs[:12]:
    print(ts(r["createdAt"]), r["bytes"], r["scope"][:10], r["attachmentId"][:30], r["variantId"][:20], r.get("name") or r.get("filename") or "")
print("scopes newest:", collections.Counter(r["scope"][:10] for r in recs[:30]))
