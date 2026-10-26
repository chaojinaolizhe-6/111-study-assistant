# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(r"subjects\04-数学物理方法1\讲义\第五章-精讲-傅里叶变换-20261022.tex")
s = p.read_text(encoding="utf-8")

pairs = [
    ("§5--§7 五个例题",
     "§5--§7 五个例题与末节七道作业"),
    ("作业 & p39、p63 & §7 题面，附录 A 详解",
     "作业 & p39、p63 & §7 末：题面与完整详解"),
    (r"\hdr{§7}{其余例题：只写与主线不同的地方}",
     r"\hdr{§7}{其余例题与课件作业：只写与主线不同的地方}"),
    ("p39 & 作业 1--4 & §7 题面，附录 A 详解",
     "p39 & 作业 1--4 & §7 末：题面与完整详解"),
    ("p63 & 作业 5--7 & §7 题面，附录 A 详解",
     "p63 & 作业 5--7 & §7 末：题面与完整详解"),
    ("附录 A 收 p39、p63 七道作业的详解与答案。",
     "§7 末收 p39、p63 七道作业的题面与完整详解（含端点、周期减半、$\\alpha\\to0^{+}$ 的奇点与 Fresnel 围道四处课件没写的推导）。"),
]

for old, new in pairs:
    n = s.count(old)
    assert n == 1, (n, old[:40])
    s = s.replace(old, new)

p.write_text(s, encoding="utf-8")
print("ok, 附录 A 残留:", s.count("附录 A"))
