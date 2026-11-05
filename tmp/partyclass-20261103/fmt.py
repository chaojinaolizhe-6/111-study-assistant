import docx
from docx.shared import Pt
p=r"D:\aaa_D_usual\DSH\111学习助手\入党\马泽宇-20251091006-党课心得体会.docx"
d=docx.Document(p)
sec=d.sections[0]
print("page", round(sec.page_width.cm,2), round(sec.page_height.cm,2), "margins", round(sec.top_margin.cm,2), round(sec.left_margin.cm,2))
for i,par in enumerate(d.paragraphs):
    if not par.text.strip(): continue
    r=par.runs[0] if par.runs else None
    size = r.font.size.pt if (r and r.font.size) else None
    name = r.font.name if r else None
    ea = None
    if r is not None:
        rpr=r._element.rPr
        if rpr is not None:
            rf=rpr.rFonts
            if rf is not None: ea=rf.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}eastAsia')
    pf=par.paragraph_format
    print(i, "size",size,"font",name,"ea",ea,"align",par.alignment,"ls",pf.line_spacing,"indent",pf.first_line_indent.pt if pf.first_line_indent else None, "|", par.text[:18])
