# -*- coding: utf-8 -*-
import io
p = r"subjects\07-俄语\讲义\parts\08-review.tex"
s = io.open(p, encoding="utf-8").read()
old = "本册 35 页"
new = "本册 37 页（第 9 节为 2026-11-12 补入的复习课）"
assert s.count(old) == 1
s = s.replace(old, new)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched page count")
