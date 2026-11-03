import numpy as np, cmath
# 校验 §9 例题 C 的四个留数
for z in [1+1j, 1-1j, -1+1j, -1-1j]:
    print('Res at %5.2f%+5.2fi = %8.4f%+8.4fi' % (z.real, z.imag, (1/(4*z**3)).real, (1/(4*z**3)).imag))
print('sum=', sum(1/(4*z**3) for z in [1+1j,1-1j,-1+1j,-1-1j]))
# 韦达：eps z^2 + 2 z + eps
for eps in [0.3, 0.5, 0.9]:
    r = np.roots([eps,2,eps]); print('eps=%.1f roots=' % eps, np.round(r,5), 'product=', np.prod(r))
# 二次共轭根模
print('z^2+2z+2 roots:', np.roots([1,2,2]), '|z|^2 =', 2/1)
# 单位根恒等式
w = cmath.exp(2j*cmath.pi/5); print('1+w+...+w^4 =', sum(w**k for k in range(5)))
