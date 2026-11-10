import sympy as sp
x=sp.symbols('x', real=True)
A=sp.Matrix([[1,-1,1],[1,1,-1],[2,-1,0]])
V=sp.Matrix([[1,1,-1],[0,1,3],[1,1,5]])
print("V^-1=", V.inv())
L=sp.diag(2,1,-1)
print("expAx="); sp.pprint(sp.simplify(V*sp.diag(sp.exp(2*x),sp.exp(x),sp.exp(-x))*V.inv()))
print("sympy exp:", sp.simplify(A*x).exp())
print("check A eigen:", [(l, (A-l*sp.eye(3)).nullspace()) for l in (2,1,-1)])
