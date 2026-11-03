import sympy as sp

def report(name, A):
    A = sp.Matrix(A)
    tau, det = A.trace(), A.det()
    disc = sp.factor(tau**2 - 4*det)
    print('='*12, name)
    print('  tau =', tau, ' Delta =', det, ' disc =', disc)
    print('  eigen:', A.eigenvals())
    for val, mult, vecs in A.eigenvects():
        print('    lam =', val, ' mult', mult, ' vecs', [list(v) for v in vecs])
    return tau, det

report('1) A=[[3,2],[1,4]]', [[3,2],[1,4]])
report('2) A=[[-1,0],[0,-1]]', [[-1,0],[0,-1]])
report('3) A=[[-1,2],[-2,-1]]', [[-1,2],[-2,-1]])

# Problem 2 Jacobian at origin
x1, x2 = sp.symbols('x1 x2')
P = x1 - x1**2 - x1*x2
Q = sp.Rational(1,2)*x2 - sp.Rational(3,4)*x1*x2 - sp.Rational(1,4)*x2**2
J = sp.Matrix([[sp.diff(P,x1), sp.diff(P,x2)],[sp.diff(Q,x1), sp.diff(Q,x2)]])
print('\n' + '='*12, 'Q2 Jacobian (symbolic)')
sp.pprint(J)
print(' at (0,0):', J.subs({x1:0,x2:0}), ' eigen', J.subs({x1:0,x2:0}).eigenvals())

print('\n critical points of Q2 system:')
sol = sp.solve([P, Q], [x1, x2], dict=True)
print('  ', sol)
for s in sol:
    pt = (sp.nsimplify(s[x1]), sp.nsimplify(s[x2]))
    Jp = J.subs({x1: pt[0], x2: pt[1]})
    print('   at', pt, 'J =', Jp.tolist(), 'tau', Jp.trace(), 'det', Jp.det(), 'eig', Jp.eigenvals())

# alternative reading of problem 2: last term linear 0.25*x2
Qalt = sp.Rational(1,2)*x2 - sp.Rational(3,4)*x1*x2 - sp.Rational(1,4)*x2
Jalt = sp.Matrix([[sp.diff(P,x1), sp.diff(P,x2)],[sp.diff(Qalt,x1), sp.diff(Qalt,x2)]])
print('\n alternative reading (0.25*x2 linear): J(0) =', Jalt.subs({x1:0,x2:0}).tolist(), 'eig', Jalt.subs({x1:0,x2:0}).eigenvals())

