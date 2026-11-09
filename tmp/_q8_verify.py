import numpy as np, sympy as sp
from scipy.integrate import quad

a_val, b_val = 1.0, 2.0
f = lambda x: a_val*(b_val-a_val)/(np.pi*b_val) / (x**2 + (b_val-a_val)**2)
kernel = lambda x: 1.0/(x**2 + a_val**2)

print("check convolution identity  (f * 1/(x^2+a^2))(x)  vs  1/(x^2+b^2)")
for x0 in [0.0, 0.5, 1.0, 2.5]:
    lhs = quad(lambda e: f(e)*kernel(x0-e), -np.inf, np.inf, limit=400)[0]
    rhs = 1.0/(x0**2 + b_val**2)
    print(f"  x={x0:4}: lhs={lhs:.10f}  rhs={rhs:.10f}  diff={lhs-rhs:+.2e}")

# symbolic check of transform pair under F(k)=1/(2pi) int f e^{-ikx} dx
x, k, c = sp.symbols('x k c', real=True)
F_of = 1/(2*sp.pi)*sp.integrate(sp.exp(-sp.I*k*x)/(x**2+c**2), (x, -sp.oo, sp.oo))
print("F[1/(x^2+c^2)] =", sp.simplify(F_of))
print("target e^{-|k|c}/(2c) matches for k>0:", sp.simplify(F_of.subs(k, sp.Symbol('k', positive=True)) - sp.exp(-k*c)/(2*c)) == 0)

# symbolic convolution identity check (general a,b) via transforms
kpos = sp.Symbol('k', positive=True)
F1 = (a_val/(2*sp.pi*b_val))*sp.exp(-kpos*(b_val-a_val))
F2 = sp.exp(-kpos*a_val)/(2*a_val)
print("2*pi*F1*F2 =", sp.simplify(2*sp.pi*F1*F2), " vs e^{-kb}/(2b) =", sp.exp(-kpos*b_val)/(2*b_val))
