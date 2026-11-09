import math
from scipy.integrate import quad
import numpy as np

def check(alpha, k, kind):
    # 用 e^{-eps x^2} 收敛因子做直接数值积分，eps 很小
    eps = 1e-4
    if kind == "cos":
        f = lambda x: math.cos(alpha*x*x)*math.cos(k*x)*math.exp(-eps*x*x)
    else:
        f = lambda x: math.sin(alpha*x*x)*math.cos(k*x)*math.exp(-eps*x*x)
    half,_ = quad(f, 0, 700, limit=40000)
    full = 2*half
    phi = math.pi/4 - k*k/(4*alpha)
    if kind == "cos":
        claim = math.sqrt(math.pi/alpha)*math.cos(phi)
    else:
        claim = math.sqrt(math.pi/alpha)*math.sin(phi)
    print(f"alpha={alpha} k={k} {kind}: 数值全积分={full:.6f}  解析={claim:.6f}  差={full-claim:+.2e}")

check(1.0, 1.0, "cos"); check(1.0, 1.0, "sin")
check(2.0, 3.0, "cos"); check(2.0, 3.0, "sin")
check(0.5, 2.5, "sin")

# 相位一致性：cos 支与 sin 支的模平方和为 1/(4 pi alpha)
for a in [0.5,1.0,2.0]:
    print(f"alpha={a}: |F_cos|^2+|F_sin|^2 = {1/(4*math.pi*a):.8f}")
