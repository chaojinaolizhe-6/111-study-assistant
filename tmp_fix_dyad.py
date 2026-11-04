import re

p = r"subjects\01-理论力学\讲义\专题-并矢-从张量积到惯量张量-20261103.tex"
s = open(p, encoding="utf-8").read()

tok = r"\\vect(?:\{[^{}]*\}|\s+[A-Za-z])(?:'?_\{?[A-Za-z0-9]+\}?)?"
pat = re.compile(r"(" + tok + r")\s*(?=" + tok + r")")
new, n = pat.subn(r"\1\\otimes", s)
open(p, "w", encoding="utf-8", newline="\n").write(new)
print("pass2 replacements:", n)

left = re.findall(tok + r"\s*(?=" + tok + r")", new)
print("remaining:", len(left))
for m in left[:10]:
    print("  ", m)
