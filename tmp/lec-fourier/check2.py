# -*- coding: utf-8 -*-
"""Re-check p50 convolution identity and p61 jump with correct formulas."""
import numpy as np

aa, bb = 0.6, 1.9
c = bb - aa
eta = np.linspace(-400, 400, 8000001)
coef = aa * c / (np.pi * bb)
f_eta = coef / (eta ** 2 + c ** 2)          # f(eta) = a(b-a)/(pi b) * 1/(eta^2+(b-a)^2)
for x in (0.0, 0.5, -1.3, 2.7):
    lhs = np.trapezoid(f_eta / ((x - eta) ** 2 + aa ** 2), eta)
    rhs = 1 / (x ** 2 + bb ** 2)
    print("p50 x=%5.1f  lhs=%.12f  rhs=%.12f  diff=%.2e" % (x, lhs, rhs, abs(lhs - rhs)))

ag, x0, h = 1.1, 0.3, 1e-5
gp = lambda xx: 0.5 * np.sign(xx - x0) * np.exp(-ag * abs(xx - x0))
print("p61 jump g'(x0+)-g'(x0-) =", gp(x0 + h) - gp(x0 - h))
gg = lambda xx: -np.exp(-ag * abs(xx - x0)) / (2 * ag)
lhs_ode = lambda xx: (gg(xx + h) - 2 * gg(xx) + gg(xx - h)) / h ** 2 - ag ** 2 * gg(xx)
print("p61 ODE residual at x=2 (should be 0):", lhs_ode(2.0))
