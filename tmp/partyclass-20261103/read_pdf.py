import sys
try:
    import fitz
except ImportError:
    print("NO_PYMUPDF"); sys.exit(0)
p = r"D:\aaa..D盘常用文件夹\xwechat_files\wxid_4g9cekhsy71c22_9d64\msg\file\2026-09\思想汇报_2026年9月_第2篇.pdf"
d = fitz.open(p)
out=[]
for i,page in enumerate(d):
    out.append(f"=== page {i+1} ===")
    out.append(page.get_text())
open(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\sixiang_202609.txt","w",encoding="utf-8").write("\n".join(out))
print("ok", len(d))
