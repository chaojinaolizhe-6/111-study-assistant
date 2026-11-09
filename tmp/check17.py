import numpy as np
from scipy.special import fresnel
from scipy.integrate import quad
import math

alpha = 1.0
# (i) k=0 的锚点：∫_{-∞}^{∞} e^{iαx²}dx = sqrt(pi/α) e^{iπ/4}
#     用 Fresnel 积分 C(∞)=S(∞)=1/2: ∫_0^∞ cos(αx²)dx = (1/2)sqrt(pi/(2α))
h = (1/2)*math.sqrt(math.pi/(2*alpha))
print("Fresnel 半积分 C,S =", h, h)
print("→ F+(0) 实部 =", 2*h, " 虚部 =", 2*h)
print("→ 声称值     =", math.sqrt(math.pi/alpha)*math.cos(math.pi/4), math.sqrt(math.pi/alpha)*math.sin(math.pi/4))

# 用 scipy.special.fresnel 直接算
for X in [50, 200, 2000]:
    S, C = fresnel(math.sqrt(2*alpha/math.pi)*X)
    print(f"  X={X}: ∫0^X cos = {math.sqrt(math.pi/(2*alpha))*C:.12f}, ∫0^X sin = {math.sqrt(math.pi/(2*alpha))*S:.12f}")

# (ii) 直接数值积分（有限区间，看趋势）：∫_{-∞}^{∞} cos(αx²)cos(kx) dx, α=1,k=1
k = 1.0
fs = lambda x: math.cos(alpha*x*x)*math.cos(k*x)*math.exp(-1e-4*x*x)
for L in [200, 600]:
    v,_ = quad(fs, 0, L, limit=20000, epsabs=1e-10, epsmax=1e-10) if False else quad(fs, 0, L, limit=20000)
    print(f"L={L}: 半积分 ≈ {v:.5f}")
claim = math.sqrt(math.pi/alpha)*math.cos(k*k/(4*alpha) - math.pi/4)
print("声称 半积分 = ", claim/2, " 全积分 =", claim)
