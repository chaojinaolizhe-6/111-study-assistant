import sympy as sp
x,t=sp.symbols('x t', real=True)
def show(name,M): print('---',name); sp.pprint(sp.simplify(M))
# Ex7
A=sp.Matrix([[0,-4,0],[1,-4,0],[1,-2,-2]])
show('Ex7 A2',A*A)
show('Ex7 exp via sympy', (A*x).exp())
a2x2=sp.Rational(1,2)*sp.exp(-2*x)*x**2; a1x=(1+2*x)*x*sp.exp(-2*x); a0=(1+2*x+2*x**2)*sp.exp(-2*x)
E7=a2x2*A*A+a1x*A+a0*sp.eye(3)
show('Ex7 ours',E7)
print('match', sp.simplify(E7-(A*x).exp())==sp.zeros(3))
# Ex8
B=sp.Matrix([[0,1,0],[0,-2,-5],[0,1,2]])
show('Ex8 A2',B*B)
E8=(1-sp.cos(x))*B*B*x**0 # careful: alpha2 x^2 * A^2, alpha2x2=1-cos x
E8=(1-sp.cos(x))*B*B+sp.sin(x)*B+sp.eye(3)
show('Ex8 ours',E8)
print('match8', sp.simplify(E8-(B*x).exp())==sp.zeros(3))
# H1 H2 H3
H1=sp.Matrix([[-6,-4],[8,6]]); H2=sp.Matrix([[-4,4],[-5,4]]); H3=sp.Matrix([[-24,0,0],[4,-2,0],[1,0,2]])
for nm,H in [('H1',H1),('H2',H2),('H3',H3)]:
    show(nm+' exp', (H*x).exp())
    print(nm,'eig',H.eigenvals())
print('H3 Vinv check')
V=sp.Matrix([[286,0,0],[-52,1,0],[-11,0,1]]); print(V.inv())
