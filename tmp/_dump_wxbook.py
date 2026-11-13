import fitz, io, re
a = r"D:\aaa..D盘常用文件夹\xwechat_files\wxid_4g9cekhsy71c22_9d64\temp\RWTemp\2026-11\24318051f261c76f046bd689fc7a6d8e\ПОВТОРЕНИЕ(1)(1).pdf"
d = fitz.open(a)
out = []
for i, p in enumerate(d, 1):
    out.append(f"\n===== P{i} =====")
    out.append(p.get_text().strip())
io.open(r"tmp\wx_book.txt","w",encoding="utf-8").write("\n".join(out))
print("chars", sum(len(x) for x in out))
# 检查它自称的页码对应
t = "\n".join(out)
refs = re.findall(r"第\s*(\d+)\s*[-–]\s*(\d+)\s*页|第\s*(\d+)\s*页", t)
nums = sorted({int(x) for tup in refs for x in tup if x})
print("引用的复习文件页码:", nums)
