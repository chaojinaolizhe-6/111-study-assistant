import docx
p = r"D:\aaa_D_usual\DSH\111学习助手\入党\第36期入党积极分子培训-日程与准备清单-20261027.docx"
d = docx.Document(p)
lines=[]
for para in d.paragraphs:
    t=para.text.strip()
    if t: lines.append(t)
for tb in d.tables:
    lines.append("--- table ---")
    for row in tb.rows:
        cells=[]; prev=None
        for c in row.cells:
            v=c.text.strip().replace("\n"," / ")
            if v!=prev: cells.append(v)
            prev=v
        lines.append(" | ".join(cells))
open(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\checklist.txt","w",encoding="utf-8").write("\n".join(lines))
print("ok", len(lines))
