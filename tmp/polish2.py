p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
s = open(p, encoding="utf-8").read()

# 1) 修掉被写坏的中文引号转义
bad_open = "\\u201c"; bad_close = "\\u201d"
print("broken:", s.count(bad_open), s.count(bad_close))
s = s.replace(bad_open, "\u201c").replace(bad_close, "\u201d")

# 2) 自检整块挪到末页，别把「答案与要点」的小标题留在页底
anchor = "\\subhdr{12.2 自检三题"
print("anchor12.2:", s.count(anchor))
s = s.replace(anchor, "\\needspace{0.55\\textheight}\n" + anchor, 1)

# 3) 末页补一张英文术语对照（课件原文用词），并把它放在自检答案之后
R = ">{\\raggedright\\arraybackslash}"
term_table = (
"\n\\subhdr{12.3 英文术语对照（课件原文用词）}\n\n"
"课件是英文的，考试与作业也按英文出题，这里把本节出现的词与中文、与本文记号对齐。\n\n"
"{\\small\\setlength{\\tabcolsep}{3pt}%\n"
"\\noindent\\begin{tabular}{@{}" + R + "m{6.2cm}" + R + "m{3.6cm}" + R + "m{5.6cm}@{}}\n"
"\\thead{课件英文} & \\thead{中文} & \\thead{本文记号 / 位置}\\\\\n"
"\\tabmid\n"
"interference / interference fringes & 干涉 / 干涉条纹 & ---\\\\\n"
"constructive / destructive interference & 相长 / 相消干涉 & 明纹 / 暗纹（\\S2.2）\\\\\n"
"optical path / optical path difference & 光程 / 光程差 & $L=ns$，$\\Delta L$（\\S2.1）\\\\\n"
"fringe spacing & 条纹间距 & $\\Delta y$（双缝）、$\\Delta x$（其他装置）\\\\\n"
"contrast / visibility & 对比度 / 可见度 & $\\gamma$（\\S6）\\\\\n"
"wavefront division & 波前分割 & \\S7（与 p29 起的 split-amplitude division 相对）\\\\\n"
"spatial coherence & 空间相干性 & $b_c=\\lambda l/d$（\\S7.3）\\\\\n"
"half-wave loss & 半波损失 & 洛埃镜（\\S8.3）\\\\\n"
"Fresnel biprism / double mirror & 双棱镜 / 双平面镜 & p26--p27（\\S8.2）\\\\\n"
"\\end{tabular}}\n\\tabbot\n"
)

anchor2 = "\n\\flowerrule\n\n\\callout{\\textbf{交作业前的六项自检}"
print("anchor flowerrule+box:", s.count(anchor2))
s = s.replace(anchor2, term_table + anchor2, 1)

open(p, "w", encoding="utf-8", newline="\n").write(s)
print("ok")
