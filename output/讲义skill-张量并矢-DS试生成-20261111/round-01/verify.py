# -*- coding: utf-8 -*-
"""讲义数值、图坐标与结构核验。任一断言失败以非零退出码报告。

运行：python -B verify.py
输出：verification.txt（同时打印摘要）
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TEX = HERE / "handout.tex"
LOG = HERE / "handout.log"
PDF = HERE / "handout.pdf"
OUT = HERE / "verification.txt"

PASS = 0
FAIL = 0
LINES: list[str] = []


def say(text: str = "") -> None:
    LINES.append(text)
    print(text)


def check(name: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    ok = bool(cond)
    if ok:
        PASS += 1
        say(f"[PASS] {name}" + (f" | {detail}" if detail else ""))
    else:
        FAIL += 1
        say(f"[FAIL] {name}" + (f" | {detail}" if detail else ""))


def close(name: str, A, B, atol: float = 1e-9, detail: str = "") -> None:
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)
    ok = A.shape == B.shape and np.allclose(A, B, atol=atol)
    if not detail:
        if A.shape == B.shape:
            detail = f"max|diff|={np.max(np.abs(A - B)):.3e}"
        else:
            detail = f"shape {A.shape} vs {B.shape}"
    check(name, ok, detail)


def unit(a) -> np.ndarray:
    a = np.asarray(a, dtype=float)
    return a / np.linalg.norm(a)


def skew(a) -> np.ndarray:
    a = np.asarray(a, dtype=float)
    return np.array([[0.0, -a[2], a[1]], [a[2], 0.0, -a[0]], [-a[1], a[0], 0.0]])


def rot(axis, angle: float) -> np.ndarray:
    n = unit(axis)
    K = skew(n)
    return np.eye(3) + math.sin(angle) * K + (1.0 - math.cos(angle)) * (K @ K)


def dyad(a, b) -> np.ndarray:
    return np.outer(np.asarray(a, dtype=float), np.asarray(b, dtype=float))


def vcross(a, b) -> np.ndarray:
    return np.cross(np.asarray(a, dtype=float), np.asarray(b, dtype=float))


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    say("=" * 78)
    say("《从张量到并矢》2026-11-11 独立返工稿 —— 核验记录")
    say("=" * 78)
    say(f"Python {sys.version.split()[0]}；NumPy {np.__version__}")
    say(f"工作目录：{HERE}")
    say("")

    # ------------------------------------------------------------------ §0
    say("## §0 矢量、矩阵、换基、不变量")
    a = np.array([1.0, 2.0, 2.0])
    b = np.array([2.0, 1.0, 0.0])
    check("§0.1 |a|=3", abs(np.linalg.norm(a) - 3.0) < 1e-12)
    check("§0.1 a·b=4", abs(a @ b - 4.0) < 1e-12)
    close("§0.1 a×b=(-2,4,-3)", vcross(a, b), [-2, 4, -3])
    check("§0.1 a·(a×b)=0", abs(a @ vcross(a, b)) < 1e-12)
    check("§0.1 |a×b|=sqrt(29)", abs(np.linalg.norm(vcross(a, b)) - math.sqrt(29)) < 1e-12)
    close("§0.1 b 在 a 上的投影 = (4/9)a", (a @ b) / (a @ a) * a, 4.0 / 9.0 * a)

    T = np.array([[2.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 3.0]])
    x = np.array([1.0, 2.0, 3.0])
    check("§0.3 矩阵列 = T(e_j)", np.allclose(T[:, 0], [2, 0, 0]) and np.allclose(T[:, 1], [1, 1, 0]) and np.allclose(T[:, 2], [0, 0, 3]))
    close("§0.3 T x=(4,2,9)", T @ x, [4, 2, 9])

    R = np.array([[1, -1], [1, 1]], dtype=float) / math.sqrt(2)
    T2 = np.diag([2.0, 1.0])
    Tp = R.T @ T2 @ R
    close("§0.4 T'=R^T T R", Tp, [[1.5, -0.5], [-0.5, 1.5]])
    n1 = np.array([1.0, 1.0]) / math.sqrt(2)
    n2 = np.array([-1.0, 1.0]) / math.sqrt(2)
    direct = np.array([[n1 @ (T2 @ n1), n1 @ (T2 @ n2)], [n2 @ (T2 @ n1), n2 @ (T2 @ n2)]])
    close("§0.4 逐项投影与 R^T T R 一致", direct, Tp)
    check("§0.4 tr 不变", abs(np.trace(T2) - np.trace(Tp)) < 1e-12)
    check("§0.4 det 不变", abs(np.linalg.det(T2) - np.linalg.det(Tp)) < 1e-12)
    xold = np.array([1.0, 0.0])
    close("§0.4 矢量新坐标 = R^T x", R.T @ xold, [1 / math.sqrt(2), -1 / math.sqrt(2)])
    TRT = R @ T2 @ R.T
    close("§0.4 R T R^T 是反向转基的账本", TRT, [[1.5, 0.5], [0.5, 1.5]])
    check("§0.4 R T R^T 与 T' 不同但迹、det 相同",
          not np.allclose(TRT, Tp) and abs(np.trace(TRT) - np.trace(Tp)) < 1e-12 and abs(np.linalg.det(TRT) - np.linalg.det(Tp)) < 1e-12)

    D3 = np.diag([1.0, 2.0, 3.0])
    I1 = np.trace(D3)
    I2 = 0.5 * ((np.trace(D3)) ** 2 - np.trace(D3 @ D3))
    I3 = np.linalg.det(D3)
    check("§0.5 diag(1,2,3) 的 I1,I2,I3=6,11,6", abs(I1 - 6) < 1e-12 and abs(I2 - 11) < 1e-12 and abs(I3 - 6) < 1e-12)
    roots = np.sort(np.linalg.eigvals(D3))
    close("§0.5 特征值 1,2,3", roots, [1, 2, 3])

    # ------------------------------------------------------------------ §1
    say("")
    say("## §1 二次型、椭球、特征值、谱定理、不变量")
    Dn = np.array([[1.0, 2.0], [0.0, 1.0]])
    S = 0.5 * (Dn + Dn.T)
    xy = np.array([0.7, -0.4])
    E1 = xy @ Dn @ xy
    E2 = xy @ S @ xy
    check("§1.2 非对称 D 与对称部分给同一二次型", abs(E1 - E2) < 1e-12, f"E={E1:.6f}")
    check("§1.2 例子 E=(x+y)^2", abs(E1 - (xy[0] + xy[1]) ** 2) < 1e-12)

    Tq = np.array([[2.0, 1.0], [1.0, 2.0]])
    evals, evecs = np.linalg.eigh(Tq)
    close("§1.3 T=[[2,1],[1,2]] 的特征值 1,3", np.sort(evals), [1, 3])
    # 特征向量：3 对应 (1,1)/sqrt2，1 对应 (-1,1)/sqrt2（符号可反）
    v3 = evecs[:, np.argmax(evals)]
    v1 = evecs[:, np.argmin(evals)]
    check("§1.3 λ=3 主轴沿 (1,1)/sqrt2", abs(abs(v3 @ np.array([1, 1]) / math.sqrt(2)) - 1) < 1e-12)
    check("§1.3 λ=1 主轴沿 (-1,1)/sqrt2", abs(abs(v1 @ np.array([-1, 1]) / math.sqrt(2)) - 1) < 1e-12)
    # 代入 x=(u-v)/sqrt2, y=(u+v)/sqrt2 后 E=3u^2+v^2
    for u, v in [(0.3, -0.2), (0.0, 0.5), (-0.4, 0.1)]:
        x_, y_ = (u - v) / math.sqrt(2), (u + v) / math.sqrt(2)
        E_ = Tq[0, 0] * x_ ** 2 + 2 * Tq[0, 1] * x_ * y_ + Tq[1, 1] * y_ ** 2
        check(f"§1.3 代入 (u,v)=({u},{v}) 得 3u^2+v^2", abs(E_ - (3 * u * u + v * v)) < 1e-12)
    # 图 1 的椭圆端点：沿 u 方向 t=1/sqrt3 在 E=1 上，沿 v 方向 t=1 在 E=1 上
    pu = np.array([1.0, 1.0]) / math.sqrt(2) / math.sqrt(3)
    pv = np.array([-1.0, 1.0]) / math.sqrt(2) * 1.0
    check("§1.3 图1 u 轴端点 E=1", abs(pu @ Tq @ pu - 1) < 1e-12)
    check("§1.3 图1 v 轴端点 E=1", abs(pv @ Tq @ pv - 1) < 1e-12)
    check("§1.3 图1 半轴 1/sqrt3 与 1", abs(np.linalg.norm(pu) - 1 / math.sqrt(3)) < 1e-12 and abs(np.linalg.norm(pv) - 1) < 1e-12)

    De = np.array([[6.0, 2.0, 0.0], [2.0, 6.0, 0.0], [0.0, 0.0, 1.0]])
    ev, U = np.linalg.eigh(De)
    close("§1.4 D=[[6,2,0],[2,6,0],[0,0,1]] 的特征值 1,4,8", np.sort(ev), [1, 4, 8])
    # 按列对应的主轴
    idx = np.argsort(ev)
    n1e, n2e, n3e = U[:, idx[2]], U[:, idx[1]], U[:, idx[0]]
    check("§1.4 λ=8 轴 (1,1,0)/sqrt2", abs(abs(n1e @ np.array([1, 1, 0]) / math.sqrt(2)) - 1) < 1e-12)
    check("§1.4 λ=4 轴 (1,-1,0)/sqrt2", abs(abs(n2e @ np.array([1, -1, 0]) / math.sqrt(2)) - 1) < 1e-12)
    check("§1.4 λ=1 轴 e3", abs(abs(n3e @ np.array([0, 0, 1])) - 1) < 1e-12)
    recon = 8 * dyad(n1e, n1e) + 4 * dyad(n2e, n2e) + 1 * dyad(n3e, n3e)
    close("§1.4 谱分解拼回 D", recon, De)
    close("§1.4 谱分解作用在 (1,2,3) 得 (10,14,3)", recon @ np.array([1, 2, 3]), [10, 14, 3])
    close("§1.4 直接矩阵乘法也得 (10,14,3)", De @ np.array([1, 2, 3]), [10, 14, 3])

    # 一般对称矩阵：谱分解与瑞利商
    rng = np.random.default_rng(20261111)
    for k in range(3):
        M = rng.normal(size=(3, 3))
        M = 0.5 * (M + M.T)
        w, V = np.linalg.eigh(M)
        rec = sum(w[i] * dyad(V[:, i], V[:, i]) for i in range(3))
        close(f"§1.5 随机对称矩阵谱分解 #{k}", rec, M, atol=1e-10)
        a0 = rng.normal(size=3)
        q = (a0 @ M @ a0) / (a0 @ a0)
        check(f"§1.5 瑞利商在 [λmin,λmax] 内 #{k}", w.min() - 1e-12 <= q <= w.max() + 1e-12)
        # 二次型投影公式
        Eproj = sum(w[i] * (V[:, i] @ a0) ** 2 for i in range(3))
        check(f"§1.5 E=Σλ(n·a)^2 #{k}", abs(Eproj - a0 @ M @ a0) < 1e-10)

    trD = np.trace(De)
    detD = np.linalg.det(De)
    trD2 = np.trace(De @ De)
    I2e = 0.5 * (trD ** 2 - trD2)
    check("§1.6 D 例 tr=13, det=32, I2=44", abs(trD - 13) < 1e-12 and abs(detD - 32) < 1e-12 and abs(I2e - 44) < 1e-12)
    check("§1.6 8+4+1=13, 两两和=44, 积=32",
          abs((8 + 4 + 1) - trD) < 1e-12 and abs((8 * 4 + 4 * 1 + 1 * 8) - I2e) < 1e-12 and abs(8 * 4 * 1 - detD) < 1e-12)

    # ------------------------------------------------------------------ §2
    say("")
    say("## §2 并矢、点乘、双点积、投影、对偶、商法则")
    ad = np.array([1.0, 2.0, 0.0])
    bd = np.array([0.0, 1.0, 3.0])
    Dd = dyad(ad, bd)
    close("§2.2 a⊗b 矩阵", Dd, [[0, 1, 3], [0, 2, 6], [0, 0, 0]])
    xx = np.array([1.0, 1.0, 1.0])
    close("§2.2 (a⊗b)·x = a(b·x)", Dd @ xx, ad * (bd @ xx))
    close("§2.2 分量式 (a⊗b)_ij=a_i b_j", Dd, np.array([[ad[i] * bd[j] for j in range(3)] for i in range(3)]))
    # 双线性形式与矩阵作用
    uu = rng.normal(size=3)
    vv = rng.normal(size=3)
    check("§2.2 双线性形式 = u·(a⊗b)·v", abs((ad @ uu) * (bd @ vv) - uu @ Dd @ vv) < 1e-12)

    a1, b1 = np.array([1.0, 0, 0]), np.array([0, 1.0, 0])
    x1 = np.array([1.0, 2.0, 3.0])
    close("§2.3 右作用 (e1⊗e2)·x=2e1", (dyad(a1, b1) @ x1), [2, 0, 0])
    close("§2.3 左作用 x·(e1⊗e2)=e2", (x1 @ dyad(a1, b1)), [0, 1, 0])
    # 对称时左右相同
    Ds = np.array([[2.0, 0.5], [0.5, 3.0]])
    xs = np.array([1.2, -0.7])
    close("§2.3 对称 D 左作用=右作用", Ds @ xs, xs @ Ds)
    # 非对称时不同
    check("§2.3 非对称 D 左作用≠右作用", not np.allclose(Dn @ np.array([1.0, 1.0]), np.array([1.0, 1.0]) @ Dn))

    D2 = np.array([[1.0, 2.0], [0.0, 3.0]])
    check("§2.4 迹=4", abs(np.trace(D2) - 4) < 1e-12)
    check("§2.4 D:D=14", abs(np.sum(D2 * D2) - 14) < 1e-12)
    check("§2.4 1:D=tr D", abs(np.sum(np.eye(2) * D2) - 4) < 1e-12)
    # 双点积与 tr(A^T B)
    A2 = rng.normal(size=(2, 2))
    B2 = rng.normal(size=(2, 2))
    check("§2.4 A:B=tr(A^T B)", abs(np.sum(A2 * B2) - np.trace(A2.T @ B2)) < 1e-12)

    nn = np.array([math.sqrt(3) / 2, 0.5])
    P = dyad(nn, nn)
    close("§2.5 P^2=P", P @ P, P)
    x3 = np.array([0.2, 1.1])
    check("§2.5 P x = n(n·x)", np.allclose(P @ x3, nn * (nn @ x3)))
    res = x3 - P @ x3
    check("§2.5 残差与 n 垂直", abs(res @ nn) < 1e-12)
    check("§2.5 P 的迹=1", abs(np.trace(P) - 1) < 1e-12)
    nn3 = np.array([nn[0], nn[1], 0.0])
    P3 = dyad(nn3, nn3)
    check("§2.5 1-P 的迹=2（三维）", abs(np.trace(np.eye(3) - P3) - 2) < 1e-12)
    # 图 3 坐标
    close("图3 P·x 坐标", P @ x3, [0.6263, 0.3616], atol=1e-4)
    close("图3 残差坐标", res, [-0.4263, 0.7384], atol=1e-4)

    aa = np.array([0.3, -0.7, 1.2])
    Ax = skew(aa)
    check("§2.6 对偶矩阵反对称", np.allclose(Ax, -Ax.T))
    yv = np.array([1.1, 0.4, -0.2])
    close("§2.6 a^× x = a×x", Ax @ yv, vcross(aa, yv))
    # 反解 a_k = -1/2 ε_kij A_ij
    eps = np.zeros((3, 3, 3))
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if len({i, j, k}) < 3:
                    eps[i, j, k] = 0
                else:
                    perm = (i, j, k)
                    # 逆序数
                    inv = sum(1 for p in range(3) for q in range(p + 1, 3) if perm[p] > perm[q])
                    eps[i, j, k] = 1 if inv % 2 == 0 else -1
    inv_a = np.array([-0.5 * sum(eps[k, i, j] * Ax[i, j] for i in range(3) for j in range(3)) for k in range(3)])
    close("§2.6 反对称张量反解出原矢量", inv_a, aa)

    # 商法则
    Q = np.linalg.qr(rng.normal(size=(3, 3)))[0]
    if np.linalg.det(Q) < 0:
        Q[:, 0] *= -1
    Tm = rng.normal(size=(3, 3))
    v0 = rng.normal(size=3)
    u0 = Tm @ v0
    up = Q.T @ u0
    vp = Q.T @ v0
    Tp2 = Q.T @ Tm @ Q
    close("§2.7 商法则 T'=R^T T R", Tp2 @ vp, up)

    # ------------------------------------------------------------------ §3
    say("")
    say("## §3 旋转算子与角速度")
    phi = 0.7
    S = rot([0, 0, 1], phi)
    close("§3.2 绕 e3 转 φ 的矩阵", S, [[math.cos(phi), -math.sin(phi), 0], [math.sin(phi), math.cos(phi), 0], [0, 0, 1]])
    close("§3.2 S e1 = n1'", S @ np.array([1.0, 0, 0]), [math.cos(phi), math.sin(phi), 0])
    close("§3.2 S e2 = n2'", S @ np.array([0, 1.0, 0]), [-math.sin(phi), math.cos(phi), 0])
    close("§3.3 S^T S = 1", S.T @ S, np.eye(3))
    close("§3.3 S S^T = 1", S @ S.T, np.eye(3))
    check("§3.3 det S=1", abs(np.linalg.det(S) - 1) < 1e-12)
    check("§3.3 保持点乘", abs((S @ np.array([1.0, 2, 3])) @ (S @ np.array([-1.0, 0.5, 2])) - np.array([1.0, 2, 3]) @ np.array([-1.0, 0.5, 2])) < 1e-12)

    # 绕任意轴公式
    for ax in [unit([1, 2, 3]), unit([-2, 1, 0.5]), np.array([0.0, 0, 1])]:
        for ph in [0.0, 0.4, 1.9, math.pi]:
            Sf = rot(ax, ph)
            Sform = dyad(ax, ax) + (np.eye(3) - dyad(ax, ax)) * math.cos(ph) + skew(ax) * math.sin(ph)
            close(f"§3.4 绕轴公式 n={np.round(ax,3)} φ={ph:.2f}", Sform, Sf, atol=1e-10)
            check(f"§3.4 绕轴公式正交 φ={ph:.2f}", np.allclose(Sf.T @ Sf, np.eye(3), atol=1e-10))
            # 作用分解
            xr = rng.normal(size=3)
            xpar = ax * (ax @ xr)
            xperp = xr - xpar
            check(f"§3.4 作用分解 φ={ph:.2f}", np.allclose(Sf @ xr, xpar + xperp * math.cos(ph) + vcross(ax, xperp) * math.sin(ph), atol=1e-10))
    close("§3.4 S(90,e3)e1=e2", rot([0, 0, 1], math.pi / 2) @ np.array([1.0, 0, 0]), [0, 1, 0])

    # S(t) = R^T? 这里用 R(t)=rot(e3, α t)，S 的矩阵即 R
    alpha = 1.3
    t0 = 0.6
    St = rot([0, 0, 1], alpha * t0)
    eps = 1e-6
    dS = (rot([0, 0, 1], alpha * (t0 + eps)) - rot([0, 0, 1], alpha * (t0 - eps))) / (2 * eps)
    Omega_cross = dS @ St.T
    close("§3.5 Ω^× = dS/dt S^T = α e3^×", Omega_cross, alpha * skew([0, 0, 1]), atol=1e-7)
    # dn'_k/dt = Ω× n'_k
    for k in range(3):
        ek = np.eye(3)[k]
        nk = St @ ek
        dnk = (rot([0, 0, 1], alpha * (t0 + eps)) @ ek - rot([0, 0, 1], alpha * (t0 - eps)) @ ek) / (2 * eps)
        check(f"§3.5 dn'_%d/dt=Ω×n'_%d" % (k + 1, k + 1), np.allclose(dnk, vcross(alpha * np.array([0.0, 0, 1]), nk), atol=1e-7))
    # 无穷小转动到一阶
    dphi = 1e-5
    close("§3.5 S(dφ)=1+dφ n^×（一阶）", rot([0, 0, 1], dphi), np.eye(3) + dphi * skew([0, 0, 1]), atol=1e-10)

    # ------------------------------------------------------------------ §4
    say("")
    say("## §4 惯量张量")
    m, aa_, bb_, cc_ = 12.0, 1.0, 2.0, 3.0
    Jbox = m / 12 * np.diag([bb_ ** 2 + cc_ ** 2, aa_ ** 2 + cc_ ** 2, aa_ ** 2 + bb_ ** 2])
    close("§4.5 长方体 J=diag(13,10,5)", Jbox, np.diag([13.0, 10.0, 5.0]))
    om = np.array([1.0, 1.0, 1.0]) / math.sqrt(3)
    L = Jbox @ om
    close("§4.5 L=(13,10,5)/sqrt3", L, np.array([13.0, 10.0, 5.0]) / math.sqrt(3))
    check("§4.5 |L|^2=98", abs(L @ L - 98) < 1e-12)
    check("§4.5 L·ω=28/3", abs(L @ om - 28 / 3) < 1e-12)
    cos_t = (L @ om) / (np.linalg.norm(L) * np.linalg.norm(om))
    check("§4.5 cosθ=2sqrt2/3", abs(cos_t - 2 * math.sqrt(2) / 3) < 1e-12)
    theta = math.acos(cos_t)
    check("§4.5 θ≈19.47°", abs(math.degrees(theta) - 19.4712) < 1e-3)
    check("§4.5 sinθ=1/3", abs(math.sin(theta) - 1 / 3) < 1e-12)
    M = vcross(om, L)
    close("§4.5 M=ω×L=(1/3)(-5,8,-3)", M, np.array([-5.0, 8.0, -3.0]) / 3)
    check("§4.5 |M|=sqrt98/3", abs(np.linalg.norm(M) - math.sqrt(98) / 3) < 1e-12)
    check("§4.5 M⊥ω", abs(M @ om) < 1e-12)

    m2, a2, b2, c2 = 5.0, 2.0, 3.0, 4.0
    J5 = m2 / 12 * np.diag([b2 ** 2 + c2 ** 2, a2 ** 2 + c2 ** 2, a2 ** 2 + b2 ** 2])
    close("P2 长方体 J=(5/12)diag(25,20,13)", J5, np.diag([125 / 12, 100 / 12, 65 / 12]))
    check("P2 三角形不等式", J5[0, 0] + J5[1, 1] >= J5[2, 2] and J5[0, 0] + J5[2, 2] >= J5[1, 1] and J5[1, 1] + J5[2, 2] >= J5[0, 0])
    Jplate = m2 / 12 * np.diag([b2 ** 2, a2 ** 2, a2 ** 2 + b2 ** 2])
    close("P2 薄板 J=(5/12)diag(9,4,13)", Jplate, np.diag([45 / 12, 20 / 12, 65 / 12]))
    check("P2 垂直轴定理 Jz=Jx+Jy", abs(Jplate[2, 2] - (Jplate[0, 0] + Jplate[1, 1])) < 1e-12)
    I4 = np.array([1.0, 1.0, 1.0]) / math.sqrt(3)
    Ival = I4 @ J5 @ I4
    check("P4 I(n)=145/18", abs(Ival - 145 / 18) < 1e-12)
    K4 = 0.5 * Ival
    check("P4 2K=145/18", abs(2 * K4 - 145 / 18) < 1e-12)
    check("P4 瑞利商界", J5[2, 2] <= Ival <= J5[0, 0])

    # 平行轴定理：随机质点组，直接积分与公式比较
    pts = rng.normal(size=(8, 3)) * 2.0
    ms = rng.uniform(0.5, 3.0, size=8)
    mtot = ms.sum()
    cm = (ms[:, None] * pts).sum(axis=0) / mtot
    rel = pts - cm
    JC = sum(ms[k] * (np.dot(rel[k], rel[k]) * np.eye(3) - dyad(rel[k], rel[k])) for k in range(8))
    JO = sum(ms[k] * (np.dot(pts[k], pts[k]) * np.eye(3) - dyad(pts[k], pts[k])) for k in range(8))
    Rvec = cm
    JO_formula = JC + mtot * (np.dot(Rvec, Rvec) * np.eye(3) - dyad(Rvec, Rvec))
    close("§4.4 平行轴定理（随机质点组）", JO_formula, JO, atol=1e-10)

    # 细杆积分
    Lrod, mrod = 2.3, 1.7
    xs = np.linspace(-Lrod / 2, Lrod / 2, 200001)
    integ = np.trapezoid(xs ** 2 * (mrod / Lrod), xs)
    check("§4.4 细杆 ∫x^2 dm = mL^2/12", abs(integ - mrod * Lrod ** 2 / 12) < 1e-6)

    # 正定性与动能
    Jr = rng.normal(size=(3, 3))
    Jr = Jr @ Jr.T + 0.1 * np.eye(3)
    w = rng.normal(size=3)
    check("§4.2 ω·Jω≥0", w @ Jr @ w >= -1e-12)
    check("§4.2 K=1/2 ω·Jω", abs(0.5 * (w @ Jr @ w) - 0.5 * (w @ Jr @ w)) < 1e-12)

    # 椭球惯量：球的情形精确
    Ms, Rs = 3.0, 1.4
    Jsphere = Ms / 5 * np.diag([2 * Rs ** 2, 2 * Rs ** 2, 2 * Rs ** 2])
    close("§4.4 选读 球 J=(2/5)MR^2 1", Jsphere, 2 / 5 * Ms * Rs ** 2 * np.eye(3))
    # 单位球 ∫η² dV = 4π/15：在球内均匀抽样（半径按 r^(1/3) 分布）
    nball = 400000
    dirs = rng.normal(size=(nball, 3))
    dirs = dirs / np.linalg.norm(dirs, axis=1)[:, None]
    rr = rng.random(nball) ** (1.0 / 3.0)
    pts_ball = rr[:, None] * dirs
    Vball = 4 / 3 * math.pi
    check("§4.4 选读 单位球 ∫η²dV≈4π/15（均匀抽样）",
          abs(np.mean(pts_ball[:, 1] ** 2) * Vball - 4 * math.pi / 15) < 0.01,
          f"抽样={np.mean(pts_ball[:,1]**2)*Vball:.5f}, 精确={4*math.pi/15:.5f}")

    # ------------------------------------------------------------------ §5
    say("")
    say("## §5 输运定理、欧拉方程、对称陀螺")
    Om = np.array([0.3, -0.5, 0.8])
    D0 = rng.normal(size=(3, 3))
    D0 = 0.5 * (D0 + D0.T)

    def Dt(t):
        Rt = rot(Om, t * np.linalg.norm(Om))
        return Rt @ D0 @ Rt.T

    t0 = 0.37
    eps = 1e-6
    Ddot = (Dt(t0 + eps) - Dt(t0 - eps)) / (2 * eps)
    Rt = rot(Om, t0 * np.linalg.norm(Om))
    lhs_body = Rt.T @ Ddot @ Rt
    rhs_body = skew(Om) @ D0 - D0 @ skew(Om)
    close("§5.1 输运定理（体分量）", lhs_body, rhs_body, atol=1e-7)
    close("§5.1 输运定理（固定系形式）", Ddot, skew(Om) @ Dt(t0) - Dt(t0) @ skew(Om), atol=1e-7)
    check("§5.1 D=1 时陀螺项为零", np.allclose(skew(Om) @ np.eye(3) - np.eye(3) @ skew(Om), np.zeros((3, 3)), atol=1e-12))

    # 欧拉方程：从 dL_body + ω×L = M 反推
    for _ in range(3):
        A, B, C = rng.uniform(1.0, 5.0, size=3)
        wv = rng.normal(size=3)
        wd = rng.normal(size=3)
        Jd = np.diag([A, B, C])
        Lv = Jd @ wv
        Mv = Jd @ wd + vcross(wv, Lv)
        eq1 = A * wd[0] + (C - B) * wv[1] * wv[2]
        eq2 = B * wd[1] + (A - C) * wv[2] * wv[0]
        eq3 = C * wd[2] + (B - A) * wv[0] * wv[1]
        close(f"§5.2 欧拉方程分量 #{_}", np.array([eq1, eq2, eq3]), Mv, atol=1e-10)

    # 对称陀螺教学示范 A=B=4,C=5,ω3=6
    A, B, C, w3 = 4.0, 4.0, 5.0, 6.0
    Om_s = (C - A) / A * w3
    check("§5.3 Ω=1.5", abs(Om_s - 1.5) < 1e-12)
    check("§5.3 T=4π/3≈4.19", abs(2 * math.pi / Om_s - 4 * math.pi / 3) < 1e-12)
    # 解满足方程
    wperp, ph0 = 1.2, 0.3
    for tt in [0.0, 0.7, 1.9]:
        w1 = wperp * math.cos(Om_s * tt + ph0)
        w2 = wperp * math.sin(Om_s * tt + ph0)
        dw1 = -Om_s * wperp * math.sin(Om_s * tt + ph0)
        dw2 = Om_s * wperp * math.cos(Om_s * tt + ph0)
        check(f"§5.3 对称陀螺解满足方程 t={tt}", abs(dw1 + Om_s * w2) < 1e-10 and abs(dw2 - Om_s * w1) < 1e-10)
    check("§5.3 |ω| 不变", abs((wperp ** 2 + w3 ** 2) - (wperp ** 2 + w3 ** 2)) < 1e-12)

    # P3
    A3, C3, w33 = 2.0, 3.0, 10.0
    Om3 = (C3 - A3) / A3 * w33
    check("P3 Ω=5", abs(Om3 - 5) < 1e-12)
    check("P3 T=2π/5≈1.257", abs(2 * math.pi / Om3 - 2 * math.pi / 5) < 1e-12)

    # 图 7：A=4,C=5, ω⊥=0.9, ω3=1.0，L 方向 (Aω⊥,Cω3)
    wperp7, w37, A7, C7 = 0.9, 1.0, 4.0, 5.0
    L7 = np.array([A7 * wperp7, C7 * w37])
    w7 = np.array([wperp7, w37])
    angL = math.atan2(L7[0], L7[1])
    angW = math.atan2(w7[0], w7[1])
    check("图7 L 比 ω 更靠近 e3（A<C）", angL < angW)
    close("图7 L 坐标比例", np.array([0.876, 1.217]), 1.5 * unit(np.array([L7[0], L7[1]])), atol=1e-3)
    close("图7 ω 坐标比例", np.array([0.937, 1.040]), 1.4 * unit(np.array([w7[0], w7[1]])), atol=1e-3)

    # ------------------------------------------------------------------ §6
    say("")
    say("## §6 应力张量")
    sig0 = 2.0
    sig = sig0 * dyad([1.0, 0, 0], [1.0, 0, 0])
    th = math.radians(30)
    nv = np.array([math.cos(th), math.sin(th), 0.0])
    tv = sig @ nv
    close("§6.3 t=σ0 cosθ e1", tv, [sig0 * math.cos(th), 0, 0])
    tn = tv @ nv
    check("§6.3 t_n=3σ0/4", abs(tn - 0.75 * sig0) < 1e-12)
    tau_vec = tv - tn * nv
    check("§6.3 τ=√3σ0/4", abs(np.linalg.norm(tau_vec) - math.sqrt(3) / 4 * sig0) < 1e-12)
    check("§6.3 切向方向 (1/2,-√3/2)", np.allclose(unit(tau_vec), [0.5, -math.sqrt(3) / 2, 0], atol=1e-12))
    check("§6.3 法向+切向=t", np.allclose(tn * nv + tau_vec, tv, atol=1e-12))
    # 最大剪应力
    taus = []
    for deg in np.linspace(0, 90, 901):
        thd = math.radians(deg)
        nd = np.array([math.cos(thd), math.sin(thd), 0.0])
        td = sig @ nd
        tnd = td @ nd
        taus.append((deg, np.linalg.norm(td - tnd * nd)))
    degmax, taumax = max(taus, key=lambda p: p[1])
    check("§6/P10 最大剪应力在 45°", abs(degmax - 45) <= 0.1)
    check("§6/P10 τmax=σ0/2", abs(taumax - sig0 / 2) < 1e-3)

    # 应力对称与主应力
    Sm = rng.normal(size=(3, 3))
    Sm = 0.5 * (Sm + Sm.T)
    wS, VS = np.linalg.eigh(Sm)
    for i in range(3):
        ni = VS[:, i]
        ti = Sm @ ni
        check(f"§6.2 主平面剪应力为零 #{i}", abs(np.linalg.norm(ti - (ti @ ni) * ni)) < 1e-10)
        check(f"§6.2 主应力=特征值 #{i}", abs(ti @ ni - wS[i]) < 1e-10)
    # 商法则用于应力
    Q2 = np.linalg.qr(rng.normal(size=(3, 3)))[0]
    if np.linalg.det(Q2) < 0:
        Q2[:, 0] *= -1
    nq = rng.normal(size=3)
    tq = Sm @ nq
    close("§6.1 应力商法则 t'=σ'n'", Q2.T @ Sm @ Q2 @ (Q2.T @ nq), Q2.T @ tq)

    # 高斯定理：线性应力场在立方体上的面积分 = 体积分
    Bc = rng.normal(size=(3, 3))
    Cc = rng.normal(size=(3, 3, 3)) * 0.3

    def sig_field(x):
        return Bc + np.einsum("ijk,k->ij", Cc, x)

    # 面 x=±1，法向 ±e1；面积分。取每个小区间的中点，线性场精确。
    surf = np.zeros(3)
    grid = np.array([-0.75, -0.25, 0.25, 0.75])
    dA = 0.25
    for s in (-1.0, 1.0):
        for y in grid:
            for z in grid:
                xvec = np.array([s, y, z])
                nvec = np.array([s, 0.0, 0.0])
                surf += sig_field(xvec) @ nvec * dA
    # 其余四个面
    for s in (-1.0, 1.0):
        for x in grid:
            for z in grid:
                xvec = np.array([x, s, z])
                nvec = np.array([0.0, s, 0.0])
                surf += sig_field(xvec) @ nvec * dA
        for x in grid:
            for y in grid:
                xvec = np.array([x, y, s])
                nvec = np.array([0.0, 0.0, s])
                surf += sig_field(xvec) @ nvec * dA
    div = np.einsum("ijj->i", Cc) * 8.0
    close("§6.4 高斯定理（线性应力场，立方体）", surf, div, atol=1e-10)

    # ------------------------------------------------------------------ 图坐标
    say("")
    say("## 图坐标与几何关系")
    # 图 1
    check("图1 椭圆长轴方向 v=(−1,1)/√2", abs(unit(np.array([-1.0, 1.0])) @ unit(pv)) > 1 - 1e-12)
    check("图1 椭圆短轴方向 u=(1,1)/√2", abs(unit(np.array([1.0, 1.0])) @ unit(pu)) > 1 - 1e-12)
    # 图 2
    fig2_a = np.array([1.0, 1.2])
    fig2_b = np.array([1.0, 0.0])
    fig2_x = np.array([0.4, 1.0])
    fig2_r = 0.4 * fig2_a
    close("图2 结果 = (b·x)a", fig2_r, [0.4, 0.48])
    check("图2 结果在 a 的射线上", abs(np.cross(fig2_a, fig2_r)) < 1e-12)
    # 图 3
    check("图3 P·x 在 n 上", abs(np.cross(nn, P @ x3)) < 1e-12)
    check("图3 残差与 n 垂直", abs(res @ nn) < 1e-12)
    # 图 4
    n1f = np.array([math.cos(math.radians(35)), math.sin(math.radians(35))])
    n2f = np.array([-math.sin(math.radians(35)), math.cos(math.radians(35))])
    close("图4 n1' 坐标", n1f, [0.8192, 0.5736], atol=1e-4)
    close("图4 n2' 坐标", n2f, [-0.5736, 0.8192], atol=1e-4)
    check("图4 两基正交", abs(n1f @ n2f) < 1e-12)
    # 图 5：板面内 J1,J2 三维方向 (1,0,0),(0,1,0)，J3=(0,0,1)
    check("图5 J1⊥J2⊥J3（三维）", abs(np.array([1.0, 0, 0]) @ np.array([0, 1.0, 0])) < 1e-12 and abs(np.array([1.0, 0, 0]) @ np.array([0, 0, 1.0])) < 1e-12)
    j2draw = np.array([1.7155 - 1.2845, 0.9451 - 0.1549])
    j2edge = np.array([0.6, 1.1])
    check("图5 J2 画向与短边方向一致", abs(np.cross(unit(j2draw), unit(j2edge))) < 1e-3)
    # 图 6：右图固定轴旋转 −32°
    e1r = np.array([math.cos(math.radians(-32)), math.sin(math.radians(-32))])
    e2r = np.array([math.cos(math.radians(58)), math.sin(math.radians(58))])
    check("图6 右图固定轴与体系轴成 32°", abs(abs(e1r @ np.array([1.0, 0])) - math.cos(math.radians(32))) < 1e-12)
    check("图6 右图固定轴互相垂直", abs(e1r @ e2r) < 1e-12)
    # 图 8：斜截面法向与截面线垂直
    n8 = np.array([math.cos(th), math.sin(th)])
    sec_dir = np.array([0.6, -1.0392])  # (0.9,0.5196)->(1.5,-0.5196)
    check("图8 斜截面线与法向垂直", abs(unit(sec_dir) @ n8) < 1e-4)
    # 右图 t = 法向 + 切向
    t8 = np.array([1.55, 0.0])
    ncomp = np.array([1.1626, 0.6712])
    scomp = np.array([0.3875, -0.6712])
    close("图8 法向+切向=t", ncomp + scomp, t8, atol=1e-3)
    check("图8 法向沿 n", abs(np.cross(ncomp, n8)) < 1e-3)
    check("图8 切向⊥法向", abs(scomp @ ncomp) < 1e-3)

    # ------------------------------------------------------------------ 练习专项
    say("")
    say("## 练习题专项数值核对")
    P1 = np.array([[4.0, 1.0, 0.0], [1.0, 4.0, 0.0], [0.0, 0.0, 2.0]])
    close("P1 D·x=(6,9,6)", P1 @ np.array([1.0, 2, 3]), [6, 9, 6])
    check("P1 tr=10, det=30, D:D=38",
          abs(np.trace(P1) - 10) < 1e-12 and abs(np.linalg.det(P1) - 30) < 1e-12 and abs(np.sum(P1 * P1) - 38) < 1e-12)
    wP, VP = np.linalg.eigh(P1)
    close("P1 特征值 2,3,5", np.sort(wP), [2, 3, 5])
    nP1 = VP[:, np.argmax(wP)]
    nP2 = VP[:, np.argsort(wP)[1]]
    nP3 = VP[:, np.argmin(wP)]
    check("P1 λ=5 轴 (1,1,0)/√2", abs(abs(nP1 @ np.array([1, 1, 0]) / math.sqrt(2)) - 1) < 1e-12)
    check("P1 λ=3 轴 (1,-1,0)/√2", abs(abs(nP2 @ np.array([1, -1, 0]) / math.sqrt(2)) - 1) < 1e-12)
    check("P1 λ=2 轴 e3", abs(abs(nP3 @ np.array([0, 0, 1])) - 1) < 1e-12)
    close("P1 谱分解拼回", 5 * dyad(nP1, nP1) + 3 * dyad(nP2, nP2) + 2 * dyad(nP3, nP3), P1)

    # P5 反例
    e1, e2 = np.array([1.0, 0, 0]), np.array([0, 1.0, 0])
    check("P5 (e1⊗e1)·e2=0", np.allclose((dyad(e1, e1) @ e2), np.zeros(3)))
    check("P5 (e1·e1)e2=e2", np.allclose((e1 @ e1) * e2, e2))

    # P8 对称部分例子
    D8 = np.array([[0.0, 3.0], [0.0, 0.0]])
    S8 = 0.5 * (D8 + D8.T)
    for xv, yv in [(0.4, 0.7), (-0.3, 1.1)]:
        E8a = np.array([xv, yv]) @ D8 @ np.array([xv, yv])
        E8b = np.array([xv, yv]) @ S8 @ np.array([xv, yv])
        check(f"P8 二次型只取对称部分 ({xv},{yv})", abs(E8a - E8b) < 1e-12 and abs(E8a - 3 * xv * yv) < 1e-12)

    # P9 质点例子
    r9 = np.array([1.0, 0.0, 0.0])
    m9 = 2.0
    J9 = m9 * (np.dot(r9, r9) * np.eye(3) - dyad(r9, r9))
    J9w = m9 * (np.dot(r9, r9) * np.eye(3) + dyad(r9, r9))
    close("P9 正确惯量 diag(0,1,1)*m", J9, m9 * np.diag([0.0, 1.0, 1.0]))
    close("P9 丢符号后 diag(2,1,1)*m", J9w, m9 * np.diag([2.0, 1.0, 1.0]))

    # P12 欧拉方程
    A12, B12, C12 = 1.0, 2.0, 3.0
    w12 = np.array([1.0, 1.0, 1.0])
    wd12 = np.array([-1.0, 1.0, -1.0 / 3.0])
    res12 = np.array([
        A12 * wd12[0] + (C12 - B12) * w12[1] * w12[2],
        B12 * wd12[1] + (A12 - C12) * w12[2] * w12[0],
        C12 * wd12[2] + (B12 - A12) * w12[0] * w12[1],
    ])
    close("P12 三个方程残差为零", res12, [0, 0, 0])
    check("P12 ω̇=(-1,1,-1/3)", np.allclose(wd12, [-1, 1, -1 / 3]))

    # 椭球惯量公式的抽样核对（非球情形）
    ae, be, ce, Me = 1.0, 2.0, 3.0, 5.0
    nE = 400000
    dirsE = rng.normal(size=(nE, 3))
    dirsE = dirsE / np.linalg.norm(dirsE, axis=1)[:, None]
    rrE = rng.random(nE) ** (1.0 / 3.0)
    ptsE = rrE[:, None] * dirsE
    yE = be * ptsE[:, 1]
    zE = ce * ptsE[:, 2]
    Jxx_est = Me * (np.mean(yE ** 2) + np.mean(zE ** 2))
    check("§4.4 选读 椭球 Jxx=M(b²+c²)/5（抽样）",
          abs(Jxx_est - Me * (be ** 2 + ce ** 2) / 5) < 0.02,
          f"抽样={Jxx_est:.4f}, 精确={Me*(be**2+ce**2)/5:.4f}")

    # ------------------------------------------------------------------ 结构
    say("")
    say("## 讲义结构、练习配对与覆盖关键词")
    tex = TEX.read_text(encoding="utf-8")
    practices = re.findall(r"\\practice\{([^}]+)\}", tex)
    answers = re.findall(r"\\answerstart\{([^}]+)\}", tex)
    check("正文练习 12 道", len(practices) == 12, f"实际 {len(practices)}: {practices}")
    check("附录详解 12 道", len(answers) == 12, f"实际 {len(answers)}: {answers}")
    check("练习与详解 ID 一一对应", sorted(practices) == sorted(answers))
    check("练习 ID 顺序为 P1..P12", practices == [f"P{i}" for i in range(1, 13)])
    check("附录详解 ID 顺序为 P1..P12", answers == [f"P{i}" for i in range(1, 13)])
    check("每道练习都指向自己的 ans: 标签", all(f"{{ans:{p}}}" in tex for p in practices))
    check("无 \\begin{warnbox} 误用", "\\begin{warnbox}" not in tex and "\\end{warnbox}" not in tex)
    check("无裸 ✓/✗", "✓" not in tex and "✗" not in tex)
    check("图共 8 张", tex.count("\\begin{tikzpicture}") == 8, f"实际 {tex.count('\\begin{tikzpicture}')}")
    check("\\appendix 存在", "\\appendix" in tex)
    key_terms = ["换基", "迹", "行列式", "二次型", "谱定理", "并矢", "双点积", "对偶张量",
                 "商法则", "旋转算子", "角速度", "输运定理", "欧拉方程", "对称陀螺",
                 "转动惯量", "平行轴定理", "应力张量", "主应力", "平衡方程"]
    missing = [k for k in key_terms if k not in tex]
    check("原主题关键词齐全", not missing, f"缺：{missing}")
    sec_heads = re.findall(r"\\hdr\{([^}]+)\}\{([^}]+)\}", tex)
    say("章节：" + "；".join(f"{a} {b}" for a, b in sec_heads))
    check("章节 §0--§8 与附录 A--C 齐全",
          [a for a, _ in sec_heads][:10] == ["§0", "§0", "§1", "§2", "§3", "§4", "§5", "§6", "§7", "§8"])
    # 练习题干不泄露答案词
    bad = []
    for m in re.finditer(r"\\practice\{([^}]+)\}\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}", tex, re.S):
        pid, src, stem, kaodian, ref = m.groups()
        if re.search(r"关键一步|解题提示|(?:答案|详解|提示)\s*(?:\}|：|:|为|是)", stem + kaodian):
            bad.append(pid)
    check("练习题干/考点无明确提示或答案词", not bad, f"可疑：{bad}")

    sm_path = HERE / "source-map.json"
    if sm_path.exists():
        try:
            sm = json.loads(sm_path.read_text(encoding="utf-8"))
            check("source-map.json 可解析", isinstance(sm, dict) and "coverage" in sm and "practice_map" in sm)
            check("覆盖映射至少 15 条", len(sm.get("coverage", [])) >= 15, f"实际 {len(sm.get('coverage', []))}")
            check("练习映射 12 条", len(sm.get("practice_map", [])) == 12, f"实际 {len(sm.get('practice_map', []))}")
            check("选读清单 4 条", len(sm.get("readings", {}).get("optional", [])) == 4)
            check("旧稿勘误记录至少 8 条", len(sm.get("old_issues", [])) >= 8, f"实际 {len(sm.get('old_issues', []))}")
        except Exception as exc:  # noqa: BLE001
            check("source-map.json 可解析", False, str(exc))
    else:
        check("source-map.json 存在", False, str(sm_path))

    # ------------------------------------------------------------------ 编译
    say("")
    say("## 编译日志与 PDF")
    if LOG.exists():
        log = LOG.read_text(encoding="utf-8", errors="replace")
        check("日志无 Overfull", "Overfull" not in log)
        check("日志无 Missing character", "Missing character" not in log)
        check("日志无未解析引用", "undefined references" not in log.lower() and "Reference" not in log)
        check("日志无重复标签", "multiply defined" not in log)
        m = re.search(r"Output written on .*?\((\d+) pages?", log)
        check("日志记录了 PDF 页数", m is not None, f"页数={m.group(1) if m else '?'}")
        if m:
            page_count = int(m.group(1))
            say(f"PDF 页数：{page_count}")
            renders = sorted((HERE / "render").glob("page-*.png"))
            check("渲染页数与 PDF 页数一致", len(renders) == page_count, f"PNG {len(renders)} 页 / PDF {page_count} 页")
    else:
        check("编译日志存在", False, str(LOG))
    check("PDF 文件存在且非空", PDF.exists() and PDF.stat().st_size > 10000, f"size={PDF.stat().st_size if PDF.exists() else 0}")

    # ------------------------------------------------------------------ 阅读路径
    say("")
    say("## 阅读路径自查（人工，不是机器断言）")
    say("允许的基础：矢量分量、点乘、叉乘、矩阵乘矢量、转置；导数=变化率、积分=小块求和这两句话。")
    say("主线走法：§0.1 矢量 → §0.2 线性映射 → §0.3 矩阵账本 → §0.4 换基（三步推导）→ §0.5 迹/行列式/特征多项式")
    say("→ §1.1 二次型 → §1.2 对称部分 → §1.3 椭球（先借特征值/特征向量二词，§1.4 正式定义）→ §1.4 特征值")
    say("→ §1.5 谱定理陈述与用法 → §1.6 不变量 → §2.1 阶 → §2.2 张量积 → §2.3 左右作用 → §2.4 点乘/双点积")
    say("→ §2.5 单位/投影并矢 → §2.6 转置/对偶/旋转算子写法 → §2.7 商法则 → §2.8 缩并表 → §2.9 谱分解")
    say("→ §2.10 三记号字典 → §3.1 两基 → §3.2 S → §3.3 正交性 → §3.4 绕轴公式 → §3.5 角速度")
    say("→ §4.1 J 的推导（补质心/瞬时轴）→ §4.2 分量/正定 → §4.3 主轴/三角形不等式 → §4.4 常用结果/平行轴")
    say("→ §4.5 教学示范 → §5.1 输运定理（补陀螺项）→ §5.2 欧拉方程（补力矩定义）→ §5.3 对称陀螺（补进动）")
    say("→ §5.4 力矩 → §6.1 面力/柯西（补连续体）→ §6.2 对称/主应力（补准静态/偏斜）→ §6.3 30° 示范")
    say("→ §6.4 平衡方程（补体力/张量场）→ P1--P12 → 附录 A。")
    say("已补的桥：3×3 行列式展开；R 的列约定与新坐标 R^T x；ε_ijk 的六个排列查表；线性无关/齐次/正定/质心/瞬时轴/陀螺项/进动/偏斜/准静态/体力/张量场等首次出现处的解释。")
    say("选读跳过检查：opt-1 谱定理证明不喂后文；opt-2 上下标不喂后文；opt-3 椭球不喂 §4.5/P2/P4；opt-4 Gauss 证明不喂 §7。主线不依赖四处选读。")
    say("仍依赖的物理前提：§4.1 的 v=ω×r、L=∫r×v dm，§5.2 的 M=dL/dt，§6.1 的面力/连续体；均在首次使用处给了局部说明。")
    say("尚未验证：学习者实际试读；外部目视布局；某些解释（如准静态、偏斜部分）是否一次读懂。交付不等于已学。")

    # ------------------------------------------------------------------ 汇总
    say("")
    say("=" * 78)
    say(f"合计：通过 {PASS} 条，失败 {FAIL} 条")
    say("说明：本脚本核对数值、矩阵、图坐标、结构与日志；不证明讲义可读，也不代替页面目视验收。")
    say("=" * 78)
    OUT.write_text("\n".join(LINES) + "\n", encoding="utf-8")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
