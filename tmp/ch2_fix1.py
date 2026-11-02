# -*- coding: utf-8 -*-
import io, re
p = r"subjects\04-数学物理方法1\讲义\第二章-精讲-复变函数的积分-20261101.tex"
s = io.open(p, encoding="utf-8").read()
orig_len = len(s)

# ---- (a) 图与图注绑定 ----
s = s.replace(
"""% 图注
\\newcommand{\\figcap}[1]{\\par\\vspace{-2pt}{\\centering\\small\\color{inkgray}#1\\par}\\vspace{4pt}}""",
"""% 图与图注必须同页（局部自足）：用不可分的 minipage 绑在一起
\\newenvironment{figbox}{\\par\\begin{center}\\begin{minipage}{0.94\\linewidth}\\centering}{\\end{minipage}\\end{center}\\par}""")

# ---- (b) qbreak 阈值 ----
s = s.replace("\\begin{document}",
"""% 本章例题块平均半页强：把起页保护阈值从 0.92 页调到 0.62 页，
% 既保证「标题 + 题干 + 关键一步」不被拆开，又避免每道例题都逼出一页空白。
\\renewcommand{\\qbreak}{\\needspace{0.62\\textheight}}

\\begin{document}""", 1)

# ---- (c) 三张图改为 figbox ----
pat = re.compile(r"\\begin\{center\}\s*(\\begin\{tikzpicture\}.*?)\\figcap\{(.*?)\}\s*\\end\{center\}", re.S)
def rep(m):
    return ("\\begin{figbox}\n" + m.group(1).rstrip() +
            "\n\\par\\vspace{2pt}\n{\\small\\color{inkgray}" + m.group(2) + "\\par}\n\\end{figbox}")
s, n_fig = pat.subn(rep, s)

# ---- (d) §0 重排：把 53 页坐标表挪到 §0 末尾 ----
start = s.index("\\subhdr{0.1\\quad 53 页讲了什么}")
end = s.index("\\subhdr{0.2\\quad 记号：全文只用这一套}")
block = s[start:end]
s = s[:start] + s[end:]
block = block.replace("\\subhdr{0.1\\quad 53 页讲了什么}", "\\subhdr{0.3\\quad 53 页坐标表：页 $\\to$ 内容}")
block = block.replace("\\displaystyle", "")
anchor = "\\flowerrule\n\n\\hdr{§1}{定义：复积分就是两个实积分}"
s = s.replace(anchor, block.rstrip() + "\n\n" + anchor, 1)
s = s.replace("\\subhdr{0.2\\quad 记号：全文只用这一套}", "\\subhdr{0.1\\quad 记号：全文只用这一套}")
s = s.replace("\\subhdr{0.3\\quad 三处伏笔：课件埋了，但没在同一页回收}", "\\subhdr{0.2\\quad 三处伏笔：课件埋了，但没在同一页回收}")

# ---- (e) 两张表用 minipage 包住，防止跨页拆散 ----
t1_start = s.index("\\tabtop\n\\begin{tabular}{@{}ll@{}}\n\\thead{课件页}")
t1_end = s.index("\\tabbot", t1_start) + len("\\tabbot")
s = s[:t1_start] + "\\begin{minipage}{\\linewidth}\n" + s[t1_start:t1_end] + "\n\\end{minipage}" + s[t1_end:]

t2_start = s.index("\\tabtop\n\\begin{tabular}{@{}ll@{}}\n\\thead{本讲义}")
t2_end = s.index("\\tabbot", t2_start) + len("\\tabbot")
s = s[:t2_start] + "\\begin{minipage}{\\linewidth}\n" + s[t2_start:t2_end] + "\n\\end{minipage}" + s[t2_end:]

io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("figures:", n_fig, " len", orig_len, "->", len(s))
