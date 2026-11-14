# -*- coding: utf-8 -*-
r"""验算：X'' + λX = 0 在四类边界条件下的特征值与特征函数。

只用 sympy 的精确运算（整数 n、正参数 l、μ）核对讲义正文与附录里的每个式子：
  1) 每类情形 λ>0 的特征函数确实满足方程与边界条件；
  2) 判据式（sin μl = 0 / cos μl = 0）的根与给出的 λ_n 一致；
  3) λ<0、λ=0 时系数矩阵行列式是否为零，与"只有零解 / 有非零解"的结论一致；
  4) 正交性 ∫X_m X_n = 0 (m≠n)；归一化值 ∫X_n² 与正文一致；
  5) 能量恒等式 λ = ∫(X')²/∫X² 与 Rayleigh 商数值一致；
  6) 内点零点个数与正文表格一致（第一条 n-1 个，其余 n 个）。

任一断言失败以非零退出码报告。仅打印数值不算通过。
"""
from __future__ import annotations

import sys

import sympy as sp

x, l, mu = sp.symbols("x l mu", real=True, positive=True)
checks = 0


def ok(name: str, cond: bool) -> None:
    global checks
    if not cond:
        print(f"[FAIL] {name}")
        sys.exit(1)
    checks += 1
    print(f"[ok] {name}")


def zero(expr) -> bool:
    """精确判零。"""
    return sp.simplify(sp.expand(expr)) == 0


L0 = 1  # 数值核对用的具体长度

# ---------------------------------------------------------------- 1. λ>0 解与边界条件
print("\n== 1. λ>0 的特征函数满足方程与边界条件 ==")
families = {
    "case1": [(sp.sin(n * sp.pi * x / l), (n * sp.pi / l) ** 2, n) for n in range(1, 5)],
    "case2": [(sp.sin((n + sp.Rational(1, 2)) * sp.pi * x / l),
               ((n + sp.Rational(1, 2)) * sp.pi / l) ** 2, n) for n in range(0, 4)],
    "case3": [(sp.cos((n + sp.Rational(1, 2)) * sp.pi * x / l),
               ((n + sp.Rational(1, 2)) * sp.pi / l) ** 2, n) for n in range(0, 4)],
    "case4": [(sp.cos(n * sp.pi * x / l), (n * sp.pi / l) ** 2, n) for n in range(0, 4)],
}
bc = {
    "case1": ("value", "value"),
    "case2": ("value", "deriv"),
    "case3": ("deriv", "value"),
    "case4": ("deriv", "deriv"),
}

for label, items in families.items():
    k0, kl = bc[label]
    for X, lam, n in items:
        ok(f"{label} n={n}: X''+λX=0", zero(sp.diff(X, x, 2) + lam * X))
        for at, kind in ((0, k0), (l, kl)):
            f = X if kind == "value" else sp.diff(X, x)
            ok(f"{label} n={n}: 在 x={'0' if at == 0 else 'l'} 处 {kind}=0",
               zero(f.subs(x, at)))

# ---------------------------------------------------------------- 2. 判据式的根
print("\n== 2. 判据式的根就是给出的 μ_n ==")
for k in range(1, 6):
    ok(f"sin(μl)=0 在 μ={k}π/l 成立", zero(sp.sin(k * sp.pi / l * l)))
for k in range(0, 5):
    ok(f"cos(μl)=0 在 μ=(k+1/2)π/l 成立",
       zero(sp.cos((k + sp.Rational(1, 2)) * sp.pi / l * l)))
import numpy as np

def root_positions(func, hi, step=1e-3):
    """在 (0, hi) 上按符号变化定位正根（简单零点）。"""
    grid = np.arange(step, hi, step)
    vals = func(grid)
    pos = []
    for i in range(len(grid) - 1):
        if vals[i] * vals[i + 1] < 0:
            a, b, fa = grid[i], grid[i + 1], vals[i]
            pos.append(a - fa * (b - a) / (vals[i + 1] - fa))  # 线性插值
    return pos

spos = root_positions(np.sin, 5.5 * np.pi)
ok("sin 在 (0, 5.5π) 内恰有 5 个正根，且逐个等于 kπ（k=1..5）",
   len(spos) == 5 and all(abs(p - k * np.pi) < 1e-6 for k, p in zip(range(1, 6), spos)))
cpos = root_positions(np.cos, 5.5 * np.pi)
ok("cos 在 (0, 5.5π) 内恰有 5 个正根，且逐个等于 (k+1/2)π（k=0..4）",
   len(cpos) == 5 and all(abs(p - (k + 0.5) * np.pi) < 1e-6
                          for k, p in zip(range(0, 5), cpos)))

