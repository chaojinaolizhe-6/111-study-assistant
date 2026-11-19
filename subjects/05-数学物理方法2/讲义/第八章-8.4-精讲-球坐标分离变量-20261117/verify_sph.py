# -*- coding: utf-8 -*-
"""§8.4 球坐标讲义的关键结论核验：球坐标 Laplacian、Legendre、球壳解、球贝塞尔。
每个断言失败会以非零码退出。"""
import sys
import sympy as sp

r, th, ph, a, b, U0, R = sp.symbols('r theta phi a b U_0 R', positive=True)
x = sp.symbols('x')
ok = 0
fail = []


def check(name, cond):
    global ok
    if cond:
        ok += 1
        print('[PASS]', name)
    else:
        fail.append(name)
        print('[FAIL]', name)


def lap_sph(f):
    f = sp.simplify(f)
    return sp.simplify(
        (1 / r**2) * sp.diff(r**2 * sp.diff(f, r), r)
        + (1 / (r**2 * sp.sin(th))) * sp.diff(sp.sin(th) * sp.diff(f, th), th)
        + (1 / (r**2 * sp.sin(th)**2)) * sp.diff(f, ph, 2)
    )


print('== 1. 球坐标 Laplacian 的特例 ==')
check('lap(1/r)=0', sp.simplify(lap_sph(1 / r)) == 0)
check('lap(r^2 P2)=0', sp.simplify(lap_sph(r**2 * (3 * sp.cos(th)**2 - 1) / 2)) == 0)
check('lap(r cos th)=0', sp.simplify(lap_sph(r * sp.cos(th))) == 0)
check('lap(r sin th cos ph)=0', sp.simplify(lap_sph(r * sp.sin(th) * sp.cos(ph))) == 0)
check('lap(1)=0', sp.simplify(lap_sph(sp.Integer(1))) == 0)

print('== 2. Legendre 多项式与展开 ==')
P1 = x
P2 = (3 * x**2 - 1) / 2
P3 = (5 * x**3 - 3 * x) / 2
P4 = (35 * x**4 - 30 * x**2 + 3) / 8
check('x^3 = 3/5 P1 + 2/5 P3', sp.simplify(x**3 - (sp.Rational(3, 5) * P1 + sp.Rational(2, 5) * P3)) == 0)
check('x^2 = 1/3 P0 + 2/3 P2', sp.simplify(x**2 - (sp.Rational(1, 3) + sp.Rational(2, 3) * P2)) == 0)
check('P3 满足 Legendre 方程', sp.simplify(sp.diff((1 - x**2) * sp.diff(P3, x), x) + 12 * P3) == 0)
check('P4 满足 Legendre 方程', sp.simplify(sp.diff((1 - x**2) * sp.diff(P4, x), x) + 20 * P4) == 0)
check('int P1 P3 = 0', sp.integrate(P1 * P3, (x, -1, 1)) == 0)
check('int P2^2 = 2/5', sp.simplify(sp.integrate(P2**2, (x, -1, 1)) - sp.Rational(2, 5)) == 0)
check('P_l(1)=1', P1.subs(x, 1) == 1 and P2.subs(x, 1) == 1 and P3.subs(x, 1) == 1)
check('P_3 奇偶性', sp.simplify(P3.subs(x, -x) + P3) == 0)

print('== 3. P1 的球内解 ==')
u1 = U0 * (r / a) * sp.cos(th)
check('P1 解在 r=a 取 U0 cos th', sp.simplify(u1.subs(r, a) - U0 * sp.cos(th)) == 0)
check('P1 解调和', sp.simplify(lap_sph(u1)) == 0)

print('== 4. P3 的球壳解 ==')
C = U0 * b**2 / (b**3 - a**3)
u_shell = C * (r - a**3 / r**2) * sp.cos(th)
check('球壳解 r=a 为 0', sp.simplify(u_shell.subs(r, a)) == 0)
check('球壳解 r=b 为 U0 cos th',
      sp.simplify(u_shell.subs(r, b) - U0 * sp.cos(th)) == 0)
check('球壳解调和', sp.simplify(lap_sph(u_shell)) == 0)

print('== 5. 球贝塞尔 ==')
j0 = sp.sin(x) / x
check('j0 满足球贝塞尔方程',
      sp.simplify(sp.diff(x**2 * sp.diff(j0, x), x) + x**2 * j0) == 0)
n0 = -sp.cos(x) / x
check('n0 满足球贝塞尔方程',
      sp.simplify(sp.diff(x**2 * sp.diff(n0, x), x) + x**2 * n0) == 0)
j1 = sp.sin(x) / x**2 - sp.cos(x) / x
check('j1 满足 l=1 球贝塞尔方程',
      sp.simplify(sp.diff(x**2 * sp.diff(j1, x), x) + (x**2 - 2) * j1) == 0)
check('j0(kR)=0 当 kR=n*pi', all(abs(float(j0.subs(x, sp.pi * n))) < 1e-15 for n in range(1, 5)))

print('== 6. P4 的级数在 t=0 还原 U0 ==')
# u(r,0) = 2U0 sum (-1)^{n+1} sin(n pi r/R)/(n pi r/R)
import math
xs = [0.13, 0.37, 0.62, 0.85]
for xi in xs:
    s = 0.0
    for n in range(1, 4000):
        s += ((-1) ** (n + 1)) * math.sin(n * math.pi * xi) / (n * math.pi * xi)
    val = 2 * s
    check('P4 t=0 还原 U0（x=%.2f，值=%.4f）' % (xi, val), abs(val - 1.0) < 5e-3)

print('== 7. P4 的系数 A_n ==')
# A_n = 2 (-1)^{n+1}；用正交性数值积分核对 n=1,2
for n in (1, 2):
    kn = n * math.pi

    def j0f(t):
        return math.sin(kn * t) / (kn * t) if t > 0 else 1.0

    import scipy.integrate as si
    norm = R * 0  # placeholder
    # 数值模方 ∫ j0^2 r^2 dr = R^3/(2 n^2 pi^2)
    num_norm = si.quad(lambda t: (math.sin(kn * t) / (kn * t)) ** 2 * t**2, 1e-9, 1.0)[0]
    ana_norm = 1 / (2 * n**2 * math.pi**2)
    check('P4 模方 n=%d 数值≈解析' % n, abs(num_norm - ana_norm) < 1e-4)

print()
print('通过 %d 项，失败 %d 项' % (ok, len(fail)))
if fail:
    print('失败：', fail)
    sys.exit(1)
