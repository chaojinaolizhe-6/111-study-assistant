# -*- coding: utf-8 -*-
"""验算 A 卷 8 道题的全部答案。"""
import sympy as sp

t = sp.symbols('t', real=True)
print("=" * 60)

# ---------- S1 梯子 + 摩擦 ----------
L, W, th, mu = sp.symbols('L W theta mu', positive=True)
# A 在地面 (0,0)，梯子沿与水平成 theta；B 靠墙
# 力矩关于 A: W*(L/2)*cos(th) = N_w * L*sin(th)  -> N_w
Nw = W * sp.Rational(1, 2) / sp.tan(th)
# 平衡: N_g = W, f = N_w <= mu*N_g  -> mu >= Nw/W
mu_min = sp.simplify(Nw / W)
print("[S1] mu_min =", mu_min, "=", sp.simplify(1/(2*sp.tan(th))),
      "| 数值 theta=60:", float(mu_min.subs(th, sp.pi/3)))
print("     力学一致性: 取 theta=90 直立 mu_min->0 :", sp.limit(mu_min, th, sp.pi/2))

# ---------- S2 桁架 ----------
# A(0,0) 铰, B(4,0) 滚, C(2,3), 载荷 P 向下
P = sp.symbols('P', positive=True)
AC = sp.sqrt(13); # 长度
# 支座反力: 对称 R_Ay = R_By = P/2, R_Ax = 0
# 节点 C: 两杆沿 C->A, C->B
uCA = sp.Matrix([-2, -3]) / AC
uCB = sp.Matrix([2, -3]) / AC
SAC, SBC = sp.symbols('SAC SBC')
eqC = sp.Eq(uCA*SAC + uCB*SBC + sp.Matrix([0, -P]), sp.Matrix([0, 0]))
solC = sp.solve(eqC, [SAC, SBC], dict=True)[0]
print("[S2] 节点C 解:", {str(k): sp.simplify(v) for k, v in solC.items()},
      "| P*sqrt13/6 =", sp.nsimplify(sp.sqrt(13)/6*P))
# 节点 A: 力 = 杆 AC 对节点反作用 (-SAC*uCA) + 支座 (0,P/2) + 杆 AB
SAB = sp.symbols('SAB')
eqA = sp.Eq(-solC[SAC]*uCA*AC/AC + sp.Matrix([0, P/2]) + sp.Matrix([SAB, 0]), sp.Matrix([0, 0]))
solA = sp.solve(eqA, [SAB], dict=True)[0]
print("[S2] AB 杆:", sp.simplify(solA[SAB]), "  (P/3 ?)", sp.simplify(solA[SAB] - P/3) == 0)
# 整体校核: 竖向 2*(P/2)=P OK

# ---------- K1 旋转管 + 科氏 ----------
r, u, om = sp.symbols('r u omega', positive=True)
v_vec = sp.Matrix([u, om*r])          # (径向, 横向)
a_vec = sp.Matrix([-om**2*r, 2*om*u]) # r'' - r th'^2 ; 2 r' th'
vmag = sp.sqrt(v_vec.dot(v_vec))
amag = sp.sqrt(a_vec.dot(a_vec))
cross = v_vec[0]*a_vec[1] - v_vec[1]*a_vec[0]
rho = sp.simplify(vmag**3 / cross)
print("[K1] |v| =", vmag, " |a| =", amag)
print("[K1] rho =", rho, " 简化:", sp.simplify(rho - (u**2+om**2*r**2)**sp.Rational(3,2)/(om*(2*u**2+om**2*r**2))))
# 数值: r=0.5,u=1,om=2
sub = {r: sp.Rational(1,2), u: 1, om: 2}
print("[K1] 数值 |v|=", float(vmag.subs(sub)), " |a|=", float(amag.subs(sub)),
      " rho=", float(rho.subs(sub)))
# 极坐标独立核对
rr = sp.Function('rr')(t)
r0 = sp.symbols('r0', positive=True)
rfun = r0 + u*t
x = rfun*sp.cos(om*t); y = rfun*sp.sin(om*t)
ax = sp.diff(x, t, 2); ay = sp.diff(y, t, 2)
axr = sp.simplify((ax*sp.cos(om*t) + ay*sp.sin(om*t)).subs(t, 0))
atr = sp.simplify((-ax*sp.sin(om*t) + ay*sp.cos(om*t)).subs(t, 0))
print("[K1] 极坐标核对 a_r =", axr, "(应 -omega^2*r0) ; a_th =", atr, "(应 2*omega*u)")

# ---------- K2 杆在墙角滑动 ----------
th2, L2, vA = sp.symbols('theta L v_A', positive=True)
x = L2*sp.cos(th2); y = L2*sp.sin(th2)
thdot = -vA/(L2*sp.sin(th2))
ydot = sp.diff(y, th2)*thdot
# theta 的二阶导: ddot{x}=0
thddot = -sp.cos(th2)*thdot**2/sp.sin(th2)
acc_y = sp.diff(sp.diff(y, th2), th2)*thdot**2 + sp.diff(y, th2)*thddot
acc_y = sp.simplify(acc_y)
print("[K2] omega =", sp.simplify(-thdot), " | vB =", sp.simplify(-ydot),
      " | aB =", acc_y, " (应 -vA^2/(L sin^3))",
      sp.simplify(acc_y + vA**2/(L2*sp.sin(th2)**3)) == 0)
