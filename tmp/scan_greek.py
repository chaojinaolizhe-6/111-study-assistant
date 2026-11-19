import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
files = ['main.tex', 's0-3.tex', 's4.tex', 's5-7.tex', 's8-10.tex', 'exercises.tex', 'answers.tex']
chars = 'θφλμπσων'
for f in files:
    t = open(f, encoding='utf-8').read()
    for ch in chars:
        for m in re.finditer(re.escape(ch), t):
            s = max(0, m.start() - 25)
            e = min(len(t), m.end() + 20)
            line = t.count('\n', 0, m.start()) + 1
            print(f, ch, 'L%d' % line, '|', t[s:e].replace('\n', ' '))
