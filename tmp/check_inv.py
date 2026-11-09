import sympy as sp
k, r, th, mu = sp.symbols("k r theta mu", positive=True)
# 反演核验：∫ (e^{ik·r}/(k^2+mu^2)) d^3k = 2*pi^2 e^{-mu r}/r
ang = sp.integrate(sp.sin(th)*sp.exp(sp.I*k*r*sp.cos(th)), (th, 0, sp.pi))
val = sp.simplify(2*sp.pi*sp.integrate(k**2*ang/(k**2+mu**2), (k, 0, sp.oo)))
print("∫ e^{ik·r}/(k²+μ²) d³k =", sp.simplify(val))
print("与 2π²e^{-μr}/r 之差 =", sp.simplify(val - 2*sp.pi**2*sp.exp(-mu*r)/r))
