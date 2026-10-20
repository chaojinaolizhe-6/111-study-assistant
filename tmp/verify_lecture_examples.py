import sympy as sp
x, s = sp.symbols('x s', real=True)

def chk(name, A, E):
    ok0 = sp.simplify(E.subs(x,0) - sp.eye(A.shape[0])) == sp.zeros(A.shape[0])
    ok = sp.simplify(sp.diff(E,x) - A*E) == sp.zeros(*A.shape)
    ok2 = sp.simplify(sp.exp(x*A) - E) == sp.zeros(*A.shape)
    print(f"[{name}] E(0)=I {ok0} | E'=AE {ok} | ==sympy.exp {ok2}")

# E2 CH 实不同特征值 A=[[2,1],[1,2]] lam=3,1
A = sp.Matrix([[2,1],[1,2]])
E = sp.Rational(1,2)*sp.Matrix([[sp.exp(3*x)+sp.exp(x), sp.exp(3*x)-sp.exp(x)],
                                [sp.exp(3*x)-sp.exp(x), sp.exp(3*x)+sp.exp(x)]])
chk("E2 CH distinct", A, E)

# E3 CH 复共轭 A=[[0,1],[-1,0]]
A = sp.Matrix([[0,1],[-1,0]])
E = sp.Matrix([[sp.cos(x), sp.sin(x)],[-sp.sin(x), sp.cos(x)]])
chk("E3 CH complex", A, E)

# E4 CH 重根不可对角化 A=[[1,1],[0,1]]
A = sp.Matrix([[1,1],[0,1]])
E = sp.exp(x)*sp.Matrix([[2-x, 1],[0, 2-x]])
chk("E4 CH repeated", A, E)

# E1 对角化路线 作业一第1题
A = sp.Matrix([[-6,-4],[8,6]]); V = sp.Matrix([[1,1],[-2,-1]]); Vinv = sp.simplify(V.inv())
print("V^-1 =", Vinv.tolist())
E1 = sp.simplify(V*sp.diag(sp.exp(2*x), sp.exp(-2*x))*Vinv)
chk("E1 diag hw1", A, E1); print("E1 =", [[sp.simplify(t) for t in row] for row in E1.tolist()])

# E8 共振 A=diag(1,2), F=e^{2x}(0,1)
A = sp.diag(1,2); F = sp.exp(2*x)*sp.Matrix([0,1])
C1, C2 = sp.symbols('C1 C2')
Y = sp.Matrix([C1*sp.exp(x), (C2+x)*sp.exp(2*x)])
print("[E8 resonance] 通解满足:", sp.simplify(sp.diff(Y,x)-(A*Y+F)) == sp.zeros(2,1))
Yp = sp.Matrix([0, x*sp.exp(2*x)])
print("[E8] 特解满足:", sp.simplify(sp.diff(Yp,x)-(A*Yp+F)) == sp.zeros(2,1))
# 相容性条件核对: (A-2E) beta = alpha - gamma
al = sp.Matrix([0,1]); ga = sp.Matrix([0,1]); be = sp.Matrix([0,0])
print("[E8] (A-2E)beta =", ((A-2*sp.eye(2))*be).T.tolist(), " alpha-gamma =", (al-ga).T.tolist())

# T1 自测题 A=[[1,2],[3,2]]
A = sp.Matrix([[1,2],[3,2]])
print("T1 eigenvalues:", A.eigenvals(), "charpoly:", sp.factor(A.charpoly().as_expr()))
E = sp.Rational(1,5)*sp.Matrix([[2*sp.exp(4*x)+3*sp.exp(-x), 2*(sp.exp(4*x)-sp.exp(-x))],
                                [3*(sp.exp(4*x)-sp.exp(-x)), 3*sp.exp(4*x)+2*sp.exp(-x)]])
chk("T1 selftest", A, E)

# 作业二 待定系数关键量
A = sp.Matrix([[-2,-2,2],[-3,1,-4],[-3,2,-5]])
print("hw2 eigen:", A.eigenvals())
al = sp.Matrix([1,0,0]); be = sp.Matrix([0,1,0])
print("A alpha =", (A*al).T.tolist(), " -gamma1 =", [-2,-3,-3])
print("A beta  =", (A*be).T.tolist(), " alpha - gamma0 =", [1-3, 0-(-1), 0-(-2)])
