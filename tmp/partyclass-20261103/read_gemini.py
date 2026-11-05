import docx, re, csv, io
p=r"D:\aaa_D_usual\DSH\111学习助手\入党\马泽宇-20251091006-党课心得体会.docx"
d=docx.Document(p)
paras=[x.text.strip() for x in d.paragraphs]
text="\n".join([x for x in paras if x])
open(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\gemini_draft.txt","w",encoding="utf-8").write(text)
cn=len(re.findall(r"[\u4e00-\u9fff]", text)); allc=len(re.sub(r"\s","",text))
print("chars(no space):", allc, "hanzi:", cn, "paras:", len([x for x in paras if x]))
print("tables:", len(d.tables))
