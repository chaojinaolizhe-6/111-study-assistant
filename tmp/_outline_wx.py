import fitz
a = r"D:\aaa..D盘常用文件夹\xwechat_files\wxid_4g9cekhsy71c22_9d64\temp\RWTemp\2026-11\24318051f261c76f046bd689fc7a6d8e\ПОВТОРЕНИЕ(1)(1).pdf"
d = fitz.open(a)
for i, p in enumerate(d, 1):
    t = p.get_text().strip().replace("\n", " | ")
    print(f"{i:3d} ({len(t):4d}): {t[:130]}")
