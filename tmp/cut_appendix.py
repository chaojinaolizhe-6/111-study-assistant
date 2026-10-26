# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(r"subjects\04-数学物理方法1\讲义\第五章-精讲-傅里叶变换-20261022.tex")
lines = p.read_text(encoding="utf-8").split("\n")

hdr_i = next(i for i, l in enumerate(lines) if "hdr{附录 A}" in l)
start = hdr_i - 2  # 去掉前面的 "%====" 与 "\newpage"
assert lines[start].startswith("%===="), lines[start]
assert lines[start + 1].strip() == r"\newpage", lines[start + 1]

end = next(i for i, l in enumerate(lines) if l.strip() == r"\flowerrule" and i > hdr_i)
print("cut lines", start + 1, "..", end, "count", end - start)

new = lines[:start] + lines[end:]
p.write_text("\n".join(new), encoding="utf-8")
print("remaining lines", len(new))
print("tail:")
for l in new[-12:]:
    print("   ", l[:100])
