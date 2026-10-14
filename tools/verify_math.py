#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""留数/积分 自动复核工具（导师用，防手算错）

用途：凡是要报给学习者的数值、留数、积分值，一律先用本工具复核。
背景：2026-10-08 会话中导师在同一类复数代数上连续手算出错四五次，
      学习者要求「配点东西增强做题能力」。结论：工具已够，缺的是硬性流程。

用法（从工作区根目录跑）：

  # 1) 留数：给出函数、变量、极点（可用 I 表示虚数单位）
  python -B tools/verify_math.py residue "1/((z**2+1)**2*(z-1))" z "1" "I" "-I"

  # 2) 定积分
  python -B tools/verify_math.py integral "x**2/((x**2+1)*(x**2+4))" x "-oo" "oo"

  # 3) 围道积分（把留数×2πi 一并算出来）
  python -B tools/verify_math.py contour "cos(z)/z**3" z "0"

  # 4) 数值抽查（被积函数无法符号积分时）
  python -B tools/verify_math.py numeric "x**2/(x**4+16)" x 0 50

注意：变量名里不要用 epsilon 之类带下划线以外的特殊字符；
     虚数单位写 I，无穷写 oo。
"""
import sys

try:
    import sympy as sp
except ImportError:
    sys.exit("需要 sympy：请用 GPU 环境（. $env:DSH_HOME\\.desktop-bin\\use-gpu.ps1）或 pip install sympy")


def build(expr_str, var_name):
    var = sp.Symbol(var_name)
    return sp.sympify(expr_str, locals={var_name: var}), var


def cmd_residue(args):
    expr, var = build(args[0], args[1])
    total = 0
    print("f(%s) = %s" % (var, expr))
    for s in args[2:]:
        z0 = sp.sympify(s, locals={str(var): var})
        r = sp.residue(expr, var, z0)
        total += r
        print("  Res f(%s) = %s" % (z0, sp.simplify(r)))
    print("  Σ Res      = %s" % sp.simplify(total))
    print("  2πi·Σ Res  = %s" % sp.simplify(2 * sp.pi * sp.I * total))
    print("  数值       = %s" % sp.N(2 * sp.pi * sp.I * total))


def cmd_integral(args):
    expr, var = build(args[0], args[1])
    lo = sp.sympify(args[2], locals={str(var): var})
    hi = sp.sympify(args[3], locals={str(var): var})
    val = sp.integrate(expr, (var, lo, hi))
    print("∫ %s d%s  from %s to %s" % (expr, var, lo, hi))
    print("  = %s" % sp.simplify(val))
    print("  ≈ %s" % sp.N(val))


def cmd_contour(args):
    """围道积分 = 2πi × (所选留数之和)；极点由调用者确认都在围道内。"""
    cmd_residue(args)


def cmd_numeric(args):
    expr, var = build(args[0], args[1])
    lo = float(args[2])
    hi = float(args[3])
    val = sp.N(sp.integrate(expr, (var, lo, hi)))
    print("数值积分 %s d%s 从 %s 到 %s" % (expr, var, lo, hi))
    print("  = %s" % val)


CMDS = {
    "residue": cmd_residue,
    "contour": cmd_contour,
    "integral": cmd_integral,
    "numeric": cmd_numeric,
}


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in CMDS:
        print(__doc__)
        sys.exit(1)
    CMDS[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    main()