# ---------------------------------------------------------------- 3. λ<0 与 λ=0 的行列式
print("\n== 3. 三种 λ 下系数矩阵的行列式（奇异 ⇔ 存在非零解） ==")
boundary = {
    "case1": ((0, "value"), (l, "value")),
    "case2": ((0, "value"), (l, "deriv")),
    "case3": ((0, "deriv"), (l, "value")),
    "case4": ((0, "deriv"), (l, "deriv")),
}
# (情形, λ 类型) -> (行列式, 是否应奇异, 奇异时的 μ0 = μ·l)
table = {
    ("case1", "neg"): (sp.sinh(mu * l), False, None),
    ("case1", "zero"): (l, False, None),
    ("case1", "pos"): (sp.sin(mu * l), True, sp.pi),
    ("case2", "neg"): (mu * sp.cosh(mu * l), False, None),
    ("case2", "zero"): (sp.Integer(1), False, None),
    ("case2", "pos"): (mu * sp.cos(mu * l), True, sp.pi / 2),
    ("case3", "neg"): (-mu * sp.cosh(mu * l), False, None),
    ("case3", "zero"): (sp.Integer(-1), False, None),
    ("case3", "pos"): (-mu * sp.cos(mu * l), True, sp.pi / 2),
    ("case4", "neg"): (-mu ** 2 * sp.sinh(mu * l), False, None),
    ("case4", "zero"): (sp.Integer(0), True, None),
    ("case4", "pos"): (mu ** 2 * sp.sin(mu * l), True, sp.pi),
}


def basis(kind):
    if kind == "neg":
        return sp.cosh(mu * x), sp.sinh(mu * x)
    if kind == "zero":
        return sp.Integer(1), x
    return sp.cos(mu * x), sp.sin(mu * x)


for case, bset in boundary.items():
    for kind in ("neg", "zero", "pos"):
        expected, singular, mu0 = table[(case, kind)]
        b1, b2 = basis(kind)
        M = sp.zeros(2, 2)
        for i, (at, knd) in enumerate(bset):
            for j, f in enumerate((b1, b2)):
                g = f if knd == "value" else sp.diff(f, x)
                M[i, j] = sp.simplify(g.subs(x, at))
        det = sp.simplify(M.det())
        ok(f"{case} λ{kind}: 行列式与正文一致（{sp.sstr(expected)}）", zero(det - expected))
        if not singular:
            for m0, l0 in ((0.5, 1.0), (3.0, 2.0)):
                ok(f"{case} λ{kind}: 行列式在 μ={m0}, l={l0} 不为零",
                   abs(complex(det.subs({mu: m0, l: l0}))) > 1e-10)
        elif mu0 is None:
            ok(f"{case} λ=0: 矩阵奇异且核为 1 维（常数解）", M.rank() == 1)
        else:
            ok(f"{case} λ>0: μl={sp.sstr(mu0)} 时矩阵秩为 1",
               M.subs(mu, mu0 / l).rank() == 1)
            # 与 μl 相邻的点上矩阵非奇异：确认这不是恒等式
            Mnum = M.subs(l, sp.Integer(1)).subs(mu, float(mu0) + 0.3)
            ok(f"{case} λ>0: μl={sp.sstr(mu0)} 附近行列式非零",
               abs(complex(sp.N(Mnum.det()))) > 1e-8)

# ---------------------------------------------------------------- 4. 正交性与归一化
print("\n== 4. 正交性与 ∫X_n² dx ==")
for m, n in ((1, 2), (2, 3), (1, 3), (2, 2), (1, 1)):
    val = sp.integrate(sp.sin(m * sp.pi * x / l) * sp.sin(n * sp.pi * x / l), (x, 0, l))
    ok(f"case1 ∫sin{m}·sin{n} = {'l/2' if m == n else '0'}",
       zero(val - (l / 2 if m == n else 0)))
f2 = lambda k: sp.sin((k + sp.Rational(1, 2)) * sp.pi * x / l)
for m, n in ((0, 1), (1, 2), (0, 3), (2, 3)):
    ok(f"case2 ∫sin({m}+1/2)·sin({n}+1/2) = {'l/2' if m == n else '0'}",
       zero(sp.integrate(f2(m) * f2(n), (x, 0, l)) - (l / 2 if m == n else 0)))
g3 = lambda k: sp.cos((k + sp.Rational(1, 2)) * sp.pi * x / l)
for m, n in ((0, 1), (1, 2), (0, 2)):
    ok(f"case3 ∫cos({m}+1/2)·cos({n}+1/2) = {'l/2' if m == n else '0'}",
       zero(sp.integrate(g3(m) * g3(n), (x, 0, l)) - (l / 2 if m == n else 0)))