num2 = {L2: 1, vA: 2, th2: sp.pi/6}
print("[K2] 数值 omega=", float((-thdot).subs(num2)), " vB=", float((-ydot).subs(num2)),
      " aB=", float(acc_y.subs(num2)))

# ---------- D1 圆柱 + 细绳 ----------
M, m, R, g, aa, T = sp.symbols('M m R g a T', positive=True)
sol = sp.solve([sp.Eq(m*g - T, m*aa), sp.Eq(T*R, (M*R**2/2)*(aa/R))], [aa, T], dict=True)[0]
print("[D1] a =", sp.simplify(sol[aa]), " T =", sp.simplify(sol[T]))
print("[D1] a = 2mg/(2m+M)?", sp.simplify(sol[aa] - 2*m*g/(2*m+M)) == 0,
      " T = Mmg/(2m+M)?", sp.simplify(sol[T] - M*m*g/(2*m+M)) == 0)
Rx = sp.simplify(M*g + sol[T])
print("[D1] 轴反力 =", Rx, " = Mg(3m+M)/(2m+M)?", sp.simplify(Rx - M*g*(3*m+M)/(2*m+M)) == 0)
num = {M: 2, m: 1, g: sp.Rational(98,10), R: 1}
print("[D1] 数值 M=2,m=1,g=9.8: a=", float(sol[aa].subs(num)), " T=", float(sol[T].subs(num)),
      " R=", float(Rx.subs(num)))

# ---------- D2 珠子在旋转圆环 ----------
th3, R3, om3 = sp.symbols('theta R omega', positive=True)
Ueff = -m*g*R3*sp.cos(th3) - sp.Rational(1, 2)*m*om3**2*R3**2*sp.sin(th3)**2
d1 = sp.simplify(sp.diff(Ueff, th3))
d2 = sp.simplify(sp.diff(Ueff, th3, 2))
print("[D2] dU/dth =", d1, " -> roots:", sp.solve(sp.Eq(d1, 0), th3), "或 cos th = g/(om^2 R)")
print("[D2] d2U/dth2 =", d2)
crit0 = sp.simplify(d2.subs(th3, 0))
print("[D2] 在 th=0 处 d2U =", crit0, " (稳定当 <0, 即 om^2 R < g)")
thstar = sp.acos(g/(om3**2*R3))
critstar = sp.simplify(d2.subs(th3, thstar))
print("[D2] 在 th* 处 d2U =", sp.simplify(critstar))
num3 = {R3: 1, om3: 3, g: sp.Rational(98,10), m: 1}
print("[D2] 数值 R=1,om=3: th* =", float(thstar.subs(num3)), " d2U(th*)=", float(critstar.subs(num3)))

# ---------- D3 斜碰墙 ----------
v, e = sp.symbols('v e', positive=True)
vn = v*sp.cos(sp.pi/4); vt = v*sp.sin(sp.pi/4)
J = m*vn*(1+e)
K1_ = sp.Rational(1,2)*m*v**2
K2_ = sp.Rational(1,2)*m*(e**2*vn**2 + vt**2)
loss = sp.simplify((K1_-K2_)/K1_)
print("[D3] J =", sp.simplify(J), " = m v (1+e)/sqrt2 ?", sp.simplify(J - m*v*(1+e)/sp.sqrt(2)) == 0)
print("[D3] 动能相对损失 =", loss, " = (1-e^2)/2 ?", sp.simplify(loss - (1-e**2)/2) == 0)
print("[D3] 数值 m=1,v=10,e=0.5: J=", float(sp.simplify(J).subs({m:1,v:10,e:sp.Rational(1,2)})),
      " loss=0.375?", float(loss.subs({e: sp.Rational(1,2)})))

# ---------- D4 有心力 -k/r ----------
k, Lm, E = sp.symbols('k L E', positive=True)
rr4 = sp.symbols('r', positive=True)
f = sp.Eq(-k/rr4 + Lm**2/(2*m*rr4**2), E)
roots = sp.solve(f, rr4)
print("[D4] 二次方程根:", [sp.simplify(x) for x in roots])
disc = sp.simplify(k**2 + 2*E*Lm**2/m)
print("[D4] 判别式 =", disc, " (>0 即允许两个转向点)")
# 圆轨道: 判别式为 0
Ecirc = sp.solve(sp.Eq(disc, 0), E)[0]
rcirc = sp.simplify(k/(2*sp.Abs(Ecirc)).subs({}))
rcirc = sp.simplify(k/(2*(-Ecirc)))
print("[D4] 圆轨道 E =", Ecirc, " r =", rcirc, " = L^2/(m k)?",
      sp.simplify(rcirc - Lm**2/(m*k)) == 0)
num4 = {k: 1, Lm: 1, m: 1, E: -sp.Rational(3,8)}
print("[D4] 数值 k=L=m=1, E=-3/8: r_min=", float(min([x.subs(num4) for x in roots])),
      " r_max=", float(max([x.subs(num4) for x in roots])),
      " sqrt(k^2+2EL^2/m)=", float(sp.sqrt(disc).subs(num4)))
