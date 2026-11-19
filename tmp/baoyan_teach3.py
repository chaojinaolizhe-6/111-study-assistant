# -*- coding: utf-8 -*-
import re, urllib.request, urllib.parse

proxy = "http://127.0.0.1:27890"
opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
opener.addheaders = [("User-Agent", "Mozilla/5.0")]

def get(url):
    with opener.open(url, timeout=45) as r:
        raw = r.read()
    for enc in ("utf-8", "gbk"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            pass
    return raw.decode("utf-8", "ignore")

base = "http://teach.dlut.edu.cn/"
lists = [
    "zhongyaotonggao/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1016",
    "jiaoxuewenjian/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1082",
]
for lst in lists:
    url = urllib.parse.urljoin(base, lst)
    try:
        h = get(url)
    except Exception as e:
        print("ERR", url, e); continue
    print("=== ", url, len(h))
    items = [(m.group(1), m.group(2).strip()) for m in re.finditer(r'href="([^"]*(?:ny\.jsp|wenjian\.jsp)[^"]*)"[^>]*>\s*([^<]{2,90})', h)]
    for link, t in items:
        flag = "*" if re.search(r"选课|四史|思政|培养方案", t) else " "
        print(flag, link[:100], "|", t)
