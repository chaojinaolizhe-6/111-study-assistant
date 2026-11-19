import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
files = ['answers.tex', 's5-7.tex', 's0-3.tex', 's4.tex', 's8-10.tex', 'exercises.tex', 'main.tex']
pat = re.compile(r'[\\$]*checkmark[\\$]*')
for f in files:
    t = open(f, encoding='utf-8').read()
    n = len(pat.findall(t))
    if n:
        t = pat.sub('$\\\\checkmark$', t)
        open(f, 'w', encoding='utf-8').write(t)
    print(f, n)

# 再检查是否还有缺反斜杠的希腊命令，如 $theta$
print('--- 可疑 $命令 ---')
for f in files:
    t = open(f, encoding='utf-8').read()
    for m in re.finditer(r'\$(theta|lambda|varphi|phi|mu|pi|sigma|omega|nu|alpha|beta|gamma|psi)\b', t):
        s = max(0, m.start() - 30)
        e = min(len(t), m.end() + 20)
        print(f, '|', t[s:e].replace('\n', ' '))
