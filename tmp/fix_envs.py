import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
files = ['main.tex', 's0-3.tex', 's4.tex', 's5-7.tex', 's8-10.tex', 'exercises.tex', 'answers.tex']
pairs = [('warnbox', '\\warnbox'), ('aside', '\\aside'), ('callout', '\\callout')]
for f in files:
    t = open(f, encoding='utf-8').read()
    total = 0
    for env, cmd in pairs:
        pat = re.compile(r'\\begin\{' + env + r'\}(.*?)\\end\{' + env + r'\}', re.S)
        t, n = pat.subn(lambda m: cmd + '{' + m.group(1).strip() + '}', t)
        total += n
    open(f, 'w', encoding='utf-8').write(t)
    print(f, 'converted', total)
