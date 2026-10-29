import fitz
d = fitz.open(r"tmp\texbuild-optics\第五章-杨氏双缝与云母片-精讲-20261027.pdf")
txt = []
for i, p in enumerate(d, 1):
    txt.append(f"===== p{i} =====\n" + p.get_text("text"))
open(r"tmp\lec_text.txt", "w", encoding="utf-8").write("\n".join(txt))
print("chars", sum(len(t) for t in txt))
