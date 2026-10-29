import io
p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
src = open(p, encoding="utf-8").read()
src = src.replace(r"\begin{document}", "\\begin{document}\n\\typeout{DIAG hsize=\\the\\hsize textwidth=\\the\\textwidth linewidth=\\the\\linewidth}", 1)
open(r"tmp\modex\diag.tex", "w", encoding="utf-8").write(src.replace(r"\input{../../../.dsh", r"\input{D:/aaa_D_usual/DSH/111学习助手/.dsh"))
