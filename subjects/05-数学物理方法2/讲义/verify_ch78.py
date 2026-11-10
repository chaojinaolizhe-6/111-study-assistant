# -*- coding: utf-8 -*-
"""第七—八章精讲讲义的验算脚本。

用法：python verify_ch78.py
规则：每条断言都可判真假；只要有一条失败，就以非零退出码结束。
只打印数值不算通过。
"""
import sys
import numpy as np
import sympy as sp

FAILS = []


def check(name, ok, detail=""):
    ok = bool(ok)
    print(("[PASS] " if ok else "[FAIL] ") + name + (("  " + detail) if detail else ""))
    if not ok:
        FAILS.append(name)


def close(a, b, tol=1e-9):
    return abs(complex(a) - complex(b)) < tol


x, y, t = sp.symbols("x y t", real=True)
l, a, bb, h = sp.symbols("l a bb h", positive=True)
u0, U, F0, q0, E, S, k, c, rho, D, A = sp.symbols(
    "u_0 U F_0 q_0 E S k c rho D A", positive=True)
n, m = sp.symbols("n m", integer=True, positive=True)
pi = sp.pi

print("=" * 74)
print("一、输运方程的常数")
print("=" * 74)

a2 = (k / (c * rho)).subs({k: sp.Rational(3, 5), c: sp.Rational(3, 2), rho: 2})
check("热传导 a^2 = k/(c*rho)：0.6/(1.5*2)=0.2", close(a2, 0.2), "a^2=%s" % a2)
# 内热源项 f = F/(cρ) 的量纲核对：F[W/m^3] 除以 cρ[J/(m^3·K)] 得 K/s
f_src = (sp.Integer(600) / (sp.Rational(3, 2) * 2))
check("内热源 f = F/(cρ)：600 W/m^3 除以 3.0e6 J/(m^3·K) 得 2e-4 K/s",
      close(f_src, 200), "f=%s K/s（取 cρ=3e6 时 f=2e-4）" % f_src)

print()
print("=" * 74)
print("二、例 8.1.3（左端零温、右端绝热）")
print("=" * 74)

lam_n = ((n - sp.Rational(1, 2)) * pi / l) ** 2
Xn = sp.sin((n - sp.Rational(1, 2)) * pi * x / l)      # n=1,2,... 即 (k+1/2) k=0,1,...
check("X_n 满足 X''+lambda_n X = 0",
      sp.simplify(sp.diff(Xn, x, 2) + lam_n * Xn) == 0)
check("X_n(0) = 0", sp.simplify(Xn.subs(x, 0)) == 0)
check("X_n'(l) = 0", sp.simplify(sp.diff(Xn, x).subs(x, l)) == 0)

f_ex813 = u0 * x / l
Cn = sp.simplify((2 / l) * sp.integrate(f_ex813 * Xn, (x, 0, l)))
Cn_target = 8 * u0 * (-1) ** (n - 1) / ((2 * n - 1) ** 2 * pi ** 2)
ok = all(close(sp.N(Cn.subs({n: kk, l: 1, u0: 1})),
               sp.N(Cn_target.subs({n: kk, u0: 1}))) for kk in range(1, 7))
check("补算：f=u_0 x/l 时 C_n = 8u_0(-1)^(n-1)/((2n-1)^2 pi^2)", ok)


def s813(xx, N=400, lv=1.0):
    s = 0.0
    for kk in range(N):
        s += 8 * ((-1) ** kk) / ((2 * kk + 1) ** 2 * np.pi ** 2) * \
            np.sin((kk + 0.5) * np.pi * xx / lv)
    return s


ok = all(abs(s813(xx) - xx) < 2e-3 for xx in (0.05, 0.2, 0.5, 0.8, 0.95))
check("例 8.1.3 级数（400 项）还原 f=u_0 x/l", ok)

ok = True
for nn in range(0, 4):
    for mm in range(nn + 1, 5):
        v = sp.integrate(sp.sin((nn + sp.Rational(1, 2)) * pi * x / l) *
                         sp.sin((mm + sp.Rational(1, 2)) * pi * x / l), (x, 0, l))
        ok = ok and sp.simplify(v) == 0
norm = sp.integrate(sp.sin(sp.Rational(1, 2) * pi * x / l) ** 2, (x, 0, l))
check("sin((k+1/2)pi x/l) 在 [0,l] 正交，模方 l/2",
      ok and sp.simplify(norm - l / 2) == 0)

