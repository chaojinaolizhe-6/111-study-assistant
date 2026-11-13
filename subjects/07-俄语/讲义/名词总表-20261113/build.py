# -*- coding: utf-8 -*-
"""把 content 里的词条生成 main.tex（俄语名词总表）。"""
import io, os

HERE = os.path.dirname(os.path.abspath(__file__))

PREAMBLE = r"""% !TEX program = xelatex
% 俄语 · 名词总表（按课件分类）· 2026-11-13
\documentclass[11pt]{ctexart}
\input{../../../../.dsh/skills/lecture-deepdive/assets/theme-violet}
\setmainfont{Times New Roman}
\setsansfont{Times New Roman}
\usepackage{longtable}
\setlength{\headheight}{22pt}
\settags{俄语 · 名词总表}{俄语（第二外语）}
\newcommand{\zn}[1]{{\color{violetdeep}\bfseries #1}}
\begin{document}
"""

HEAD = r"""
\doctitle{俄语名词总表}
{按课件分类 · УРОК 1--8 · 中俄双语}
{每一课的名词都按课件的分法归类：先看性（он／она́／оно́），再看数（单数→复数）；\\
收录 \textbf{%(count)d} 条（含跨课复现），重音、词性、复数一并给出 \quad 2026-11-13}

\hdr{§0}{怎么用这份表}

\callout{\textbf{这份表解决什么问题}：期末考的不是「背词典」，是\textbf{拿到一个名词，能立刻说出它配 этот 还是 эта、配 мой 还是 моя}。所以全表只有一个组织原则：\textbf{按课件的分类走}——У4 按性分，У5 按复数词尾分，У6 按物主代词的四栏分，У7、У8 按形容词、指示代词与名词的搭配分。每一节标题后面都标了课件页码，「У4 p13」就是第 4 课 PDF 的第 13 页，可以随时回去对。}

\subhdr{0.1　三栏怎么读}

\begin{minipage}{\linewidth}
\tabtop
\begin{tabular}{@{}p{0.16\linewidth}p{0.30\linewidth}p{0.46\linewidth}@{}}
\thead{栏} & \thead{写法} & \thead{意思} \\
\end{tabular}
\tabmid
\begin{tabular}{@{}p{0.16\linewidth}p{0.30\linewidth}p{0.46\linewidth}@{}}
俄语 & сло́во、тетра́дь & 重音符「´」标在重读元音上；一个词通常只有一个重音 \\
中文 & 词、练习本 & 取课件语境里的常用义，不堆词典义项 \\
性 · 数 & 中 · слова́ & 「阳／阴／中」是性，「·」后面是复数形式；「复」表示只有复数 \\
\end{tabular}
\tabbot
\end{minipage}

\subhdr{0.2　四种特殊写法}

\begin{itemize}
\item \textbf{常用单数}：молоко́、му́зыка、пого́да 这类词平时不用复数，考试也不会让你变复数。
\item \textbf{不变格}：ко́фе、метро́、пальто́、такси́ 永远一个写法，性靠记（ко́фе 是阳性，其余多是中性）。
\item \textbf{单数 фрукт}：表里给的是课件上的复数形式 фру́кты，单数另注。
\item \textbf{★}：出现在标题里，表示这一批是课件明确要求「需要记住／Запомните」的清单，优先级最高。
\end{itemize}

\warnbox{\textbf{一句提醒}：这份表是「认词」用的，不是「做题」用的。看的时候遮住右边两栏，只留俄语，先自己说中文和性；说不出来的，回到对应课的那一节，别在整张表上从头滑到尾。}

\subhdr{0.3　建议的三遍读法}

\begin{enumerate}
\item \textbf{第一遍（按课）}：从 §1 读到 §6，一课一课过。每节先看开头那句「这一课在讲什么」，再看表。
\item \textbf{第二遍（遮中文）}：只看俄语列，说中文、说性、说复数。错的词在页边画一道。
\item \textbf{第三遍（考前）}：只看 §7 速查卡和自己画过道的词；§7 是全表的「词尾规则压缩版」，考前一天翻两页就够。
\end{enumerate}
"""


def esc(s):
    return (s.replace('\\', r'\textbackslash{}')
             .replace('&', r'\&').replace('%', r'\%')
             .replace('#', r'\#').replace('_', r'\_'))


