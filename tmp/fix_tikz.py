import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = r'subjects/05-数学物理方法2/讲义/第八章-8.4-精讲-球坐标分离变量-20261117/main.tex'
s = open(p, encoding='utf-8').read()

# 给各节点加最小高度，避免 TikZ 低估高度导致文字出框
repls = [
    (r'\\node\[box,text width=7\.3cm,anchor=north west\] \(A\) at \(0\.2,-2\.15\)',
     r'\\node[box,text width=7.3cm,minimum height=3.4cm,anchor=north west] (A) at (0.2,-2.10)'),
    (r'\\node\[box,text width=7\.3cm,anchor=north west\] \(B\) at \(7\.9,-2\.15\)',
     r'\\node[box,text width=7.3cm,minimum height=3.4cm,anchor=north west] (B) at (7.9,-2.10)'),
    (r'\\node\[cream,text width=7\.3cm,anchor=north west\] \(C\) at \(0\.2,-5\.00\)',
     r'\\node[cream,text width=7.3cm,minimum height=3.4cm,anchor=north west] (C) at (0.2,-5.75)'),
    (r'\\node\[cream,text width=7\.3cm,anchor=north west\] \(D\) at \(7\.9,-5\.00\)',
     r'\\node[cream,text width=7.3cm,minimum height=3.4cm,anchor=north west] (D) at (7.9,-5.75)'),
    (r'\\node\[box,text width=15\.2cm,anchor=north west\] \(E\) at \(0\.2,-9\.55\)',
     r'\\node[box,text width=15.2cm,minimum height=3.2cm,anchor=north west] (E) at (0.2,-9.45)'),
    (r'\\node\[box,text width=15\.2cm,anchor=north west\] \(F\) at \(0\.2,-13\.35\)',
     r'\\node[box,text width=15.2cm,minimum height=2.9cm,anchor=north west] (F) at (0.2,-13.05)'),
    (r'\\node\[cream,text width=15\.2cm,anchor=north west\] \(G\) at \(0\.2,-16\.75\)',
     r'\\node[cream,text width=15.2cm,minimum height=1.4cm,anchor=north west] (G) at (0.2,-16.35)'),
]
for old, new in repls:
    n = len(re.findall(old, s))
    s = re.sub(old, new, s)
    print(n, old[:40])
open(p, 'w', encoding='utf-8').write(s)
print('done')
