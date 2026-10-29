import subprocess, re, os
p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
lines = open(p, encoding="utf-8").read().splitlines()
head = "\n".join(lines[:1])
theme = r"\input{D:/aaa_D_usual/DSH/111学习助手/.dsh/skills/lecture-deepdive/assets/theme-violet}"
os.makedirs(r"tmp\bisect", exist_ok=True)

def build(rng, name):
    body = "\n".join(lines[i-1] for i in rng)
    doc = "\\documentclass[11pt]{ctexart}\n" + theme + "\n" + body + "\n\\end{document}\n"
    open(rf"tmp\bisect\{name}.tex", "w", encoding="utf-8").write(doc)
    r = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", f"{name}.tex"],
                       cwd=r"tmp\bisect", capture_output=True, text=True, errors="replace")
    log = open(rf"tmp\bisect\{name}.log", encoding="utf-8", errors="replace").read()
    ov = re.findall(r"Overfull \\hbox \(([\d.]+)pt too wide\) (?:detected at line (\d+)|in paragraph at lines (\d+)--(\d+))", log)
    print(name, "->", len(ov), "overfull", ov[:4])

build(list(range(7, 91)), "t_a")   # begin document .. display + aside
build(list(range(7, 84)), "t_b")   # up to line before display