h4 = lambda k: sp.cos(k * sp.pi * x / l)
for m, n in ((0, 0), (1, 1), (1, 2), (2, 3), (0, 1), (0, 2)):
    want = l if (m == n == 0) else (0 if m != n else l / 2)
    ok(f"case4 ∫cos{m}·cos{n} = {want}",
       zero(sp.integrate(h4(m) * h4(n), (x, 0, l)) - want))

# ---------------------------------------------------------------- 5. Rayleigh 商
print("\n== 5. 能量恒等式 λ = ∫(X')²/∫X² ==")
ray = [(sp.sin(n * sp.pi * x / l), (n * sp.pi / l) ** 2, 1, n) for n in range(1, 5)] + \
      [(sp.cos(n * sp.pi * x / l), (n * sp.pi / l) ** 2, 4, n) for n in range(0, 4)] + \
      [(f2(n), ((n + sp.Rational(1, 2)) * sp.pi / l) ** 2, 2, n) for n in range(0, 3)] + \
      [(g3(n), ((n + sp.Rational(1, 2)) * sp.pi / l) ** 2, 3, n) for n in range(0, 3)]
for X, lam, case, n in ray:
    num = sp.integrate(sp.diff(X, x) ** 2, (x, 0, l))
    den = sp.integrate(X ** 2, (x, 0, l))
    ok(f"case{case} n={n}: ∫(X')² = λ·∫X²", zero(num - lam * den))

# ---------------------------------------------------------------- 6. 零点个数
print("\n== 6. 内点零点个数 ==")
import numpy as np


def interior_zeros(func, expect):
    f = sp.lambdify(x, func.subs(l, L0), "numpy")
    grid = np.linspace(0, L0, 4001)
    vals = np.asarray(f(grid), dtype=float)
    if vals.ndim == 0:  # 常函数（case4 的 n=0）
        vals = np.full_like(grid, float(vals))
    zeros = []
    for i in range(len(grid) - 1):
        if vals[i] == 0 and 0 < grid[i] < L0:
            zeros.append(grid[i])
        if vals[i] * vals[i + 1] < 0:
            zeros.append(0.5 * (grid[i] + grid[i + 1]))
    dedup = []
    for z in zeros:
        if not dedup or abs(z - dedup[-1]) > 1e-3:
            dedup.append(z)
    return len(dedup) == expect


for n in range(1, 5):
    ok(f"case1 n={n}: 内点零点 n-1={n-1} 个",
       interior_zeros(sp.sin(n * sp.pi * x), n - 1))
for n in range(0, 4):
    ok(f"case2 n={n}: 内点零点 n={n} 个", interior_zeros(f2(n), n))
    ok(f"case3 n={n}: 内点零点 n={n} 个", interior_zeros(g3(n), n))
    ok(f"case4 n={n}: 内点零点 n={n} 个", interior_zeros(h4(n), n))

# ---------------------------------------------------------------- 7. 附录练习
print("\n== 7. 附录练习的数值 ==")
for k, want in enumerate((2.467, 22.207, 61.685)):
    v = float(((k + sp.Rational(1, 2)) ** 2 * sp.pi ** 2).evalf(12))
    ok(f"练习 P1: λ_{k} ≈ {v:.6f}（正文写 {want}）", abs(v - want) < 5e-4)
ok("练习 P1: X_1=cos(3πx/2) 的零点是 x=1/3",
   zero(sp.cos(3 * sp.pi * sp.Rational(1, 3) / 2)))
ok("练习 P2: λ<0 的行列式 μ·cosh(μl) 非零",
   abs(complex((mu * sp.cosh(mu * l)).subs({mu: 1.3, l: 2.0}))) > 1e-10)
ok("练习 P3: l=π 时 λ_n=n²",
   all(zero((n * sp.pi / sp.pi) ** 2 - n ** 2) for n in (1, 2, 3)))
c = sp.sqrt(2 / sp.pi)
ok("练习 P3: c_n=√(2/π) 使 ∫_0^π (c·sin nx)²=1",
   all(zero(sp.integrate((c * sp.sin(n * x)) ** 2, (x, 0, sp.pi)) - 1) for n in (1, 2, 3)))

print(f"\n全部通过：{checks} 条断言。")
print("核对范围：四类情形的方程/边界条件、判据式根、λ<0 与 λ=0 的行列式、正交性与归一化、"
      "Rayleigh 商、内点零点个数、附录练习数值。未核对：完备性（本讲义按引用处理，不作证明）、页面排版。")
sys.exit(0)
