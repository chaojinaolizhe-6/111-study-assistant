# -*- coding: utf-8 -*-
"""合并引擎：把分册 tex 的 section/subhdr 块按配置搬运、重编号、替换引用。

用法：在仓库根运行 python -B tmp/build_ch7.py
输出到 subjects/05-数学物理方法2/讲义/合集-第七八章-20261117/
"""
import re, os

SRC = r'subjects/05-数学物理方法2/讲义'
OUT = r'subjects/05-数学物理方法2/讲义/合集-第七八章-20261117'

HDR = re.compile(r'\\hdr\s*\{')


def braced(s, i):
    """s[i] 必须是 '{'；返回 (内容, 结束位置)。"""
    assert s[i] == '{', (s[i:i+10], i)
    depth = 0
    j = i
    while j < len(s):
        c = s[j]
        if c == '\\':
            j += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    raise ValueError('unbalanced braces')


def parse_sections(text):
    """返回 {节号字符串: (标题, body)}，节号取 \hdr 第一参数原样（可能含 \S）。"""
    starts = []
    for m in HDR.finditer(text):
        i = m.end() - 1
        num, j = braced(text, i)
        while j < len(text) and text[j] in ' \t':
            j += 1
        title, k = braced(text, j)
        starts.append((num.strip(), title.strip(), m.start(), k))
    out = {}
    for idx, (num, title, s, e) in enumerate(starts):
        end = starts[idx + 1][2] if idx + 1 < len(starts) else len(text)
        body = text[e:end]
        # 各分册在 \hdr 之后紧跟 \phantomsection\label{sec:sN}；合集自己重写 label，去掉这一处
        body = re.sub(r'^\s*\\phantomsection\s*\\label\{[^}]*\}', '', body, count=1)
        out[num] = (title, body)
    return out


SUB = re.compile(r'\\subhdr\s*\{')


def split_subs(body):
    """返回 [(编号或None, 标题, 整段文本)]；第一段是 \subhdr 之前的引言（编号为 'LEAD'）。"""
    pos = []
    for m in SUB.finditer(body):
        i = m.end() - 1
        content, j = braced(body, i)
        pos.append((m.start(), j, content))
    blocks = []
    if not pos:
        return [('LEAD', '', body)]
    blocks.append(('LEAD', '', body[:pos[0][0]]))
    for idx, (s, e, content) in enumerate(pos):
        end = pos[idx + 1][0] if idx + 1 < len(pos) else len(body)
        mm = re.match(r'^(\d+(?:\.\d+)*)\\quad\s*(.*)$', content, re.S)
        if mm:
            blocks.append((mm.group(1), mm.group(2), body[s:end]))
        else:
            blocks.append((None, content, body[s:end]))
    return blocks


def transform(body, submap, skip_ranges=()):
    """重写 \\subhdr 编号，删除 skip 范围内的子块。"""
    blocks = split_subs(body)
    out = []
    skipping = False
    for num, title, raw in blocks:
        if num == 'LEAD':
            out.append(raw)
            continue
        if skipping:
            if num is not None and not any(_in_range(num, a, b) for a, b in skip_ranges):
                skipping = False
            else:
                continue
        if num is not None:
            for a, b in skip_ranges:
                if num == a:
                    skipping = True
                    break
            if skipping:
                continue
        if num is not None and num in submap:
            pos = raw.index('\\subhdr') + len('\\subhdr')
            _, j = braced(raw, pos)
            newnum = submap[num]
            if newnum is None:
                head = raw[:raw.index('\\subhdr')] + '\\subhdr{' + title + '}'
            else:
                head = raw[:raw.index('\\subhdr')] + '\\subhdr{' + newnum + '\\quad ' + title + '}'
            out.append(head + raw[j:])
        else:
            out.append(raw)
    return ''.join(out)


def _in_range(num, a, b):
    """num 是否落在 [a, b) 之间；b 为 None 表示无上界。"""
    if _tupl(num) < _tupl(a):
        return False
    if b is None:
        return True
    return _tupl(num) < _tupl(b)


def _tupl(s):
    return tuple(int(x) for x in s.split('.'))


def _geq(a, b):
    return _tupl(a) >= _tupl(b)


def _leq_lt(a, b):
    return _tupl(a) < _tupl(b)


