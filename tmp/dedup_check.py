import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
files = ['answers.tex', 's5-7.tex', 's0-3.tex', 's4.tex', 's8-10.tex', 'exercises.tex', 'main.tex']
pat = re.compile(r'(?:[ \t]*\$\s*\\checkmark\s*\$)+')
for f in files:
    t = open(f, encoding='utf-8').read()
    n = len(pat.findall(t))
    if n:
        t = pat.sub(r' $\\checkmark$', t)
        open(f, 'w', encoding='utf-8').write(t)
    print(f, n)
