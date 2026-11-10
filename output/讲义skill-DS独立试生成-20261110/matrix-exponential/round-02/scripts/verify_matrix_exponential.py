#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""可复现的数学核验：matrix-exponential/round-01/handout.tex 的公式、例题与作业。

每一行断言对应讲义中的一处结论；任一断言失败即非零退出。
独立基准优先用 SymPy 的 Matrix.exp()（不依赖讲义推导），
再与讲义写出的闭式逐元素比较。

运行：python -B scripts/verify_matrix_exponential.py
"""
from __future__ import annotations

import sys

import sympy as sp
from sympy import I, Matrix, Rational as R, cos, diag, exp, eye, simplify, sin, zeros

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

x, t, s, lam = sp.symbols("x t s lambda", real=True)
c1, c2, c3 = sp.symbols("c1 c2 c3")
C2 = Matrix([c1, c2])
C3 = Matrix([c1, c2, c3])

checks = 0
failures: list[str] = []


def ok(name: str, condition) -> None:
    global checks
    checks += 1
    try:
        passed = bool(condition)
    except Exception as exc:  # pragma: no cover - 仅在表达式异常时触发
        passed = False
        name = f"{name}（求值异常：{exc}）"
    if passed:
        print(f"[PASS] {name}")
    else:
        failures.append(name)
        print(f"[FAIL] {name}")


def eq(name: str, lhs, rhs) -> None:
    """矩阵或标量等式：simplify(lhs-rhs)==0。"""
    if isinstance(lhs, sp.MatrixBase) and rhs == 0:
        rhs = zeros(*lhs.shape)
    elif isinstance(rhs, sp.MatrixBase) and lhs == 0:
        lhs = zeros(*rhs.shape)
    diff = simplify(lhs - rhs)
    if isinstance(diff, sp.MatrixBase):
        ok(name, diff == zeros(*diff.shape))
    else:
        ok(name, diff == 0)


def eq0(name: str, expr) -> None:
    eq(name, expr, 0)


# =====================================================================
print("== A. 定义与性质（p4--p7） ==")
# A0: 幂零矩阵的级数截断
N = Matrix([[0, 1], [0, 0]])
eq("幂零 N^2=0 与 e^{Nx}=E+Nx", (N * x).exp(), eye(2) + N * x)
eq("幂零 e^{N0}=E", (N * 0).exp(), eye(2))

# A1: 对角矩阵
D = diag(1, 2, -3)
eq("对角 e^{Dx}=diag(e^{x},e^{2x},e^{-3x})", (D * x).exp(), diag(exp(x), exp(2 * x), exp(-3 * x)))

# A2: 纯量矩阵
eq("纯量矩阵 e^{r x E}=e^{rx}E", ((2 * eye(3)) * x).exp(), exp(2 * x) * eye(3))

# A3: 1x1 矩阵指数就是标量解；p4 的 e^{atx} 与 n=1 定义矛盾
a = sp.symbols("a", real=True)
eq("1x1: e^{at}=exp(at)，不是 exp(atx)", (Matrix([[a]]) * t).exp(), Matrix([[exp(a * t)]]))

# A4: 求导公式 (e^{Ax})'=A e^{Ax}，取某非对角矩阵
A0 = Matrix([[1, 2], [3, 4]])
E0 = (A0 * x).exp()
eq("求导公式 d/dx e^{Ax}=A e^{Ax}", sp.diff(E0, x), A0 * E0)
eq("x=0 时 e^{A0}=E", E0.subs(x, 0), eye(2))
eq("x=0 时导数=A", sp.diff(E0, x).subs(x, 0), A0)

# A5: e^{At}e^{As}=e^{A(t+s)}，以及逆
eq("e^{At}e^{As}=e^{A(t+s)}", (A0 * t).exp() * (A0 * s).exp(), (A0 * (t + s)).exp())
eq("e^{-At}=(e^{At})^{-1}", (A0 * (-t)).exp(), (A0 * t).exp().inv())

# A6: AB=BA 时可加；不可交换时不可加
A = Matrix([[0, 1], [0, 0]])
B = Matrix([[0, 0], [1, 0]])
ok("反例：AB-BA != 0", simplify(A * B - B * A) != zeros(2))
eq("反例：e^A=E+A", A.exp(), eye(2) + A)
eq("反例：e^B=E+B", B.exp(), eye(2) + B)
ok("反例：e^{A+B} != e^A e^B", simplify((A + B).exp() - A.exp() * B.exp()) != zeros(2))
eq("反例数值：e^A e^B=[[2,1],[1,1]]", A.exp() * B.exp(), Matrix([[2, 1], [1, 1]]))

# A7: 特征向量性质
H1 = Matrix([[-6, -4], [8, 6]])
V1 = Matrix([1, -2])
eq("特征向量性质 e^{Ax}V=e^{2x}V", (H1 * x).exp() * V1, exp(2 * x) * V1)

# =====================================================================
print("\n== B. 课件例题 1（p13--p15，3x3 对角化） ==")
A1 = Matrix([[1, -1, 1], [1, 1, -1], [2, -1, 0]])
V1m = Matrix([[1, 1, -1], [0, 1, 3], [1, 1, 5]])
L1 = diag(2, 1, -1)
# 特征多项式检查
pA1 = (A1 - lam * eye(3)).det()
eq0("Ex1 特征多项式恒等式", pA1 + (lam - 2) * (lam - 1) * (lam + 1))
eq("Ex1 AV=VΛ", A1 * V1m, V1m * L1)
eq("Ex1 det V=6", V1m.det(), 6)
V1inv = Matrix([[R(1, 3), -1, R(2, 3)],
                [R(1, 2), 1, -R(1, 2)],
                [-R(1, 6), 0, R(1, 6)]])
eq("Ex1 V^{-1}（正确值，含 (1,2)=-1）", V1m.inv(), V1inv)
eq("Ex1 V V^{-1}=E", V1m * V1inv, eye(3))
E1 = V1m * diag(exp(2 * x), exp(x), exp(-x)) * V1inv
eq("Ex1 e^{Ax} 与 SymPy Matrix.exp 一致", E1, (A1 * x).exp())
eq("Ex1 x=0 得 E", E1.subs(x, 0), eye(3))
eq("Ex1 导数在 0 处=A", sp.diff(E1, x).subs(x, 0), A1)
eq("Ex1 通解 = V e^{Λx} C", V1m * diag(exp(2 * x), exp(x), exp(-x)) * C3,
   c1 * Matrix([1, 0, 1]) * exp(2 * x)
   + c2 * Matrix([1, 1, 1]) * exp(x)
   + c3 * Matrix([-1, 3, 5]) * exp(-x))
V1inv_src = Matrix([[R(1, 3), 0, R(2, 3)],
                    [R(1, 2), 1, -R(1, 2)],
                    [-R(1, 6), 0, R(1, 6)]])
ok("勘误 p14：原印刷 V^{-1} 不满足 V V^{-1}=E",
   simplify(V1m * V1inv_src - eye(3)) != zeros(3))

# =====================================================================
print("\n== C. 课件例题 2（p20，多项式降阶） ==")
A2 = Matrix([[3, 1], [1, 2]])
p_poly = s ** 4 + 3 * s ** 3 + 2 * s ** 2 + s + 1
Delta2 = s ** 2 - 5 * s + 5
eq0("Ex2 长除法恒等式",
    sp.expand((s ** 2 + 8 * s + 37) * Delta2 + (146 * s - 184) - p_poly))
pA2 = A2 ** 4 + 3 * A2 ** 3 + 2 * A2 ** 2 + A2 + eye(2)
eq("Ex2 p(A)=146A-184E", pA2, 146 * A2 - 184 * eye(2))
eq("Ex2 直接值 [[254,146],[146,108]]", pA2, Matrix([[254, 146], [146, 108]]))

# =====================================================================
print("\n== D. 课件例题 4（p24--p25，实特征值 4,-2） ==")
A4 = Matrix([[1, 1], [9, 1]])
E4 = (A4 * x).exp()
eq("Ex4 特征多项式 (λ-4x)(λ+2x)",
    (A4 * x - lam * eye(2)).det(), sp.expand((lam - 4 * x) * (lam + 2 * x)))
a1x4 = (exp(4 * x) - exp(-2 * x)) / 6
a04 = (exp(4 * x) + 2 * exp(-2 * x)) / 3
eq("Ex4 α1x 与 α0", a1x4 * A4 + a04 * eye(2), E4)
eq("Ex4 闭式矩阵",
    E4, R(1, 6) * Matrix([[3 * exp(4 * x) + 3 * exp(-2 * x), exp(4 * x) - exp(-2 * x)],
                          [9 * exp(4 * x) - 9 * exp(-2 * x), 3 * exp(4 * x) + 3 * exp(-2 * x)]]))
eq("Ex4 导数在 0 处=A", sp.diff(E4, x).subs(x, 0), A4)
ct14, ct24 = (3 * c1 + c2) / 6, (3 * c1 - c2) / 6
Y4 = E4 * C2
eq("Ex4 通解（正确 c̃1,c̃2）",
    Y4, ct14 * exp(4 * x) * Matrix([1, 3]) + ct24 * exp(-2 * x) * Matrix([1, -3]))
Y4_src = (3 * c1 + c2) * exp(4 * x) * Matrix([1, 3]) + (3 * c1 - c2) * exp(-2 * x) * Matrix([1, -3])
ok("勘误 p25：缺 1/6 的 c̃ 不满足通解", simplify(Y4_src - Y4) != zeros(2))

# =====================================================================
print("\n== E. 课件例题 5（p26--p27，特征值 ±i） ==")
A5 = Matrix([[0, 1], [-1, 0]])
E5 = (A5 * x).exp()
eq("Ex5 特征多项式 λ^2+x^2", (A5 * x - lam * eye(2)).det(), lam ** 2 + x ** 2)
eq("Ex5 e^{Ax}=[[cos,sin],[-sin,cos]]", E5, Matrix([[cos(x), sin(x)], [-sin(x), cos(x)]]))
eq("Ex5 导数在 0 处=A", sp.diff(E5, x).subs(x, 0), A5)
eq("Ex5 det e^{Ax}=1", E5.det(), 1)
eq("Ex5 通解（正确符号）", E5 * C2,
   c1 * Matrix([cos(x), -sin(x)]) + c2 * Matrix([sin(x), cos(x)]))
Ys5 = c1 * Matrix([cos(x), -sin(x)]) + c2 * Matrix([-sin(x), cos(x)])
ok("勘误 p27：印刷的第二个基向量不满足 Y'=AY",
   simplify(sp.diff(Ys5, x).subs(x, 0) - A5 * Ys5.subs(x, 0)) != zeros(2))

# =====================================================================
print("\n== F. 课件例题 6（p30--p31，重特征值方程组与补充解） ==")
a0, a1, a2, a3 = sp.symbols("a0 a1 a2 a3")
eqs6 = [
    sp.Eq(exp(5 * x), a3 * (5 * x) ** 3 + a2 * (5 * x) ** 2 + a1 * (5 * x) + a0),
    sp.Eq(exp(5 * x), 3 * a3 * (5 * x) ** 2 + 2 * a2 * (5 * x) + a1),
    sp.Eq(exp(5 * x), 6 * a3 * (5 * x) + 2 * a2),
    sp.Eq(exp(2 * x), a3 * (2 * x) ** 3 + a2 * (2 * x) ** 2 + a1 * (2 * x) + a0),
]
sol6 = sp.solve(eqs6, [a3, a2, a1, a0], simplify=True)
r6 = a3 * lam ** 3 + a2 * lam ** 2 + a1 * lam + a0
eq("Ex6 解满足 r(5x)=e^{5x}", r6.subs(sol6).subs(lam, 5 * x), exp(5 * x))
eq("Ex6 解满足 r'(5x)=e^{5x}", sp.diff(r6, lam).subs(sol6).subs(lam, 5 * x), exp(5 * x))
eq("Ex6 解满足 r''(5x)=e^{5x}", sp.diff(r6, lam, 2).subs(sol6).subs(lam, 5 * x), exp(5 * x))
eq("Ex6 解满足 r(2x)=e^{2x}", r6.subs(sol6).subs(lam, 2 * x), exp(2 * x))
for name, value, target in (("α3", a3, R(1, 6)), ("α2", a2, R(1, 2)), ("α1", a1, 1), ("α0", a0, 1)):
    ok(f"Ex6 x→0 时 {name}→{target}", sp.limit(sol6[value], x, 0) == target)
# 讲义写出的四个闭式
A3_form = (exp(5 * x) * (2 - 6 * x + 9 * x ** 2) - 2 * exp(2 * x)) / (54 * x ** 3)
A2_form = (exp(5 * x) * (-18 * x ** 2 + 15 * x - 5) + 5 * exp(2 * x)) / (9 * x ** 2)
A1_form = (exp(5 * x) * (135 * x ** 2 - 132 * x + 50) - 50 * exp(2 * x)) / (18 * x)
A0_form = (exp(5 * x) * (-225 * x ** 2 + 240 * x - 98) + 125 * exp(2 * x)) / 27
eq("Ex6 讲义 α3 与解一致", A3_form, sol6[a3])
eq("Ex6 讲义 α2 与解一致", A2_form, sol6[a2])
eq("Ex6 讲义 α1 与解一致", A1_form, sol6[a1])
eq("Ex6 讲义 α0 与解一致", A0_form, sol6[a0])

# =====================================================================
print("\n== G. 课件例题 7（p33--p35，三重特征值 -2） ==")
A7 = Matrix([[0, -4, 0], [1, -4, 0], [1, -2, -2]])
eq("Ex7 A^2", A7 ** 2, Matrix([[-4, 16, 0], [-4, 12, 0], [-4, 8, 4]]))
eq0("Ex7 特征多项式 det(A-λE)=-(λ+2)^3",
    (A7 - lam * eye(3)).det() + (lam + 2) ** 3)
E7 = (A7 * x).exp()
eq("Ex7 e^{Ax} 闭式", E7,
   exp(-2 * x) * Matrix([[2 * x + 1, -4 * x, 0], [x, -2 * x + 1, 0], [x, -2 * x, 1]]))
eq("Ex7 导数在 0 处=A", sp.diff(E7, x).subs(x, 0), A7)
ct17, ct37 = c1 - 2 * c2, c3 - c2
Y7 = E7 * C3
eq("Ex7 通解（正确 c̃3=c3-c2）",
    Y7,
    ct17 * exp(-2 * x) * (x * Matrix([2, 1, 1]) + Matrix([1, 0, 0]))
    + c2 * exp(-2 * x) * Matrix([2, 1, 1])
    + ct37 * exp(-2 * x) * Matrix([0, 0, 1]))
Y7_src = (c1 - 2 * c2) * exp(-2 * x) * (x * Matrix([2, 1, 1]) + Matrix([1, 0, 0])) \
    + c2 * exp(-2 * x) * Matrix([2, 1, 1]) + (c3 - 2 * c2) * exp(-2 * x) * Matrix([0, 0, 1])
ok("勘误 p35：c̃3=c3-2c2 不满足通解", simplify(Y7_src - Y7) != zeros(3))

# =====================================================================
print("\n== H. 课件例题 8（p36--p38，0,±i） ==")
A8 = Matrix([[0, 1, 0], [0, -2, -5], [0, 1, 2]])
eq("Ex8 A^2", A8 ** 2, Matrix([[0, -2, -5], [0, -1, 0], [0, 0, -1]]))
eq0("Ex8 特征多项式 det(A-λE)=-λ(λ^2+1)",
    (A8 - lam * eye(3)).det() + lam * (lam ** 2 + 1))
E8 = (A8 * x).exp()
a2x2 = 1 - cos(x)
a1x = sin(x)
eq("Ex8 e^{Ax} 闭式", E8,
   Matrix([[1, -2 * a2x2 + a1x, -5 * a2x2],
           [0, -a2x2 - 2 * a1x + 1, -5 * a1x],
           [0, a1x, -a2x2 + 2 * a1x + 1]]))
eq("Ex8 导数在 0 处=A", sp.diff(E8, x).subs(x, 0), A8)
E8_p36 = Matrix([[1, -2 * a2x2 + a1x, -5 * a2x2],
                 [0, -a2x2 - 2 * a1x + 1, -5 * a1x],
                 [0, -a1x, -a2x2 + 2 * a1x + 1]])
ok("勘误 p36：(3,2) 印成 -α1x 与 e^{Ax} 不符", simplify(E8_p36 - E8) != zeros(3))

# =====================================================================
print("\n== I. 作业 H1（p44 第 1 题，实特征值 ±2） ==")
eq0("H1 特征多项式 λ^2-4", (H1 - lam * eye(2)).det() - (lam ** 2 - 4))
V1h = Matrix([[1, 1], [-2, -1]])
eq("H1 det V=1", V1h.det(), 1)
eq("H1 V^{-1}", V1h.inv(), Matrix([[-1, -1], [2, 1]]))
E1h = (H1 * x).exp()
eq("H1 e^{Ax} 闭式", E1h,
   Matrix([[-exp(2 * x) + 2 * exp(-2 * x), -exp(2 * x) + exp(-2 * x)],
           [2 * exp(2 * x) - 2 * exp(-2 * x), 2 * exp(2 * x) - exp(-2 * x)]]))
eq("H1 导数在 0 处=A", sp.diff(E1h, x).subs(x, 0), H1)
eq("H1 x=0 得 E", E1h.subs(x, 0), eye(2))
eq("H1 通解", V1h * diag(exp(2 * x), exp(-2 * x)) * C2,
   c1 * Matrix([1, -2]) * exp(2 * x) + c2 * Matrix([1, -1]) * exp(-2 * x))
a1x_h1 = (exp(2 * x) - exp(-2 * x)) / 4
a0_h1 = (exp(2 * x) + exp(-2 * x)) / 2
eq("H1 Cayley--Hamilton 交叉核对", a1x_h1 * H1 + a0_h1 * eye(2), E1h)

# =====================================================================
print("\n== J. 作业 H2（p44 第 2 题，共轭复特征值 ±2i） ==")
H2 = Matrix([[-4, 4], [-5, 4]])
eq0("H2 特征多项式 λ^2+4", (H2 - lam * eye(2)).det() - (lam ** 2 + 4))
E2h = (H2 * x).exp()
eq("H2 e^{Ax} 闭式",
   E2h, Matrix([[cos(2 * x) - 2 * sin(2 * x), 2 * sin(2 * x)],
                [-R(5, 2) * sin(2 * x), cos(2 * x) + 2 * sin(2 * x)]]))
eq("H2 导数在 0 处=A", sp.diff(E2h, x).subs(x, 0), H2)
eq("H2 x=0 得 E", E2h.subs(x, 0), eye(2))
eq("H2 通解", E2h * C2,
   c1 * Matrix([cos(2 * x) - 2 * sin(2 * x), -R(5, 2) * sin(2 * x)])
   + c2 * Matrix([2 * sin(2 * x), cos(2 * x) + 2 * sin(2 * x)]))
a1x_h2 = sin(2 * x) / 2
a0_h2 = cos(2 * x)
eq("H2 Cayley--Hamilton 交叉核对", a1x_h2 * H2 + a0_h2 * eye(2), E2h)
vech2 = Matrix([2, 2 + I])
eq("H2 复特征向量 AV=2iV", H2 * vech2, 2 * I * vech2)

# =====================================================================
print("\n== K. 作业 H3（p44 第 3 题，三个不同实特征值） ==")
H3 = Matrix([[-24, 0, 0], [4, -2, 0], [1, 0, 2]])
V3h = Matrix([[286, 0, 0], [-52, 1, 0], [-11, 0, 1]])
eq("H3 det V=286", V3h.det(), 286)
eq("H3 V^{-1}", V3h.inv(),
   Matrix([[R(1, 286), 0, 0], [R(2, 11), 1, 0], [R(1, 26), 0, 1]]))
eq("H3 AV=VΛ", H3 * V3h, V3h * diag(-24, -2, 2))
E3h = (H3 * x).exp()
eq("H3 e^{Ax} 闭式", E3h,
   Matrix([[exp(-24 * x), 0, 0],
           [R(2, 11) * (exp(-2 * x) - exp(-24 * x)), exp(-2 * x), 0],
           [R(1, 26) * (exp(2 * x) - exp(-24 * x)), 0, exp(2 * x)]]))
eq("H3 导数在 0 处=A", sp.diff(E3h, x).subs(x, 0), H3)
eq("H3 x=0 得 E", E3h.subs(x, 0), eye(3))
eq("H3 通解", V3h * diag(exp(-24 * x), exp(-2 * x), exp(2 * x)) * C3,
   c1 * Matrix([286, -52, -11]) * exp(-24 * x)
   + c2 * Matrix([0, 1, 0]) * exp(-2 * x)
   + c3 * Matrix([0, 0, 1]) * exp(2 * x))

# =====================================================================
print("\n== L. 基本矩阵（p39--p43） ==")
x0 = sp.symbols("x0", real=True)
eq("Φ(x)Φ^{-1}(x0)=e^{A(x-x0)}",
   E5 * E5.subs(x, x0).inv(), (A5 * (x - x0)).exp())
eq("e^{Ax}e^{-Ax}=E", E5 * E5.inv(), eye(2))
eq("Φ(0)=E 时 e^{Ax}=Φ(x)", E5.subs(x, 0), eye(2))

# =====================================================================
print("\n== M. 条件与反例 ==")
mu = sp.symbols("mu")
J = Matrix([[mu, 1], [0, mu]])
eq("2x2 Jordan 块 e^{Ax}=e^{μx}[[1,x],[0,1]]",
   (J * x).exp(), exp(mu * x) * Matrix([[1, x], [0, 1]]))
eq("Jordan 块几何重数 g=1<代数重数 m=2",
   2 - (J - mu * eye(2)).rank(), 1)

# =====================================================================
print("\n== N. 重根插值条件与首一约定（R1/R3/R4） ==")
# 纯量矩阵：代数重数 2，但最大 Jordan 块为 1；按 m 加的导数条件仍给出 e^{Ax}
A_scalar = mu * eye(2)
E_scalar = (A_scalar * x).exp()
a1s, a0s = sp.symbols("a1s a0s")
sol_scalar = sp.solve(
    [sp.Eq(a1s * mu * x + a0s, exp(mu * x)), sp.Eq(a1s, exp(mu * x))],
    [a1s, a0s], dict=True,
)[0]
r_scalar_at = sol_scalar[a1s] * A_scalar * x + sol_scalar[a0s] * eye(2)
eq("R1 纯量矩阵：Hermite 条件给出 r(Ax)=e^{Ax}", r_scalar_at, E_scalar)
eq("R1 纯量矩阵：r(μx)=e^{μx}",
   sol_scalar[a1s] * mu * x + sol_scalar[a0s], exp(mu * x))
eq("R1 纯量矩阵：r'(μx)=e^{μx}", sol_scalar[a1s], exp(mu * x))
# 只用值条件（一次多项式退化为常数）也给出同一个 r(Ax)
r_value_only = exp(mu * x) * eye(2)
eq("R1 纯量矩阵：只用值条件 r(Ax) 仍为 e^{Ax}", r_value_only, E_scalar)
ok("R1 零多项式不满足 r(μx)=e^{μx}", sp.simplify(0 - exp(mu * x)) != 0)

# 3x3 Jordan 块：按 m=3 加到二阶导数，r(J)=e^J
J3 = Matrix([[mu, 1, 0], [0, mu, 1], [0, 0, mu]])
a2j, a1j, a0j = sp.symbols("a2j a1j a0j")
rj = a2j * lam ** 2 + a1j * lam + a0j
sol_j = sp.solve(
    [sp.Eq(rj.subs(lam, mu), exp(mu)),
     sp.Eq(sp.diff(rj, lam).subs(lam, mu), exp(mu)),
     sp.Eq(sp.diff(rj, lam, 2).subs(lam, mu), exp(mu))],
    [a2j, a1j, a0j], dict=True,
)[0]
rJ = sol_j[a2j] * J3 ** 2 + sol_j[a1j] * J3 + sol_j[a0j] * eye(3)
eq("R1 3x3 Jordan 块：r(J)=e^J", rJ, J3.exp())

# R3：首一特征多项式与 det(A-λE) 的符号关系
eq("R3 n=3：det(λE-A)=(λ+2)^3", (lam * eye(3) - A7).det(), (lam + 2) ** 3)
eq("R3 n=3：det(A-λE)=(-1)^3 det(λE-A)",
   (A7 - lam * eye(3)).det(), (-1) ** 3 * (lam * eye(3) - A7).det())
eq("R3 Example 8：det(λE-A)=λ(λ^2+1)",
   (lam * eye(3) - A8).det(), lam * (lam ** 2 + 1))

# R4：Ax 的特征值只在 x=0 合并
ok("R4 4x 与 -2x 仅在 x=0 重合", sp.solve(sp.Eq(4 * x, -2 * x), x) == [0])
ok("R4 ix 与 -ix 仅在 x=0 重合", sp.solve(sp.Eq(I * x, -I * x), x) == [0])

# =====================================================================
print(f"\n共执行 {checks} 条断言，失败 {len(failures)} 条。")
if failures:
    print("失败项：")
    for item in failures:
        print("  -", item)
    sys.exit(1)
print("ALL CHECKS PASSED")
