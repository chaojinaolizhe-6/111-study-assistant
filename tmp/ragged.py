import re
p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
src = open(p, encoding="utf-8").read()
specs = re.findall(r"\\noindent\\begin\{tabular\}(\{@\{\}[^\n]*@\{\}\})", src)
print("specs:", len(specs))
for s in specs:
    new = "{" + s.strip("{}").replace("p{", ">{\\raggedright\\arraybackslash}p{") + "}"
    src = src.replace("\\noindent\\begin{tabular}" + s, "\\noindent\\begin{tabular}" + new)
open(p, "w", encoding="utf-8", newline="\n").write(src)
print("done")
