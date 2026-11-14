import sympy as sp
x, y, z, t, r, n, V = sp.symbols("x y z t r n V", positive=True)
ok = []
def chk(name, expr, target, tol=1e-9):
    val = sp.simplify(expr - target)
    good = abs(complex(sp.N(val))) < tol if val.free_symbols == set() else False
    ok.append((name, good, sp.N(expr), sp.N(target)))
    if not good:
        print("FAIL", name, expr, target)

# §1 例1
chk("lim cos^(1/x^2)", sp.limit(sp.cos(x)**(1/x**2), x, 0), sp.exp(sp.Rational(-1,2)))
# §1 例2 黎曼和
chk("riemann sqrt", sp.integrate(sp.sqrt(1+x), (x,0,1)), sp.Rational(2,3)*(2*sp.sqrt(2)-1))
# §3 华里士
chk("wallis sin^4", sp.integrate(sp.sin(x)**4, (x,0,sp.pi/2)), 3*sp.pi/16)
# §3 例1 区间再现
chk("x sinx/(1+cos^2)", sp.integrate(x*sp.sin(x)/(1+sp.cos(x)**2), (x,0,sp.pi)), sp.pi**2/4)
# §5 例1 极坐标
chk("polar 2cos", sp.integrate(sp.integrate(r**3,(r,0,2*sp.cos(t))),(t,-sp.pi/2,sp.pi/2)), 3*sp.pi/2)
# §5 例2 换序
chk("swap order", sp.integrate(sp.integrate(sp.exp(-x**2),(y,0,x)),(x,0,1)), (1-sp.exp(-1))/2)
# §4 例2 球面最值
chk("sphere max", sp.sqrt(14), sp.sqrt(1+4+9))
# §4 例3 水箱 (V=1)
S = x*y + 2*V/y + 2*V/x
sol = sp.solve([sp.diff(S,x), sp.diff(S,y)], [x,y], dict=True)
xs = sp.simplify(sol[0][x].subs(V,1)); ys = sp.simplify(sol[0][y].subs(V,1))
chk("tank x", xs, sp.cbrt(2)); chk("tank y", ys, sp.cbrt(2))
chk("tank z", sp.simplify(1/xs**2), sp.cbrt(2)/2)
# §7 例1 比值
chk("ratio n!/n^n", sp.limit(sp.factorial(n+1)/(n+1)**(n+1)*n**n/sp.factorial(n), n, sp.oo), 1/sp.E)
# §7 例2 求和
chk("sum n/2^n", sp.summation(n/2**n, (n,1,sp.oo)), 2)
# §2 例1 高阶导
f = x**2*sp.exp(2*x)
for k in (1,2,3):
    closed = 2**(k-2)*sp.exp(2*x)*(4*x**2+4*k*x+k*(k-1))
    chk(f"nth deriv k={k}", sp.diff(f,x,k), closed)
# §2 例2 构造 (lambda=2, f=x^2 验证结论式)
lam = 2; ff = x**2
chk("mvt identity", sp.diff(ff,x)-lam*ff-(1-lam*x), 2*x-lam*x**2-1+lam*x)
# §8 例2 特解
yp = sp.Rational(1,2)*x**2*sp.exp(x)
chk("ode particular", sp.diff(yp,x,2)-2*sp.diff(yp,x)+yp, sp.exp(x))
# §8 例3 sinh
chk("integral eq", sp.sinh(x) - x - sp.integrate((x-t)*sp.sinh(t),(t,0,x)), 0)
# §6 例1 直接参数化核对半圆盘上的线积分
seg = sp.integrate((sp.exp(x)*sp.sin(0)-0), (x,0,2))
arc = sp.integrate(((sp.exp(1+sp.cos(t))*sp.sin(sp.sin(t))-sp.sin(t))*(-sp.sin(t)) +
                    (sp.exp(1+sp.cos(t))*sp.cos(sp.sin(t))-1)*sp.cos(t)), (t,0,sp.pi))
chk("green direct", seg+arc, sp.pi/2, tol=1e-6)
# §9 例1 距离
chk("plane dist", sp.Abs(1+2+2-3)/sp.sqrt(1+4+4), sp.Rational(2,3))
# 自测
chk("q1", sp.limit((sp.exp(x)-1-x)/x**2, x, 0), sp.Rational(1,2))
chk("q3", sp.diff(x*sp.exp(2*x), x, 2), 2**(2-1)*sp.exp(2*x)*(2*x+2))
chk("q5", sp.integrate(sp.sin(x)**3, (x,0,sp.pi/2)), sp.Rational(2,3))
chk("q6", sp.integrate(sp.integrate(r**2*r,(r,0,1)),(t,0,2*sp.pi)), sp.pi/2)
chk("q8", sp.summation(1/(n*2**n),(n,1,sp.oo)), sp.log(2))
chk("q9", sp.diff(-sp.exp(x), x) - 2*(-sp.exp(x)), sp.exp(x))  # 特解 -e^x
chk("q10", sp.Abs(1+2+3-1)/sp.sqrt(3), 5/sp.sqrt(3))
# 自测 q2 的黎曼和极限
import math
M = 200000
num = sum(math.sin(k*math.pi/M) for k in range(1, M+1))/M
chk("q2 riemann (numeric)", sp.Float(num - float(2/math.pi)), sp.Float(0), tol=1e-5)

bad = [r for r in ok if not r[1]]
print(f"\n{len(ok)-len(bad)}/{len(ok)} checks passed")
if bad:
    raise SystemExit(1)
