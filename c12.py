import sympy as sp
x=sp.symbols("x")
A=sp.Matrix([[-2,1],[-5,2]])
print("eigen:", A.eigenvects())
C1,C2=sp.symbols("C1 C2")
# try V=(2+i,5)
V=sp.Matrix([2+sp.I,5]); print("A V - i V =", (A-sp.I*sp.eye(2))*V)
print("real/imag of e^{ix}V:")
z=sp.exp(sp.I*x)*V
print("  Re:", sp.simplify(sp.re(sp.expand(z))))
print("  Im:", sp.simplify(sp.im(sp.expand(z))))
# check claimed
Y=M=None
Y1=sp.Matrix([2*sp.cos(x)-sp.sin(x), 5*sp.cos(x)])
Y2=sp.Matrix([2*sp.sin(x)+sp.cos(x), 5*sp.sin(x)])
print("res1:", sp.simplify(sp.diff(Y1,x)-A*Y1).T)
print("res2:", sp.simplify(sp.diff(Y2,x)-A*Y2).T)
# L17-05
A5=sp.Matrix([[-8,1,-5],[18,-1,10],[11,-7,10]])
Yp=sp.Matrix([sp.cos(2*x),0,sp.cos(2*x)+sp.sin(2*x)])
F = sp.diff(Yp,x)-A5*Yp
print("L17-05 由特解反推出的 F =", sp.simplify(F).T)
print("   即 cos2x 系数:", sp.simplify(sp.expand(F).coeff(sp.cos(2*x))).T, " sin2x 系数:", sp.simplify(sp.expand(F).coeff(sp.sin(2*x))).T)
