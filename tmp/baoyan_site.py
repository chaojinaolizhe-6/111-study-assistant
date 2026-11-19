# -*- coding: utf-8 -*-
import re, sys, urllib.request

proxy = "http://127.0.0.1:27890"
opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
opener.addheaders = [("User-Agent", "Mozilla/5.0")]

def get(url):
    with opener.open(url, timeout=40) as r:
        raw = r.read()
    for enc in ("utf-8", "gbk"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", "ignore")

urls = [
    "http://dbji.dlut.edu.cn/bkspy/ggtz1.htm",
    "http://dbji.dlut.edu.cn/bkspy/ggtz1/2.htm",
    "http://dbji.dlut.edu.cn/bkspy/ggtz1/3.htm",
]
kw = re.compile(r"培养|方案|选课|四史|推免|免试|成绩|学分")
for u in urls:
    try:
        h = get(u)
    except Exception as e:
        print("ERR", u, e)
        continue
    print("=== ", u, len(h))
    for m in re.finditer(r'href="([^"]*info/[^"]+)"[^>]*>\s*([^<]{2,80})', h):
        title = m.group(2).strip()
        if kw.search(title):
            print("  ", m.group(1), "|", title)
