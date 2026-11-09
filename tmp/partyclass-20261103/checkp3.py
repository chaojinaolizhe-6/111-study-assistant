import fitz
d=fitz.open(r"D:\aaa_D_usual\DSH\111学习助手\入党\马泽宇-20251091006-党课心得体会-定稿.pdf")
t=d[2].get_text()
i=t.find("第二件")
print(t[i:i+120])
