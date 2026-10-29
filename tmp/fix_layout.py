p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
s = open(p, encoding="utf-8").read()

# (a) 去掉多余的 $\ $ 空格
s = s.replace("观察点必须走到$\\ $离上缝更近", "观察点必须走到离上缝更近")

# (b) 表格列改为垂直居中 m{}，并调整两处列宽
s = s.replace(">{\\raggedright\\arraybackslash}p{", ">{\\raggedright\\arraybackslash}m{")
s = s.replace("p{2.1cm}>{\\raggedright\\arraybackslash}m{3.3cm}>{\\raggedright\\arraybackslash}m{4.7cm}>{\\raggedright\\arraybackslash}m{4.9cm}",
              "p{2.1cm}>{\\raggedright\\arraybackslash}m{3.2cm}>{\\raggedright\\arraybackslash}m{5.2cm}>{\\raggedright\\arraybackslash}m{4.8cm}")
s = s.replace("m{5.0cm}>{\\raggedright\\arraybackslash}m{5.4cm}>{\\raggedright\\arraybackslash}m{5.6cm}",
              "m{6.3cm}>{\\raggedright\\arraybackslash}m{4.6cm}>{\\raggedright\\arraybackslash}m{5.0cm}")
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("m cols:", s.count("arraybackslash}m{"))
