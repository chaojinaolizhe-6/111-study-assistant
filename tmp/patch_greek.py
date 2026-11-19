import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
files = ['main.tex', 's0-3.tex', 's4.tex', 's5-7.tex', 's8-10.tex', 'exercises.tex', 'answers.tex']
mp = {
    'θ': '$\\theta$',
    'φ': '$\\varphi$',
    'λ': '$\\lambda$',
    'μ': '$\\mu$',
    'π': '$\\pi$',
    'σ': '$\\sigma$',
    'ω': '$\\omega$',
    'ν': '$\\nu$',
}
for f in files:
    t = open(f, encoding='utf-8').read()
    n = 0
    for k, v in mp.items():
        c = t.count(k)
        if c:
            t = t.replace(k, v)
            n += c
    open(f, 'w', encoding='utf-8').write(t)
    print(f, 'replaced', n)