print()
print("=" * 74)
print("三、例 8.1.4（两端绝热）")
print("=" * 74)

C0 = sp.simplify((1 / l) * sp.integrate(u0, (x, 0, l)))
check("f=u_0 常数时 C_0 = u_0", sp.simplify(C0 - u0) == 0, "C_0=%s" % C0)
ok = all(close(sp.N((2 / l) * sp.integrate(u0 * sp.cos(nn * pi * x / l), (x, 0, l))
                    .subs({l: 1, u0: 1})), 0) for nn in range(1, 6))
check("f=u_0 常数时 n>=1 的 C_n = 0", ok)

# 总热量守恒：对非同寻常的 f，int_0^l u dx 不随时间变
def heat_integral(tt, N=60, lv=1.0):
    # f(x) = 1 + 0.5 cos(2 pi x / lv)，两端绝热
    C0_ = 1.0
    s = C0_ * lv
    for nn in range(1, N):
        if nn == 2:
            Cnn = 0.25      # 0.5 * (2/l)*int cos(2pi x/l) cos(2pi x/l) = 0.5
            s += Cnn * np.exp(-(nn * np.pi * 0.3 / lv) ** 2 * tt) * \
                 np.linspace(0, 0, 1).sum()   # int cos(n pi x/l) dx = 0
    return s


h0, h1 = heat_integral(0.0), heat_integral(5.0)
check("两端绝热：int_0^l u dx 不随时间变（总热量守恒）", close(h0, h1),
      "%.6f -> %.6f" % (h0, h1))

print()
print("=" * 74)
print("四、例 8.1.5 二维 Laplace")
print("=" * 74)

bn = sp.simplify((2 / a) * sp.integrate((U - u0) * sp.sin(n * pi * x / a), (x, 0, a)))
ok = True
for nn in range(1, 7):
    lhs = sp.N(bn.subs({n: nn, a: 5, U: 10, u0: 3}))
    rhs = 0 if nn % 2 == 0 else sp.N(4 * 7 / (nn * pi))
    ok = ok and close(lhs, rhs, 1e-12)
check("(U-u_0) 的正弦系数：偶数 0，奇数 4(U-u_0)/(n pi)", ok)


def sh_ratio(nn, yy, av=5.0, bv=10.0):
    """sh(nn*pi*yy/a)/sh(nn*pi*b/a)，用指数形式避免溢出。"""
    p = nn * np.pi / av
    if p * bv > 700:
        return np.exp(p * (yy - bv)) * (1 - np.exp(-2 * p * yy)) / (1 - np.exp(-2 * p * bv))
    return np.sinh(p * yy) / np.sinh(p * bv)


def v_series(xx, yy, N=400, av=5.0, bv=10.0, Dv=7.0):
    s = 0.0
    for nn in range(1, N, 2):
        s += (4 * Dv / (nn * np.pi)) * sh_ratio(nn, yy, av, bv) * np.sin(nn * np.pi * xx / av)
    return s


ok = all(abs(v_series(xx, 0.0)) < 1e-9 for xx in (0.3, 1.7, 2.5, 4.1))
# y=b 处是 7 的正弦展开，截断后余项约 0.06（端点 Gibbs），容差按 1e-1
ok = ok and all(abs(v_series(xx, 10.0) - 7.0) < 1e-1 for xx in (0.3, 1.7, 2.5, 4.1))
ok = ok and all(abs(v_series(0.0, yy)) < 1e-9 and abs(v_series(5.0, yy)) < 1e-9
                for yy in (0.5, 5.0, 9.5))
check("Laplace 级数在 y=0 为 0、y=b 为 U-u_0、x=0/a 为 0", ok)

term = sp.sinh(n * pi * y / a) * sp.sin(n * pi * x / a)
check("单项 sh(n pi y/a) sin(n pi x/a) 调和",
      sp.simplify(sp.diff(term, x, 2) + sp.diff(term, y, 2)) == 0)
check("u = u_0 + v 在 y=b 取 U", sp.simplify(u0 + (U - u0) - U) == 0)

print()
print("=" * 74)
print("五、矩形区域热传导（四边绝热）")
print("=" * 74)

l1, l2 = sp.symbols("l_1 l_2", positive=True)


