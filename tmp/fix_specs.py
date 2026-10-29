import re
p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
src = open(p, encoding="utf-8").read()
R = r">{\raggedright\arraybackslash}"
specs = [
 f"{{@{{}}{R}p{{1.25cm}}{R}p{{5.3cm}}{R}p{{6.0cm}}{R}p{{3.1cm}}@{{}}}}",
 f"{{@{{}}{R}p{{2.1cm}}{R}p{{13.4cm}}@{{}}}}",
 f"{{@{{}}{R}p{{3.2cm}}{R}p{{5.4cm}}{R}p{{7.9cm}}@{{}}}}",
 f"{{@{{}}{R}p{{2.8cm}}{R}p{{5.0cm}}{R}p{{7.6cm}}@{{}}}}",
 f"{{@{{}}{R}p{{2.1cm}}{R}p{{3.3cm}}{R}p{{4.7cm}}{R}p{{4.9cm}}@{{}}}}",
 f"{{@{{}}{R}p{{5.0cm}}{R}p{{5.4cm}}{R}p{{5.6cm}}@{{}}}}",
]
cnt = [0]
def repl(m):
    i = cnt[0]; cnt[0] += 1
    return "\\begin{tabular}" + specs[i]

src = re.sub(r"\\begin\{tabular\}\{[^\n]*\}", repl, src)
open(p, "w", encoding="utf-8", newline="\n").write(src)
print("replaced:", cnt[0])
for s in specs: print(s[:50])