def table(rows, layout="std", title="", note="", cols=None):
    out = []
    if layout == "quad":
        ncol = 4
        colspec = r"{@{}p{0.235\linewidth}p{0.235\linewidth}p{0.235\linewidth}p{0.235\linewidth}@{}}"
        head = " & ".join(r"\thead{%s}" % esc(c) for c in (cols or ["", "", "", ""])) + r" \\"
    elif layout == "pair":
        ncol = 3
        colspec = r"{@{}p{0.22\linewidth}p{0.30\linewidth}p{0.44\linewidth}@{}}"
        head = r"\thead{单数} & \thead{复数} & \thead{中文} \\"
    else:
        ncol = 3
        colspec = r"{@{}p{0.27\linewidth}p{0.30\linewidth}p{0.37\linewidth}@{}}"
        head = r"\thead{俄语} & \thead{中文} & \thead{性 · 复数} \\"
    top = ""
    if title:
        top = r"\subhdr{%s}" % title
    if note:
        top += r"\par{\small %s}" % note
    out.append(r"\begin{longtable}" + colspec)
    if top:
        out.append(r"\multicolumn{%d}{@{}p{\linewidth}@{}}{%s} \\" % (ncol, top))
    out.append(r"\hline")
    out.append(head)
    out.append(r"\hline")
    out.append(r"\endfirsthead")
    out.append(r"\hline")
    out.append(head)
    if title:
        out.append(r"\multicolumn{%d}{@{}l}{\scriptsize\color{inkgray}（接上页）%s} \\" % (ncol, title))
    else:
        out.append(r"\multicolumn{%d}{@{}l}{\scriptsize\color{inkgray}（接上页）} \\" % ncol)
    out.append(r"\hline")
    out.append(r"\endhead")
    if layout == "quad":
        for row in rows:
            cells = [esc(c) for c in row] + [""] * (4 - len(row))
            out.append(" & ".join(cells) + r" \\")
    elif layout == "pair":
        for ru, pl, zh in rows:
            out.append("%s & %s & %s \\\\" % (esc(ru), esc(pl), esc(zh)))
    else:
        for ru, zh, g, num in rows:
            cell = esc(g) if g else ""
            tail = ("%s · %s" % (cell, esc(num))) if num and num != "—" else (cell or "—")
            out.append("%s & %s & %s \\\\" % (esc(ru), esc(zh), tail))
    out.append(r"\hline")
    out.append(r"\end{longtable}")
    return "\n".join(out)


def render(sections):
    total = 0
    for s in sections:
        for b in s["blocks"]:
            if b["kind"] != "table":
                continue
            if b.get("layout") == "quad":
                total += sum(1 for row in b["rows"] for c in row if c)
            else:
                total += len(b["rows"])
    body = [HEAD % {"count": total}]
    # 目录
    toc = [r"\begin{minipage}{\linewidth}", r"\subhdr{0.4　目录}", r"\tabtop",
           r"\begin{tabular}{@{}p{0.09\linewidth}p{0.76\linewidth}p{0.09\linewidth}@{}}"]
    for s in sections:
        toc.append(r"%s & %s & \pageref{sec:%s} \\" % (s["id"], s["title"], s["id"][1:]))
    toc.append(r"\end{tabular}")
    toc.append(r"\tabbot")
    toc.append(r"\end{minipage}")
    body.append("\n".join(toc))
    for sec in sections:
        body.append(r"\hdr{%s}{%s}\label{sec:%s}" % (sec["id"], sec["title"], sec["id"][1:]))
        for para in sec.get("intro", []):
            body.append(para)
        for b in sec["blocks"]:
            if b["kind"] == "table":
                body.append(table(b["rows"], b.get("layout", "std"),
                                  b.get("h", ""), b.get("note", ""), b.get("cols")))
            elif b["kind"] == "raw":
                body.append(b["tex"].replace(r"\subhdr{", r"\needspace{6\baselineskip}\subhdr{", 1))
            elif b["kind"] == "note":
                body.append(b["tex"])
    body.append(r"\end{document}")
    tex = PREAMBLE + "\n".join(body) + "\n"
    return tex.replace("★", r"\ding{72}")


if __name__ == "__main__":
    import c1, c2, c3
    sections = c1.SECTIONS + c2.SECTIONS + c3.SECTIONS
    tex = render(sections)
    with io.open(os.path.join(HERE, "main.tex"), "w", encoding="utf-8") as f:
        f.write(tex)
    print("written", len(tex), "chars")