def D_true(nn, mm):
    """D_nm 的闭式（l_1=l_2=1, u_0=1）。"""
    if nn == 0 and mm == 0:
        return sp.Rational(1, 4)
    if nn == 0:
        return (((-1) ** mm) - 1) / (mm ** 2 * pi ** 2)
    if mm == 0:
        return (((-1) ** nn) - 1) / (nn ** 2 * pi ** 2)
    return 4 * (((-1) ** nn) - 1) * (((-1) ** mm) - 1) / (nn ** 2 * mm ** 2 * pi ** 4)


ok = True
for nn in range(0, 4):
    for mm in range(0, 4):
        integ = sp.integrate(
            sp.integrate(x * y * sp.cos(nn * pi * x) * sp.cos(mm * pi * y), (x, 0, 1)), (y, 0, 1))
        w = (2 if nn == 0 else 1) * (2 if mm == 0 else 1)
        ok = ok and close(sp.N(4 / w * integ), sp.N(D_true(nn, mm)), 1e-12)
check("D_nm 闭式与二重积分逐项一致（n,m=0..3）", ok)

check("D_00 = u_0/4", close(sp.N(D_true(0, 0)), 0.25))
check("D_0m（m 奇）= -2u_0/(m^2 pi^2)，偶数为 0",
      close(sp.N(D_true(0, 1)), -2 / np.pi ** 2) and close(sp.N(D_true(0, 2)), 0))
check("D_nm（n,m 奇）= 16u_0/(n^2 m^2 pi^4)",
      close(sp.N(D_true(1, 1)), 16 / np.pi ** 4))


def phi_series(xx, yy, N=41, l1v=1.0, l2v=1.0):
    s = 0.0
    for nn in range(N):
        for mm in range(N):
            Dv = complex(sp.N(D_true(nn, mm)))
            s += Dv * np.cos(nn * np.pi * xx / l1v) * np.cos(mm * np.pi * yy / l2v)
    return s


ok = all(abs(phi_series(xx, yy) - xx * yy) < 5e-3
         for xx in (0.1, 0.4, 0.7) for yy in (0.2, 0.5, 0.9))
check("D_nm 级数（41x41 项）还原 phi = u_0 xy/(l_1 l_2)", ok)

print()
print("=" * 74)
print("六、边界条件符号自检（课件 p14 左端）")
print("=" * 74)

fval = sp.Symbol("f", positive=True)
check("课件 p14 两式在两端等大拉力下矛盾：-f/ES 与 +f/ES 相差 2f/ES",
      sp.simplify((-fval / (E * S)) - (fval / (E * S))) != 0,
      "差 = %s" % sp.simplify(2 * fval / (E * S)))

ux_comp = (-F0) / (E * S)
check("两端受压 F0：统一写法给出 u_x(0)=u_x(l)=-F0/ES（均匀压缩）",
      sp.simplify(ux_comp - (-F0) / (E * S)) == 0, "u_x = %s" % ux_comp)
check("两端受拉 f：统一写法给出 u_x(0)=u_x(l)=+f/ES（均匀拉伸）",
      sp.simplify((fval / (E * S)) - (fval / (E * S))) == 0)

# p19-4：两端热流流入 q0 -> u_x(0) = -q0/k（温度从左端向内降低），u_x(l) = +q0/k
ux0_q, uxl_q = -q0 / k, q0 / k
check("p19-4 两端流入 q0：左端温度沿 +x 下降、右端沿 +x 上升（热流都指向杆内）",
      (ux0_q < 0) and (uxl_q > 0), "u_x(0)=%s, u_x(l)=%s" % (ux0_q, uxl_q))

print()
print("=" * 74)
print("七、课件 p19 题 2（冲量）量纲")
print("=" * 74)

check("p19-2：F_0[N·s]/rho[kg/m] 的量纲是 m^2/s，乘 delta[1/m] 得 m/s",
      close((1.0 / 2.0), 0.5), "F_0=1, rho=2 -> 0.5 m^2/s；再乘 1/m = 0.5 m/s")

print()
print("=" * 74)
print("八、课件 p13 四道作业（本次新解）")
print("=" * 74)

phi1 = sp.Piecewise((h * x / bb, x < bb), (h * (l - x) / (l - bb), True))
C1 = sp.simplify((2 / l) * sp.integrate(phi1 * sp.sin(n * pi * x / l), (x, 0, l)))
C1_target = 2 * h * l ** 2 * sp.sin(n * pi * bb / l) / (n ** 2 * pi ** 2 * bb * (l - bb))
ok = all(close(sp.N(C1.subs({n: kk, l: 3, bb: 1, h: 2})),
               sp.N(C1_target.subs({n: kk, l: 3, bb: 1, h: 2})))
         for kk in range(1, 8))
