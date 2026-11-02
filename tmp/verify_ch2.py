# -*- coding: utf-8 -*-
import mpmath as mp
mp.mp.dps = 25
I = 1j
def cquad(f, zfun, a, b):
    """complex line integral: int f(z) z'(t) dt over t in [a,b]"""
    g = lambda t: f(zfun(t)) * mp.diff(zfun, t)
    return mp.quad(g, [a, b])

def circ(f, c, r, th0=0.0, th1=2*mp.pi):
    z = lambda t: c + r*mp.e**(I*t)
    return cquad(f, z, th0, th1)

def show(name, val, expect=None):
    v = mp.chop(mp.nsimplify(mp.nstr(val, 15)) if False else val, 1e-15)
    s = mp.nstr(v, 12)
    e = "" if expect is None else "   expect=" + str(expect)
    print(f"{name:<52} {s}{e}")

print("== A homework 1: int |z| dz from -i to i ==")
show("straight segment  -i -> i", cquad(abs, lambda t: I*t, -1, 1), "i")
show("right half unit circle",    cquad(abs, lambda t: mp.e**(I*t), -mp.pi/2, mp.pi/2), "2i")

print("== B homework 2 ==")
show("oint dz/z", circ(lambda z: 1/z, 0, 1), "2 pi i")
show("oint dz/|z|", circ(lambda z: 1/abs(z), 0, 1), "0")
show("oint |dz|/|z|", mp.quad(lambda t: abs(mp.diff(lambda s: mp.e**(I*s), t))/1, [0, 2*mp.pi]), "2 pi")

print("== C/D/E/F homework 3,4 ==")
show("oint_{|z|=2} (2z^2-z+1)/(z-1)", circ(lambda z: (2*z**2-z+1)/(z-1), 0, 2), "4 pi i")
show("oint e^z/(z^2+1)", circ(lambda z: mp.e**z/(z**2+1), 0, 2), "2 pi i sin 1")
show("oint (2z^2-z+1)/(z-1)^2", circ(lambda z: (2*z**2-z+1)/(z-1)**2, 0, 2), "6 pi i")
show("oint cos(pi z)/(z-1)^3", circ(lambda z: mp.cos(mp.pi*z)/(z-1)**3, 0, 2), "pi^3 i")

print("== G homework 5 ==")
show("int_0^{2pi} (1+2cos)/(5+4cos) dtheta",
     mp.quad(lambda t: (1+2*mp.cos(t))/(5+4*mp.cos(t)), [0, 2*mp.pi]), "0")

print("== H homework 6 ==")
show("oint_{|z|=1} e^z/z dz", circ(lambda z: mp.e**z/z, 0, 1), "2 pi i")
show("int_0^pi e^{cos} cos(sin)", mp.quad(lambda t: mp.e**mp.cos(t)*mp.cos(mp.sin(t)), [0, mp.pi]), "pi")

print("== I example 1 p8: Im z dz ==")
show("c1 (0,0)->(1,0)->(1,1)", cquad(lambda z: z.imag, lambda t: t, 0,1) + cquad(lambda z: z.imag, lambda t: 1+I*t, 0,1), "i/2")
show("c2 (0,0)->(0,1)->(1,1)", cquad(lambda z: z.imag, lambda t: I*t, 0,1) + cquad(lambda z: z.imag, lambda t: t+I, 0,1), "i/2+1")
show("c3 (0,0)->(1,1) diagonal", cquad(lambda z: z.imag, lambda t: (1+I)*t, 0,1), "(1+i)/2")

print("== J example 2 p10: (x-y+i x^2) dz ==")
f2 = lambda z: z.real - z.imag + I*z.real**2
show("c1 y=x^2", cquad(f2, lambda t: t+I*t**2, 0, 1), "-1/3 + i/2")
show("c2 y=x",   cquad(f2, lambda t: (1+I)*t, 0, 1), "-1/3 + i/3")

print("== K example 3 p13: (2xy - i(x^2-y^2)) dz ==")
f3 = lambda z: 2*z.real*z.imag - I*(z.real**2 - z.imag**2)
show("c1", cquad(f3, lambda t: t, 0,1) + cquad(f3, lambda t: 1+I*t, 0,1), "2/3(1+i)")
show("c2", cquad(f3, lambda t: I*t, 0,1) + cquad(f3, lambda t: t+I, 0,1), "2/3(1+i)")
show("c3", cquad(f3, lambda t: (1+I)*t, 0,1), "2/3(1+i)")
print("   f3 vs -i z^2 :", mp.nstr(f3(0.3+0.4j) - (-I*(0.3+0.4j)**2), 5))

