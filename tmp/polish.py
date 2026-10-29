p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
s = open(p, encoding="utf-8").read()

# (a) ASCII 引号按行成对换成中文引号
out = []
for line in s.split("\n"):
    if '"' not in line:
        out.append(line); continue
    res, open_q = [], True
    for ch in line:
        if ch == '"':
            res.append("\u201c" if open_q else "\u201d")
            open_q = not open_q
        else:
            res.append(ch)
    out.append("".join(res))
s = "\n".join(out)
print("quotes left:", s.count('"'))

# (b) §6.2 那句写糊了，改清楚
old = "：$\\gamma=1$，$I_{\\max}=4I_0/2$ 型的完全调制；$\\rho\\to0$ 或 $\\rho\\to\\infty$：$\\gamma\\to0$，条纹消失。"
new = "：$\\gamma=1$，$I_{\\min}=0$、$I_{\\max}=2I_0$，条纹从全黑到全亮；$\\rho\\to0$ 或 $\\rho\\to\\infty$：$\\gamma\\to0$，条纹消失。"
print("rho fix:", s.count(old))
s = s.replace(old, new)

# (c) 末尾补一个交作业前的自检框，占满末页并直接服务作业
anchor = "\\callout{\\textbf{下一步。}"
box = ("\\callout{\\textbf{交作业前的六项自检}：\\textcircled{1} 图上标清被盖的 $S_1$、另一条缝 $S_2$、$P$ 与 $O$；"
       "\\textcircled{2} 写出\\u201c新零级 $\\Leftrightarrow$ 光程差为零\\u201d这一句；"
       "\\textcircled{3} 片厚一律写 $h$，别再用 $d$；"
       "\\textcircled{4} 级次取 $m=8$，并用一句话写明你的计数约定（零级算第 1 条）；"
       "\\textcircled{5} 答出移动方向：向被盖住的那条缝一侧；"
       "\\textcircled{6} 答案写 $h=7.6\\ \\mu\\mathrm{m}$，并核对量纲与数量级（14 个波长上下）。}\n\n")
print("anchor:", s.count(anchor))
s = s.replace(anchor, box + anchor, 1)

open(p, "w", encoding="utf-8", newline="\n").write(s)
