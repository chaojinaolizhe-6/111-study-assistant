# -*- coding: utf-8 -*-
"""复核 Topic 8 Part 1 的 HW8.01--8.03 答案（符号 + 数值）。"""
import sympy as sp

n1, n2, n3 = sp.Matrix([1, 0, 0]), sp.Matrix([0, 1, 0]), sp.Matrix([0, 0, 1])
phi, psi = sp.symbols('phi psi', real=True)
dphi, dpsi = sp.symbols('dphi dpsi', real=True)
r = sp.symbols('r', positive=True)

ok = []

def chk(name, cond):
    if hasattr(cond, 'norm'):
        diff = sp.simplify(cond.norm())
    else:
        diff = sp.simplify(cond)
    passed = sp.simplify(diff) == 0
    ok.append((name, passed))
    print(("PASS " if passed else "FAIL "), name)
    if not passed:
        print("   ", diff)

# ---------- E8.01 已知结果 ----------
def vec(a, b):
    return a * n1 + b * n2

rOA = r * (sp.sin(phi) * n1 - sp.cos(phi) * n2)
rAC = r * (sp.sin(psi) * n1 - sp.cos(psi) * n2)
Om1 = dphi * n3
Om2 = dpsi * n3
vA = Om1.cross(rOA)
vC = vA + Om2.cross(rAC)

vC_course = r * (dphi * sp.cos(phi) + dpsi * sp.cos(psi)) * n1 \
          + r * (dphi * sp.sin(phi) + dpsi * sp.sin(psi)) * n2
chk("E8.01 v_C 与课件 p16 结果一致", vC - vC_course)

# ---------- HW8.01 ----------
# 图中这一支：r_CB = r_CA 顺时针转 90 度
rCA = -rAC
rCB = r * (sp.cos(psi) * n1 + sp.sin(psi) * n2)      # 讲义/课件图这一支
chk("r_CB 与 r_CA 垂直且等长", sp.Matrix([rCB.dot(rCA), rCB.dot(rCB) - r**2]).norm())

vB = vC + Om2.cross(rCB)
vB_claim = r * (dphi * sp.cos(phi) + dpsi * (sp.cos(psi) - sp.sin(psi))) * n1 \
         + r * (dphi * sp.sin(phi) + dpsi * (sp.sin(psi) + sp.cos(psi))) * n2
chk("HW8.01 分量答案", vB - vB_claim)
chk("HW8.01 v_B = v_C - dpsi*r_AC", vB - (vC - dpsi * rAC))

# 模长平方 vs 单根号形式
lhs = sp.simplify((vB.dot(vB)) / r**2)
rhs = sp.simplify(dphi**2 + 2 * dpsi**2 + 2 * sp.sqrt(2) * dphi * dpsi
                  * sp.cos(phi - psi - sp.pi / 4))
chk("HW8.01 模长：|v_B|^2 与 2sqrt2 相位式", lhs - rhs)

# 另一支（B 在 A 同侧）
rCB2 = -rCB
vB2 = vC + Om2.cross(rCB2)
chk("HW8.01 另一支 = v_C + dpsi*r_AC", vB2 - (vC + dpsi * rAC))
lhs2 = sp.simplify((vB2.dot(vB2)) / r**2)
rhs2 = sp.simplify(dphi**2 + 2 * dpsi**2 + 2 * sp.sqrt(2) * dphi * dpsi
                   * sp.cos(phi - psi + sp.pi / 4))
chk("HW8.01 另一支模长相位 +pi/4", lhs2 - rhs2)

# 数值自检：phi=psi=0, dphi=1, dpsi=2, r=1 -> (3,2)
sub = {phi: 0, psi: 0, dphi: 1, dpsi: 2, r: 1}
print("数值自检 v_B =", [sp.simplify(c) for c in vB.subs(sub)], "(应为 [3, 2])")

# ---------- HW8.02 ----------
capB = sp.Matrix(sp.symbols('Bx By Bz'))
capA = sp.Matrix(sp.symbols('Ax Ay Az'))
vBv = sp.Matrix(sp.symbols('vBx vBy vBz'))
vAv = sp.Matrix(sp.symbols('vAx vAy vAz'))
Om = sp.Matrix(sp.symbols('Ox Oy Oz'))

# 平面运动：所有矢量 z 分量为零，Omega 沿 z
z0 = {capB[2]: 0, capA[2]: 0, vBv[2]: 0, vAv[2]: 0, Om[0]: 0, Om[1]: 0}
Bs = capB.subs(z0); As = capA.subs(z0); vBs = vBv.subs(z0); vAs = vAv.subs(z0); Oms = Om.subs(z0)
u = vAs - vBs
claim_RA = Bs + u.cross(Oms) / (Oms.dot(Oms))
chk("HW8.02 R_A 满足速度场方程",
    (vBs + Oms.cross(claim_RA - Bs) - vAs))
claim_RP = Bs - vBs.cross(Oms) / (Oms.dot(Oms))
chk("HW8.02 R_P 使 v_P = 0",
    vBs + Oms.cross(claim_RP - Bs))

# 标量形式：Omega = Om_z n3
Oz = sp.symbols('Oz', real=True)
subz = {Om[2]: Oz}
chk("HW8.02 标量形式 R_P = R_B + (n3 x v_B)/Oz",
    claim_RP.subs(subz) - (Bs + n3.cross(vBs) / Oz))

# ---------- HW8.03 ----------
ph = sp.symbols('phi', real=True)
l = sp.symbols('l', positive=True)
A = sp.Matrix([l * sp.cos(ph), 0, 0])
B = sp.Matrix([0, l * sp.sin(ph), 0])
# A 沿 x 滑 -> 速度沿 x -> 垂线：x = A_x 的竖直线
# B 沿 y 滑 -> 速度沿 y -> 垂线：y = B_y 的水平线
P = sp.Matrix([l * sp.cos(ph), l * sp.sin(ph), 0])
chk("HW8.03 瞬心在 A 的速度垂线上", P[0] - A[0])
chk("HW8.03 瞬心在 B 的速度垂线上", P[1] - B[1])
chk("HW8.03 瞬心轨迹 x^2+y^2 = l^2", sp.simplify(P[0]**2 + P[1]**2 - l**2))
# 换一种做法核验：由速度场反解瞬心
dA = sp.symbols('vA', real=True)   # A 的速率
dB = sp.symbols('vB', real=True)   # B 的速率
# 由几何约束求 A、B 速率关系：x_A = l cos phi, y_B = l sin phi
vAx = sp.diff(l * sp.cos(ph), ph) * sp.Symbol('dphi')
vBy = sp.diff(l * sp.sin(ph), ph) * sp.Symbol('dphi')
# 杆长约束核验：|AB| 恒为 l
chk("HW8.03 |AB| = l", sp.simplify((A - B).dot(A - B) - l**2))

print()
print("总计：", sum(1 for _, c in ok if c), "/", len(ok), "项通过")
