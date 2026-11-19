import re, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'subjects/05-数学物理方法2/讲义/第八章-8.4-精讲-球坐标分离变量-20261117'
LOCAL = {'s0-3', 's4', 's5-7', 's8-10', 'exercises', 'answers'}


def expand(name):
    text = open(os.path.join(BASE, name + '.tex'), encoding='utf-8').read()

    def repl(m):
        t = m.group(1).strip()
        if t in LOCAL:
            return '\n%% ==== begin %s ====\n' % t + expand(t) + '\n%% ==== end %s ====\n' % t
        return m.group(0)

    return re.sub(r'\\input\{([^}]*)\}', repl, text)


out = expand('main').replace('\\end{document}', '')
open(os.path.join(BASE, 'main-flat.tex'), 'w', encoding='utf-8').write(out)
print('wrote', len(out.split('\n')), 'lines')
