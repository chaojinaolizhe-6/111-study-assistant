# -*- coding: utf-8 -*-
import re, urllib.request, urllib.parse

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

base = "http://teach.dlut.edu.cn/"
pages = ["zlxz1.htm", "jxjw/xjyzjgl.htm", "bszn/xsxg.htm", "jyjg/zysz.htm"]
kw = re.compile(r"培养方案|四史|选修|选课|成绩|必修")
for p in pages:
    url = urllib.parse.urljoin(base, p)
    try:
        h = get(url)
    except Exception as e:
        print("ERR", url, e); continue
    print("=== ", url, len(h))
    for m in re.finditer(r'href="([^"]+)"[^>]*>\s*([^<]{2,90})', h):
        t = m.group(2).strip()
        if kw.search(t):
            print("   ", m.group(1)[:90], "|", t)
