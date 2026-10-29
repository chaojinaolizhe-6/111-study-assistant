p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
src = open(p, encoding="utf-8").read()

# 1) 补上遗漏的 \end{tabular}，并把表格收进 {\small + 3pt 列距} 的组
n_close = src.count("\\tabbot\n")
src = src.replace("\\tabbot\n", "\\end{tabular}\n\\tabbot}\n")
print("tabbot closed:", n_close)

mapping = {
 r"{@{}p{1.3cm}p{6.1cm}p{4.5cm}p{4.0cm}@{}}": r"{@{}p{1.25cm}p{5.3cm}p{6.0cm}p{3.1cm}@{}}",
 r"{@{}p{2.2cm}p{13.0cm}@{}}": r"{@{}p{2.1cm}p{13.4cm}@{}}",
 r"{@{}p{3.4cm}p{5.6cm}p{7.4cm}@{}}": r"{@{}p{3.2cm}p{5.4cm}p{7.9cm}@{}}",
 r"{@{}p{3.0cm}p{5.2cm}p{7.8cm}@{}}": r"{@{}p{2.8cm}p{5.0cm}p{7.6cm}@{}}",
 r"{@{}p{2.4cm}p{3.4cm}p{5.0cm}p{5.0cm}@{}}": r"{@{}p{2.1cm}p{3.3cm}p{4.7cm}p{4.9cm}@{}}",
 r"{@{}p{5.4cm}p{5.6cm}p{5.0cm}@{}}": r"{@{}p{5.0cm}p{5.4cm}p{5.6cm}@{}}",
}
n_open = 0
for old, new in mapping.items():
    pat = "\\noindent\\begin{tabular}" + old
    cnt = src.count(pat)
    n_open += cnt
    src = src.replace(pat, "{\\small\\setlength{\\tabcolsep}{3pt}%\n\\noindent\\begin{tabular}" + new)
print("tables opened:", n_open)

open(p, "w", encoding="utf-8", newline="\n").write(src)
