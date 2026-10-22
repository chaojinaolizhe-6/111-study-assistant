# -*- coding: utf-8 -*-
import io
import sys
import runpy

out = io.open(r"tmp\lec-lap\textlayer.txt", "w", encoding="utf-8", newline="\n")
sys.stdout = out
sys.argv = [
    "read_slides.py",
    r"subjects\04-数理方法1\课件\第六章+拉普拉斯变换+-+上传课件.pdf",
    "--pages", "1-46",
    "--max-chars", "2500",
]
pdf = r"subjects\04-数学物理方法1\课件\第六章+拉普拉斯变换+-+上传课件.pdf"
sys.argv[1] = pdf
runpy.run_path(r".dsh\skills\lecture-deepdive\scripts\read_slides.py", run_name="__main__")
out.close()
print("OK")
