import numpy as np, cmath
def show(name, c):
    r = np.roots(np.array(c, dtype=complex))
    print(name, '=>')
    for z in r:
        print('   %10.6f %+10.6fi  |z|=%.6f  arg=%.4f pi' % (z.real, z.imag, abs(z), cmath.phase(z)/np.pi))
show('z^4+4 (correct)', [1,0,0,0,4])
show('(z^2-2z+2)(z^2+2z+2)', [1,0,0,0,4])

# residue sums & contour integrals by direct numerical quadrature
def quad(f, R, N=20000, c=0):
    s = 0j
    for k in range(N):
        t0 = 2*np.pi*k/N; t1 = 2*np.pi*(k+1)/N
        tm = 0.5*(t0+t1)
        z = c + R*np.exp(1j*tm)
        dzdt = 1j*R*np.exp(1j*tm)
        s += f(z)*dzdt*(t1-t0)
    return s
print('int_{|z|=2} z/(z^4-1) =', quad(lambda z: z/(z**4-1), 2))
print('int_{|z-i|=1} z/(z^4-1) =', quad(lambda z: z/(z**4-1), 1, c=1j))
print('int_{|z|=3} 1/(z^3-3z+2) =', quad(lambda z: 1/(z**3-3*z+2), 3))
print('int_{|z|=2.5} 1/(z^4+4) =', quad(lambda z: 1/(z**4+4), 2.5))
print('int_{|z|=1.5} 1/(z^4-5z^2+4) =', quad(lambda z: 1/(z**4-5*z**2+4), 1.5))
print('int_{|z|=1.5} z/(z^4-5z^2+4) =', quad(lambda z: z/(z**4-5*z**2+4), 1.5))
print('int_{|z|=0.5} 1/(z^3-2z^2+z) =', quad(lambda z: 1/(z**3-2*z**2+z), 0.5))
print('int_{|z|=0.5} 1/(z^2*(z^2-1)) =', quad(lambda z: 1/(z**2*(z**2-1)), 0.5))
print('int_{|z|=1} 1/(z^4-16) =', quad(lambda z: 1/(z**4-16), 1))
print('res 1/(z^3-3z+2) at -2:', 1/(3*(-2)**2-3), ' at 1 (double):', -1/9)
