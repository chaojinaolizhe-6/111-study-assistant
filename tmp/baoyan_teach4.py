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

base = "http://teach.dlut.edu.cn/zhongyaotonggao/"
ids = [17918, 17878, 17868]
for wid in ids:
    url = base + f"ny.jsp?urltype=news.NewsContentUrl&wbtreeid=1016&wbnewsid={wid}"
    try:
        h = get(url)
    except Exception as e:
        print("ERR", wid, e); continue
    txt = re.sub(r"<script[\s\S]*?</script>", " ", h)
    txt = re.sub(r"<style[\s\S]*?</style>", " ", txt)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = re.sub(r"\s+", " ", txt)
    print("=====", wid, "len", len(txt))
    for kw in ("必修", "选择性必修", "选修", "四史", "学习成绩", "加权"):
        for m in re.finditer(kw, txt):
            s = max(0, m.start() - 90)
            print(f"  [{kw}] ...{txt[s:m.start()+120]}...")
            break
