import json
p = r"C:\Users\M\AppData\Roaming\dsh-desktop\harness\llm-deepseek\files-v3.json"
d = json.load(open(p, encoding='utf-8'))
print(type(d), list(d)[:10] if isinstance(d, dict) else len(d))
s = json.dumps(d, ensure_ascii=False)
print("len", len(s))
print(s[:800])
if isinstance(d, dict):
    for k,v in d.items():
        print("KEY", k, type(v), (len(v) if hasattr(v,'__len__') else ''))
