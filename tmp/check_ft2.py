import numpy as np
from scipy.integrate import quad
import math
lam, k = 2.0, 3.0
pref = 1/(2*math.pi)**3
# 二维自适应求积：直接在 (r,theta) 上积原始被积函数，不预先化简成 sin(kr)/(kr)
def inner(r):
    f = lambda th: math.sin(th)*math.cos(k*r*math.cos(th))
    val,_ = quad(f, 0, math.pi, limit=200)
    return r*math.exp(-r/lam)*val      # r^2 * (1/r) * ...
I,_ = quad(inner, 0, np.inf, limit=400)
F_num = pref*2*math.pi*I
F_exact = lam**2/(2*math.pi**2*(1+k**2*lam**2))
print("2D quad F(k) =", F_num)
print("closed form   =", F_exact)
print("rel.err       =", abs(F_num-F_exact)/F_exact)
# 再核 k->0 极限：F(0) 应等于 lambda^2/(2 pi^2)
def inner0(r):
    return r*math.exp(-r/lam)*2.0
I0,_ = quad(inner0, 0, np.inf)
print("F(0) quad =", pref*2*math.pi*I0, " closed =", lam**2/(2*math.pi**2))
