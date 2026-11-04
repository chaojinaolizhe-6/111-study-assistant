# -*- coding: utf-8 -*-
"""收尾修补（2026-11-04，实验5 讲义）：列宽 + 中文引号。"""
import io

p = r"D:\aaa_D_usual\DSH\111学习助手\subjects\06-电工电子技术\实验\实验5-单管放大电路-实验讲义-20261104.tex"
s = io.open(p, encoding="utf-8").read()

pairs = [
    (r"\begin{tabular}{@{}p{1.5cm}p{8.2cm}p{6.4cm}@{}}",
     r"\begin{tabular}{@{}p{1.8cm}p{8.0cm}p{6.3cm}@{}}"),
    (r"\begin{tabular}{@{}p{1.9cm}p{1.3cm}p{1.3cm}p{1.3cm}p{1.4cm}p{1.5cm}p{1.4cm}p{1.4cm}p{1.9cm}@{}}",
     r"\begin{tabular}{@{}p{1.6cm}p{1.25cm}p{1.25cm}p{1.25cm}p{1.35cm}p{1.4cm}p{1.35cm}p{1.35cm}p{2.35cm}@{}}"),
    (r"\begin{tabular}{@{}p{3.6cm}p{5.4cm}p{6.2cm}@{}}",
     r"\begin{tabular}{@{}p{4.7cm}p{3.4cm}p{7.1cm}@{}}"),
    (r"\begin{tabular}{@{}p{4.6cm}p{4.4cm}p{3.0cm}p{2.8cm}@{}}",
     r"\begin{tabular}{@{}p{4.3cm}p{4.0cm}p{2.6cm}p{4.4cm}@{}}"),
]
for a, b in pairs:
    if a not in s:
        print("MISS:", a[:50])
    s = s.replace(a, b)

n = s.count('"')
assert n % 2 == 0, f"引号数 {n} 不是偶数"
out = []
open_q = True
for ch in s:
    if ch == '"':
        out.append("“" if open_q else "”")
        open_q = not open_q
    else:
        out.append(ch)
io.open(p, "w", encoding="utf-8").write("".join(out))
print("ok, quotes:", n)
