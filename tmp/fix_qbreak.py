import re, io
p = r"subjects\04-数学物理方法1\讲义\第二章-精讲-复变函数的积分-20261101.tex"
s = io.open(p, encoding="utf-8").read()
pat = re.compile(r"(\\subhdr\{[^\n]*\}\n)\n\\qbreak\n(?=\\qstem\{)")
s2, n = pat.subn(lambda m: "\\qbreak\n" + m.group(1) + "\n", s)
print("moved:", n)
io.open(p, "w", encoding="utf-8", newline="\n").write(s2)
