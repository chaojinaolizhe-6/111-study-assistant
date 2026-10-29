import subprocess, re, os
p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
lines = open(p, encoding="utf-8").read().splitlines()
theme = r"\input{D:/aaa_D_usual/DSH/111学习助手/.dsh/skills/lecture-deepdive/assets/theme-violet}"
os.makedirs(r"tmp\bisect", exist_ok=True)

def build(body, name):
    doc = "\\documentclass[11pt]{ctexart}\n" + theme + "\n\\begin{document}\n" + body + "\n\\end{document}\n"
    open(rf"tmp\bisect\{name}.tex", "w", encoding="utf-8").write(doc)
    subprocess.run(["xelatex", "-interaction=nonstopmode", f"{name}.tex"],
                   cwd=r"tmp\bisect", capture_output=True, text=True, errors="replace")
    log = open(rf"tmp\bisect\{name}.log", encoding="utf-8", errors="replace").read()
    ov = re.findall(r"Overfull \\hbox \(([\d.]+)pt too wide\)", log)
    print(name, "->", len(ov), ov[:5])

disp = "\n\\[\n\\vec{E}(P,t)=\\vec{E}_1(P,t)+\\vec{E}_2(P,t).\n\\]\n"
doct = "\n".join(lines[8:11])
call = "\n".join(lines[12:15])
tab = "\n".join(lines[25:46])
warn = lines[71]
hdr1 = lines[19]
sub1 = lines[21]
text1 = "p3--p5 给的是场矢量相加：" if False else "p3--p5 给的是场矢量相加："

build(doct + "\n" + disp, "v1")
build(doct + "\n" + call + "\n" + disp, "v2")
build(tab + "\n" + disp, "v3")
build(warn + "\n" + disp, "v4")
build(text1 + disp, "v5")
build("\\hdr{\\S1}{地基：叠加、强度、相干三条件}\n\\subhdr{1.1 叠加原理}\n" + text1 + disp, "v6")
