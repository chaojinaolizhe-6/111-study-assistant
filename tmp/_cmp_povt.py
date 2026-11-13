import fitz, io, hashlib
a = r"D:\aaa..D盘常用文件夹\xwechat_files\wxid_4g9cekhsy71c22_9d64\temp\RWTemp\2026-11\24318051f261c76f046bd689fc7a6d8e\ПОВТОРЕНИЕ(1)(1).pdf"
b = r"D:\aaa_D_usual\DSH\111学习助手\subjects\07-俄语\课件\ПОВТОРЕНИЕ.pdf"
for name, path in (("微信副本", a), ("本地原件", b)):
    d = fitz.open(path)
    total = sum(len(p.get_text().strip()) for p in d)
    imgs = sum(len(p.get_images(full=True)) for p in d)
    print(f"{name}: pages={d.page_count} chars={total} images={imgs} meta={d.metadata.get('producer','')[:30]}")
    print("   page texts hash:", hashlib.md5("|".join(p.get_text().strip() for p in d).encode()).hexdigest())
