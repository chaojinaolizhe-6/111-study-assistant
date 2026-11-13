# -*- coding: utf-8 -*-
"""把 content 里的形容词词条生成 main.tex（俄语形容词总表）。"""
import io, os

HERE = os.path.dirname(os.path.abspath(__file__))

PREAMBLE = r"""% !TEX program = xelatex
% 俄语 · 形容词总表（按课件分类）· 2026-11-13
\documentclass[11pt]{ctexart}
\input{../../../../.dsh/skills/lecture-deepdive/assets/theme-violet}
\setmainfont{Times New Roman}
\setsansfont{Times New Roman}
\usepackage{longtable}
\setlength{\headheight}{22pt}
\settags{俄语 · 形容词总表}{俄语（第二外语）}
\newcommand{\blank}{\underline{\hspace{3.2em}}}
\begin{document}
"""

HEAD = r"""
\doctitle{俄语形容词总表}
{按课件分类 · 五族词尾 · 中俄双语}
{УРОК 1--8 里出现的形容词全部收进来，按课件顺序分块；\\
每一条给出原形与阴／中／复三个形式，并标出它属于哪一族 \quad 2026-11-13}

\hdr{§0}{怎么用这份表}

\callout{\textbf{形容词只有一个难点}：词尾要跟着名词的性、数变。课件把它压成\textbf{五族}——硬词干、г／к／х、ж／ш／ч／щ、软词干、词尾重音。所以这份表按「族」组织：每条的\textbf{族}一栏告诉你它走哪一套词尾，右边三格直接给出阴、中、复三个形式。考试里的构形题（Это … (интересный) книга）只要做对两件事：\textbf{认出原形、选对族}。}

\subhdr{0.1　四栏怎么读}

\begin{minipage}{\linewidth}
\tabtop
\begin{tabular}{@{}p{0.14\linewidth}p{0.30\linewidth}p{0.46\linewidth}@{}}
\thead{栏} & \thead{写法} & \thead{意思} \\
\end{tabular}
\tabmid
\begin{tabular}{@{}p{0.14\linewidth}p{0.30\linewidth}p{0.46\linewidth}@{}}
原形 & но́вый & 阳性单数第一格，回答 Како́й?；词典、单词表都只收这一格 \\
中文 & 新的 & 取课件语境里的常用义 \\
族 & 硬／гкх／жшчщ／软／-ой & 词干类型，决定挂哪一套词尾（0.2） \\
三形式 & но́вая · но́вое · но́вые & 阴性（она́）、中性（оно́）、复数（они́） \\
\end{tabular}
\tabbot
\end{minipage}

\subhdr{0.2　五个族：为什么有的写 -ый，有的写 -ий}

\begin{minipage}{\linewidth}\small
\tabtop
\begin{tabular}{@{}p{0.15\linewidth}p{0.20\linewidth}p{0.16\linewidth}p{0.16\linewidth}p{0.16\linewidth}@{}}
\thead{族} & \thead{原形} & \thead{阴性} & \thead{中性} & \thead{复数} \\
\end{tabular}
\tabmid
\begin{tabular}{@{}p{0.15\linewidth}p{0.20\linewidth}p{0.16\linewidth}p{0.16\linewidth}p{0.16\linewidth}@{}}
硬词干 & но́вый & но́вая & но́вое & но́вые \\
г／к／х & высо́кий & высо́кая & высо́кое & высо́кие \\
ж, ш, ч, щ & хоро́ший & хоро́шая & хоро́шее & хоро́шие \\
软词干 & си́ний & си́няя & си́нее & си́ние \\
词尾重音 & голубо́й & голуба́я & голубо́е & голубы́е \\
\end{tabular}
\tabbot
\end{minipage}

\textbf{一句话记法}：\textbf{词干硬就 -ый／-ая／-ое／-ые；词干末是 г、к、х 就写 -ий（阴 -ая、中 -ое、复 -ие）；词干末是 ж、ш、ч、щ 也写 -ий，但中性换 -ее、复数仍是 -ие；词干软就 -ий／-яя／-ее／-ие；重音落在词尾就整族换 -о́й／-а́я／-о́е／-ы́е}。

\warnbox{\textbf{两个反例，考试最爱考}：\textbf{голубы́е}（浅蓝的复数）写 ы，因为词干末尾是 б，不在那七个字母里；\textbf{больши́е}（大的复数）写 и，因为词干末尾是 ш。判断依据永远是\textbf{词干最后一个字母}，不是整个词看起来像谁。}

\subhdr{0.3　建议的三遍读法}

\begin{enumerate}
\item \textbf{第一遍（按课）}：从 §1 读到 §10。每块标题后面的页码就是课件出处，可以回原 PDF 对。
\item \textbf{第二遍（遮右边）}：只看原形，先说中文、再说族、最后念出阴／中／复三个形式。
\item \textbf{第三遍（考前）}：只看 §11 速查卡，加上自己画过道的词。
\end{enumerate}
"""


def esc(s):
    return (s.replace('\\', r'\textbackslash{}')
             .replace('&', r'\&').replace('%', r'\%')
             .replace('#', r'\#').replace('_', r'\_'))


def table(rows, title="", note=""):
    out = []
    head = (r"\thead{原形（он）} & \thead{中文} & \thead{族} & "
            r"\thead{она́／оно́／они́} \\")
    top = ""
    if title:
        top = r"\subhdr{%s}" % title
    if note:
        top += r"\par{\small %s}" % note
    out.append(r"\begin{longtable}{@{}p{0.17\linewidth}p{0.19\linewidth}p{0.06\linewidth}p{0.52\linewidth}@{}}")
    if top:
        out.append(r"\multicolumn{4}{@{}p{\linewidth}@{}}{%s} \\" % top)
    out.append(r"\hline")
    out.append(head)
    out.append(r"\hline")
    out.append(r"\endfirsthead")
    out.append(r"\hline")
    out.append(head)
    if title:
        out.append(r"\multicolumn{4}{@{}l}{\scriptsize\color{inkgray}（接上页）%s} \\" % title)
    else:
        out.append(r"\multicolumn{4}{@{}l}{\scriptsize\color{inkgray}（接上页）} \\")
    out.append(r"\hline")
    out.append(r"\endhead")
    for ru, zh, fam, forms in rows:
        size = r"\footnotesize" if len(forms) > 42 else r"\small"
        out.append("%s & %s & %s & {%s %s} \\\\" % (esc(ru), esc(zh), esc(fam), size, esc(forms)))
    out.append(r"\hline")
    out.append(r"\end{longtable}")
    return "\n".join(out)


def render(sections):
    total = sum(len(b["rows"]) for s in sections for b in s["blocks"] if b["kind"] == "table")
    body = [HEAD % {"count": total}]
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
                body.append(table(b["rows"], b.get("h", ""), b.get("note", "")))
            elif b["kind"] == "raw":
                body.append(b["tex"].replace(r"\subhdr{", r"\needspace{6\baselineskip}\subhdr{", 1))
    body.append(r"\end{document}")
    tex = PREAMBLE + "\n".join(body) + "\n"
    return tex.replace("★", r"\ding{72}")


if __name__ == "__main__":
    import a1
    sections = a1.SECTIONS
    tex = render(sections)
    with io.open(os.path.join(HERE, "main.tex"), "w", encoding="utf-8") as f:
        f.write(tex)
    print("written", len(tex), "chars")






