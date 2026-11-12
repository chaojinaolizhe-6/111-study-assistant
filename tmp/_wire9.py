# -*- coding: utf-8 -*-
import io, sys
base = r"subjects\07-俄语\讲义"
main = base + r"\俄语-全课程精讲-20261023.tex"
toc = base + r"\parts\00-toc.tex"
m = io.open(main, encoding="utf-8").read()
t = io.open(toc, encoding="utf-8").read()

old_in = "\\input{parts/08-review}"
new_in = "\\input{parts/08-review}\n\\input{parts/09-povtorenie}"
assert m.count(old_in) == 1
m = m.replace(old_in, new_in)

old_rows = (r"\S9 & 易错点 & 十二条，每条都能指回某个词的某一步 \\" "\n"
            r"\S10 & 缺口清单 & 12 条：课件跳了哪一步，本讲义补在哪 \\" "\n"
            r"\S11 & 三句话总结 & 判性数、一条规律多个位置、能回指页码 \\" "\n"
            r"\S12 & 页码对照表 & 12 份课件 → 本讲义哪一节 \\")
new_rows = r"\S9 & 复习课与题型 & 连词 и／а／но／потому́ что／что；人称代词第四格；考试结构 60／25／15；十种题型清单 \\"
if t.count(old_rows) != 1:
    print("TOC pattern count:", t.count(old_rows)); sys.exit(1)
t = t.replace(old_rows, new_rows)

io.open(main, "w", encoding="utf-8", newline="\n").write(m)
io.open(toc, "w", encoding="utf-8", newline="\n").write(t)
print("wired §9 into main + toc")
