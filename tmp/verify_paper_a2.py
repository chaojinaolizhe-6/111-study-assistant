import sympy as sp
m,v,e=sp.symbols("m v e", positive=True)
vn=v*sp.cos(sp.pi/4); vt=v*sp.sin(sp.pi/4)
J=m*vn*(1+e); print("[D3] J =", sp.simplify(J), "| (1+e)m v/sqrt2 ?", sp.simplify(J-m*v*(1+e)/sp.sqrt(2))==0)
K1_=sp.Rational(1,2)*m*v**2; K2_=sp.Rational(1,2)*m*(e**2*vn**2+vt**2)
loss=sp.simplify((K1_-K2_)/K1_); print("[D3] loss =", loss, "| (1-e^2)/2 ?", sp.simplify(loss-(1-e**2)/2)==0)
print("[D3] 数值 m=1,v=10,e=0.5: J=", float(J.subs({m:1,v:10,e:sp.Rational(1,2)})), " loss=", float(loss.subs({e:sp.Rational(1,2)})))
k,L,E=sp.symbols("k L E", positive=True); r=sp.symbols("r", positive=True)
f=sp.Eq(-k/r+L**2/(2*m*r**2), E); roots=sp.solve(f,r)
print("[D4] roots:", [sp.simplify(x) for x in roots])
disc=sp.simplify(k**2+2*E*L**2/m); Ecirc=sp.solve(sp.Eq(disc,0),E)[0]
rcirc=sp.simplify(k/(2*(-Ecirc))); print("[D4] disc:",disc," E_circ:",Ecirc," r_circ:",rcirc," =L^2/(mk)?", sp.simplify(rcirc-L**2/(m*k))==0)
num={k:1,L:1,m:1,E:-sp.Rational(3,8)}
print("[D4] 数值 k=L=m=1,E=-3/8: r_min=",float(min([x.subs(num) for x in roots]))," r_max=",float(max([x.subs(num) for x in roots]))," sqrt=",float(sp.sqrt(disc).subs(num)))
