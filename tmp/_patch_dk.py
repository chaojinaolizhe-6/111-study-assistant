# -*- coding: utf-8 -*-
import io, sys
p = r"大创\答辩准备-MPS-LD马赫探针-20261112.tex"
s = io.open(p, encoding="utf-8").read()
pairs = [
 (r"{\small 项目负责人：马泽宇　｜　指导教师：桑超峰　｜　物理学院　｜　编号 20271014111371　｜　2026 年 11 月}",
  r"{\small 项目负责人：马泽宇　｜　指导教师：桑超峰　｜　物理学院}\\[3pt]" "\n" r"{\small 项目编号 20271014111371　｜　2026 年 11 月}"),
 (r"\begin{tabular}{@{}p{2.1cm}p{3.2cm}p{10.2cm}@{}}",
  r"\begin{tabular}{@{}>{\raggedright\arraybackslash}p{2.1cm}>{\raggedright\arraybackslash}p{3.2cm}>{\raggedright\arraybackslash}p{10.2cm}@{}}"),
 (r"\section{答辩问答（20 题）}",
  r"\clearpage" "\n" r"\section{答辩问答（20 题）}"),
]
for old, new in pairs:
    if s.count(old) != 1:
        print("pattern", s.count(old), old[:40]); sys.exit(1)
    s = s.replace(old, new)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched")
