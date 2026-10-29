import fitz
d = fitz.open(r"tmp\texbuild-optics\第五章-杨氏双缝与云母片-精讲-20261027.pdf")
for i in range(8, 11):
    t = d[i].get_text("text")
    print(f"===== p{i+1} =====")
    print(t.encode("utf-8", "replace").decode("utf-8")[:2600])
