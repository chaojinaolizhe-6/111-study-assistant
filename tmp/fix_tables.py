import re
p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
src = open(p, encoding="utf-8").read()

src = src.replace('"移动了 8 条"与"(n-1)h=8\\lambda"', '"移动了 8 条"与"$(n-1)h=8\\lambda$"')

mapping = {
 r"{@{}p{1.3cm}p{6.1cm}p{4.5cm}p{4.0cm}@{}}": r"{@{}p{1.25cm}p{5.3cm}p{6.0cm}p{3.1cm}@{}}",
 r"{@{}p{2.2cm}p{13.0cm}@{}}": r"{@{}p{2.1cm}p{13.4cm}@{}}",
 r"{@{}p{3.4cm}p{5.6cm}p{7.4cm}@{}}": r"{@{}p{3.2cm}p{5.4cm}p{7.9cm}@{}}",
 r"{@{}p{3.0cm}p{5.2cm}p{7.8cm}@{}}": r"{@{}p{2.8cm}p{5.0cm}p{7.6cm}@{}}",
 r"{@{}p{2.4cm}p{3.4cm}p{5.0cm}p{5.0cm}@{}}": r"{@{}p{2.1cm}p{3.3cm}p{4.7cm}p{4.9cm}@{}}",
 r"{@{}p{5.4cm}p{5.6cm}p{5.0cm}@{}}": r"{@{}p{5.0cm}p{5.4cm}p{5.6cm}@{}}",
}

def repl(m):
    spec = m.group(1)
    body = m.group(2)
    newspec = mapping.get(spec, spec)
    return "{\\small\\setlength{\\tabcolsep}{3pt}%\n\\noindent\\begin{tabular}" + newspec + "\n" + body + "\\end{tabular}}"

pat = re.compile(r"\\noindent\\begin\{tabular\}(\{[^\n]*\})\n(.*?)\\end\{tabular\}", re.S)
src, n = pat.subn(repl, src)
open(p, "w", encoding="utf-8", newline="\n").write(src)
print("tables wrapped:", n)