print("== L p24 example 1 ==")
show("int_{-i}^{i} z^2 dz", cquad(lambda z: z**2, lambda t: I*t, -1, 1), "-2i/3")
show("int_0^i z sin z dz", cquad(lambda z: z*mp.sin(z), lambda t: I*t, 0, 1), "sin i - i cos i")
print("   sin i - i cos i =", mp.nstr(mp.sin(I) - I*mp.cos(I), 12), " -i/e =", mp.nstr(-I/mp.e, 12))

print("== M p24 example 2 ==")
show("int_2^0 (e^x+sin x+2x)dx", mp.quad(lambda x: mp.e**x + mp.sin(x) + 2*x, [2, 0]), "cos2-e^2-4")
print("   cos2-e^2-4 =", mp.nstr(mp.cos(2)-mp.e**2-4, 12))

print("== N p29 ==")
show("oint_{|z|=2} dz/(z^2-1)", circ(lambda z: 1/(z**2-1), 0, 2), "0")

print("== O p39 example 1 ==")
a = mp.mpc(0.7, -0.4)
show("oint e^{az}/(z^2-1) |z|=2", circ(lambda z: mp.e**(a*z)/(z**2-1), 0, 2), "pi i (e^a - e^-a)")
print("   pi i (e^a - e^-a) =", mp.nstr(mp.pi*I*(mp.e**a - mp.e**(-a)), 12))

print("== P p40 example 2 ==")
show("oint_{|z|=2} e^z/(z+i pi/2)", circ(lambda z: mp.e**z/(z+I*mp.pi/2), 0, 2), "2 pi")

print("== Q p41 example 3 ==")
show("oint_{|z|=r>1} sin z/(z^2+1) r=3", circ(lambda z: mp.sin(z)/(z**2+1), 0, 3), "2 pi sin i")
print("   2 pi sin i =", mp.nstr(2*mp.pi*mp.sin(I), 12), " 2 pi i sinh 1 =", mp.nstr(2*mp.pi*I*mp.sinh(1), 12))

print("== R p42 examples 4,5 ==")
al = mp.mpc(0.5, 0.3)
show("oint e^{a z}/(z-1)^2 |z|=2", circ(lambda z: mp.e**(al*z)/(z-1)**2, 0, 2), "2 pi i a e^a")
print("   2 pi i a e^a =", mp.nstr(2*mp.pi*I*al*mp.e**al, 12))
show("oint cos z/(z-i)^3 |z|=2", circ(lambda z: mp.cos(z)/(z-I)**3, 0, 2), "-pi i cos i")
print("   -pi i cos i =", mp.nstr(-mp.pi*I*mp.cos(I), 12))

print("== S p19 exercise ==")
show("oint_{|z-2|=1} z^2/(z-2)^3 dz", circ(lambda z: z**2/(z-2)**3, 2, 1), "2 pi i")
show("oint_{|z-1|=1} z/(z-1) dz", circ(lambda z: z/(z-1), 1, 1), "2 pi i")

print("== T Poisson kernel checks ==")
a0, r0, phi = mp.mpf(2), mp.mpf('0.7'), mp.mpf('0.9')
K = lambda th: (a0**2-r0**2)/(a0**2+r0**2-2*a0*r0*mp.cos(phi-th))
show("(1/2pi) int K = 1", mp.quad(K,[0,2*mp.pi])/(2*mp.pi), "1")
show("(1/2pi) int a e^{i th} K = r e^{i phi}",
     mp.quad(lambda th: a0*mp.e**(I*th)*K(th), [0,2*mp.pi])/(2*mp.pi), "r e^{i phi} = "+mp.nstr(r0*mp.e**(I*phi),8))
F = lambda m: mp.quad(lambda th: mp.e**(I*m*th), [0,2*mp.pi])/(2*mp.pi)
print("   series check, first coeffs (should be 0 except m=0 ->1):", [mp.nstr(F(m),4) for m in range(3)])
