# -*- coding: utf-8 -*-
r"""round-03 讲义的可复现验证。

三条原则（对应上一轮审核指出的问题）：
1. 每条数值断言都从\textbf{题干/正文给出的实际参数}重新算出，再与\textbf{印在解答里的数}
   比较；不做“向量与自身比较”，也不把同一随机输入重复五次充作五个案例。
2. 多个案例用\textbf{显式不同}的确定性输入；案例数不当作质量证据。
3. 结构断言从\textbf{最终 PDF 的实际内容}定位章节与题号，不使用固定页号，
   也不设“页数 >= N”这类与质量无关的门槛。
脚本只检查可复算的数值与结构；不能代替一般证明、逐页目视或学习者试读。
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

ROOT = Path(__file__).resolve().parent
TEX = ROOT / "handout.tex"
PDF = ROOT / "handout.pdf"
LOG = ROOT / "handout.log"

FAILS: list[str] = []
CHECKS = 0


def check(cond, msg: str) -> None:
    global CHECKS
    CHECKS += 1
    if cond:
        print(f"[ok] {msg}")
    else:
        FAILS.append(msg)
        print(f"[FAIL] {msg}")


def close(a, b, tol=1e-9) -> bool:
    return np.allclose(np.asarray(a, float), np.asarray(b, float), atol=tol, rtol=tol)


def v(*xs):
    return np.array(xs, dtype=float)


E1, E2, E3 = v(1, 0, 0), v(0, 1, 0), v(0, 0, 1)
_T = np if hasattr(np, "trapezoid") else np


def trap(y, x):
    return (np.trapezoid(y, x) if hasattr(np, "trapezoid") else np.trapz(y, x))


def ax_of(a):
    a = np.asarray(a, float)
    return np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])


def rot_axis(n, phi):
    n = np.asarray(n, float)
    return np.outer(n, n) + (np.eye(3) - np.outer(n, n)) * math.cos(phi) + ax_of(n) * math.sin(phi)


# ---------------------------------------------------------------- LaTeX 数字解析
_FRAC = re.compile(r"\\frac\{?(-?\d+)\}?\{?(-?\d+)\}?")
_PLAIN = re.compile(r"-?\d+(?:\.\d+)?")


def parse_num(s: str):
    s = s.strip()
    sign = 1.0
    if s.startswith("-"):
        sign, s = -1.0, s[1:].strip()
    m = _FRAC.fullmatch(s)
    if m:
        return sign * float(m.group(1)) / float(m.group(2))
    m = _PLAIN.fullmatch(s)
    if m:
        return sign * float(m.group(0))
    return None


def printed_has(ans: str, value: float, ctx: str | None = None) -> bool:
    """检查某个算出来的数是否真的印在解答里（含常见四舍五入写法）。"""
    if abs(value - round(value)) < 1e-12:
        forms = [f"{int(round(value))}"]
    else:
        forms = [f"{value:.{d}f}" for d in (1, 2, 3)] + [f"{abs(value):.{d}f}" for d in (1, 2, 3)]
    for f in forms:
        token = f
        if ctx is None:
            if token in ans:
                return True
        elif (ctx + token) in ans or (ctx + (f if value >= 0 else f)) in ans:
            return True
    return False


# ---------------------------------------------------------------- 正文数值恒等式
def body_checks() -> None:
    print("\n== §0 起点 ==")
    a, b = v(3, 0), v(3, 4)
    check(close(a @ b, 9) and close(np.linalg.norm(a), 3) and close(np.linalg.norm(b), 5),
          "§0.1 (3,0)·(3,4)=9，长度 3 与 5")
    check(close((a @ b) / (np.linalg.norm(a) * np.linalg.norm(b)), 3 / 5), "§0.1 cosθ=3/5")
    check(close(np.linalg.norm(b) * 3 / 5, 3), "§0.1 b 在 a 上的投影长 = 3")
    check(close(v(0, 4) @ a, 0), "§0.1 (3,0) 与 (0,4) 正交")

    a2 = v(1, 2, 2)
    n = v(1, 1, 1) / math.sqrt(3)
    proj = (a2 @ n) * n
    check(close(a2 @ n, 5 / math.sqrt(3)), "§0.1 a·n=5/√3")
    check(close(proj, v(5, 5, 5) / 3), "§0.1 投影矢量=(5/3)(1,1,1)")
    check(abs((a2 - proj) @ n) < 1e-12, "§0.1 残差与 n 正交")

    print("\n== §0.2 叉乘与右手基 ==")
    check(close(np.cross(v(1, 0, 0), v(0, 1, 0)), v(0, 0, 1)), "§0.2 E1×E2=E3")
    aa, bb = v(1, 2, 2), v(2, 1, 0)
    c = np.cross(aa, bb)
    check(close(c, v(-2, 4, -3)), "§0.2 (1,2,2)×(2,1,0)=(-2,4,-3)")
    check(abs(aa @ c) < 1e-12 and abs(bb @ c) < 1e-12, "§0.2 叉乘与两个因子都垂直")
    check(close(c @ c, 29), "§0.2 |a×b|²=29")
    check(close((aa @ bb) / (np.linalg.norm(aa) * np.linalg.norm(bb)), 4 / (3 * math.sqrt(5))),
          "§0.2 cosθ=4/(3√5)")
    check(close(np.linalg.norm(aa) * np.linalg.norm(bb) * math.sqrt(1 - (4 / (3 * math.sqrt(5))) ** 2),
                math.sqrt(29)), "§0.2 |a||b|sinθ 与 |a×b|=√29 自洽")
    # 新增 warnbox 的反例：反射基下未改动的分量式会差一个负号
    Rrefl = np.diag([-1.0, 1.0, 1.0])
    aR, xR = Rrefl.T @ v(1, 0, 0), Rrefl.T @ v(0, 1, 0)
    check(close(Rrefl.T @ np.cross(v(1, 0, 0), v(0, 1, 0)), v(0, 0, 1)),
          "§0.2 右手基约定：反射后几何叉乘的分量是 +E3")
    check(close(np.cross(aR, xR), v(0, 0, -1)),
          "§0.2 右手基约定：在反射基里直接套分量式会得到 -E3（差一个负号）")

    print("\n== §0.3--§0.5 矩阵、换基、不变量 ==")
    T = np.array([[2, 1, 0], [0, 1, 0], [0, 0, 3]], float)
    check(close(T @ v(1, 2, 3), v(4, 2, 9)), "§0.3 T(1,2,3)=(4,2,9)")

    T2 = np.diag([2.0, 1.0])
    for deg in (45.0, 30.0):                       # 45° 是印出的例子，30° 是独立核对
        th = math.radians(deg)
        R = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
        n1, n2 = R[:, 0], R[:, 1]
        Tp = np.array([[n1 @ T2 @ n1, n1 @ T2 @ n2], [n2 @ T2 @ n1, n2 @ T2 @ n2]])
        check(close(Tp, R.T @ T2 @ R), f"§0.4 {deg:.0f}° 换基：逐项投影 = R^T T R")
        check(close(R.T @ v(3, 4), v(3 * math.cos(th) + 4 * math.sin(th),
                                    -3 * math.sin(th) + 4 * math.cos(th))),
              f"§0.4 {deg:.0f}° 矢量新坐标 = R^T 旧坐标")
    R45 = np.array([[1, -1], [1, 1]], float) / math.sqrt(2)
    check(close(R45.T @ T2 @ R45, np.array([[1.5, -0.5], [-0.5, 1.5]])),
          "§0.4 45° 例给出 [[3/2,-1/2],[-1/2,3/2]]")

    De = np.array([[3, 1, 0], [1, 3, 0], [0, 0, 2]], float)
    check(close(np.linalg.det(De), 16), "§0.5 新的行列式例子 det=16")
    Dh = np.array([[6, 2, 0], [2, 6, 0], [0, 0, 1]], float)
    th = 0.7
    Q3 = rot_axis(v(1, 2, 2) / 3, th)              # 任意正交矩阵，验迹不变
    check(close(Q3.T @ Q3, np.eye(3)) and close(np.trace(Q3.T @ Dh @ Q3), np.trace(Dh)),
          "§0.5 迹在正交换基下不变（任意轴 0.7 rad）")
    check(close(np.linalg.det(Q3.T @ Dh @ Q3), np.linalg.det(Dh)), "§0.5 行列式在正交换基下不变")
    check(close(np.linalg.det(Dh - 4 * np.eye(3)), 0), "§0.5 det(T-4I)=0 检验非零解判据")

    print("\n== §1 二次型、谱定理 ==")
    T1 = np.array([[1, 2], [0, 1]], float)
    x2 = v(2.0, 3.0)
    S1 = 0.5 * (T1 + T1.T)
    check(close(x2 @ T1 @ x2, (x2[0] + x2[1]) ** 2), "§1.1 不对称 T 的二次型 =(x+y)²")
    check(close(x2 @ S1 @ x2, x2 @ T1 @ x2), "§1.1 对称部分给同一个二次型")

    Tq = np.array([[2, 1], [1, 2]], float)
    check(close(np.sort(np.linalg.eigvalsh(Tq)), [1, 3]), "§1.2 [[2,1],[1,2]] 特征值 1,3")
    u_, v_ = 1.3, -0.7
    xy = np.array([(u_ - v_) / math.sqrt(2), (u_ + v_) / math.sqrt(2)])
    check(close(xy @ Tq @ xy, 3 * u_ ** 2 + v_ ** 2), "§1.2 代入后 E=3u²+v²")
    Tdiag = np.diag([3.0, 7.0])
    check(close([1 / math.sqrt(e) for e in np.diag(Tdiag)], [1 / math.sqrt(3), 1 / math.sqrt(7)]),
          "§1.2 半轴 = 1/√λ（λ=3,7 的独立例子）")

    D1 = np.array([[6, 2, 0], [2, 6, 0], [0, 0, 1]], float)
    ev = np.sort(np.linalg.eigvalsh(D1))
    check(close(ev, [1, 4, 8]), "§1.3 D 的特征值 1,4,8")
    q1, q2, q3 = v(1, 1, 0) / math.sqrt(2), v(1, -1, 0) / math.sqrt(2), v(0, 0, 1)
    check(close(D1 @ q1, 8 * q1) and close(D1 @ q2, 4 * q2) and close(D1 @ q3, q3),
          "§1.3 三个特征方向")
    check(close(8 * np.outer(q1, q1) + 4 * np.outer(q2, q2) + 1 * np.outer(q3, q3), D1),
          "§1.3 谱分解重组 D")
    check(close(np.trace(D1), 13) and close(np.linalg.det(D1), 32), "§1.3 tr=13, det=32")
    check(close(np.trace(D1 @ D1), 81) and close(0.5 * (13 ** 2 - 81), 44), "§1.3 tr(D²)=81, I2=44")

    Ts = np.array([[5, 0, 0], [0, 2, 1], [0, 1, 2]], float)
    check(close(np.sort(np.linalg.eigvalsh(Ts)), [1, 3, 5]), "§1.4 降维例特征值 1,3,5")
    u1, u2, u3 = v(1, 0, 0), v(0, 1, 1) / math.sqrt(2), v(0, 1, -1) / math.sqrt(2)
    check(close(Ts @ u1, 5 * u1) and close(Ts @ u2, 3 * u2) and close(Ts @ u3, u3),
          "§1.4 降维例三个特征向量")
    check(abs(u1 @ u2) < 1e-12 and abs(u2 @ u3) < 1e-12 and abs(u1 @ u3) < 1e-12,
          "§1.4 三个特征向量两两正交")

    # 瑞利商：五个显式不同的确定性方向，而不是同一个随机向量重复五次
    dirs = [v(1, 0, 0), v(0, 1, 0), v(1, 1, 1), v(2, -1, 3), v(-1, 4, 2)]
    for d in dirs:
        d = d / np.linalg.norm(d)
        r = d @ D1 @ d
        check(1 - 1e-12 <= r <= 8 + 1e-12, f"§1.5 瑞利商在 [1,8]（方向 {tuple(np.round(d,3))}，ρ={r:.4f}）")
    check(close(q1 @ D1 @ q1, 8), "§1.5 主轴方向取到上界 λ=8")
    check(close(E3 @ D1 @ E3, 1), "§1.5 主轴方向取到下界 λ=1")

    print("\n== §2 并矢 ==")
    a3, b3 = v(1, 2, 0), v(0, 1, 3)
    check(close(np.outer(a3, b3), np.array([[0, 1, 3], [0, 2, 6], [0, 0, 0]], float)),
          "§2.2 a⊗b 的矩阵")
    check(close(np.outer(a3, b3) @ v(1, 1, 1), v(4, 8, 0)), "§2.2 (a⊗b)·x=(4,8,0)")
    x3 = v(1, 2, 3)
    check(close(np.outer(E1, E2) @ x3, 2 * E1), "§2.3 右作用给 2e1")
    check(close(x3 @ np.outer(E1, E2), E2), "§2.3 左作用给 E2（与右作用不同）")
    Dc = np.array([[1, 2], [0, 3]], float)
    check(close(np.trace(Dc), 4) and close(np.sum(Dc * Dc), 14), "§2.4 tr=4, D:D=14")
    nP = v(1, 1, 1) / math.sqrt(3)
    P = np.outer(nP, nP)
    check(close(P @ P, P) and close(np.trace(P), 1) and close(np.trace(np.eye(3) - P), 2),
          "§2.5 P²=P, trP=1, tr(I-P)=2")
    A4 = np.array([[1, 2, 0], [0, 3, 1], [2, 0, 1]], float)
    uu, vv = v(1, 2, 0), v(0, 1, 2)
    check(close(np.sum(A4 * np.outer(uu, vv)), uu @ A4 @ vv), "§2.4 A:(u⊗v)=u·A·v")
    aa3 = v(1, 2, 3)
    check(close(ax_of(aa3) @ x3, np.cross(aa3, x3)), "§2.6 a^×x=a×x")
    check(close(ax_of(aa3), -ax_of(aa3).T), "§2.6 a^× 反对称")
    M_ax = ax_of(aa3)
    check(close([M_ax[2, 1], M_ax[0, 2], M_ax[1, 0]], aa3), "§2.6 a=(A32,A13,A21)")
    rec = 0.5 * np.array([M_ax[2, 1] - M_ax[1, 2], M_ax[0, 2] - M_ax[2, 0], M_ax[1, 0] - M_ax[0, 1]])
    check(close(rec, aa3), "§2.6 a_k=-1/2 ε_kij A_ij")
    Tns = np.array([[1, 2, 0], [3, 1, 1], [0, 2, 2]], float)   # 故意非对称
    Qb = rot_axis(v(1, 2, 2) / 3, 0.9)
    Tp = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            Tp[i, j] = sum(Qb[k, i] * Qb[l, j] * Tns[k, l] for k in range(3) for l in range(3))
    check(close(Tp, Qb.T @ Tns @ Qb), "§2.7 变换律指标式 = R^T T R（非对称 T）")
    check(close(Qb.T @ Qb, np.eye(3)), "§2.7 δ_ij 在任何正交基下都是单位阵")

    print("\n== §3 旋转算子 ==")
    nM = v(1, 2, 2) / 3
    phi = 0.8
    S = rot_axis(nM, phi)
    check(close(S.T @ S, np.eye(3)) and close(S @ S.T, np.eye(3)), "§3.3 S^T S = S S^T = 1")
    check(abs(np.linalg.det(S) - 1) < 1e-12, "§3.3 det S = +1")
    xx = v(0.3, -1.2, 2.0)
    par = (xx @ nM) * nM
    perp = xx - par
    check(close(S @ xx, par + perp * math.cos(phi) + np.cross(nM, perp) * math.sin(phi)),
          "§3.4 绕轴公式：平行分量不动、垂直分量转 φ")
    check(close(np.linalg.norm(S @ xx), np.linalg.norm(xx)), "§3.4 绕轴公式保持长度")
    check(close(rot_axis(nM, 0.0), np.eye(3)), "§3.4 φ=0 时 S=1")
    al = 0.6
    hstep = 1e-6
    S3 = rot_axis(E3, al)
    dS = al * (rot_axis(E3, al + hstep) - rot_axis(E3, al - hstep)) / (2 * hstep)
    check(close(dS @ S3.T, al * ax_of(E3), 1e-7), "§3.5 dS/dt S^T = α E3^×（对 S 用中心差分）")
    check(close(dS, (al * ax_of(E3)) @ S3, 1e-7), "§3.5 dS/dt = Ω^× S")
    check(close(rot_axis(E3, math.pi / 2) @ E1, E2), "§3.4 绕 E3 转 90° 把 E1 送到 E2")
    Vloc, Om, rloc, a_shift = v(0.4, -0.2, 0.7), v(0.3, 1.1, -0.5), v(1.2, 0.4, -0.9), v(0.5, -0.3, 0.2)
    v_abs = Vloc + np.cross(Om, rloc)
    v_abs2 = (Vloc + np.cross(Om, a_shift)) + np.cross(Om, rloc - a_shift)
    check(close(v_abs, v_abs2), "§3.6 换基点：V'=V+Ω×a 且 Ω 不变")

    print("\n== §4 惯量 ==")
    masses = [2.0, 3.0, 5.0]
    pts = [v(1.0, 0.5, -0.5), v(-0.6, 1.2, 0.4), v(0.2, -0.9, 1.1)]
    Jd = sum(m * (np.dot(p, p) * np.eye(3) - np.outer(p, p)) for m, p in zip(masses, pts))
    om = v(0.7, -0.3, 1.1)
    Ldir = sum(m * np.cross(p, np.cross(om, p)) for m, p in zip(masses, pts))
    check(close(Jd @ om, Ldir), "§4.1 J·ω = Σ m r×(ω×r)（离散质量核对）")
    Jcomp = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            Jcomp[i, j] = sum(m * (np.dot(p, p) * (1 if i == j else 0) - p[i] * p[j])
                              for m, p in zip(masses, pts))
    check(close(Jcomp, Jd), "§4.2 分量式 J_ij=∫(r²δ_ij-x_ix_j)dm 与构造式一致")
    check(om @ Jd @ om >= 0, "§4.2 二次型非负（半正定）")
    check(close(om @ Jd @ om, sum(m * np.linalg.norm(np.cross(p, om)) ** 2
                                  for m, p in zip(masses, pts))),
          "§4.2 ω·J·ω = Σ m|r×ω|²")
    # 等号条件：所有质量在过基点的一条直线上时退化为零
    pts_line = [v(1.0, 2.0, -1.0) * s for s in (1.0, -2.0, 0.5)]
    Jline = sum(m * (np.dot(p, p) * np.eye(3) - np.outer(p, p)) for m, p in zip(masses, pts_line))
    check(abs(v(1.0, 2.0, -1.0) / math.sqrt(6) @ Jline @ (v(1.0, 2.0, -1.0) / math.sqrt(6))) < 1e-12,
          "§4.2 质量全在一条线上时该方向惯量为零（等号条件）")
    check(abs(v(0, 0, 0) @ Jd @ v(0, 0, 0)) < 1e-12, "§4.2 ω=0 时等号恒成立（与质量分布无关）")
    # 对称分布：x→-x 对称时 J13=J23=0
    sym_pts = [v(1.0, 0.4, 0.7), v(-1.0, 0.4, 0.7), v(1.0, -0.4, 0.7), v(-1.0, -0.4, 0.7)]
    Jsym = sum(1.0 * (np.dot(p, p) * np.eye(3) - np.outer(p, p)) for p in sym_pts)
    check(abs(Jsym[0, 2]) < 1e-12 and abs(Jsym[1, 2]) < 1e-12,
          "§4.3 x→-x 与 y→-y 对称的分布给出 J13=J23=0")
    mb = 12.0
    w_, h_, d_ = 1.0, 2.0, 3.0
    Jblk = mb / 12 * np.diag([h_ ** 2 + d_ ** 2, w_ ** 2 + d_ ** 2, w_ ** 2 + h_ ** 2])
    check(close(Jblk, np.diag([13, 10, 5])), "§4.4 长方体 a=1,b=2,c=3,m=12 给 diag(13,10,5)")
    # 直接数值积分核对方块公式（中点法则，与印出的公式独立）
    def mid_int(f, lo, hi, n=200001):
        xs = lo + (np.arange(n) + 0.5) * ((hi - lo) / n)
        return float(np.sum(f(xs)) * ((hi - lo) / n))

    rho = mb / (w_ * h_ * d_)
    Izz = rho * (mid_int(lambda s: s ** 2, -w_ / 2, w_ / 2) * h_ * d_
                 + mid_int(lambda s: s ** 2, -h_ / 2, h_ / 2) * w_ * d_)
    check(close(Izz, Jblk[2, 2], 1e-6), f"§4.4 长方体 Jzz：数值积分 {Izz:.6f} 与 mb²/12 公式一致")
    check(close(mb * (w_ ** 2 + h_ ** 2) / 12, Jblk[2, 2]), "§4.4 Jzz=m(a²+b²)/12")
    for i, j, k in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
        check(Jblk[i, i] + Jblk[j, j] >= Jblk[k, k] - 1e-9, f"§4.3 三角形不等式 {i}+{j}>={k}")
    # 平行轴：细杆绕端点 = mL²/3
    mrod, Lrod = 2.0, 3.0
    check(close(mrod * Lrod ** 2 / 12 + mrod * (Lrod / 2) ** 2, mrod * Lrod ** 2 / 3),
          "§4.5 平行轴：细杆绕端点 = mL²/3")
    mm2 = 2.0
    r1, r2 = v(1.3, 0, 0), v(-1.3, 0, 0)
    Jc = 0.5 * mm2 * (r1 @ r1 * np.eye(3) - np.outer(r1, r1)) + 0.5 * mm2 * (r2 @ r2 * np.eye(3) - np.outer(r2, r2))
    R0 = v(0.4, 0.9, -0.2)
    Jo = (0.5 * mm2 * ((r1 + R0) @ (r1 + R0) * np.eye(3) - np.outer(r1 + R0, r1 + R0))
          + 0.5 * mm2 * ((r2 + R0) @ (r2 + R0) * np.eye(3) - np.outer(r2 + R0, r2 + R0)))
    check(close(Jo, Jc + mm2 * (R0 @ R0 * np.eye(3) - np.outer(R0, R0))),
          "§4.5 平行轴定理（两点质量直接核对）")
    # §4.4 选读：均质椭球（球面上的 ∫η²dV 在 ellipsoid_checks 里用一元积分独立核算）
    a_, b_, c_ = 1.6, 1.0, 0.7
    Vol = 4 * math.pi * a_ * b_ * c_ / 3
    check(close(a_ * b_ * c_ * b_ ** 2 * (4 * math.pi / 15), Vol * b_ ** 2 / 5),
          "§4.4 选读：∫_椭球 y²dV = V b²/5")
    Ms = 3.0
    Jell = Ms / 5 * np.diag([b_ ** 2 + c_ ** 2, a_ ** 2 + c_ ** 2, a_ ** 2 + b_ ** 2])
    Rs = 1.4
    Jsph = Ms / 5 * np.diag([2 * Rs ** 2] * 3)
    check(close(Jsph, 2 / 5 * Ms * Rs ** 2 * np.eye(3)), "§4.4 选读：球极限 J=(2/5)MR²·1")

    Jex = np.diag([13.0, 10.0, 5.0])
    omex = v(1, 1, 1) / math.sqrt(3)
    Lex = Jex @ omex
    check(close(Lex, v(13, 10, 5) / math.sqrt(3)), "§4.6 L=(13,10,5)/√3")
    cth = Lex @ omex / (np.linalg.norm(Lex) * np.linalg.norm(omex))
    check(close(cth, 2 * math.sqrt(2) / 3), "§4.6 cosθ=2√2/3")
    check(close(math.degrees(math.acos(cth)), 19.471220634490691, 1e-6), "§4.6 θ≈19.47°")
    check(close(math.sqrt(1 - cth ** 2), 1 / 3), "§4.6 sinθ=1/3")
    check(abs(omex @ Lex - np.linalg.norm(Lex) * np.linalg.norm(omex) * cth) < 1e-12,
          "§4.6 夹角余弦与点积一致")

    print("\n== §5 输运、欧拉方程、对称陀螺 ==")
    Dtr = np.outer(E1, E2)
    check(close(ax_of(E3) @ Dtr - Dtr @ ax_of(E3), np.outer(E2, E2) - np.outer(E1, E1)),
          "§5.1 单并矢输运核对")
    check(close(ax_of(E3) @ np.eye(3) - np.eye(3) @ ax_of(E3), np.zeros((3, 3))),
          "§5.1 单位张量的固定系导数为零")
    A_, B_, C_ = 4.0, 7.0, 9.0
    wv, wd = v(0.7, -0.4, 1.1), v(1.2, -0.3, 0.8)
    euler = np.array([A_ * wd[0] + (C_ - B_) * wv[1] * wv[2],
                      B_ * wd[1] + (A_ - C_) * wv[2] * wv[0],
                      C_ * wd[2] + (B_ - A_) * wv[0] * wv[1]])
    check(close(euler, np.diag([A_, B_, C_]) @ wd + np.cross(wv, np.diag([A_, B_, C_]) @ wv)),
          "§5.2 欧拉方程与 (dL/dt)体+ω×L 一致（A,B,C 各不相同）")
    At = Bt = 4.0
    Ct = 5.0
    check(close((Ct - At) / At * 6.0, 1.5) and close(2 * math.pi / 1.5, 4 * math.pi / 3),
          "§5.3 Ω=1.5, T=4π/3（ω3=+6）")
    check(close((Ct - At) / At * (-6.0), -1.5),
          "§5.3 ω3=-6 时 Ω=-1.5（符号随自转反向，与修正后的框一致）")
    Mbox = np.cross(omex, Lex)
    check(close(Mbox, v(-5, 8, -3) / 3), "§5.4 M=ω×L=(1/3)(-5,8,-3)")
    check(close(np.linalg.norm(Mbox), math.sqrt(98) / 3), "§5.4 |M|=√98/3≈3.30")
    check(abs(Mbox @ omex) < 1e-12 and abs(Mbox @ Lex) < 1e-12, "§5.4 M 垂直于 ω 与 L")

    print("\n== §6 应力 ==")
    sig0 = 2.0
    sig = sig0 * np.outer(E1, E1)
    check(close(sig @ E1, sig0 * E1) and close(sig @ E2, np.zeros(3)), "§6.1 t(E1)=σ0e1, t(E2)=0")
    th = math.radians(30)
    n30 = math.cos(th) * E1 + math.sin(th) * E2
    t30 = sig @ n30
    check(close(t30, sig0 * math.cos(th) * E1), "§6.3 t=σ0cos30°E1")
    tn = t30 @ n30
    check(close(tn, sig0 * math.cos(th) ** 2), "§6.3 tn=σ0cos²30°=(3/4)σ0")
    tau = math.sqrt(t30 @ t30 - tn ** 2)
    check(close(tau, sig0 * math.sin(th) * math.cos(th)), "§6.3 τ=σ0sin30°cos30°=(√3/4)σ0")
    check(close(t30 @ t30, tn ** 2 + tau ** 2), "§6.3 |t|²=tn²+τ²")
    th135 = math.radians(135)
    check(math.sin(th135) * math.cos(th135) < 0 < math.sqrt(sig0 ** 2 - (sig0 * math.cos(th135) ** 2) ** 2),
          "P10 θ=135° 时 sinθcosθ<0 而根号给正数（必须取绝对值）")
    grid = np.linspace(0, 2 * math.pi, 200001)
    check(close(np.max(np.abs(np.sin(grid) * np.cos(grid))), 0.5, 1e-6),
          "P10 全周最大 |sinθcosθ| = 1/2，出现在 45° 与 135°")
    # 应力对称性：两对切应力对中心的力矩
    h = 0.3
    m21 = (0.5 * h * E1).__mul__(1.0)
    coup1 = np.cross(0.5 * h * E1, 1.0 * E2) + np.cross(-0.5 * h * E1, -1.0 * E2)
    coup2 = np.cross(0.5 * h * E2, 1.0 * E1) + np.cross(-0.5 * h * E2, -1.0 * E1)
    check(close(coup1, h * E3) and close(coup2, -h * E3), "§6.2 两对切应力力矩方向相反")
    check(close(coup1 + coup2, np.zeros(3)), "§6.2 σ21=σ12 时两对力矩相消")
    # 小立方体净面力
    s0, L0 = 3.0, 2.0
    hh = 1e-4
    diff = (s0 * (0.7 + hh) / L0 - s0 * 0.7 / L0) * hh ** 2
    check(close(diff / hh ** 3, s0 / L0, 1e-6), "§6.4 小立方体净面力/体积 → ∂1σ11=σ0/L")
    check(close(-np.array([s0 / L0, 0, 0]), v(-1.5, 0, 0)), "§6.4 体力 f=-∇·σ=(-1.5,0,0)")


# ---------------------------------------------------------------- 题干参数 → 解答数字
def _slice(text: str, start_pat: str, end_pat: str) -> str:
    s = text.index(start_pat)
    e = text.index(end_pat, s)
    return text[s:e]


def exercise_checks(tex: str) -> None:
    print("\n== 独立练习：从题干参数重新计算，与印出的解答数字比较 ==")
    stmts = {}
    for pid in [f"P{i}" for i in range(1, 13)]:
        stmts[pid] = _slice(tex, rf"\practice{{{pid}}}{{", rf"\answerstart{{{pid}}}{{")

    # ---- P12：从题干 (A,B,C,ω) 解欧拉方程（上一轮此处是硬编码向量自比）
    st = stmts["P12"]
    mA = re.search(r"A\s*=\s*(\d+)", st)
    mB = re.search(r"B\s*=\s*(\d+)", st)
    mC = re.search(r"C\s*=\s*(\d+)", st)
    mW = re.search(r"\\boldsymbol\\omega\s*=\s*\(([-\d,\s.]+)\)", st)
    check(bool(mA and mB and mC and mW), "P12 题干能解析出 (A,B,C,ω)")
    if mA and mB and mC and mW:
        A, B, C = float(mA.group(1)), float(mB.group(1)), float(mC.group(1))
        w = np.array([float(x) for x in mW.group(1).split(",")])
        wdot = np.array([-(C - B) * w[1] * w[2] / A,
                         -(A - C) * w[2] * w[0] / B,
                         -(B - A) * w[0] * w[1] / C])
        ansp12 = _slice(tex, r"\answerstart{P12}{", r"\hdr{附录 B}")
        printed = re.findall(r"\\dot\\omega_(\d)\s*=\s*(-?(?:\\frac\{?-?\d+\}?\{?-?\d+\}?|\d+(?:\.\d+)?))",
                             ansp12)
        got = {int(i): parse_num(s) for i, s in printed}
        check(len(got) == 3, "P12 解答印出三个 ω̇ 分量")
        for k in (1, 2, 3):
            if k in got:
                check(got[k] is not None and close(got[k], wdot[k - 1], 1e-12),
                      f"P12 ω̇{k}: 题干参数算出 {wdot[k-1]:.6f}，解答印出 {got[k]}")
        check(close(wdot, v(-1, 1, -1 / 3)), "P12 由 A=1,B=2,C=3,ω=(1,1,1) 解得 (-1,1,-1/3)")

    # ---- P3：从题干 (A=B, C, ω3) 算 Ω 与 T
    st = stmts["P3"]
    mAB = re.search(r"A\s*=\s*B\s*=\s*(\d+)", st)
    mC = re.search(r"C\s*=\s*(\d+)", st)
    mW3 = re.search(r"\\omega_3\s*=\s*(\d+)", st)
    check(bool(mAB and mC and mW3), "P3 题干能解析出 (A=B, C, ω3)")
    if mAB and mC and mW3:
        A, C, w3 = float(mAB.group(1)), float(mC.group(1)), float(mW3.group(1))
        Om = (C - A) / A * w3
        Tp = 2 * math.pi / Om
        ansp3 = _slice(tex, r"\answerstart{P3}{", r"\answerstart{P4}{")
        check(printed_has(ansp3, Om, ctx="\\times10=") or printed_has(ansp3, Om),
              f"P3 印出 Ω={Om}")
        check(printed_has(ansp3, Tp) or f"{Tp:.3f}" in ansp3, f"P3 印出 T≈{Tp:.3f}")
        check(close(Om, 5.0) and close(Tp, 2 * math.pi / 5), "P3 Ω=5, T=2π/5")

    # ---- P2：从题干 (m,a,b,c) 算 J
    st = stmts["P2"]
    mm = re.search(r"m\s*=\s*(\d+)", st)
    ma = re.search(r"a\s*=\s*(\d+)", st)
    mb = re.search(r"b\s*=\s*(\d+)", st)
    mc = re.search(r"c\s*=\s*(\d+)", st)
    check(bool(mm and ma and mb and mc), "P2 题干能解析出 (m,a,b,c)")
    J2 = None
    if mm and ma and mb and mc:
        m, a, b, c = (float(x.group(1)) for x in (mm, ma, mb, mc))
        J2 = m / 12 * np.diag([b ** 2 + c ** 2, a ** 2 + c ** 2, a ** 2 + b ** 2])
        ansp2 = _slice(tex, r"\answerstart{P2}{", r"\answerstart{P3}{")
        check(f"\\frac{{{int(round(J2[0,0]*12))}}}{{12}}" in ansp2,
              f"P2 印出 Jxx = {J2[0,0]:.4f} 的分数形式")
        check(close(J2[2, 2], J2[0, 0] + J2[1, 1]) is False,
              "P2 厚长方体不满足垂直轴定理（只有薄板才满足）")
        Jplate = m / 12 * np.diag([b ** 2, a ** 2, a ** 2 + b ** 2])
        check(close(Jplate[2, 2], Jplate[0, 0] + Jplate[1, 1]), "P2 薄板极限满足 Jzz=Jxx+Jyy")

    # ---- P1：从解答印出的矩阵独立算不变量，与解答印出的结果比较
    ansp1 = _slice(tex, r"\answerstart{P1}{", r"\answerstart{P2}{")
    mD = re.search(r"\\ten D=\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}", ansp1, re.S)
    check(bool(mD), "P1 解答印出 D 的矩阵")
    if mD:
        rows = [[float(t) for t in r.split("&")] for r in mD.group(1).split(r"\\")]
        D1 = np.array(rows, float)
        tr = np.trace(D1)
        det = np.linalg.det(D1)
        dd = np.sum(D1 * D1)
        ev1 = np.sort(np.linalg.eigvalsh(D1))
        check(close(tr, 10) and "=4+4+2=10" in ansp1, "P1 tr：算得 10，与印出的 4+4+2=10 一致")
        check(close(det, 30) and "=2(16-1)=30" in ansp1, "P1 det：算得 30，与印出的 2(16-1)=30 一致")
        check(close(dd, 38) and "=38" in ansp1, "P1 D:D：算得 38，与印出的 38 一致")
        check(close(ev1, [2, 3, 5]) and "特征值是 $2,3,5$" in ansp1, "P1 特征值 2,3,5")
        n1 = v(1, 1, 0) / math.sqrt(2)
        check(close(D1 @ n1, 5 * n1), "P1 主轴 (1,1,0)/√2 对应 λ=5")
        check(close(5 * np.outer(n1, n1) + 3 * np.outer(v(1, -1, 0) / math.sqrt(2), v(1, -1, 0) / math.sqrt(2))
                    + 2 * np.outer(E3, E3), D1), "P1 谱分解重组 D")
        xp1 = v(1, 2, 3)
        check(close(D1 @ xp1, v(6, 9, 6)) and "=(6,9,6)" in ansp1.replace(" ", ""),
              "P1 D·x=(6,9,6)")

    # ---- P4：用 P2 的 J 与题干方向 n
    st = stmts["P4"]
    mn = re.search(r"\\vect n\s*=\s*\(([-\d,\s.]+)\)\s*/\s*\\sqrt\{?3\}?", st)
    check(bool(mn), "P4 题干能解析出 n=(1,1,1)/√3")
    if mn and J2 is not None:
        n4 = np.array([float(x) for x in mn.group(1).split(",")]) / math.sqrt(3)
        I4 = n4 @ J2 @ n4
        ansp4 = _slice(tex, r"\answerstart{P4}{", r"\answerstart{P5}{")
        check(close(I4, 145 / 18) and "\\frac{145}{18}" in ansp4, f"P4 I(n)=145/18（算得 {I4:.6f}）")
        check(close(n4 @ (J2 @ n4), 2 * 0.5 * I4), "P4 ω·L=2K")
        check(close(I4, np.trace(J2) / 3), "P4 沿 (1,1,1) 的 I = tr(J)/3")

    # ---- P10：一般式与最大值的数值核对
    ansp10 = _slice(tex, r"\answerstart{P10}{", r"\answerstart{P11}{")
    check("|\\sin2\\theta|" in ansp10 or "\\lvert\\sin2\\theta\\rvert" in ansp10
          or "|\\sin 2\\theta|" in ansp10, "P10 解答用 |sin2θ| 表示切应力大小")
    check("\\frac{\\sigma_0}{2}" in ansp10, "P10 印出 τmax=σ0/2")
    ths = np.linspace(0, 2 * math.pi, 100001)
    taus = np.abs(np.sin(ths) * np.cos(ths))
    amax = ths[int(np.argmax(taus))]
    check(close(taus.max(), 0.5, 1e-6), "P10 数值最大 |sinθcosθ|=0.5")
    check(min(abs(amax - math.pi / 4), abs(amax - 3 * math.pi / 4)) < 1e-3,
          "P10 最大值出现在 45° 或 135°")

    # ---- P11：数值核对旋转算子与 Ω
    al = 0.9
    hstep = 1e-6
    S11 = rot_axis(E3, al)
    dS11 = al * (rot_axis(E3, al + hstep) - rot_axis(E3, al - hstep)) / (2 * hstep)
    check(close(S11.T @ S11, np.eye(3)), "P11 S^T S=I")
    check(close(dS11 @ S11.T, al * ax_of(E3), 1e-7), "P11 Ω^×=α E3^×（中心差分）")
    ansp11 = _slice(tex, r"\answerstart{P11}{", r"\answerstart{P12}{")
    check("\\boldsymbol\\Omega=\\alpha\\,\\vect e_3" in ansp11,
          "P11 印出 Ω=α e3")

    # ---- P9：错误矩阵的谱（核对印出的 (λ-1)²(λ-4)）
    ansp9 = _slice(tex, r"\answerstart{P9}{", r"\answerstart{P10}{")
    mA9 = re.search(r"\\ten A=\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}", ansp9, re.S)
    check(bool(mA9), "P9 表达式印出 A 的矩阵")
    if mA9:
        rows = [[float(t) for t in r.split("&")] for r in mA9.group(1).split(r"\\")]
        A9 = np.array(rows, float)
        check(close(np.sort(np.linalg.eigvalsh(A9)), [1, 1, 4]), "P9 A 的特征值 1,1,4")
        check(close(np.trace(A9), 6) and "6" in ansp9, "P9 tr A=6")
        check(close(np.linalg.det(A9), 4), "P9 det A=4")
        check(close(np.sum(A9 * A9), 18), "P9 tr A²=Σ A_ij²=18")
        check("(\\lambda-1)^2(\\lambda-4)".replace("(", "(") in ansp9.replace(" ", ""),
              "P9 印出 (λ-1)²(λ-4)")
        r9 = v(1, 1, 1)
        Jtrue = r9 @ r9 * np.eye(3) - np.outer(r9, r9)
        check(close(np.sort(np.linalg.eigvalsh(Jtrue)), [0, 3, 3]), "P9 真实 J 主值 0,3,3")

    # ---- P5/P6/P7/P8：概念题的结构与关键论证是否印出
    ansp7 = _slice(tex, r"\answerstart{P7}{", r"\answerstart{P8}{")
    check("\\tr(\\ten A\\ten B)=\\tr(\\ten B\\ten A)" in ansp7, "P7 印出迹的循环性")
    check("\\ten R\\ten R^{\\mathsf T}=\\unitd" in ansp7, "P7 印出正交性 R R^T=1")
    ansp8 = _slice(tex, r"\answerstart{P8}{", r"\answerstart{P9}{")
    check("\\tfrac12" in ansp8 or "\\frac12" in ansp8, "P8 印出对称化 S=½(D+D^T)")
    ansp5 = _slice(tex, r"\answerstart{P5}{", r"\answerstart{P6}{")
    check("\\vect e_1\\otimes\\vect e_1" in ansp5, "P5 给出具体反例并矢")
    ansp6 = _slice(tex, r"\answerstart{P6}{", r"\answerstart{P7}{")
    check("T'_{ij}=R_{ki}R_{lj}T_{kl}" in ansp6, "P6 印出变换律判据")
    check("仿射" in ansp6 or "平移" in ansp6, "P6 区分三类坐标对象")


# ---------------------------------------------------------------- PDF 结构
def structure_checks() -> None:
    print("\n== 最终 PDF 的结构与断页（动态定位，不依赖固定页号） ==")
    for p, name in ((TEX, "handout.tex"), (PDF, "handout.pdf"), (LOG, "handout.log")):
        check(p.exists() and p.stat().st_size > 0, f"{name} 存在且非空")
    if not (TEX.exists() and PDF.exists() and LOG.exists()):
        return
    tex = TEX.read_text(encoding="utf-8")

    import fitz
    doc = fitz.open(PDF)
    pages = doc.page_count
    texts = [doc[i].get_text() for i in range(pages)]
    check(pages >= 1, f"PDF 实际页数 {pages}")
    joined = "\n".join(texts)
    check("??" not in joined, "PDF 中没有未解析的 ?? 引用")

    # 章节位置：按内容定位（PDF 抽取会把中文与数字拉开，先归一化空白再匹配）
    flat = [re.sub(r"\s+", "", t) for t in texts]

    def find_page(pred):
        for i, t in enumerate(flat):
            if pred(t):
                return i + 1
        return None

    sec7 = find_page(lambda t: "§7" in t and "独立练习" in t and "下面十二道题" in t)
    appA = find_page(lambda t: "附录A" in t and "练习详解" in t)
    check(sec7 is not None, f"按内容定位到 §7 独立练习（第 {sec7} 页）")
    check(appA is not None, f"按内容定位到 附录 A 练习详解（第 {appA} 页）")
    if sec7 and appA:
        check(sec7 < appA, "§7 在附录 A 之前")

    # 正文练习：完整题干、考点、附录页码
    ids = re.findall(r"\\practice\{(P\d+)\}", tex)
    aids = re.findall(r"\\answerstart\{(P\d+)\}", tex)
    check(ids == [f"P{i}" for i in range(1, 13)], "正文 P1--P12 齐全且按序")
    check(aids == [f"P{i}" for i in range(1, 13)], "附录 A 的 P1--P12 详解齐全且按序")
    check(tex.count("\\begin{tikzpicture}") == tex.count("\\figcap{") == 11,
          "11 幅自绘图与 11 条图注一一对应")

    # 正文里印出的“详解见附录第 N 页”与附录实际起始页一致（按出现顺序配题号）
    body = [flat[i] for i in range(((sec7 - 1) if sec7 else 0), ((appA - 1) if appA else pages))]
    refs, cur = {}, None
    for t in body:
        for m in re.finditer(r"(?:练习(P\d+))|(?:详解见附录第(\d+)页)", t):
            if m.group(1):
                cur = m.group(1)
            elif m.group(2) and cur and cur not in refs:
                refs[cur] = int(m.group(2))
    starts = {}
    for i, t in enumerate(texts):
        lines = [s.strip() for s in t.splitlines() if s.strip()]
        for k in range(len(lines) - 1):
            m = re.fullmatch(r"(P\d+)", lines[k])
            if m and lines[k + 1] == "详解" and m.group(1) not in starts:
                starts[m.group(1)] = i + 1
    for pid in [f"P{i}" for i in range(1, 13)]:
        check(pid in refs, f"{pid} 正文印有附录页码（{refs.get(pid)}）")
        check(pid in starts, f"{pid} 附录有详解起始页（{starts.get(pid)}）")
        if pid in refs and pid in starts:
            check(refs[pid] == starts[pid],
                  f"{pid} 正文页码与附录实际起始页一致（{refs[pid]} / {starts[pid]}）")

    # 续解：把“实际续页”本身作为验收目标。
    #   (a) 正文里每一条 \answercontinue 都必须落在真正续页的页首（正文前 3 行）；
    #       落在页中一律失败——不放宽为“页中但后随 3 行也算过”。
    #   (b) 凡某题详解跨到下一页，该页开头必须能认出题号（题号或“续解”）。
    #   (c) 不限制每题续页次数（同一题可以有多条续解），也不要求每题恰好一条。
    def body_rows(i):
        # i 为 1 起的页号；按坐标只取正文区（页眉、页脚不计入“正文第几行”）
        rows = []
        for b in doc[i - 1].get_text("dict")["blocks"]:
            for line in b.get("lines", []):
                txt = "".join(s["text"] for s in line["spans"]).strip()
                if txt and 55 < line["bbox"][1] < 797:
                    rows.append((line["bbox"][1], txt))
        rows.sort()
        return [t for _, t in rows]

    def neighbour_pid(rows, k):
        # PDF 抽取把“Pk”与“详解/续解”排成两行，先后顺序不固定，按相邻行判断
        if k >= len(rows) or rows[k] not in ("详解", "续解"):
            return None, None
        for j in (k - 1, k + 1):
            if 0 <= j < len(rows):
                m = re.fullmatch(r"(P\d+)", rows[j])
                if m:
                    return m.group(1), rows[k]
        return None, None

    starts, conts = {}, {}
    for i in range(1, pages + 1):
        rows = body_rows(i)
        for k in range(len(rows)):
            pid, kind = neighbour_pid(rows, k)
            if not pid:
                continue
            if kind == "详解":
                starts.setdefault(pid, i)
            else:
                conts.setdefault(pid, []).append((i, k + 1))

    tex_cont = re.findall(r"\\answercontinue\{(P\d+)\}", tex)
    pdf_cont = sum(len(v) for v in conts.values())
    check(len(tex_cont) == pdf_cont,
          f"正文 {len(tex_cont)} 条续解标记在 PDF 里都印出来了（PDF 实际 {pdf_cont} 条）")
    for pid, lst in conts.items():
        for page, line_no in lst:
            check(line_no <= 3,
                  f"{pid} 的续解标记在实际续页页首（第 {page} 页，正文第 {line_no} 行）")
            check(page > starts.get(pid, 0),
                  f"{pid} 的续解页在第 {starts.get(pid)} 页详解起页之后（第 {page} 页）")
    # 反向：正文没有续解标记时，PDF 里也不应凭空出现
    check(set(tex_cont) == set(conts),
          f"续解标记的题号与正文一致（正文 {sorted(set(tex_cont))} / PDF {sorted(conts)}）")

    appB = find_page(lambda t: "指标与记号速查" in t) or pages + 1
    for k in range(1, 13):
        pid = f"P{k}"
        if pid not in starts:
            continue
        nxt = starts.get(f"P{k + 1}", appB)
        for p in range(starts[pid] + 1, nxt):
            head = " ".join(body_rows(p)[:3])
            check(pid in head,
                  f"{pid} 在第 {p} 页续排时，页首能认出题号（{head[:30]!r}）")

    # 上一轮被点名的续页上下文，按 tex 与 PDF 各查一次
    check("本页所需的输入是" in tex, "P9 续页在用到 A 之前重写了所需矩阵")
    notes9 = re.findall(r"\\answercontinue\{P9\}\{([^}]*)\}", tex)
    check(any("所需的" in n for n in notes9),
          "P9 至少一条续解说明写明本页会重写所需的矩阵")
    note10 = re.search(r"\\answercontinue\{P10\}\{([^}]*)\}", tex)
    note10 = note10.group(1) if note10 else ""
    check("\\sigma_0" in note10 and "\\theta" in note10,
          "P10 续解说明带本题独有对象：单轴拉伸 σ0 与法向角 θ")
    check("逐项核对这条链" in tex and "目标就是 (ii) 的正交性" in tex,
          "谱定理第五步续页带有目标与条件提示")
    p_lead = find_page(lambda t: "逐项核对这条链" in t)
    if p_lead:
        check("条件" in flat[p_lead - 1] and "正交" in flat[p_lead - 1],
              f"该提示所在页（第 {p_lead} 页）同时印有目标与条件")
    p_det = find_page(lambda t: "继续算" in t and "三个根全实" in t)
    check(p_det is not None, f"特征多项式那一步在续页上也标了本步目标（第 {p_det} 页）")
    check("共面关系见图8" not in "".join(flat), "§4.6 的错误图 8 引用已删除")
    fig8_pages = [i + 1 for i, t in enumerate(flat) if "图8" in t]
    check(1 <= len(fig8_pages) <= 3, f"“图 8”只在少数位置出现：{fig8_pages}")
    p8 = find_page(lambda t: "对称陀螺的" in t and "共面" in t)
    if p8 and fig8_pages:
        check(all(p <= p8 + 1 or (appA and p >= appA) for p in fig8_pages),
              f"图 8 的引用都靠近它所在页（图在 {p8}，引用在 {fig8_pages}）")
    check("法向" in tex and "截面本身" in tex, "§6.3 明确区分法向角与截面角")
    check("所需的输入是" in "".join(flat), "P9 续页在 PDF 里也印出了所需输入")

    # 日志
    log = LOG.read_text(encoding="utf-8", errors="replace")
    check("Overfull \\hbox" not in log and "Overfull \\vbox" not in log, "日志无 Overfull")
    check("Missing character:" not in log, "日志无 Missing character")
    check("undefined" not in log.lower(), "日志无 undefined 引用")
    check("Output written on handout.pdf" in log, "日志有成功生成 PDF 的记录")
    check(f"({pages} pages)" in log, f"日志页数与 PDF 实际页数一致（{pages}）")

    # 页码由主题宏里的 \pageref 生成：核查每个练习的最后参数都是与题号一致的 ans: 标签，
    # 且正文没有手写死页码（形如“附录第 47 页”）。
    pcalls = list(re.finditer(r"\\practice\{(P\d+)\}", tex))
    tag_ok = True
    for j, m in enumerate(pcalls):
        end = pcalls[j + 1].start() if j + 1 < len(pcalls) else tex.index(r"\hdr{§8}")
        seg = tex[m.end():end]
        mm = re.search(r"\{ans:(P\d+)\}", seg)
        tag_ok = tag_ok and bool(mm) and mm.group(1) == m.group(1)
    check(len(pcalls) == 12 and tag_ok, "12 个练习都用与题号一致的 ans: 标签生成附录页码")
    check(not re.search(r"详解见附录第\s*\d+\s*页", tex), "正文没有手写附录页码")


# ---------------------------------------------------------------- 椭球选读的积分
def ellipsoid_checks() -> None:
    print("\n== §4.4 选读：均质椭球（独立数值积分） ==")
    a, b, c = 1.6, 1.0, 0.7
    # 单位球上 ∫η²dV：用球坐标的三个人一元积分
    r = np.linspace(0, 1, 4001)
    th = np.linspace(0, math.pi, 2001)
    ph = np.linspace(0, 2 * math.pi, 4001)
    ir = trap(r ** 4, r)
    it = trap(np.sin(th) ** 3, th)
    ip = trap(np.cos(ph) ** 2, ph)
    check(close(ir, 1 / 5, 1e-6) and close(it, 4 / 3, 1e-6) and close(ip, math.pi, 1e-6),
          "§4.4 选读：三个一元积分 1/5、4/3、π")
    check(close(ir * it * ip, 4 * math.pi / 15, 1e-6), "§4.4 选读：乘积 = 4π/15")
    Vol = 4 * math.pi * a * b * c / 3
    check(close(a * b * c * b ** 2 * ir * it * ip, Vol * b ** 2 / 5, 1e-6),
          "§4.4 选读：∫_E y²dV = V b²/5")
    J = 3.0 / 5 * np.diag([b ** 2 + c ** 2, a ** 2 + c ** 2, a ** 2 + b ** 2])
    check(all(J[i, i] + J[j, j] >= J[(6 - i - j) % 3, (6 - i - j) % 3] - 1e-12
              for i, j in ((0, 1), (1, 2), (2, 0))), "§4.4 选读：椭球惯量满足三角形不等式")
    check(close(3.0 / 5 * np.diag([2 * 1.0 ** 2] * 3), 2.0 / 5 * 3.0 * np.eye(3)),
          "§4.4 选读：球极限 J=(2/5)MR²·1")


# ---------------------------------------------------------------- round-04 针对性检查
def round04_scope_checks(tex: str) -> None:
    """round-04 三个数学/阅读问题的针对性检查。

    这里既核对“印出的说法是否自相矛盾”，也把关键对象真的算一遍：
    位置矢量换基点、P9 的全称断言范围、P10 的截面几何。检查脚本不代替证明，
    但也不只是查关键词是否出现。
    """
    print("\n== round-04 针对性检查：位置矢量、P9 断言范围、P10 截面几何 ==")

    # ---- R3-MATH-01 / R3READ-02：三种操作（甲）点坐标 /（乙）两点之差 /（丙）位置矢量
    s27 = _slice(tex, r"\subhdr{2.7", r"\subhdr{2.8")
    check(all(k in s27 for k in ("（甲）", "（乙）", "（丙）")),
          "§2.7 把点坐标、两点之差、位置矢量分成（甲）（乙）（丙）三种操作")
    check("换基点不是换账本" in s27, "§2.7 明确：换基点换的是对象本身，不是换账本")
    check("起点跟着挪" not in tex, "含混的“起点跟着挪，差不变”已删除")
    p6 = _slice(tex, r"\answerstart{P6}{", r"\answerstart{P7}{")
    check(all(k in p6 for k in ("（甲）", "（乙）", "（丙）")),
          "P6 详解按（甲）（乙）（丙）回答，与 §2.7 同一套区分")
    s36 = _slice(tex, r"\subhdr{3.6", r"\hdr{§4}")
    check("\\vect r'=\\vect r-\\vect a" in s36 and "换的是箭头的起点" in s36,
          "§3.6 的平移规则与 §2.7（丙）一致：r'=r−a，换的是箭头的起点")
    # 数值核对：同一物理点 P，基点从 O 移到 O+a，位置矢量确实减 a；而两点之差不变
    O, a = v(0.3, -1.2, 2.0), v(1.5, 0.7, -0.4)
    P, Q = v(2.0, 3.0, -1.0), v(-0.5, 4.0, 0.5)
    r_before, r_after = P - O, P - (O + a)
    check(close(r_after, r_before - a), "同一物理点换基点后 r' = r − a（数值核对）")
    check(close((P - (O + a)) - (Q - (O + a)), (P - O) - (Q - O)),
          "两点之差在同一平移下不变（数值核对）")
    check(not close((P + a) - O, P - O),
          "把“点的坐标平移”与“换基点”混为一谈会得到不同结果（对照）")

    # ---- R3-MATH-02：P9 的“不是这个物体的惯量” vs “不可能是任何质量分布的惯量”
    p9 = _slice(tex, r"\answerstart{P9}{", r"\answerstart{P10}{")
    check("不能说得更强" in p9 and "任何质量分布都得不到它" in p9,
          "P9 明确区分“不是这个物体的惯量”与“任何质量分布都得不到”")
    check("不是任何真实质量分布的惯量" not in tex, "P9 的全称断言已撤去")
    check("三角形不等式" in p9, "P9 用三角形不等式说明该具体谱不能是惯量")
    # 四质点例：J=[[2,-1,0],[-1,2,0],[0,0,2]]，谱 1,2,3；x 反号后只翻 J12/J21，谱不变
    pts = [v(1, 1, 0), v(-1, -1, 0), v(0, 0, 1), v(0, 0, -1)]
    m = 0.5
    J4 = sum(m * (np.dot(p, p) * np.eye(3) - np.outer(p, p)) for p in pts)
    check(close(J4, np.array([[2, -1, 0], [-1, 2, 0], [0, 0, 2]], float)),
          "四质点例：按构造式算出 J=[[2,−1,0],[−1,2,0],[0,0,2]]")
    pts2 = [v(-1, 1, 0), v(1, -1, 0), v(0, 0, 1), v(0, 0, -1)]
    J4s = sum(m * (np.dot(p, p) * np.eye(3) - np.outer(p, p)) for p in pts2)
    check(close(J4s, np.array([[2, 1, 0], [1, 2, 0], [0, 0, 2]], float)),
          "四质点例：x 反号后只翻 J12/J21，得到 [[2,1,0],[1,2,0],[0,0,2]]")
    check(close(np.sort(np.linalg.eigvalsh(J4s)), np.sort(np.linalg.eigvalsh(J4))),
          "四质点例：翻符号后的矩阵与原来同谱（1,2,3），说明“谱一定变”不成立")
    # 单质点例：J'=m[[2,1,-1],[1,2,-1],[-1,-1,2]]，谱 {1,1,4}，违反 I1+I2>=I3
    A = np.array([[2, 1, -1], [1, 2, -1], [-1, -1, 2]], float)
    ev = np.sort(np.linalg.eigvalsh(A))
    check(close(ev, v(1, 1, 4)), "单质点例：J'=mA 的谱是 {1,1,4}")
    check(ev[0] + ev[1] < ev[2] - 1e-12,
          "该谱违反 I1+I2>=I3（1+1<4），所以它不可能是任何质量分布的惯量")
    s8 = _slice(tex, r"\warnbox{\textbf{八个高频错误}", r"\begin{center}")
    check("同一基点" in s8 and "可能碰巧同谱" in s8,
          "§8 第 5 条同步收窄：只否认“这个物体在同一基点下的惯量”，承认可能同谱")

    # ---- R3-MATH-03：P10 的角度参数、截面族与相反法向
    p10 = _slice(tex, r"\answerstart{P10}{", r"\answerstart{P11}{")
    check("同一个截面换了法向" not in tex, "P10 的“45°/135° 是同一截面反法向”已删除")
    check("互相垂直" in p10 and "两个不同截面" in p10,
          "P10 明确 45° 与 135° 的法向互相垂直，对应两个不同截面")
    n = lambda deg: v(math.cos(math.radians(deg)), math.sin(math.radians(deg)), 0.0)
    check(abs(float(np.dot(n(45), n(135)))) < 1e-12,
          "n(45°)·n(135°)=0：两者垂直，不互为反号")
    check(close(n(225), -n(45)) and close(n(315), -n(135)),
          "反法向是 45°↔225°、135°↔315°（相差 180°）")
    sigma0 = 3.7
    tau = lambda deg: abs(sigma0 * math.sin(math.radians(deg)) * math.cos(math.radians(deg)))
    okmax = all(close(tau(d), sigma0 / 2, 1e-12) for d in (45, 135, 225, 315))
    check(okmax, "四个参数值都达到同一最大值 σ0/2（τ=(σ0/2)|sin2θ|）")
    check(abs(tau(41) - sigma0 / 2) > 1e-3, f"θ=41° 不是最大（τ={tau(41):.4f}）")
    def plane_key(u):
        u = np.asarray(u, float)
        u = u / np.linalg.norm(u)
        for c in u:
            if abs(c) > 1e-9:
                if c < 0:
                    u = -u
                break
        return tuple(np.round(u, 8))

    planes = {plane_key(n(45)), plane_key(n(135)), plane_key(n(225)), plane_key(n(315))}
    check(len(planes) == 2, f"按无向截面计数只有 2 个不同的平面（实际 {len(planes)}）")
    tn = lambda deg: sigma0 * math.cos(math.radians(deg)) ** 2
    check(close(tn(45), sigma0 / 2, 1e-12) and close(tn(135), sigma0 / 2, 1e-12),
          "45° 与 135° 两个截面上法向应力都是 σ0/2")

    # ---- R3READ-01：§0.2 的右手基示例只用当时已建立的工具
    s02 = _slice(tex, r"\warnbox{\textbf{这一整套公式只在右手基下成立", r"\subhdr{0.3")
    check("\\det" not in s02 and "operatorname{diag}" not in s02 and "\\ten R" not in s02,
          "§0.2 右手基示例不再提前使用矩阵/转置/diag/det")
    check("左手基" in s02 and "\\vect b_1\\times\\vect b_2" in s02,
          "§0.2 用分量式与右手定则直接给出左手基反例")

    # ---- R3READ-03 / R3NAV-01：题型分类与谱分解回指
    check("P10、P11} 是\\textbf{符号推导}" in tex, "§7 把 P10/P11 单列为符号推导")
    check("P1、P2、P3、P4、P12} 要代入" in tex, "§7 只有 P1/P2/P3/P4/P12 归入“代入题目数值”")
    check("P9、P10、P11" not in tex, "§7 不再把 P9/P10/P11 一起说成“要代入题目数值”")
    check("\\S2.5 与 \\S2.8 再把它写成并矢形式" not in tex,
          "谱分解的落点不再误挂 §2.5")
    check("（\\S1.4、\\S2.8）" in tex, "速查表把谱分解指向 §1.4 与 §2.8")

    # ---- 版面结构：图与图注同一不拆块、表顶线随表头
    caps = [m.start() for m in re.finditer(r"\\figcap\{", tex)]
    wrapped = 0
    for c in caps:
        end = tex.find("\\end{center}", c)
        if end > 0 and "\\end{minipage}" in tex[c:end]:
            wrapped += 1
    check(len(caps) == 11 and wrapped == 11,
          f"11 幅图都与图注放在同一个不拆分的块里（{wrapped}/11）")
    guarded = len(re.findall(r"\\needspace\{7\\baselineskip\}\n\\begin\{center\}\n\\tabtop", tex))
    check(guarded == 7, f"7 张可拆页的表格在上粗线前加了空间保护（{guarded}/7）")


def main() -> int:
    if not TEX.exists():
        print(f"[E] 找不到 {TEX}", file=sys.stderr)
        return 1
    tex = TEX.read_text(encoding="utf-8")
    body_checks()
    ellipsoid_checks()
    exercise_checks(tex)
    round04_scope_checks(tex)
    structure_checks()
    print(f"\n合计断言 {CHECKS} 条，失败 {len(FAILS)} 条。")
    if FAILS:
        print("失败项：")
        for f in FAILS:
            print(" -", f)
        return 1
    print("全部断言通过。注意：这只覆盖脚本里实际复算的数值与结构，"
          "不证明谱定理/输运定理/柯西应力等一般推导，也不代替逐页目视与学习者试读。")
    return 0


if __name__ == "__main__":
    sys.exit(main())





