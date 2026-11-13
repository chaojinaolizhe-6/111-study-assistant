# -*- coding: utf-8 -*-
r"""第八章 p13 四道作业的答案核验（2026-11-13）。

做三件事，任一断言失败即非零退出：
1. 用 sympy 符号算出四题的系数公式，与讲义里写死的公式逐项比较；
2. 把级数截断后与初始条件/边界条件比较，给出实测误差；
3. 逐项核对每个级数项确实满足对应的 PDE。

运行：python -B subjects/05-数学物理方法2/讲义/verify_ch8_hw4-20261113.py
"""
from __future__ import annotations

import sys

import numpy as np
import sympy as sp

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

FAILS: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(("  [OK]  " if ok else "  [FAIL]") + f" {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)


# ----------------------------------------------------------------- 符号部分
l, h, b, A, a, x, y, t = sp.symbols("l h b A a x y t", positive=True)
n = sp.symbols("n", integer=True, positive=True)

print("== 1. 符号核验：四题的系数公式 ==")

# 作业 1：三角初位移，峰在中点，斜率 h（课件 p13 原文）
beta = n * sp.pi / l
I1 = sp.integrate(h * x * sp.sin(beta * x), (x, 0, l / 2))
I2 = sp.integrate(h * (l - x) * sp.sin(beta * x), (x, l / 2, l))
C1 = sp.simplify(2 / l * (I1 + I2))
C1_doc = 4 * h * l * sp.sin(n * sp.pi / 2) / (n**2 * sp.pi**2)
check("作业1 C_n = 4hℓ sin(nπ/2)/(n²π²)", sp.simplify(C1 - C1_doc) == 0, f"sympy: {C1}")

# 作业 2：杆左固定右自由，初速度 ψ=bx/ℓ
k = (2 * n + 1) * sp.pi / (2 * l)
J = sp.integrate(x * sp.sin(k * x), (x, 0, l))
A2_omega = sp.simplify(2 * b / l**2 * J)
A2_omega_doc = 8 * (-1) ** n * b / ((2 * n + 1) ** 2 * sp.pi**2)
check("作业2 A_nω_n = 8(-1)^n b/((2n+1)²π²)",
      sp.simplify(A2_omega - A2_omega_doc) == 0, f"sympy: {A2_omega}")

A2 = sp.simplify(A2_omega_doc * 2 * l / ((2 * n + 1) * sp.pi * a))
A2_doc = 16 * b * l * (-1) ** n / ((2 * n + 1) ** 3 * sp.pi**3 * a)
check("作业2 A_n = 16bℓ(-1)^n/((2n+1)³π³a)", sp.simplify(A2 - A2_doc) == 0, f"sympy: {A2}")

# 作业 3：热传导杆，初温 bx(ℓ-x)/ℓ²
K = sp.integrate(x * (l - x) * sp.sin(beta * x), (x, 0, l))
C3 = sp.simplify(2 / l * b / l**2 * K)
C3_doc = 4 * b * (1 - (-1) ** n) / (n**3 * sp.pi**3)
check("作业3 C_n = 4b(1-(-1)^n)/(n³π³)", sp.simplify(C3 - C3_doc) == 0, f"sympy: {C3}")

# 作业 4：矩形 Laplace，下边 A(1-x/a)、上边 0
kk = n * sp.pi / a
L = sp.integrate((1 - x / a) * sp.sin(kk * x), (x, 0, a))
A4 = sp.simplify(2 / a * A * L)
A4_doc = 2 * A / (n * sp.pi)
check("作业4 A_n = 2A/(nπ)", sp.simplify(A4 - A4_doc) == 0, f"sympy: {A4}")

# 作业 4 的 Y 因子必须满足 Y(b)=0 与 Y''-k²Y=0
Y4 = sp.sinh(kk * (b - y))
check("作业4 Y=sinh(k(b-y)) 满足 Y(b)=0", sp.simplify(Y4.subs(y, b)) == 0)
check("作业4 Y 满足 Y''-k²Y=0", sp.simplify(sp.diff(Y4, y, 2) - kk**2 * Y4) == 0)

print("\n== 2. 逐项 PDE 核验 ==")
u1 = sp.sin(n * sp.pi * x / l) * sp.cos(n * sp.pi * a * t / l)
check("波动项满足 u_tt=a²u_xx", sp.simplify(sp.diff(u1, t, 2) - a**2 * sp.diff(u1, x, 2)) == 0)
u2 = sp.sin((2 * n + 1) * sp.pi * x / (2 * l)) * sp.sin((2 * n + 1) * sp.pi * a * t / (2 * l))
check("半整数模态满足 u_tt=a²u_xx", sp.simplify(sp.diff(u2, t, 2) - a**2 * sp.diff(u2, x, 2)) == 0)
u3 = sp.sin(n * sp.pi * x / l) * sp.exp(-(n * sp.pi * a / l) ** 2 * t)
check("输运项满足 u_t=a²u_xx", sp.simplify(sp.diff(u3, t) - a**2 * sp.diff(u3, x, 2)) == 0)
u4 = sp.sin(kk * x) * sp.sinh(kk * (b - y))
check("Laplace 项满足 u_xx+u_yy=0", sp.simplify(sp.diff(u4, x, 2) + sp.diff(u4, y, 2)) == 0)

print("\n== 3. 级数与初始/边界条件的实测误差 ==")
L0, H0 = 1.0, 1.0
xs = np.linspace(0.0, L0, 401)

# 作业 1：t=0 时 400 项还原三角波
N1 = 400
nn = np.arange(1, N1 + 1)
Cn = 4 * H0 * L0 * np.sin(nn * np.pi / 2) / (nn**2 * np.pi**2)
series1 = (Cn[:, None] * np.sin(np.outer(nn, xs) * np.pi / L0)).sum(axis=0)
tri = np.where(xs < L0 / 2, H0 * xs, H0 * (L0 - xs))
err1 = np.max(np.abs(series1 - tri))
check("作业1 级数还原三角初位移", err1 < 3e-3, f"max|Δ|={err1:.2e}（峰值 {tri.max():.2f}）")
check("作业1 C_n 偶数项为零", np.allclose(Cn[1::2], 0.0), f"C_2={Cn[1]:.1e}")

# 作业 2：u_t(x,0) 用 600 项还原 bx/ℓ（b=1）
B2 = 1.0
N2 = 600
mm = np.arange(0, N2)
beta2 = (2 * mm + 1) * np.pi / (2 * L0)
coef2 = 8 * (-1.0) ** mm * B2 / ((2 * mm + 1) ** 2 * np.pi**2)
series2 = (coef2[:, None] * np.sin(np.outer(beta2, xs))).sum(axis=0)
target2 = B2 * xs / L0
err2 = np.max(np.abs(series2 - target2))
check("作业2 初速度级数还原 bx/ℓ", err2 < 3e-3, f"max|Δ|={err2:.2e}")

# 作业 3：初温用 400 项还原 bx(ℓ-x)/ℓ²（b=1）
N3 = 400
nn3 = np.arange(1, N3 + 1)
Cn3 = 4 * (1 - (-1.0) ** nn3) / (nn3**3 * np.pi**3)
series3 = (Cn3[:, None] * np.sin(np.outer(nn3, xs) * np.pi / L0)).sum(axis=0)
target3 = xs * (L0 - xs) / L0**2
err3 = np.max(np.abs(series3 - target3))
check("作业3 级数还原初温", err3 < 3e-3, f"max|Δ|={err3:.2e}")
check("作业3 只剩奇数项", np.allclose(Cn3[1::2], 0.0))

# 作业 4：y=0 处级数还原 A(1-x/a)，a=1,b=0.6,A=1（端点 x=0 是间断点，只比内部点）
A0, BY = 1.0, 0.6
N4 = 2000
x_in = np.linspace(0.05, 0.95, 200)
nn4 = np.arange(1, N4 + 1)
An4 = 2 * A0 / (nn4 * np.pi)
series4 = (An4[:, None] * np.sin(np.outer(nn4, x_in) * np.pi / A0)).sum(axis=0)
target4 = A0 * (1 - x_in / A0)
err4 = np.max(np.abs(series4 - target4))
check("作业4 y=0 处级数还原 A(1-x/a)（内部点）", err4 < 2e-2, f"max|Δ|={err4:.2e}（端点吉布斯）")

# 作业 4：上边边界与两侧边界（逐项解析核对）
yy = np.linspace(0, BY, 61)
Nq = 80
nq = np.arange(1, Nq + 1)
kq = nq * np.pi / A0
shape = np.sinh(np.outer(kq, BY - yy)) / np.sinh(kq * BY)[:, None]
xq = np.linspace(0, A0, 41)
uq = np.einsum("n,ny,nx->yx", 2.0 * A0 / (nq * np.pi), shape,
               np.sin(np.outer(kq, xq)))
edge_b = float(np.abs(uq[-1, :]).max())
check("作业4 上边 u(x,b)=0", edge_b < 1e-12, f"max|u|={edge_b:.1e}")
check("作业4 两侧 u(0,y)=u(a,y)=0", float(np.abs(uq[:, [0, -1]]).max()) < 1e-12)
mean0 = float(np.mean(uq[0, :]))
check("作业4 下边均值与解析值一致", abs(mean0 - A0 / 2) < 5e-2,
      f"mean u(x,0)={mean0:.4f} vs A/2={A0/2:.4f}")

# 数值表：作业 1 前三个系数（ℓ=h=1）
tab = [(k, 4 * H0 * L0 * np.sin(k * np.pi / 2) / (k**2 * np.pi**2)) for k in (1, 3, 5)]
check("作业1 系数数值表", all(abs(v - (4 * H0 * L0 * np.sin(k * np.pi / 2) / (k**2 * np.pi**2))) < 1e-12
                          for k, v in tab), str([(k, round(v, 4)) for k, v in tab]))

print("\n== 4. 衰减与极限 ==")
check("作业3 系数按 1/n³ 衰减", abs((1 / 11**3) / (1 / 9**3) - (9 / 11) ** 3) < 1e-12)
check("作业2 系数按 1/(2n+1)³ 衰减",
      abs(float(A2_doc.subs({b: 1, l: 1, a: 1, n: 10})) / float(A2_doc.subs({b: 1, l: 1, a: 1, n: 0})) - (1 / 21) ** 3) < 1e-12)
check("作业3 t=10 时首项已衰减到 1e-40 以下", np.exp(-(np.pi) ** 2 * 10.0) < 1e-40)

print()
if FAILS:
    print(f"失败 {len(FAILS)} 项：" + "；".join(FAILS))
    sys.exit(1)
print("全部断言通过。")
