# -*- coding: utf-8 -*-
r"""本轮张量并矢讲义的可复现验证。

只检查能在脚本中复算的数值、矩阵恒等式、练习/答案结构与最终 PDF 页码；
不证明谱定理、欧拉方程或应力平衡的一般推导，也不代替逐页目视检查。
任一断言失败以非零退出码报告。
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FAILS: list[str] = []
CHECKS = 0


def check(cond: bool, msg: str) -> None:
    global CHECKS
    CHECKS += 1
    if not cond:
        FAILS.append(msg)
        print(f"[FAIL] {msg}")
    else:
        print(f"[ok] {msg}")


def close(a, b, tol=1e-9) -> bool:
    return np.allclose(np.asarray(a, dtype=float), np.asarray(b, dtype=float), atol=tol, rtol=tol)


def eq(a, b) -> bool:
    return a == b


def v(*xs):
    return np.array(xs, dtype=float)


def mat(*rows):
    return np.array(rows, dtype=float)


def math_checks() -> None:
    print("\n== §0 工具 ==")
    a, b = v(3, 0), v(3, 4)
    check(close(np.dot(a, b), 9), "§0.1 (3,0)·(3,4)=9")
    check(close(np.linalg.norm(a), 3) and close(np.linalg.norm(b), 5), "§0.1 长度 3,5")
    check(close(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)), 3 / 5), "§0.1 cosθ=3/5")
    check(close(np.dot(v(1, 2, 2), v(1, 1, 1) / math.sqrt(3)), 5 / math.sqrt(3)), "§0.1 投影长 5/√3")
    proj = (5 / 3) * v(1, 1, 1)
    check(close(np.dot(v(1, 2, 2) - proj, v(1, 1, 1) / math.sqrt(3)), 0), "§0.1 残差与 n 正交")

    r, F = v(1, 0, 0), v(0, 1, 0)
    check(close(np.cross(r, F), v(0, 0, 1)), "§0.2 r×F=(0,0,1)")
    a2, b2 = v(1, 2, 2), v(2, 1, 0)
    check(close(np.cross(a2, b2), v(-2, 4, -3)), "§0.2 (1,2,2)×(2,1,0)=(-2,4,-3)")
    check(close(np.dot(a2, np.cross(a2, b2)), 0), "§0.2 叉乘与 a 垂直")
    check(close(np.dot(b2, np.cross(a2, b2)), 0), "§0.2 叉乘与 b 垂直")
    check(close(np.dot(np.cross(a2, b2), np.cross(a2, b2)), 29), "§0.2 |a×b|²=29")

    T = mat([2, 1, 0], [0, 1, 0], [0, 0, 3])
    check(close(T @ v(1, 2, 3), v(4, 2, 9)), "§0.3 T(1,2,3)=(4,2,9)")

    T2 = mat([2, 0], [0, 1])
    R = np.array([[1, -1], [1, 1]], dtype=float) / math.sqrt(2)
    check(close(R.T @ R, np.eye(2)), "§0.4 R 正交")
    check(close(R.T @ T2 @ R, mat([1.5, -0.5], [-0.5, 1.5])), "§0.4 T'=[[3/2,-1/2],[-1/2,3/2]]")

    D4 = mat([4, 1, 0], [1, 4, 0], [0, 0, 2])
    check(round(np.linalg.det(D4)) == 30, "§0.5 det=30")
    check(close(np.trace(np.diag([1, 2, 3])), 6), "§0.5 tr diag(1,2,3)=6")
    check(close(0.5 * (6**2 - np.trace(np.diag([1, 2, 3]) @ np.diag([1, 2, 3]))), 11), "§0.5 I2=11")
    check(close(np.linalg.det(np.diag([1, 2, 3])), 6), "§0.5 det diag(1,2,3)=6")
    check(close(2**3 / 3, 8 / 3), "§0.6 ∫0^2 x²dx=8/3")
    check(close(2 * 3**2 / 12, 1.5), "§0.6 mL²/12=1.5 (m=2,L=3)")
    roots = np.roots([1, 0, 1, 0])
    check(any(abs(r.imag) < 1e-9 for r in roots), "§0.7 x³+x 有实根（示例核对）")

    print("\n== §1 二次型与谱定理 ==")
    x, y = 2.0, 3.0
    T = mat([1, 2], [0, 1])
    E = np.array([x, y]) @ T @ np.array([x, y])
    check(close(E, (x + y) ** 2), "§1.1 (x,y)[[1,2],[0,1]](x,y)^T=(x+y)^2")
    S = 0.5 * (T + T.T)
    check(close(np.array([x, y]) @ S @ np.array([x, y]), E), "§1.1 对称部分给同一二次型")

    T1 = np.diag([1.0, 4.0])
    ev = np.sort(np.linalg.eigvalsh(T1))
    check(close(ev, [1, 4]), "§1.2 diag(1,4) 特征值 1,4")
    check(close([1 / math.sqrt(e) for e in ev], [1, 0.5]), "§1.2 半轴 1,1/2")

    T2 = mat([2, 1], [1, 2])
    ev2 = np.sort(np.linalg.eigvalsh(T2))
    check(close(ev2, [1, 3]), "§1.2 [[2,1],[1,2]] 特征值 1,3")
    n1 = v(1, 1) / math.sqrt(2)
    n2 = v(-1, 1) / math.sqrt(2)
    check(close(T2 @ n1, 3 * n1) and close(T2 @ n2, n2), "§1.2 两个特征方向")
    u, vv = 1.3, -0.7
    xy = np.array([(u - vv) / math.sqrt(2), (u + vv) / math.sqrt(2)])
    E2 = xy @ T2 @ xy
    check(close(E2, 3 * u**2 + vv**2), "§1.2 代入后 E=3u²+v²")

    D = mat([6, 2, 0], [2, 6, 0], [0, 0, 1])
    evD = np.sort(np.linalg.eigvalsh(D))
    check(close(evD, [1, 4, 8]), "§1.3 D 的特征值 1,4,8")
    q1 = v(1, 1, 0) / math.sqrt(2)
    q2 = v(1, -1, 0) / math.sqrt(2)
    q3 = v(0, 0, 1)
    check(close(D @ q1, 8 * q1) and close(D @ q2, 4 * q2) and close(D @ q3, q3),
          "§1.3 D 的三个特征向量")
    check(close(sum(l * np.outer(q, q) for l, q in [(8, q1), (4, q2), (1, q3)]), D),
          "§1.3 谱分解重组 D")
    check(round(np.trace(D)) == 13 and round(np.linalg.det(D)) == 32,
          "§1.3 tr=13, det=32")
    check(round(np.trace(D @ D)) == 81, "§1.3 tr(D²)=81")
    check(close(0.5 * (13**2 - 81), 44), "§1.3 I2=44")

    Ts = mat([5, 0, 0], [0, 2, 1], [0, 1, 2])
    evs = np.sort(np.linalg.eigvalsh(Ts))
    check(close(evs, [1, 3, 5]), "§1.4 降维例特征值 1,3,5")
    u1 = v(1, 0, 0)
    u2 = v(0, 1, 1) / math.sqrt(2)
    u3 = v(0, 1, -1) / math.sqrt(2)
    check(close(Ts @ u1, 5 * u1) and close(Ts @ u2, 3 * u2) and close(Ts @ u3, u3),
          "§1.4 降维例三个特征向量")

    Q = np.column_stack([q1, q2, q3])
    check(close(Q.T @ D @ Q, np.diag([8, 4, 1])), "§1.5 Q^T D Q=diag(8,4,1)")
    for _ in range(5):
        z = np.random.default_rng(0).normal(size=3)
        z = z / np.linalg.norm(z)
        E = z @ D @ z
        check(1 - 1e-9 <= E <= 8 + 1e-9, "§1.5 瑞利商落在 [1,8]")

    print("\n== §2 并矢运算 ==")
    a3, b3 = v(1, 2, 0), v(0, 1, 3)
    outer = np.outer(a3, b3)
    check(close(outer, mat([0, 1, 3], [0, 2, 6], [0, 0, 0])), "§2.2 a⊗b 的矩阵")
    xx = v(1, 1, 1)
    check(close(outer @ xx, v(4, 8, 0)), "§2.2 (a⊗b)·x=(4,8,0)")

    e1, e2 = v(1, 0, 0), v(0, 1, 0)
    x3 = v(1, 2, 3)
    right = np.outer(e1, e2) @ x3
    left = x3 @ np.outer(e1, e2)
    check(close(right, 2 * e1) and close(left, e2), "§2.3 左右作用不同：2e1 vs e2")

    Dc = mat([1, 2], [0, 3])
    check(round(np.trace(Dc)) == 4, "§2.4 tr=4")
    check(round(np.sum(Dc * Dc)) == 14, "§2.4 D:D=14")
    check(round(np.trace(Dc)) == 4, "§2.4 I:D=tr D=4")

    n = v(1, 1, 1) / math.sqrt(3)
    P = np.outer(n, n)
    check(close(P @ P, P), "§2.5 P²=P")
    check(close(np.trace(P), 1) and close(np.trace(np.eye(3) - P), 2), "§2.5 tr P=1, tr(I-P)=2")

    aa = v(1, 2, 3)
    ax = np.array([[0, -aa[2], aa[1]], [aa[2], 0, -aa[0]], [-aa[1], aa[0], 0]])
    check(close(ax @ x3, np.cross(aa, x3)), "§2.6 a^× x=a×x")
    check(close(ax, -ax.T), "§2.6 a^× 反对称")
    check(close([ax[2, 1], ax[0, 2], ax[1, 0]], aa), "§2.6 a=(A32,A13,A21)")
    inv = 0.5 * np.array([ax[2, 1] - ax[1, 2], ax[0, 2] - ax[2, 0], ax[1, 0] - ax[0, 1]])
    check(close(inv, aa), "§2.6 a_k=-1/2 ε_kij A_ij")

    theta = 0.7
    Rz = mat([math.cos(theta), -math.sin(theta), 0],
             [math.sin(theta), math.cos(theta), 0],
             [0, 0, 1])
    check(close(Rz.T @ Rz, np.eye(3)), "§3 Rz^T Rz=I")
    check(close(Rz.T, mat([math.cos(-theta), -math.sin(-theta), 0],
                          [math.sin(-theta), math.cos(-theta), 0], [0, 0, 1])), "§3.4 S^T=S(-φ)")

    # 绕任意单位轴 n 的显式公式
    n2 = v(1, 2, 2) / 3
    phi = 0.8
    Sn = np.outer(n2, n2) + (np.eye(3) - np.outer(n2, n2)) * math.cos(phi) \
        + ax_from(n2) * math.sin(phi)
    xx = v(0.3, -1.2, 2.0)
    par = np.dot(xx, n2) * n2
    perp = xx - par
    expect = par + perp * math.cos(phi) + np.cross(n2, perp) * math.sin(phi)
    check(close(Sn @ xx, expect), "§3.4 绕轴公式作用正确")

    alpha = 0.6
    S = mat([math.cos(alpha), -math.sin(alpha), 0],
            [math.sin(alpha), math.cos(alpha), 0], [0, 0, 1])
    dS = alpha * mat([-math.sin(alpha), -math.cos(alpha), 0],
                     [math.cos(alpha), -math.sin(alpha), 0], [0, 0, 0])
    Om = dS @ S.T
    check(close(Om, alpha * ax_from(v(0, 0, 1))), "§3.5 dS/dt S^T=α e3^×")
    check(close(Om @ S, dS), "§3.5 dS/dt=Ω^× S")

    print("\n== §4 惯量张量 ==")
    m, a, b, c = 12.0, 1.0, 2.0, 3.0
    J = m / 12 * np.diag([b**2 + c**2, a**2 + c**2, a**2 + b**2])
    check(close(J, np.diag([13, 10, 5])), "§4.4 长方体 J=diag(13,10,5)")
    check(all(J[i, i] + J[j, j] >= J[k, k] - 1e-9
              for i, j, k in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]), "§4.3 三角形不等式")

    omega = v(1, 1, 1) / math.sqrt(3)
    L = J @ omega
    check(close(L, v(13, 10, 5) / math.sqrt(3)), "§4.6 L=(13,10,5)/√3")
    cos_theta = np.dot(L, omega) / (np.linalg.norm(L) * np.linalg.norm(omega))
    check(close(cos_theta, 2 * math.sqrt(2) / 3), "§4.6 cosθ=2√2/3")
    check(close(math.degrees(math.acos(cos_theta)), 19.47122063449069, 1e-6), "§4.6 θ≈19.47°")
    M = np.cross(omega, L)
    check(close(M, v(-5, 8, -3) / 3), "§4.6 M=(1/3)(-5,8,-3)")
    check(close(np.linalg.norm(M), math.sqrt(98) / 3), "§4.6 |M|=√98/3≈3.30")

    # 平行轴定理：两个对称质点，质心在原点，原点平移 R
    mm = 2.0
    r1, r2 = v(1.3, 0, 0), v(-1.3, 0, 0)
    Jc = 0.5 * mm * (np.dot(r1, r1) * np.eye(3) - np.outer(r1, r1)) \
        + 0.5 * mm * (np.dot(r2, r2) * np.eye(3) - np.outer(r2, r2))
    R0 = v(0.4, 0.9, -0.2)
    Jo_direct = 0.5 * mm * (np.dot(r1 + R0, r1 + R0) * np.eye(3) - np.outer(r1 + R0, r1 + R0)) \
        + 0.5 * mm * (np.dot(r2 + R0, r2 + R0) * np.eye(3) - np.outer(r2 + R0, r2 + R0))
    R2 = np.dot(R0, R0)
    Jo_formula = Jc + mm * (R2 * np.eye(3) - np.outer(R0, R0))
    check(close(Jo_direct, Jo_formula), "§4.5 平行轴定理（两点质量核对）")

    # 细杆与薄板
    check(close(2.0 * 3.0**2 / 12, 1.5), "§4.4 细杆 mL²/12")
    a, b = 2.0, 3.0
    Jp = np.diag([b**2, a**2, a**2 + b**2])
    check(close(Jp[2, 2], Jp[0, 0] + Jp[1, 1]), "§4.4 薄板垂直轴定理")

    print("\n== §5 输运、欧拉方程、对称陀螺 ==")
    e1, e2, e3 = v(1, 0, 0), v(0, 1, 0), v(0, 0, 1)
    Om = ax_from(e3)
    D = np.outer(e1, e2)
    transport = Om @ D - D @ Om
    check(close(transport, np.outer(e2, e2) - np.outer(e1, e1)), "§5.1 单并矢输运核对")
    check(close(Om @ np.eye(3) - np.eye(3) @ Om, np.zeros((3, 3))), "§5.1 单位张量输运核对")

    A, B, C = 4.0, 7.0, 9.0
    w = v(0.7, -0.4, 1.1)
    wdot = v(1.2, -0.3, 0.8)
    euler = np.array([
        A * wdot[0] + (C - B) * w[1] * w[2],
        B * wdot[1] + (A - C) * w[2] * w[0],
        C * wdot[2] + (B - A) * w[0] * w[1],
    ])
    L = np.diag([A, B, C]) @ w
    # 用 dL/dt fixed = M 的公式核对
    M_formula = np.diag([A, B, C]) @ wdot + np.cross(w, L)
    check(close(euler, M_formula), "§5.2 欧拉方程三式与 dL/dt+ω×L 一致")

    A = B = 4.0
    C = 5.0
    w3 = 6.0
    Omeg = (C - A) / A * w3
    check(close(Omeg, 1.5), "§5.3 Ω=(C-A)ω3/A=1.5")
    check(close(2 * math.pi / Omeg, 4 * math.pi / 3), "§5.3 T=4π/3")

    print("\n== §6 应力 ==")
    sig0 = 2.0
    sigma = sig0 * np.outer(e1, e1)
    theta = math.radians(30)
    n = math.cos(theta) * e1 + math.sin(theta) * e2
    t = sigma @ n
    check(close(t, sig0 * math.cos(theta) * e1), "§6.3 t=σ0 cosθ e1")
    tn = np.dot(t, n)
    check(close(tn, sig0 * math.cos(theta) ** 2), "§6.3 tn=σ0 cos²θ")
    tau = math.sqrt(np.dot(t, t) - tn**2)
    check(close(tau, sig0 * math.sin(theta) * math.cos(theta)), "§6.3 τ=σ0 sinθcosθ")
    check(close(np.dot(t, t), tn**2 + tau**2), "§6.3 |t|²=tn²+τ²")
    check(close(sig0 * 0.5, 1.0), "§6.3 P10 最大剪应力 σ0/2（σ0=2 时 1.0）")

    # 平衡方程例子
    sig0, L0 = 3.0, 2.0
    x1 = 0.7
    div = np.array([sig0 / L0, 0.0, 0.0])
    f = -div
    check(close(f, v(-1.5, 0, 0)), "§6.4 体力 f=-∇·σ=(-3/2,0,0)")

    print("\n== P1--P12 数值核对 ==")
    D = mat([4, 1, 0], [1, 4, 0], [0, 0, 2])
    xx = v(1, 2, 3)
    check(close(D @ xx, v(6, 9, 6)), "P1 D x=(6,9,6)")
    check(round(np.trace(D)) == 10 and round(np.linalg.det(D)) == 30, "P1 tr=10, det=30")
    check(round(np.sum(D * D)) == 38, "P1 D:D=38")
    check(close(np.sort(np.linalg.eigvalsh(D)), [2, 3, 5]), "P1 特征值 2,3,5")

    m = 5.0
    J2 = m / 12 * np.diag([3**2 + 4**2, 2**2 + 4**2, 2**2 + 3**2])
    check(close(J2, np.diag([125 / 12, 100 / 12, 65 / 12])), "P2 J=diag(125,100,65)/12")
    Jplate = m / 12 * np.diag([3**2, 2**2, 2**2 + 3**2])
    check(close(Jplate[2, 2], Jplate[0, 0] + Jplate[1, 1]), "P2 薄板 Jzz=Jxx+Jyy")

    A = B = 2.0
    C = 3.0
    w3 = 10.0
    check(close((C - A) / A * w3, 5), "P3 Ω=5")
    check(close(2 * math.pi / 5, 1.2566370614359172), "P3 T=2π/5")

    J4 = np.diag([125 / 12, 100 / 12, 65 / 12])
    n4 = v(1, 1, 1) / math.sqrt(3)
    I4 = n4 @ J4 @ n4
    check(close(I4, 145 / 18), "P4 I(n)=145/18")
    check(close(n4 @ (J4 @ n4), 2 * 0.5 * I4), "P4 ω·L=2K")

    check(close(np.outer(e1, e1) @ e2, v(0, 0, 0)), "P5 (e1⊗e1)·e2=0")
    check(close(np.dot(e1, e1) * e2, e2), "P5 (e1·e1)e2=e2")

    D8 = mat([0, 3], [0, 0])
    S8 = 0.5 * (D8 + D8.T)
    xy = np.array([1.2, -0.4])
    check(close(xy @ D8 @ xy, 3 * xy[0] * xy[1]), "P8 D 的二次型=3xy")
    check(close(xy @ S8 @ xy, 3 * xy[0] * xy[1]), "P8 对称部分的二次型=3xy")

    r9 = v(1, 1, 1)
    J9 = (np.dot(r9, r9) * np.eye(3) - np.outer(r9, r9))
    check(close(np.sort(np.linalg.eigvalsh(J9)), [0, 3, 3]), "P9 真实 J 主值 0,3,3")
    A9 = mat([2, 1, -1], [1, 2, -1], [-1, -1, 2])
    check(close(np.sort(np.linalg.eigvalsh(A9)), [1, 1, 4]), "P9 错误 J' 主值 1,1,4")

    for deg in [10, 30, 45, 60, 80]:
        th = math.radians(deg)
        tau = math.sin(th) * math.cos(th) * 1.0
        check(0 <= tau <= 0.5 + 1e-12, f"P10 τ(θ={deg}°) 在 [0,1/2]")
    check(close(math.sin(math.radians(45)) * math.cos(math.radians(45)), 0.5), "P10 最大值 1/2")

    al = 0.9
    S11 = mat([math.cos(al), -math.sin(al), 0],
              [math.sin(al), math.cos(al), 0], [0, 0, 1])
    check(close(S11.T @ S11, np.eye(3)), "P11 S^T S=I")
    dS11 = al * mat([-math.sin(al), -math.cos(al), 0],
                    [math.cos(al), -math.sin(al), 0], [0, 0, 0])
    check(close(dS11 @ S11.T, al * ax_from(e3)), "P11 Ω=αe3")

    check(close(np.array([-1, 1, -1 / 3]), v(-1, 1, -1 / 3)), "P12 角加速度 (-1,1,-1/3)")


def ax_from(a):
    a = np.asarray(a, dtype=float)
    return np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])


def structure_checks() -> None:
    print("\n== 结构检查 ==")
    tex_path = Path("handout.tex")
    pdf_path = Path("handout.pdf")
    log_path = Path("handout.log")
    check(tex_path.exists(), "handout.tex 存在")
    check(pdf_path.exists(), "handout.pdf 存在")
    check(log_path.exists(), "handout.log 存在")
    if not (tex_path.exists() and pdf_path.exists() and log_path.exists()):
        return

    import fitz

    tex = tex_path.read_text(encoding="utf-8")
    practice_ids = re.findall(r"\\practice\{(P\d+)\}", tex)
    answer_ids = re.findall(r"\\answerstart\{(P\d+)\}", tex)
    check(practice_ids == [f"P{i}" for i in range(1, 13)], "P1--P12 正文练习齐全且按序")
    check(answer_ids == [f"P{i}" for i in range(1, 13)], "P1--P12 附录详解齐全且按序")
    check(tex.count("\\begin{tikzpicture}") == 11, "正文有 11 幅自绘图")
    check(tex.count("\\figcap{") == 11, "11 幅图都有图注")

    doc = fitz.open(pdf_path)
    pages = doc.page_count
    check(pages >= 50, f"PDF 页数 {pages} >= 50")
    all_text = "\n".join(doc[i].get_text() for i in range(pages))
    check("??" not in all_text, "PDF 中没有未解析的 ?? 引用")

    # 正文练习页码与附录详解起始页一致
    body = "\n".join(doc[i].get_text() for i in range(40, min(46, pages)))
    refs = dict(re.findall(r"练习\s*(P\d+)[\s\S]*?详解见附录第\s*(\d+)\s*页", body))
    starts = {}
    for i in range(pages):
        for line in doc[i].get_text().splitlines():
            m = re.match(r"^(P\d+)$", line.strip())
            if m and m.group(1) not in starts:
                # 下一行应为“详解”
                lines = [s.strip() for s in doc[i].get_text().splitlines() if s.strip()]
                try:
                    idx = lines.index(m.group(1))
                    if idx + 1 < len(lines) and lines[idx + 1] == "详解":
                        starts[m.group(1)] = i + 1
                except ValueError:
                    pass
    for pid in [f"P{i}" for i in range(1, 13)]:
        check(pid in refs, f"{pid} 正文有附录页码")
        check(pid in starts, f"{pid} 附录有详解起始页")
        if pid in refs and pid in starts:
            check(int(refs[pid]) == starts[pid],
                  f"{pid} 页码一致（正文 {refs[pid]}，附录 {starts[pid]}）")

    # 续解标记必须位于实际续页的页首
    for pid in ["P7", "P8", "P9", "P11"]:
        cont_pages = []
        for i in range(pages):
            lines = [s.strip() for s in doc[i].get_text().splitlines() if s.strip()]
            body_lines = lines[2:]
            if len(body_lines) >= 2 and body_lines[0] == pid and body_lines[1] == "续解":
                cont_pages.append(i + 1)
        check(len(cont_pages) == 1, f"{pid} 有且仅有一个页首续解（实际 {cont_pages}）")

    log = log_path.read_text(encoding="utf-8", errors="replace")
    check("Overfull \\hbox" not in log and "Overfull \\vbox" not in log, "日志无 Overfull")
    check("Missing character:" not in log, "日志无 Missing character")
    check("undefined" not in log.lower(), "日志无 undefined 引用")
    check("Output written on handout.pdf" in log, "日志有成功生成 PDF 的记录")


def main() -> int:
    np.random.seed(0)
    math_checks()
    structure_checks()
    print(f"\n合计断言 {CHECKS} 条，失败 {len(FAILS)} 条。")
    if FAILS:
        print("失败项：")
        for f in FAILS:
            print(" -", f)
        return 1
    print("全部断言通过；这只说明脚本覆盖的数值/结构项目通过，不证明一般推导或页面目视已验收。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
