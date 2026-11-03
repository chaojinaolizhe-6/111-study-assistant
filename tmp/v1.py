import numpy as np, cmath
def roots(c):  # coefficients highest first
    return np.roots(np.array(c, dtype=complex))
def show(name, c):
    r = roots(c)
    print(name, '=>')
    for z in r:
        print('   %10.6f %+10.6fi  |z|=%.6f  arg=%.4f pi' % (z.real, z.imag, abs(z), cmath.phase(z)/np.pi))
def res_z4m1():
    for z in roots([1,0,0,0,-1]):
        print('  Res at', np.round(z,6), '=', 1/(4*z**2))
    print('  sum=', sum(1/(4*(z**2)) for z in roots([1,0,0,0,-1])))
show('z^4-1', [1,0,0,0,-1])
show('z^4+1', [1,0,0,0,1])
show('z^4+4', [1,0,0,4])
show('z^4+16', [1,0,0,0,16])
show('z^3-8', [1,0,0,-8])
show('z^3-3z+2', [1,0,-3,2])
show('(z^2+1)^2', [1,0,2,0,1])
show('z^5-(1+i)', [1,0,0,0,0,-(1+1j)])
show('z^4-5z^2+4', [1,0,-5,0,4])
res_z4m1()
