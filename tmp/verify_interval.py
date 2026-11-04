# -*- coding: utf-8 -*-
import sympy as sp

x = sp.symbols("x")
pi = sp.pi
r = {}
r["E1  int_0^{pi/2} sin/(sin+cos)"] = sp.integrate(sp.sin(x) / (sp.sin(x) + sp.cos(x)), (x, 0, pi / 2))
r["E2  int_0^{pi/4} ln(1+tan)"] = sp.integrate(sp.log(1 + sp.tan(x)), (x, 0, pi / 4))
r["E3  int_0^{pi} x sinx/(1+cos^2)"] = sp.integrate(x * sp.sin(x) / (1 + sp.cos(x) ** 2), (x, 0, pi))
r["E4  int_0^{2pi} 1/(1+e^sin)"] = sp.integrate(1 / (1 + sp.exp(sp.sin(x))), (x, 0, 2 * pi))
r["E5  int_-2^2 (x^3cos(x/2)+1/2)sqrt(4-x^2)"] = sp.integrate(
    (x ** 3 * sp.cos(x / 2) + sp.Rational(1, 2)) * sp.sqrt(4 - x ** 2), (x, -2, 2)
)
r["mini int_0^2 x^2"] = sp.integrate(x ** 2, (x, 0, 2))
r["mini int_0^2 (2-x)^2"] = sp.integrate((2 - x) ** 2, (x, 0, 2))
r["int_-1^1 1/(1+e^x)"] = sp.integrate(1 / (1 + sp.exp(x)), (x, -1, 1))
r["int_0^{4pi} sin^2"] = sp.integrate(sp.sin(x) ** 2, (x, 0, 4 * pi))
r["int_0^{pi} sin^2"] = sp.integrate(sp.sin(x) ** 2, (x, 0, pi))
r["check int_0^{pi} sinx/(1+cos^2)"] = sp.integrate(sp.sin(x) / (1 + sp.cos(x) ** 2), (x, 0, pi))
r["self int_0^{pi/2} sqrt(sin)/(sqrt(sin)+sqrt(cos))"] = sp.integrate(
    sp.sqrt(sp.sin(x)) / (sp.sqrt(sp.sin(x)) + sp.sqrt(sp.cos(x))), (x, 0, pi / 2)
)

for k, v in r.items():
    print("%-46s = %-28s approx=%.10f" % (k, sp.simplify(v), float(v)))
print("pi/4      =", float(pi / 4))
print("pi ln2/8  =", float(pi * sp.log(2) / 8))
print("pi^2/4    =", float(pi ** 2 / 4))
print("pi        =", float(pi))
print("8/3       =", float(sp.Rational(8, 3)))
