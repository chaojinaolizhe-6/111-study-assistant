p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
s = open(p, encoding="utf-8").read()
anchor = "\\aside{薄棱镜偏向角"
add = ("三行里只有洛埃镜的 $d=2a$ 是精确关系；双镜与双棱镜的 $d$ 都带小角近似（$\\sin\\alpha\\approx\\alpha$），"
       "顶角超过几度时要把 $\\alpha$ 换成 $\\sin\\alpha$，否则条纹间距会偏小。\n\n")
print("anchor:", s.count(anchor))
s = s.replace(anchor, add + anchor, 1)
open(p, "w", encoding="utf-8", newline="\n").write(s)
