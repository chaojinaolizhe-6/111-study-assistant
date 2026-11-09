import sympy as sp
r, k = sp.symbols("r k", positive=True)
lam = sp.symbols("lam", positive=True)
I = sp.integrate(sp.exp(-r/lam)*sp.sin(k*r), (r, 0, sp.oo))
print("∫0∞ e^{-r/λ} sin(kr) dr =", sp.simplify(I))
F = sp.simplify(1/(2*sp.pi**2*k)*I)
print("F(k) =", F)
print("与 λ²/(2π²(1+k²λ²)) 之差:", sp.simplify(F - lam**2/(2*sp.pi**2*(1+k**2*lam**2))))
# 三维原始积分（球坐标，k 沿 z 轴）符号核验
th = sp.symbols("theta", positive=True)
J = sp.integrate(sp.sin(th)*sp.exp(-sp.I*k*r*sp.cos(th)), (th, 0, sp.pi))
print("角向积分 =", sp.simplify(J))
F3 = sp.simplify((1/(2*sp.pi)**3)*2*sp.pi*sp.integrate(r*sp.exp(-r/lam)*J, (r, 0, sp.oo)))
print("三维 F(k) =", F3)
