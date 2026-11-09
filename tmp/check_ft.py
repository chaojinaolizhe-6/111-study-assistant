import numpy as np
# 独立核验：笛卡尔三维蒙特卡洛，不含任何"球对称/角度积分"的假设
lam, k = 2.0, 3.0
R = 60.0
rng = np.random.default_rng(0)
N = 4_000_000
# 球内均匀采样
u = rng.normal(size=(N,3))
u /= np.linalg.norm(u,axis=1)[:,None]
rad = R*u_new if False else R*rng.random(N)**(1/3)
pts = u*rad[:,None]
r = rad
integrand = np.exp(-r/lam)/r*np.cos(k*pts[:,0])
V = 4/3*np.pi*R**3
F_mc = V*integrand.mean()/(2*np.pi)**3
F_exact = lam**2/(2*np.pi**2*(1+k**2*lam**2))
print("MC   F(k) =", F_mc)
print("Exact F(k) =", F_exact)
print("ratio      =", F_mc/F_exact)
