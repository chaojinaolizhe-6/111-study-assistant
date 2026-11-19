# -*- coding: utf-8 -*-
import re, urllib.request

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
            pass
    return raw.decode("utf-8", "ignore")

for p in range(1, 7):
    url = "http://dbji.dlut.edu.cn/bkspy/ggtz1.htm" if p == 1 else f"http://dbji.dlut.edu.cn/bkspy/ggtz1/{p}.htm"
    try:
        h = get(url)
    except Exception as e:
        print("ERR", url, e); break
    titles = [(m.group(1), m.group(2).strip()) for m in re.finditer(r'href="([^"]*info/[^"]+)"[^>]*>\s*([^<]{2,100})', h)]
    print(f"--- page {p}: {len(titles)} items")
    for link, t in titles:
        mark = "  *" if re.search(r"培养方案|选课|四史|课程", t) else "   "
        print(mark, link, "|", t)
