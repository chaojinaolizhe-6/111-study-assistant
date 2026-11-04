import zipfile, re
p=r"D:\aaa_D_usual\DSH\111学习助手\入党\第36期入党积极分子培训-心得体会-马泽宇-20251091006.docx"
x=zipfile.ZipFile(p).read("word/document.xml").decode("utf-8")
paras = re.findall(r"<w:p[ >].*?</w:p>", x, re.S)
for i,pp in enumerate(paras[:4]):
    txt = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", pp))
    rprs = re.findall(r"<w:rPr>(.*?)</w:rPr>", pp, re.S)
    print(i, repr(txt[:30]))
    for r in rprs[:3]:
        print("   ", re.sub(r"\s+"," ",r)[:160])
