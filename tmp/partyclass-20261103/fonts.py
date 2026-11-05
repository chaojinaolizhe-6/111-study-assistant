import docx
from docx.oxml.ns import qn
p=r"D:\aaa_D_usual\DSH\111学习助手\入党\马泽宇-20251091006-党课心得体会.docx"
d=docx.Document(p)
out=[]
for i,par in enumerate(d.paragraphs):
    if not par.text.strip(): continue
    r=par.runs[0]
    rpr=r._element.rPr
    ea=ascii_=None
    if rpr is not None and rpr.rFonts is not None:
        ea=rpr.rFonts.get(qn('w:eastAsia')); ascii_=rpr.rFonts.get(qn('w:ascii'))
    out.append((i, ea, ascii_, r.font.size.pt if r.font.size else None, par.text[:14]))
open(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\fonts.txt","w",encoding="utf-8").write("\n".join(map(str,out)))
print("ok")
