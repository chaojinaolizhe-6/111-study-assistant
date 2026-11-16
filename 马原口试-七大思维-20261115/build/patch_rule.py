# -*- coding: utf-8 -*-
"""替换 make_deck.py 中法治思维页的图形面板（天平 -> 规则/竞争对峙）。"""
import io, re

P = r"D:\aaa_D_usual\DSH\111学习助手\马原口试-七大思维-20261115\build\make_deck.py"
src = io.open(P, encoding="utf-8").read()

start = src.index("    elif idx == 5:")
end = src.index("    else:\n        T(\"rlab\"", start)

new = '''    elif idx == 5:
        R("ra", CXI, 138, 118, 74, CARD, BORDER, shape="roundRect")
        T("rat", CXI, 160, 118, 24, "规则", 14, INK, bold=True, align="center")
        R("rb", CXI + CWD - 118, 138, 118, 74, CARD, BORDER, shape="roundRect")
        T("rbt", CXI + CWD - 118, 160, 118, 24, "竞争", 14, INK, bold=True, align="center")
        T("two", CXI + 118, 158, CWD - 236, 30, "⇄", 20, RED2, bold=True, align="center")
        T("capx", CXI, 228, CWD, 44, "法律把经济关系固定下来，\\n竞争因此有了可预期的边界。", 10, SUB, align="center", lh=1.5)
        R("pill5", CXI + 34, 292, CWD - 68, 40, RED, shape="roundRect")
        T("pill5t", CXI + 34, 302, CWD - 68, 22, "规则就是竞争力", 11, "FFFDF7", bold=True, align="center")
        T("cap", CXI, 352, CWD, 40, "应诉、举证、谈判、反制：功夫全在规则里。", 9.5, SUB, align="center", lh=1.5)

'''
src = src[:start] + new + src[end:]
io.open(P, "w", encoding="utf-8").write(src)
print("patched", len(new))