def apply_refs(text, refs):
    """一次性替换：按最长匹配扫描原文，替换结果不再被后续规则命中。"""
    pairs = [(o, n) for o, n in refs if o]
    if not pairs:
        return text
    table = dict(pairs)
    pat = re.compile('|'.join(re.escape(k) for k, _ in sorted(pairs, key=lambda p: -len(p[0]))))
    return pat.sub(lambda m: table[m.group(0)], text)


def emit(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8', newline='\n').write(text)
    print('wrote', path, len(text.split('\n')), 'lines')


# ---------------------------------------------------------------- 来源一：旧稿第七章
OLD_FILE = '第七章-精讲-数学物理方程-20261102.tex'
OLD_SECTIONS = [
    # (原节号, 新节号, 新标题, submap, skip)
    ('§1', '7.1.1', '宏观态为什么是偏微分方程', {
        '1.1': '7.1.1.1', '1.2': '7.1.1.2', '1.3': '7.1.1.3', '1.5': '7.1.1.4',
    }, [('1.4', '1.5')]),
    ('§2', '7.1.2', '弦的横振动：一条完整的推导', {
        '2.1': '7.1.2.1', '2.2': '7.1.2.2', '2.3': '7.1.2.3', '2.4': '7.1.2.4',
        '2.5': '7.1.2.5', '2.6': '7.1.2.6', '2.7': '7.1.2.7',
    }, []),
    ('§3', '7.1.3', '外力与非齐次方程', {
        '3.1': '7.1.3.1', '3.2': '7.1.3.2', '3.3': '7.1.3.3',
    }, []),
    ('§4', '7.1.4', '杆的纵振动：同一个方程，换一个速度', {
        '4.1': '7.1.4.1', '4.2': '7.1.4.2', '4.3': '7.1.4.3', '4.4': '7.1.4.4',
        '4.5': '7.1.4.5', '4.6': '7.1.4.6',
    }, []),
    ('§5', '7.1.5', '膜的横振动：二维情形', {
        '5.1': '7.1.5.1', '5.2': '7.1.5.2', '5.3': '7.1.5.3', '5.4': '7.1.5.4',
        '5.5': '7.1.5.5',
    }, []),
    ('§6', '7.1.6', '电磁波：把麦克斯韦方程组变成波动方程', {
        '6.1': '7.1.6.1', '6.2': '7.1.6.2', '6.3': '7.1.6.3', '6.4': '7.1.6.4',
        '6.5': '7.1.6.5',
    }, []),
    ('§7', '7.1.7', '三个方程是同一副骨架', {
        '7.1': '7.1.7.1',
    }, [('7.2', None)]),
    ('§9', '7.1.8', '公式卡与四步用法', {
        '9.1': '7.1.8.1', '9.2': '7.1.8.2',
    }, []),
]

OLD_REFS = [
    ('§1.5', '§7.1.1.4'),
    ('§1.1', '§7.1.1.1'),
    ('§1.2', '§7.1.1.2'),
    ('§2.1', '§7.1.2.1'), ('§2.2', '§7.1.2.2'), ('§2.3', '§7.1.2.3'),
    ('§2.4', '§7.1.2.4'), ('§2.5', '§7.1.2.5'), ('§2.6', '§7.1.2.6'), ('§2.7', '§7.1.2.7'),
    ('§3.1', '§7.1.3.1'), ('§3.2', '§7.1.3.2'), ('§3.3', '§7.1.3.3'),
    ('§4.1', '§7.1.4.1'), ('§4.4', '§7.1.4.4'), ('§4.5', '§7.1.4.5'), ('§4.6', '§7.1.4.6'),
    ('§5.1', '§7.1.5.1'), ('§5.2', '§7.1.5.2'), ('§5.3', '§7.1.5.3'),
    ('§5.4', '§7.1.5.4'),
    ('§6.1', '§7.1.6.1'), ('§6.2', '§7.1.6.2'), ('§6.3', '§7.1.6.3'),
    ('§6.4', '§7.1.6.4'), ('§6.5', '§7.1.6.5'),
    ('§9.1', '§7.1.8.1'), ('§9.2', '§7.1.8.2'),
    ('\\S0.2', '本章开头的表'),
    ('§0.1', '记号表'),
    ('§7.2', '§7.4'),
    ('§10', '§7.5'),
    ('label{sec:s1}', 'label{sec:711}'),
    ('label{sec:s2}', 'label{sec:712}'),
    ('label{sec:s3}', 'label{sec:713}'),
    ('label{sec:s4}', 'label{sec:714}'),
    ('label{sec:s5}', 'label{sec:715}'),
    ('label{sec:s6}', 'label{sec:716}'),
    ('label{sec:s7}', 'label{sec:717}'),
    ('label{sec:s9}', 'label{sec:718}'),
    ('label{sec:s10}', 'label{sec:75-old}'),
    ('图 1', '图 7-1'), ('图 2', '图 7-2'), ('图 3', '图 7-3'),
    ('本讲义', '本书'), ('本讲', '本书'), ('本册', '本书'),
    ('pageref{ans:q1}', 'pageref{ans:P1}'),
    ('pageref{ans:q2}', 'pageref{ans:P2}'),
    ('pageref{ans:q3}', 'pageref{ans:P3}'),
    ('pageref{ans:q4}', 'pageref{ans:P4}'),
]

# ---------------------------------------------------------------- 来源二：合册
BOOK_FILE = '第七八章-精讲-输运方程与分离变量-20261110.tex'
BOOK_SECTIONS = [
    ('\\S1', '7.2', '输运方程：热传导与扩散', {
        '1.1': '7.2.1', '1.2': '7.2.2', '1.3': '7.2.3', '1.4': '7.2.4', '1.5': '7.2.5',
    }, []),
    ('\\S2', '7.3', '泊松方程：稳态的三种外衣', {
        '2.1': '7.3.1', '2.2': '7.3.2', '2.3': '7.3.3', '2.4': '7.3.4', '2.5': '7.3.5',
    }, []),
    ('\\S3', '7.4', '定解条件：方程为什么定不住解', {
        '3.1': '7.4.1', '3.2': '7.4.2', '3.3': '7.4.3', '3.4': '7.4.4',
        '3.4.1': '7.4.4.1', '3.4.2': '7.4.4.2', '3.4.3': '7.4.4.3',
        '3.5': '7.4.5', '3.6': '7.4.6', '3.7': '7.4.7',
    }, []),
]

BOOK_REFS = [
    ('\\S3.4.1', '\\S7.4.4.1'), ('\\S3.4.2', '\\S7.4.4.2'), ('\\S3.4.3', '\\S7.4.4.3'),
    ('\\S3.1', '\\S7.4.1'), ('\\S3.2', '\\S7.4.2'), ('\\S3.3', '\\S7.4.3'),
    ('\\S3.5', '\\S7.4.5'), ('\\S3.6', '\\S7.4.6'), ('\\S3.7', '\\S7.4.7'),
    ('\\S1.1', '\\S7.2.1'), ('\\S1.2', '\\S7.2.2'), ('\\S1.3', '\\S7.2.3'),
    ('\\S1.4', '\\S7.2.4'), ('\\S1.5', '\\S7.2.5'),
    ('\\S2.1', '\\S7.3.1'), ('\\S2.2', '\\S7.3.2'), ('\\S2.3', '\\S7.3.3'),
    ('\\S2.4', '\\S7.3.4'), ('\\S2.5', '\\S7.3.5'),
    ('\\S1', '\\S7.2'), ('\\S2', '\\S7.3'), ('\\S3', '\\S7.4'),
    ('\\S5.1', '\\S8.1.11'), ('附录 A.2', '附录 P2'),
    ('\\S7.1', '\\S7.5.1'), ('\\S7.2', '\\S7.5.2'), ('\\S7.3', '\\S7.5.3'),
    ('\\S7', '\\S7.5'), ('\\S9', '\\S7.6'),
    ('label{sec:s1}', 'label{sec:72}'),
    ('label{sec:s2}', 'label{sec:73}'),
    ('label{sec:s3}', 'label{sec:74}'),
    ('label{sec:s7}', 'label{sec:75}'),
    ('label{sec:s9}', 'label{sec:76}'),
    ('图 1', '图 7-4'), ('本讲义', '本书'), ('本讲', '本书'), ('本册', '本书'),
]


def build_ch7():
    old = parse_sections(open(os.path.join(SRC, OLD_FILE), encoding='utf-8').read())
    book = parse_sections(open(os.path.join(SRC, BOOK_FILE), encoding='utf-8').read())

    parts = []
    parts.append('% ===================== 第七章 数学物理方程与定解条件 =====================\n')
    parts.append('\\phantomsection\\label{sec:ch7}\n\\chapterhead{数学物理方法（II）· 第七章}{数学物理方程与定解条件}\n\n')
    parts.append('本章从守恒律与本构关系出发，把弦、杆、膜、电磁波、热传导、扩散与静电场\n')
    parts.append('统一写成三类方程，然后说清一个方程要配哪些初始条件与边界条件才定得住解。\n')
    parts.append('后面第八章的每一种解法，都以本章的方程分类与条件写法为前提。\n\n')

    # 7.1 波动方程（旧稿 §1-§9 重组）
    parts.append('% ------------------------------ §7.1 ------------------------------\n')
    parts.append('\\hdr{\\S7.1}{波动方程：从弦到电磁波的同一条骨架}\n\\phantomsection\\label{sec:71}\n\n')
    parts.append('本节依据 2026-11-02 的 16 页课件（旧版 §7.1，含弦、杆、膜、电磁波的完整推导）。\n')
    parts.append('2026-11-03 起的 19 页课件从 §7.2 开始，不再包含这一节，但它是后面所有分离变量问题的物理来源，\n')
    parts.append('所以放在全书开头。读的时候只需抓住一件事：\n')
    parts.append('\\textbf{取微元 $\\rightarrow$ 写受力或守恒 $\\rightarrow$ 小量近似 $\\rightarrow$ 除尺度取极限}，\n')
    parts.append('四个场景（弦、杆、膜、电磁波）用的都是这四步，换的只是「物理定律」那一格。\n\n')

    for num, new, title, submap, skip in OLD_SECTIONS:
        t, body = old[num]
        body = transform(body, submap, skip)
        body = apply_refs(body, OLD_REFS)
        parts.append('\\phantomsection\\label{sec:%s}\n%s{%s}{%s}\n' %
                     (new.replace('.', ''), '\\hdrsub' if new.count('.') >= 2 else '\\hdr',
                      ('\\S' + new) if new.count('.') < 2 else new, title))
        parts.append(body.rstrip() + '\n\n')

    # ---------- §7.2–§7.4（合册）----------
    parts.append('% ------------------------------ §7.2–§7.4 ------------------------------\n')
    for num, new, title, submap, skip in BOOK_SECTIONS:
        t, body = book[num]
        body = transform(body, submap, skip)
        body = apply_refs(body, BOOK_REFS)
        parts.append('\\phantomsection\\label{sec:%s}\n%s{%s}{%s}\n' %
                     (new.replace('.', ''), '\\hdrsub' if new.count('.') >= 2 else '\\hdr',
                      ('\\S' + new) if new.count('.') < 2 else new, title))
        parts.append(body.rstrip() + '\n\n')

    # ---------- §7.5 速查与易错 ----------
    parts.append('% ------------------------------ §7.5 ------------------------------\n')
    parts.append('\\phantomsection\\label{sec:75}\n\\hdr{\\S7.5}{速查与易错}\n\n')
    parts.append('这一节是第七章的查表页：定解条件怎么写、推导里最容易漏哪一步、' +
                 '分离变量前该检查什么。每条都回指正文的某一步，忘了就按编号翻回去。\n\n')

    t, body = book['\\S7']
    body = transform(body, {'7.1': '7.5.1', '7.2': '7.5.3', '7.3': '7.5.4'})
    extra = [('\\S7.1', '\\S7.5.1'), ('\\S7.2', '\\S7.5.3'), ('\\S7.3', '\\S7.5.4'),
             ('\\S4.4', '\\S8.1.8'), ('\\S4.5', '\\S8.1.9'), ('\\S5.1', '\\S8.1.11'),
             ('\\S6.4', '\\S8.1.19'), ('\\S6.5', '\\S8.1.20')]
    body = apply_refs(body, BOOK_REFS + extra)
    parts.append(body.rstrip() + '\n\n')

    # 旧稿 §10 的八条易错，插到 7.5.2（定解条件速查之后）
    t, body = old['§10']
    body = transform(body, {})
    body = apply_refs(body, OLD_REFS)
    marker = '\\subhdr{7.5.3\\quad'
    idx = parts[-1].find(marker)
    if idx > 0:
        parts[-1] = parts[-1][:idx] + '\\subhdr{7.5.2\\quad 波动方程推导的八条易错}\n\n' + body.strip() + '\n\n' + parts[-1][idx:]

    # ---------- §7.6 三句话 ----------
    parts.append('\\phantomsection\\label{sec:76}\n\\hdr{\\S7.6}{三句话总结}\n\n')
    t, body = book['\\S9']
    parts.append(body.strip() + '\n\n')

    text = ''.join(parts)
    emit(os.path.join(OUT, 'ch7.tex'), text)


if __name__ == '__main__':
    build_ch7()

