# -*- coding: utf-8 -*-
"""生成附录详解 answers.tex：把五份材料的题解统一成 P1–P20 的 \\answerstart 块。"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_ch7 import SRC, OUT, braced, parse_sections, emit, apply_refs
from build_ch8 import P82_REFS, P83_REFS

OLD_FILE = '第七章-精讲-数学物理方程-20261102.tex'
P19_FILE = '第七章-p19-作业四题-中英答案-20261109.tex'
HW_FILE = '第八章作业四题-分步详解-20261113.tex'
P82_FILE = '第八章-8.2-精讲-极坐标分离变量-20261116.tex'
P83_FILE = '第八章-8.3-精讲-柱坐标与贝塞尔方程-20261116.tex'


def sub_split(body):
    """按 \\subhdr{A.x} 切块，返回 {A.x: 文本}。"""
    pat = re.compile(r'\\subhdr\{A\.(\d)\\quad')
    out = {}
    marks = [(m.start(), m.group(1)) for m in pat.finditer(body)]
    for i, (s, k) in enumerate(marks):
        e = marks[i + 1][0] if i + 1 < len(marks) else len(body)
        out['A.' + k] = body[s:e]
    return out


def drop_cmd(text, cmd):
    """删掉以 cmd 开头的整条命令（含其花括号参数与行尾空白）。"""
    i = text.find(cmd)
    if i < 0:
        return text
    j = i + len(cmd)
    while j < len(text) and text[j] in ' \t':
        j += 1
    if j < len(text) and text[j] == '{':
        _, j = braced(text, j)
    return text[:i] + text[j:]


def build():
    old = parse_sections(open(os.path.join(SRC, OLD_FILE), encoding='utf-8').read())
    p19 = open(os.path.join(SRC, P19_FILE), encoding='utf-8').read()
    hw = open(os.path.join(SRC, HW_FILE), encoding='utf-8').read()
    p82 = parse_sections(open(os.path.join(SRC, P82_FILE), encoding='utf-8').read())
    p83 = parse_sections(open(os.path.join(SRC, P83_FILE), encoding='utf-8').read())

    parts = []
    parts.append('% ===================== 附录：练习详解 =====================\n')
    parts.append('\\clearpage\n\\phantomsection\\label{sec:answers}\n')
    parts.append('\\hdr{附录}{练习详解（P1--P20）}\n\n')
    parts.append('每块先复述题干与来源，再展开。正文只给题干与考点，步骤一律在这里；'
                 '做完一题再翻一题，比连着读五题有用。\n\n')

    # ---------- 附录 A：旧稿四道思考题（P1–P4）----------
    parts.append('\\hdrsub{A}{§7.1 的四道思考题（P1--P4）}\n\n')
    body = old['附录 A'][1]
    blocks = sub_split(body)
    meta = {
        'A.1': ('P1', '课件 p8 思考题',
                '同一种弦，把弦绷紧、换一根更粗的弦，音高分别怎么变？'),
        'A.2': ('P2', '课件 p13 提问',
                '杆的纵振动加单位长度外力 $F(x,t)$ 后方程怎么写？外力是自重（沿 $-x$）时又怎么写？'),
        'A.3': ('P3', '课件 p3 提问',
                '独立推导一维热传导方程，说明 $a^2$ 与 $f$ 各由哪些物理量组成。'),
        'A.4': ('P4', '按课件 p14 编排的数字练习',
                '膜的面密度 $\\rho=0.020\\ \\unit{kg\\cdot m^{-2}}$、张力 $T=2.0\\ \\unit{N\\cdot m^{-1}}$：'
                '(1) 求波速；(2) 加均匀单位面积外力 $f=0.50\\ \\unit{m\\cdot s^{-2}}$ 后写方程；(3) 说明 $f$ 的量纲。'),
    }
    for key in ['A.1', 'A.2', 'A.3', 'A.4']:
        pid, src, stem = meta[key]
        t = blocks[key]
        t = re.sub(r'^\\subhdr\{A\.\d\\quad[^}]*\}\s*', '', t)
        t = re.sub(r'\\label\{ans:q\d\}\s*', '', t)
        t = drop_cmd(t, '\\qstem')
        parts.append('\\answerstart{%s}{%s}{%s}\n' % (pid, src, stem))
        parts.append(t.strip() + '\n\n')

    # ---------- 附录 B：Ch7 p19 四题（P5–P8）----------
    parts.append('\\hdrsub{B}{§7.4 的四道定解条件题（P5--P8，课件 Ch7 p19）}\n\n')
    secs = parse_sections(p19)
    meta = {
        '题 1': ('P5', '课件 Ch7 p19 第 1 题', '长 $\\ell$ 的杆，左端固定；右端受沿外法向、大小为 $F(t)=F_0\\sin\\omega t$ 的力。写出边界条件。'),
        '题 2': ('P6', '课件 Ch7 p19 第 2 题', '长 $\\ell$ 的弦两端固定；$t=0$ 时在 $x=h$ 处受一外力 $F_0$。写出初始条件。'),
        '题 3': ('P7', '课件 Ch7 p19 第 3 题', '长 $\\ell$ 的杆两端各受一个大小 $F_0$ 的法向力，方向都指向杆内。写出边界条件。'),
        '题 4': ('P8', '课件 Ch7 p19 第 4 题', '长 $\\ell$ 的杆，两端各有热流 $q_0$ 流入杆内。写出边界条件。'),
    }
    for k in ['题 1', '题 2', '题 3', '题 4']:
        pid, src, stem = meta[k]
        t = secs[k][1]
        parts.append('\\answerstart{%s}{%s}{%s}\n' % (pid, src, stem))
        parts.append(t.strip() + '\n\n')

    # ---------- 附录 C：Ch8 p13 四题（P9–P12）----------
    parts.append('\\hdrsub{C}{§8.1 的四道分离变量题（P9--P12，课件 Ch8 p13）}\n\n')
    secs = parse_sections(hw)
    # 四题对照与自检清单放在题解之前，作为导读
    intro = secs['\\S6'][1]
    intro = intro.replace('\\subhdr{6.1\\quad 四题其实是「同一台机器换零件」}', '\\subhdr{四题对照：同一台机器换零件}')
    intro = intro.replace('\\subhdr{6.2\\quad 交卷前的六条自检}', '\\subhdr{交卷前的六条自检}')
    intro = intro.replace('\\pageref{sec:s1}', '\\pageref{sec:8111}')
    parts.append(intro.strip() + '\n\n')
    meta = {
        '\\S2': ('P9', '课件 Ch8 p13 第 1 题',
                '长 $\\ell$ 的弦两端固定，初始位移为峰在中点的三角波（斜率 $h$，峰值 $h\\ell/2$），初始速度为零。求 $u(x,t)$。'),
        '\\S3': ('P10', '课件 Ch8 p13 第 2 题',
                 '长 $\\ell$ 的杆左端固定、右端自由；初始位移为零，初始速度 $\\psi(x)=bx/\\ell$。求 $u(x,t)$。'),
        '\\S4': ('P11', '课件 Ch8 p13 第 3 题',
                 '长 $\\ell$ 的杆两端温度为零，初始温度 $u(x,0)=bx(\\ell-x)/\\ell^2$。求温度分布。'),
        '\\S5': ('P12', '课件 Ch8 p13 第 4 题',
                 '矩形 $0<x<a$、$0<y<b$，$\\nabla^2u=0$，边界为 $u(0,y)=u(a,y)=0$、$u(x,0)=A(1-x/a)$、$u(x,b)=0$。求 $u$。'),
    }
    for k in ['\\S2', '\\S3', '\\S4', '\\S5']:
        pid, src, stem = meta[k]
        t = secs[k][1]
        t = apply_refs(t, [('\\S2', '\\S8.1.6'), ('\\S3', '\\S8.1.9'), ('\\S4', '\\S8.1.16'),
                           ('\\S5', '\\S8.1.16'), ('\\S1.2', '\\S8.1.2'), ('\\S1.3', '\\S8.1.3'),
                           ('\\S6.4', '\\S8.1.19'), ('\\S6.5', '\\S8.1.20'), ('\\pageref{sec:s1}', '\\pageref{sec:8111}'),
                           ('表 1.2', '§8.1.2 的表')])
        parts.append('\\answerstart{%s}{%s}{%s}\n' % (pid, src, stem))
        parts.append(t.strip() + '\n\n')

    # 七个常见错误收在四题详解之后
    tail = secs['\\S7'][1]
    parts.append('\\subhdr{七个常见错误（按题号定位）}\n\n' + tail.strip() + '\n\n')
    parts.append('\\hdrsub{D}{§8.2 的四道极坐标题（P13--P16，自编）}\n\n')
    body = p82['附录 A'][1]
    body = apply_refs(body, [('\\S8.1', '\\xSA')])
    body = apply_refs(body, P82_REFS)
    body = apply_refs(body, [('\\xSA', '\\S8.1'), ('\\end{document}', '')])
    parts.append(renumber_answers(body, {'P1': 'P13', 'P2': 'P14', 'P3': 'P15', 'P4': 'P16'}))

    # ---------- 附录 E：§8.3 四题（P17–P20）----------
    parts.append('\\hdrsub{E}{§8.3 的四道柱坐标题（P17--P20，含课件 p6 作业）}\n\n')
    body = p83['附录 A'][1]
    body = apply_refs(body, [('\\S8.2', '\\xSB'), ('\\S8.1', '\\xSA')])
    body = apply_refs(body, P83_REFS)
    body = apply_refs(body, [('\\xSA', '\\S8.1'), ('\\xSB', '\\S8.2'), ('\\end{document}', '')])
    parts.append(renumber_answers(body, {'P1': 'P17', 'P2': 'P18', 'P3': 'P19', 'P4': 'P20'}))

    text = ''.join(parts).replace('\\end{document}', '')
    text = text.replace('本讲义', '本书').replace('本讲', '本书').replace('本册', '本书')
    emit(os.path.join(OUT, 'answers.tex'), text)


def renumber_answers(body, mapping):
    """把 \\answerstart{Pn} 的 ID 换掉（按最长键优先，避免 P1 命中 P13）。"""
    keys = sorted(mapping, key=len, reverse=True)
    pat = re.compile(r'\\answerstart\{(' + '|'.join(keys) + r')\}')
    body = pat.sub(lambda m: '\\answerstart{' + mapping[m.group(1)] + '}', body)
    # 附录内部若有 \pageref{ans:Pn} 一并改
    pat2 = re.compile(r'ans:(' + '|'.join(keys) + r')(?!\d)')
    body = pat2.sub(lambda m: 'ans:' + mapping[m.group(1)], body)
    body = re.sub(r'\\hdr\{附录 A\}\{[^}]*\}\s*', '', body)
    body = re.sub(r'\\phantomsection\\label\{sec:app\}\s*', '', body)
    return body.strip() + '\n\n'


if __name__ == '__main__':
    build()


