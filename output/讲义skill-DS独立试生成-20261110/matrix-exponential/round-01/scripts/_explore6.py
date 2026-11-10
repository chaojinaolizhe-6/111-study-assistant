import sympy as sp
x=sp.symbols('x', real=True)
a0,a1,a2,a3=sp.symbols('a0 a1 a2 a3')
eqs=[
sp.Eq(sp.exp(5*x), a3*(5*x)**3+a2*(5*x)**2+a1*(5*x)+a0),
sp.Eq(sp.exp(5*x), 3*a3*(5*x)**2+2*a2*(5*x)+a1),
sp.Eq(sp.exp(5*x), 6*a3*(5*x)+2*a2),
sp.Eq(sp.exp(2*x), a3*(2*x)**3+a2*(2*x)**2+a1*(2*x)+a0),
]
sol=sp.solve(eqs,[a3,a2,a1,a0], simplify=True)
for k,v in sol.items(): print(k, '=', sp.simplify(v))
print('limit a3 at 0:', sp.limit(sol[a3], x, 0))
