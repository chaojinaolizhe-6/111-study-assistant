# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(r"subjects\04-数学物理方法1\讲义\第五章-精讲-傅里叶变换-20261022.tex")
s = p.read_text(encoding="utf-8")

old = r"\hdr{§7}{其余例题与课件作业：只写与主线不同的地方}"
new = (
    r"\hdr{§7}{其余例题与课件作业}" "\n\n"
    "本节先补两个例题（例 5 与 p49 的例 1），只写与主线不同的地方；"
    "最后收课件 p39、p63 的七道作业——题面成组抄在前，详解紧随其后。"
)
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new)
p.write_text(s, encoding="utf-8")
print("ok")