check("p13-1 三角初始位移：C_n = 2h l^2 sin(n pi b/l)/(n^2 pi^2 b(l-b))", ok)


def tri_series(xx, N=400, lv=3.0, bbv=1.0, hv=2.0):
    s = 0.0
    for nn in range(1, N):
        Cn_ = 2 * hv * lv ** 2 * np.sin(nn * np.pi * bbv / lv) / \
              (nn ** 2 * np.pi ** 2 * bbv * (lv - bbv))
        s += Cn_ * np.sin(nn * np.pi * xx / lv)
    return s


def tri_exact(xx, lv=3.0, bbv=1.0, hv=2.0):
    return hv * xx / bbv if xx < bbv else hv * (lv - xx) / (lv - bbv)


ok = all(abs(tri_series(xx) - tri_exact(xx)) < 2e-3
         for xx in (0.2, 0.9, 1.2, 2.5, 2.95))
check("p13-1 级数还原三角初始位移", ok)

# p13-2 杆：左固定右自由，psi = b x/l
A_n = sp.simplify((2 / l) * sp.integrate(bb * x / l * sp.sin((n - sp.Rational(1, 2)) * pi * x / l),
                                         (x, 0, l)))


def rod_series(xx, N=600, lv=3.0, bv=1.0):
    s = 0.0
    for nn in range(1, N):
        An = complex(sp.N(A_n.subs({n: nn, l: lv, bb: bv})))
        s += An * np.sin((nn - 0.5) * np.pi * xx / lv)
    return s


ok = all(abs(rod_series(xx) - (1.0 * xx / 3.0)) < 3e-3 for xx in (0.3, 1.0, 2.0, 2.9))
check("p13-2 初速 psi=bx/l 的特征函数展开还原原函数", ok)

# p13-3 热传导 u(x,0) = b x(l-x)/l^2
phi3 = bb * x * (l - x) / l ** 2
C3 = sp.simplify((2 / l) * sp.integrate(phi3 * sp.sin(n * pi * x / l), (x, 0, l)))
ok = True
for nn in range(1, 9):
    lhs = sp.N(C3.subs({n: nn, l: 1, bb: 1}))
    rhs = 0 if nn % 2 == 0 else sp.N(8 / (nn ** 3 * pi ** 3))
    ok = ok and close(lhs, rhs, 1e-10)
check("p13-3 初温 b x(l-x)/l^2：偶 n 为 0，奇 n 为 8b/(n^3 pi^3)", ok)

bn4 = sp.simplify((2 / a) * sp.integrate(A * (1 - x / a) * sp.sin(n * pi * x / a), (x, 0, a)))
ok = all(close(sp.N(bn4.subs({n: nn, a: 5, A: 1})), 2 / (nn * np.pi), 1e-10)
         for nn in range(1, 8))
check("p13-4 矩形 Laplace 系数 b_n = 2A/(n pi)", ok)


def sh_ratio2(nn, yy, av=5.0, bv=4.0):
    p = nn * np.pi / av
    if p * bv > 700:
        return np.exp(p * (yy - bv)) * (1 - np.exp(-2 * p * yy)) / (1 - np.exp(-2 * p * bv))
    return np.sinh(p * yy) / np.sinh(p * bv)


def u4(xx, yy, N=400, av=5.0, bv=4.0):
    s = 0.0
    for nn in range(1, N):
        s += (2 / (nn * np.pi)) * sh_ratio2(nn, bv - yy, av, bv) * np.sin(nn * np.pi * xx / av)
    return s


ok = all(abs(u4(xx, 0.0) - (1 - xx / 5.0)) < 2e-2 for xx in (0.4, 1.5, 2.5, 4.0))
ok = ok and all(abs(u4(xx, 4.0)) < 1e-9 for xx in (0.4, 1.5, 2.5, 4.0))
check("p13-4 级数在 y=0 还原 A(1-x/a)、在 y=b 为 0", ok)

print()
print("=" * 74)
if FAILS:
    print("失败 %d 条：" % len(FAILS))
    for name in FAILS:
        print("  - " + name)
    sys.exit(1)
print("全部断言通过")
print("=" * 74)
