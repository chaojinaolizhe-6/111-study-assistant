import docx, io, sys
base = r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\附件"
out = []
for name in ["附件1：培训方案.docx","附件2：自主学习材料.docx"]:
    p = base + "\\" + name
    out.append("########## " + name + " ##########")
    d = docx.Document(p)
    for para in d.paragraphs:
        t = para.text.strip()
        if t: out.append(t)
    for i, tb in enumerate(d.tables):
        out.append(f"--- table {i} ---")
        for row in tb.rows:
            cells=[]
            prev=None
            for c in row.cells:
                v=c.text.strip().replace("\n"," / ")
                if v!=prev: cells.append(v)
                prev=v
            out.append(" | ".join(cells))
    out.append("")
open(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\attachments.txt","w",encoding="utf-8").write("\n".join(out))
print("ok")
