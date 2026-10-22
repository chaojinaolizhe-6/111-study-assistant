# -*- coding: utf-8 -*-
"""Numeric spot-check of closed forms transcribed from the slides."""
import numpy as np

ok = []


def chk(name, a, b, tol=1e-9):
    ok.append((name, abs(a - b) < tol or abs((a - b) / b) < tol, a, b))


# p12: sawtooth f=-x/l on [-l,l]; b_n = 2(-1)^n/(n pi)
l = 1.0
x = np.linspace(-l, l, 2000001)
for n in (1, 2, 3):
    integ = np.trapezoid((-x / l) * np.sin(n * np.pi * x / l), x) / l
    chk("p12 b_n n=%d" % n, integ, 2 * (-1) ** n / (n * np.pi))

# p12 a_n should vanish
chk("p12 a_n n=2", np.trapezoid((-x / l) * np.cos(2 * np.pi * x / l), x) / l, 0.0, 1e-12)

# p24: rectangular pulse, A(w) = 2 sin(wT)/(pi w), T=1
T = 1.0
t = np.linspace(0, T, 200001)
for w in (0.7, 2.3, 5.1):
    chk("p24 A(w=%g)" % w, (2 / np.pi) * np.trapezoid(np.cos(w * t), t), 2 * np.sin(w * T) / (np.pi * w))

# p26: B(w) for truncated sine: (2A/pi) * w0/(w^2-w0^2) * sin(2N pi w/w0)
A0, w0, N = 1.0, 1.3, 2.0
lim = 2 * N * np.pi / w0
tt = np.linspace(0, lim, 2000001)
for w in (0.5, 0.9, 1.7):
    integ = (2 * A0 / np.pi) * np.trapezoid(np.sin(w0 * tt) * np.sin(w * tt), tt)
    closed = (2 * A0 / np.pi) * w0 / (w ** 2 - w0 ** 2) * np.sin(2 * N * np.pi * w / w0)
    chk("p26 B(w=%g)" % w, integ, closed, 1e-6)

# p32: gaussian F(k) = 1/(pi sqrt(2a)) exp(-k^2/(2a^2))
a = 1.7
xx = np.linspace(-40, 40, 4000001)
f = np.sqrt(a / np.pi) * np.exp(-(a ** 2) * xx ** 2 / 2)
for k in (0.0, 0.8, 2.0):
    integ = np.trapezoid(f * np.exp(-1j * k * xx), xx) / (2 * np.pi)
    chk("p32 F(k=%g) real" % k, integ.real, np.exp(-k ** 2 / (2 * a ** 2)) / (np.pi * np.sqrt(2 * a)), 1e-7)

# p38: F(k) = lambda^2/(2 pi^2 (1+k^2 lambda^2)) for f=(1/r)e^{-r/lambda}
lam = 0.9
r = np.linspace(1e-9, 60, 4000001)
for k in (0.4, 1.2):
    # F(k) = 1/(2 pi^2 k) * int e^{-r/lam} sin(kr) dr
    I = np.trapezoid(np.exp(-r / lam) * np.sin(k * r), r)
    chk("p38 F(k=%g)" % k, I / (2 * np.pi ** 2 * k), lam ** 2 / (2 * np.pi ** 2 * (1 + k ** 2 * lam ** 2)), 1e-6)

# p38 inner integral = k lam^2/(1+k^2 lam^2)
for k in (0.4, 1.2):
    I = np.trapezoid(np.exp(-r / lam) * np.sin(k * r), r)
    chk("p38 int(k=%g)" % k, I, k * lam ** 2 / (1 + k ** 2 * lam ** 2), 1e-6)

# p50: f(x) = a(b-a)/(pi b) * 1/(x^2+(b-a)^2) solves the convolution equation
aa, bb = 0.6, 1.9
eta = np.linspace(-300, 300, 6000001)
for x0v in (0.0, 0.5):
    Fx = aa * (bb - aa) / (np.pi * bb) / ((x0v - eta) ** 2 + (bb - aa) ** 2)
    lhs = np.trapezoid(Fx / ((x0v - eta) ** 2 + aa ** 2) * 0 + Fx * 0 + Fx, eta)  # placeholder
    # correct convolution: int f(eta)/((x-eta)^2+a^2) deta
    lhs = np.trapezoid(Fx / ((x0v - eta) ** 2 + aa ** 2), eta)
    chk("p50 conv x=%g" % x0v, lhs, 1 / (x0v ** 2 + bb ** 2), 1e-6)

# p60: F(k) = (1/(ik))(e^{ik r0}-e^{-ik r0}) for f=(4 pi^2/r) delta(r-r0)
r0 = 1.4
for k in (0.6, 1.9):
    # (1/(2pi)^3) * 4pi^2 * 2pi * r0 * int_0^pi sin th e^{-i k r0 cos th} d th
    th = np.linspace(0, np.pi, 2000001)
    ang = np.trapezoid(np.sin(th) * np.exp(-1j * k * r0 * np.cos(th)), th)
    val = (1 / (2 * np.pi) ** 3) * 4 * np.pi ** 2 * 2 * np.pi * r0 * ang
    ref = (np.exp(1j * k * r0) - np.exp(-1j * k * r0)) / (1j * k)
    chk("p60 F(k=%g)" % k, val.real, ref.real, 1e-7)

# p61: g(x) = -(1/(2a)) e^{-a|x-x0|} solves g'' - a^2 g = delta(x-x0)
# check: satisfies ODE away from x0 and jump in g' equals 1
ag, x0 = 1.1, 0.3
h = 1e-6
gp = lambda xx: -np.exp(-ag * abs(xx - x0)) / (2 * ag)
lhs_ode = lambda xx: (gp(xx + h) - 2 * gp(xx) + gp(xx - h)) / h ** 2 - ag ** 2 * gp(xx)
chk("p61 ODE residual x=2", lhs_ode(2.0), 0.0, 1e-4)
jump = (gp(x0 + h) - gp(x0 - h)) / (2 * h) - (gp(x0 - h) - gp(x0 - 3 * h)) / (2 * h)
print("p61 derivative jump near x0 (should be about 1):", jump)

bad = [row for row in ok if not row[1]]
for name, good, a, b in ok:
    print(("OK  " if good else "FAIL"), name, "->", a, "vs", b)
print("\n%d checks, %d failed" % (len(ok), len(bad)))
