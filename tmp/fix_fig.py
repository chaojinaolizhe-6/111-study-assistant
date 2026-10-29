p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
s = open(p, encoding="utf-8").read()

old1 = "  \\fill (6,0.40) circle (1.2pt) node[above left=-1pt]{$S_1$};\n  \\fill (6,-0.40) circle (1.2pt) node[below left=-1pt]{$S_2$};"
new1 = ("  \\fill (6,0.40) circle (1.2pt);\n  \\node[anchor=west] at (6.10,0.60) {\\scriptsize $S_1$};\n"
        "  \\fill (6,-0.40) circle (1.2pt);\n  \\node[anchor=west] at (6.10,-0.60) {\\scriptsize $S_2$};")
print("labels:", s.count(old1))
s = s.replace(old1, new1)

old2 = "  \\draw[->] (12.0,-0.15)--(12.0,-2.0) node[right=2pt] {\\scriptsize $y$};"
new2 = ("  \\draw[->] (12.35,-0.20)--(12.35,0.95) node[above=1pt] {\\scriptsize $y$};")
print("yaxis:", s.count(old2))
s = s.replace(old2, new2)

old3 = "  \\draw[<->] (6.9,0.40)--(6.9,-0.40) node[midway,right=2pt] {\\scriptsize $d$};"
new3 = "  \\draw[<->] (6.45,0.40)--(6.45,-0.40) node[midway,right=2pt] {\\scriptsize $d$};"
print("darrow:", s.count(old3))
s = s.replace(old3, new3)

open(p, "w", encoding="utf-8", newline="\n").write(s)
