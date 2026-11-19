# -*- coding: utf-8 -*-
import re, os, urllib.request, urllib.parse

proxy = "http://127.0.0.1:27890"
opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
opener.addheaders = [("User-Agent", "Mozilla/5.0")]

out = r"D:\aaa_D_usual\DSH\111学习助手\tmp\baoyan"
os.makedirs(out, exist_ok=True)

def get(url, binary=False):
    with opener.open(url, timeout=60) as r:
        raw = r.read()
    if binary:
        return raw
    for enc in ("utf-8", "gbk"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            pass
    return raw.decode("utf-8", "ignore")

page = "http://dbji.dlut.edu.cn/info/1113/8689.htm"
h = get(page)
open(os.path.join(out, "pyfa-2024.html"), "w", encoding="utf-8").write(h)
print("page len", len(h))

links = []
for m in re.finditer(r'(?:href|src)="([^"]*(?:virtual_attach_file|download\.jsp)[^"]*)"', h):
    links.append(m.group(1))
for m in re.finditer(r'showVsbpdfIframe\("([^"]+)"', h):
    links.append(m.group(1))
links = list(dict.fromkeys(links))
print("attach links:", len(links))
for l in links:
    print("  ", l[:160])

for i, l in enumerate(links):
    url = urllib.parse.urljoin(page, l.replace("&amp;", "&"))
    try:
        data = get(url, binary=True)
    except Exception as e:
        print("ERR", url, e)
        continue
    ext = ".pdf" if data[:4] == b"%PDF" else ".bin"
    dst = os.path.join(out, f"pyfa-2024-{i}{ext}")
    open(dst, "wb").write(data)
    print("saved", dst, len(data), "bytes", "isPDF" if ext == ".pdf" else "NOT-PDF")
