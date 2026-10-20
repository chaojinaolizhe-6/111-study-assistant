# -*- coding: utf-8 -*-
"""符号验算：Lecture 16 矩阵指数 + Lecture 17-18 非齐次线性方程组。"""
import sympy as sp

x = sp.symbols('x', real=True)
I2 = sp.eye(2)
I3 = sp.eye(3)


def check(name, A, E, var=x):
    E0 = sp.simplify(E.subs(var, 0))
    ok0 = sp.simplify(E0 - sp.eye(A.shape[0])) == sp.zeros(A.shape[0])
    dE = sp.diff(E, var)
    ok = sp.simplify(dE - A * E) == sp.zeros(*A.shape)
    ok2 = sp.simplify(E * A - A * E) == sp.zeros(*A.shape)
    print(f"[{name}] E(0)=I: {ok0};  E'=A*E: {ok};  E*A=A*E: {ok2}")
    return ok0 and ok and ok2


# ---------- Lecture 16 ----------
# Q1
A1 = sp.Matrix([[-6, -4], [8, 6]])
E1 = sp.Matrix([[-sp.exp(2 * x) + 2 * sp.exp(-2 * x), -sp.exp(2 * x) + sp.exp(-2 * x)],
                [2 * sp.exp(2 * x) - 2 * sp.exp(-2 * x), 2 * sp.exp(2 * x) - sp.exp(-2 * x)]])
print("A1^2 =", sp.simplify(A1 * A1).tolist())
check("L16-Q1 (exp form)", A1, E1)
E1h = sp.Matrix([[sp.cosh(2 * x) - 3 * sp.sinh(2 * x), -2 * sp.sinh(2 * x)],
                 [4 * sp.sinh(2 * x), sp.cosh(2 * x) + 3 * sp.sinh(2 * x)]])
print("  hyperbolic form equals exp form:",
      sp.simplify(E1h - E1) == sp.zeros(2, 2))
print("  sympy 直接求: ", sp.simplify(A1.exp() if False else (sp.exp(x * A1)) - E1) == sp.zeros(2, 2))

# Q2
A2 = sp.Matrix([[-4, 4], [-5, 4]])
E2 = sp.Matrix([[sp.cos(2 * x) - 2 * sp.sin(2 * x), 2 * sp.sin(2 * x)],
                [-sp.Rational(5, 2) * sp.sin(2 * x), sp.cos(2 * x) + 2 * sp.sin(2 * x)]])
print("A2^2 =", sp.simplify(A2 * A2).tolist())
check("L16-Q2", A2, E2)
print("  sympy 直接求一致:", sp.simplify(sp.exp(x * A2) - E2) == sp.zeros(2, 2))

# Q3
A3 = sp.Matrix([[-24, 0, 0], [4, -2, 0], [1, 0, 2]])
E3 = sp.Matrix([[sp.exp(-24 * x), 0, 0],
                [sp.Rational(2, 11) * (sp.exp(-2 * x) - sp.exp(-24 * x)), sp.exp(-2 * x), 0],
                [sp.Rational(1, 26) * (sp.exp(2 * x) - sp.exp(-24 * x)), 0, sp.exp(2 * x)]])
check("L16-Q3", A3, E3)
print("  sympy 直接求一致:", sp.simplify(sp.exp(x * A3) - E3) == sp.zeros(3, 3))
print("  eigenvalues:", A3.eigenvals())

# ---------- Lecture 17-18 ----------
C1, C2, C3 = sp.symbols('C1 C2 C3')
A = sp.Matrix([[-2, -2, 2], [-3, 1, -4], [-3, 2, -5]])
f = sp.Matrix([2 * x + 3, 3 * x - 1, 3 * x - 2])
print("A eigenvalues:", A.eigenvals())
print("charpoly:", sp.factor(A.charpoly().as_expr()))

Y = sp.Matrix([-2 * C1 * sp.exp(-x) - C2 * sp.exp(-2 * x) + x,
               5 * C1 * sp.exp(-x) + 3 * C2 * sp.exp(-2 * x) + C3 * sp.exp(-3 * x) + 1,
               4 * C1 * sp.exp(-x) + 3 * C2 * sp.exp(-2 * x) + C3 * sp.exp(-3 * x)])
res = sp.simplify(sp.diff(Y, x) - (A * Y + f))
print("[L17-18] 通解满足 Y'=AY+f:", res == sp.zeros(3, 1))

# 待定系数法：特解
Yp = sp.Matrix([x, 1, 0])
print("  特解 Yp=(x,1,0) 满足:", sp.simplify(sp.diff(Yp, x) - (A * Yp + f)) == sp.zeros(3, 1))

# 常数变易法：基本解矩阵与积分
P = sp.Matrix([[-2, -1, 0], [5, 3, 1], [4, 3, 1]])
Pinv = sp.simplify(P.inv())
print("P^-1 =", Pinv.tolist())
Phi = P * sp.diag(sp.exp(-x), sp.exp(-2 * x), sp.exp(-3 * x))
g = sp.simplify(Pinv * f)
print("P^-1 f =", [sp.simplify(t) for t in g])
# 常数变易法正确用法：Phi^{-1} f，再积分
Phi_inv = sp.simplify(Phi.inv())
print("Phi^-1 =", [[sp.simplify(t) for t in row] for row in Phi_inv.tolist()])
gf = sp.simplify(Phi_inv * f)
print("Phi^-1 f =", [sp.simplify(t) for t in gf])
ints = [sp.integrate(sp.simplify(sp.expand(t)), x) for t in gf]
print("积分:", [sp.simplify(t) for t in ints])
Yp2 = sp.simplify(Phi * sp.Matrix(ints))
print("Phi∫ =", [sp.simplify(t) for t in Yp2], " 与 (x,1,0) 一致:",
      sp.simplify(Yp2 - Yp) == sp.zeros(3, 1))

# 齐次通解验证
Yh = sp.Matrix([-2 * C1 * sp.exp(-x) - C2 * sp.exp(-2 * x),
                5 * C1 * sp.exp(-x) + 3 * C2 * sp.exp(-2 * x) + C3 * sp.exp(-3 * x),
                4 * C1 * sp.exp(-x) + 3 * C2 * sp.exp(-2 * x) + C3 * sp.exp(-3 * x)])
print("齐次部分满足 Y'=AY:", sp.simplify(sp.diff(Yh, x) - A * Yh) == sp.zeros(3, 1))
print("e^{Ax} 直接求 (齐次基本解) 行数检查:", sp.exp(x * A).shape)
