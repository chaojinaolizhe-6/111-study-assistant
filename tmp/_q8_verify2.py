import numpy as np
from scipy.integrate import quad

b = 2.0
print("=== 1) transform of 1/(x^2+b^2), both signs of k ===")
for kk in (1.0, -1.0, 3.0, -3.0):
    val = (1 / (2 * np.pi)) * quad(lambda x: np.cos(kk * x) / (x ** 2 + b ** 2),
                                   -np.inf, np.inf, limit=500)[0]
    print(f"  k={kk:+}: F={val:.10f}   e^(-|k|b)/(2b)={np.exp(-abs(kk) * b) / (2 * b):.10f}")

a = 1.0
c = b - a
print("=== 2) inverse transform of F1 = (a/(2 pi b)) e^{-|k|(b-a)} ===")
for x0 in (0.0, 1.0, 2.0):
    val = quad(lambda k: (a / (2 * np.pi * b)) * np.exp(-abs(k) * c) * np.cos(k * x0),
               -np.inf, np.inf, limit=500)[0]
    tgt = a * c / (np.pi * b) / (x0 ** 2 + c ** 2)
    print(f"  x={x0}: {val:.10f}  vs  a(b-a)/(pi b)/(x^2+(b-a)^2) = {tgt:.10f}")

print("=== 3) mass check: |int f dx| = a/b < 1 ===")
mass = quad(lambda x: (a * c / (np.pi * b)) / (x ** 2 + c ** 2), -np.inf, np.inf)[0]
print(f"  int f dx = {mass:.10f}   a/b = {a / b:.10f}")

print("=== 4) boundary case b->a : f should degenerate ===")
for eps in (1e-1, 1e-2, 1e-3):
    bb = a + eps
    cc = bb - a
    peak = a * cc / (np.pi * bb) / (0.0 ** 2 + cc ** 2)
    print(f"  b-a={cc:g}: f(0)={peak:.6f}, mass={quad(lambda x: (a*cc/(np.pi*bb))/(x**2+cc**2), -np.inf, np.inf)[0]:.6f}")
