import re
p = r"subjects\02-光学\讲义\第五章-杨氏双缝与云母片-精讲-20261027.tex"
s = open(p, encoding="utf-8").read()

m = re.search(r"\\subhdr\{0\.3 读的顺序（一条主线）\}.*?\\end\{enumerate\}\n", s, re.S)
print("roadmap block found:", bool(m))
block = m.group(0)
s = s.replace(block, "")

block = block.replace("\\subhdr{0.3 读的顺序（一条主线）}", "\\subhdr{0.1 读的顺序（一条主线）}")
anchor = "\\hdr{\\S0}{课件坐标、范围与记号}\n\n"
print("anchor S0:", s.count(anchor))
s = s.replace(anchor, anchor + "\n" + block + "\n", 1)

s = s.replace("\\subhdr{0.1 这 16 页分别在讲什么}", "\\subhdr{0.2 这 16 页分别在讲什么}")
s = s.replace("\\subhdr{0.2 记号表（全文只此一套）}", "\\subhdr{0.3 记号表（全文只此一套）}")
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("done")
