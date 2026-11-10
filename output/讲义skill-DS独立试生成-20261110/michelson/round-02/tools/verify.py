# -*- coding: utf-8 -*-
r"""round-02 讲义：数值、推导与图 4 几何的可复现核验（不代替内容审校）。

用法：python -B michelson/round-02/tools/verify.py
每条断言失败即打印 [FAIL] 并以退出码 1 结束；全部通过时打印断言条数。
本轮重点：
  M01 整数级次 k 与环号 m 的编号方向、相邻级次相减的符号与正间距；
  M02 工作式 lambda=dl/(10N) 的单位（毫米输入先得毫米，换米乘 1e-3）；
  M04 图 4 的 z 从两虚光源中点 M 量起、theta 顶点在 M、有符号光程差与正文一致；
  M05 附加相位 delta0 与理想亮纹条件 (11-1) 分开；
  M06 固定 I1+I2 时等分只提高可见度/峰值，不提高相位平均总强度；
  M07 源资料 0.01 mm 对应关系不等于最小分度，分歧只作说明用假设；
  M08 G2 只补偿玻璃路程，不消除可调 2d；
  M09 thinner/denser 与 Delta r 公式方向自洽（用词疑点，不是数学冲突）。
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "handout.tex"

LAM = 632.8e-9          # He-Ne 真空波长（示例取值）
LAM_NA = 589.3e-9       # 钠黄光（示例取值）
Z = 1.00                # 屏到虚光源中点的距离（示例设定）
K0 = 316                # 例 3.2 的中心整数级次
D = K0 * LAM / 2        # 使中心恰为亮纹的理想膜厚（delta0=0 约定）

checks = 0
fails: list[str] = []


def ok(cond: bool, msg: str) -> None:
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def close(a: float, b: float, tol: float, msg: str) -> None:
    ok(abs(a - b) <= tol, f"{msg}：得到 {a:.10g}，应为 {b:.10g}（容差 {tol:g}）")


def r_order(k: float, d: float = D, z: float = Z) -> float:
    """第 k 级亮环半径（delta0=0 的理想式 (11-1)）。"""
    return z * math.sqrt(max(0.0, 2.0 * (1.0 - k * LAM / (2.0 * d))))


def r_ring(m: int, d: float = D, z: float = Z) -> float:
    """从中心向外的第 m 个亮环半径（中心亮、k0=2d/lambda 为整数）。"""
    return z * math.sqrt(m * LAM / d)


def figure4_checks() -> None:
    tex = TEX.read_text(encoding="utf-8")
    blocks = re.findall(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", tex, re.S)
    fig = [b for b in blocks if "(S1)" in b and "(M)" in b]
    ok(len(fig) == 1, f"图 4 的 TikZ 块应唯一，实际 {len(fig)} 个")
    if len(fig) != 1:
        return
    block = fig[0]

    def coord(name: str) -> tuple[float, float]:
        m = re.search(
            r"\\coordinate\s*\(" + re.escape(name) + r"\)\s*at\s*\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)",
            block,
        )
        if not m:
            fails.append(f"图 4 找不到坐标 {name}")
            return (float("nan"), float("nan"))
        return (float(m.group(1)), float(m.group(2)))

    S1 = coord("S1")
    S2 = coord("S2")
    M = coord("M")
    P = coord("P")

    # 屏幕：图 4 块内唯一的 1.4pt 竖线
    scr = re.search(
        r"\\draw\[line width=1\.4pt\]\s*\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)\s*--\s*"
        r"\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)",
        block,
    )
    ok(scr is not None, "图 4 找不到屏幕线")
    if scr is None:
        return
    sx0, sy0, sx1, sy1 = (float(scr.group(i)) for i in range(1, 5))
    screen_x = sx0
    close(sx1, sx0, 1e-9, "图 4 屏幕线为竖直线")

    arrows = re.findall(
        r"\\draw\[<->\]\s*\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)\s*--\s*"
        r"\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)",
        block,
    )
    zcands = [tuple(float(v) for v in a) for a in arrows]
    zcands = [a for a in zcands if abs(a[1] - a[3]) < 1e-9 and a[1] < 0]
    ok(len(zcands) == 1, f"图 4 的 z 尺寸线应唯一，实际 {len(zcands)} 条")
    if len(zcands) != 1:
        return
    zx0, zy0, zx1, zy1 = zcands[0]

    arc = re.search(
        r"\\draw\s*\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)\s*arc\s*"
        r"\(\s*([-\d.]+)\s*:\s*([-\d.]+)\s*:\s*([-\d.]+)\s*\)",
        block,
    )
    ok(arc is not None, "图 4 找不到 theta 圆弧")
    if arc is None:
        return
    ax, ay, a0, a1, rad = (float(arc.group(i)) for i in range(1, 6))

    # 中点、尺寸线端点与弧心必须是同一个对象 M
    mx, my = (S1[0] + S2[0]) / 2, (S1[1] + S2[1]) / 2
    close(M[0], mx, 1e-9, "图 4 坐标 M 是 S1、S2' 中点（x）")
    close(M[1], my, 1e-9, "图 4 坐标 M 是 S1、S2' 中点（y）")
    close(zx0, mx, 1e-9, "图 4 的 z 尺寸线起点 x = 中点 M（x）")
    close(zy0, my - 1.05, 1e-9, "图 4 的 z 尺寸线是离轴 1.05 的标注线")
    close(zx1, screen_x, 1e-9, "图 4 的 z 尺寸线终点在屏上")
    close(zx1 - zx0, screen_x - mx, 1e-9, "图 4 的 z 尺寸线长度 = 屏到 M 的距离")

    # TikZ 弧：给定起点与起始角，圆心 = 起点 - R(cos a0, sin a0)
    cx = ax - rad * math.cos(math.radians(a0))
    cy = ay - rad * math.sin(math.radians(a0))
    close(cx, mx, 1e-6, "图 4 的 theta 弧心 = 中点 M（x）")
    close(cy, my, 1e-6, "图 4 的 theta 弧心 = 中点 M（y）")

    # 几何量与正文定义一致
    z_geo = screen_x - mx
    d_geo = abs(S2[0] - S1[0]) / 2.0
    r_geo = P[1] - my
    close(z_geo, 4.08, 1e-9, "图 4 的 z = 4.08（作图坐标）")
    close(d_geo, 0.30, 1e-9, "图 4 的 d = |S1-S2'|/2 = 0.30")
    close(r_geo, 1.00, 1e-9, "图 4 的 r = 1.00")
    theta_geo = math.degrees(math.atan2(P[1] - my, P[0] - mx))
    close(theta_geo, a1, 1e-5, "图 4 的 theta 弧终点角 = atan(r/z)")
    close(theta_geo, math.degrees(math.atan(r_geo / z_geo)), 1e-9, "图 4 的 theta = atan(r/z)")

    # 实际光线长度：有符号差为负，大小与 2d cos(theta) 一致
    s1p = math.hypot(screen_x - S1[0], P[1] - S1[1])
    s2p = math.hypot(screen_x - S2[0], P[1] - S2[1])
    signed = s2p - s1p
    cos_t = z_geo / math.hypot(z_geo, r_geo)
    ok(signed < 0, f"图 4 中 S2'P-S1P 应为负（S2' 离屏更近），得到 {signed:.6f}")
    close(abs(signed) / (2 * d_geo * cos_t), 1.0, 1e-3,
          "图 4 的 |S2'P-S1P| 与 2d cos(theta) 一致")
    # 记录旧错误的量：若 z 从 S2' 量到屏，会短 d=0.30
    close(abs((screen_x - S2[0]) - z_geo), d_geo, 1e-9,
          "图 4 若把 z 从 S2' 量起会差一个 d（本图必须从 M 量起）")
    ok(abs((screen_x - S2[0]) - z_geo) > 0.2, "图 4 的 z 起点不是 S2'（旧稿错误）")


def main() -> int:
    # ---------- M07 / §2.4：20:1 与“最小分度”只作假设 ----------
    close(0.01 / 0.0005, 20.0, 1e-12, "读数:动镜位移 = 20:1（源 p2）")
    close(0.01e-3 / 20, 0.5e-6, 1e-18, "每 0.01 mm 读数对应 0.5 µm 位移")
    one_ring = LAM / 2
    close(one_ring * 1e6, 0.3164, 1e-6, "一个环对应 λ/2 ≈ 0.3164 µm")
    per_interval = one_ring / 0.01e-3
    close(per_interval, 0.03164, 1e-7, "1:1 时一个环只占 0.01 mm 间隔的 1/31.6")
    close(20 * per_interval, 0.6328, 1e-6, "20:1 时一个环占 0.6328 个 0.01 mm 间隔")
    ok(per_interval < 0.05, "1:1 时一个环不到 1/20 个 0.01 mm 间隔，读数不可分辨")

    # ---------- 式 (1)：2d cosθ 的几何推导 ----------
    for theta_deg in (5, 20, 35, 45):
        th = math.radians(theta_deg)
        d = 1.0
        bc_cd = 2 * d / math.cos(th)
        bf = 2 * d * math.tan(th) * math.sin(th)
        close(bc_cd - bf, 2 * d * math.cos(th), 1e-12, f"式(1) 在 θ={theta_deg}° 的恒等变形")

    # ---------- M04：虚光源（z 以中点为起点） ----------
    for r in (0.02, 0.05, 0.12):
        dl_exact = math.sqrt((Z - D) ** 2 + r ** 2) - math.sqrt((Z + D) ** 2 + r ** 2)
        cos_t = Z / math.hypot(Z, r)
        ok(dl_exact < 0, f"虚光源 S2'P-S1P 在 r={r} m 处应为负")
        ok(abs(abs(dl_exact) - 2 * D * cos_t) / (2 * D * cos_t) < 1e-9,
           f"虚光源光程差大小在 r={r} m 处与 2d cosθ 一致")
    figure4_checks()

    # ---------- M05：相位约定与理想级次 ----------
    ok(abs(2 * D / LAM - K0) < 1e-9, "例 3.2 取 2d=316λ（δ0=0 约定的中心亮纹）")
    # δ0=0：2d/λ = 316 为整数 -> 亮；δ0=π：2d/λ + 1/2 = 316.5 非整数 -> 中心暗
    order_delta0_pi = 2 * D / LAM + 0.5
    ok(abs(order_delta0_pi - round(order_delta0_pi)) > 1e-6,
       "若 δ0=π，2d=316λ 不满足整数亮纹条件（中心变暗）")
    ok(abs(K0 - round(K0)) < 1e-12, "δ0=0 时中心亮纹的整数级次 k0=316 成立")

    # ---------- M01：整数级次 k 与环号 m 的方向、正间距 ----------
    ok(abs(D - 99.982e-6) < 1e-9, f"k0=316 时 d=316λ/2={D*1e6:.3f} µm ≈ 0.100 mm")
    close(2 * D / LAM, 316.0, 1e-9, "中心级次 k0=2d/λ")
    # 固定 d：k 越小半径越大
    for k in (310, 314, 315, 316):
        ok(r_order(k - 1) > r_order(k),
           f"固定 d 时 r_(k-1) > r_k（k={k}），即 k 越小半径越大")
    # 相邻级次相减的符号：r_k^2 - r_(k-1)^2 = -λz^2/d
    kk = 315
    minus = r_order(kk) ** 2 - r_order(kk - 1) ** 2
    plus = r_order(kk - 1) ** 2 - r_order(kk) ** 2
    close(minus, -LAM * Z ** 2 / D, 1e-15, "r_k^2 - r_(k-1)^2 = -λz^2/d（符号为负）")
    close(plus, LAM * Z ** 2 / D, 1e-15, "r_(k-1)^2 - r_k^2 = +λz^2/d（较外减较内）")
    ok(r_order(kk - 1) - r_order(kk) > 0, "正的物理间距 = r_(较外) - r_(较内) > 0")
    # 环号 m：r_m 与级次 k=k0-m 一致
    for m in (1, 2, 3, 10):
        close(r_ring(m), r_order(K0 - m), 1e-15, f"环号 m={m} 与级次 k=k0-m 的半径一致")
    # 环号差分的正号
    for m in (2, 5, 20):
        ok(r_ring(m) - r_ring(m - 1) > 0, f"环号 m={m} 的向外间距 r_m-r_(m-1)>0")
        close(r_ring(m) ** 2 - r_ring(m - 1) ** 2, LAM * Z ** 2 / D, 1e-15,
              f"r_m^2-r_(m-1)^2=λz^2/d（m={m}）")

    # ---------- 例 3.2：数值与两种间距式 ----------
    r1, r2 = r_ring(1), r_ring(2)
    close(r1 * 1e3, 79.56, 0.01, "r1（mm）")
    close(r2 * 1e3, 112.51, 0.01, "r2（mm）")
    close(math.degrees(math.atan(r1 / Z)), 4.55, 0.01, "θ1（度）")
    close(math.degrees(math.atan(r2 / Z)), 6.42, 0.01, "θ2（度）")
    close(r1 / Z, 0.0796, 5e-4, "r1/z（rad）")
    close(r2 / Z, 0.1125, 5e-4, "r2/z（rad）")
    ok(r2 / Z < 0.15, f"例 3.2 满足 r≪z 的弱形式：r2/z={r2/Z:.3f} < 0.15")

    dr_exact = r2 - r1
    dr_inner = LAM * Z ** 2 / (2 * D * r1)
    dr_mean = LAM * Z ** 2 / (2 * D * ((r1 + r2) / 2))
    close(dr_exact * 1e3, 32.95, 0.02, "精确环间距 r2-r1（mm）")
    close(dr_inner * 1e3, 39.78, 0.02, "把较内环 r1 代入间距式（mm）")
    ok(dr_inner > dr_exact, "用较内环 r1 代入会偏大")
    close(dr_inner / dr_exact - 1, 0.207, 0.002, "用 r1 代入的相对偏差（20.7%）")
    close(dr_mean, dr_exact, 2e-6, "用平均半径代入与精确值相同（恒等）")
    # 恒等式的符号方向必须与正文一致
    close(r_order(K0 - 2) - r_order(K0 - 1), dr_exact, 1e-15,
          "r_(较外)-r_(较内) 与 r2-r1 是同一个正间距")

    # 同一组数里 ΔL 的近似误差
    dl_exact = 2 * D * math.cos(math.atan(r2 / Z))
    dl_approx = 2 * D * (1 - r2 ** 2 / (2 * Z ** 2))
    close(dl_exact * 1e6, 198.71, 0.01, "ΔL 精确值（µm）")
    close(dl_approx * 1e6, 198.70, 0.01, "ΔL 二级近似（µm）")
    close(abs(dl_exact - dl_approx) / LAM, 0.019, 0.002, "ΔL 近似误差折合条纹数")
    ok(abs(dl_exact - dl_approx) / dl_exact < 1e-4,
       "ΔL 近似相对误差 <1e-4（与间距式的 20% 形成对照）")

    # ---------- 例 3.1：膜厚与环数 ----------
    n1 = 50
    dd1 = n1 * LAM / 2
    close(dd1 * 1e6, 15.82, 0.01, "50 环对应的 Δd（µm）")
    close(20 * dd1 * 1e3, 0.3164, 1e-4, "50 环对应的鼓轮读数差（mm）")
    close((20 * dd1 / 0.01e-3), 31.64, 1e-3, "0.3164 mm 合 31.64 个 0.01 mm 读数间隔")
    close(100 * (LAM / 2) / dd1, 2.0, 0.01, "数错一环对 N=50 的相对影响（%）")

    # ---------- 例 3.3：M02 单位一致性 ----------
    n3, dl3_mm = 500, 3.164             # Δl 以毫米计
    dl3 = dl3_mm * 1e-3                 # 同一读数换成米
    dd3 = dl3 / 20
    close(2 * dd3 / n3 * 1e9, 632.8, 0.05, "由 Δl、N 反算的波长（nm）")
    lam_mm = dl3_mm / (10 * n3)         # 输入 mm，结果 mm
    close(lam_mm, 6.328e-4, 1e-12, "λ=Δl/(10N) 在 Δl 用毫米时先得毫米")
    close(lam_mm * 1e-3 * 1e9, 632.8, 0.05, "毫米结果乘 1e-3 换米后为 632.8 nm")
    close(lam_mm / (632.8e-9), 1000.0, 1e-6,
          "若把 6.328e-4 直接当作米，会比真值大 1000 倍（旧口径错误）")
    close(1e5 * dl3_mm / n3, 632.8, 0.05, "λ[nm]=1e5·Δl[mm]/N")
    dd_na = n3 * LAM_NA / 2
    close(20 * dd_na * 1e3, 2.947, 0.001, "钠光 500 环应移动的读数（mm）")
    close(100 * (2.947 / 3.164 - 1), -6.85, 0.05, "两光源读数差相对差（%）")
    close(10 * 160 * LAM * 1e3, 1.0125, 1e-4, "ΔN=160 时读数差约 1.0125 mm")

    # ---------- M06：可见度 vs 总强度 ----------
    def vis(i1: float, i2: float) -> float:
        return 2 * math.sqrt(i1 * i2) / (i1 + i2)

    S = 10.0
    close(vis(5, 5), 1.0, 1e-12, "I1=I2=5 时 V=1")
    close(vis(9, 1), 0.6, 1e-12, "I1:I2=9:1 时 V=0.6")
    close(4 / 16, 0.25, 1e-12, "9:1 时暗纹/亮纹强度 = 0.25")
    imax_eq, imin_eq = S + 2 * math.sqrt(25), S - 2 * math.sqrt(25)
    imax_91, imin_91 = S + 2 * math.sqrt(9), S - 2 * math.sqrt(9)
    close(imax_eq, 20.0, 1e-12, "等分时亮纹峰值 Imax=20（S=10 固定）")
    close(imax_91, 16.0, 1e-12, "9:1 时亮纹峰值 Imax=16")
    close(imin_eq, 0.0, 1e-12, "等分时暗纹谷值 Imin=0")
    close(imin_91, 4.0, 1e-12, "9:1 时暗纹谷值 Imin=4")
    ok(imax_eq > imax_91 and imin_eq < imin_91, "固定 I1+I2 时等分使峰值最大、谷值最小")
    # 相位平均总强度始终等于 I1+I2
    for i1 in (1, 3, 5, 7, 9):
        close(i1 + (S - i1), S, 1e-12, f"相位平均总强度 = I1+I2 = {S}（与分配无关）")
    # 等分确实最大化 Imax（数值抽样）
    for i1 in (1, 2, 3, 4):
        ok(S + 2 * math.sqrt(i1 * (S - i1)) < imax_eq,
           f"固定 S 时 I1={i1} 的 Imax 小于等分值")
    ok(vis(1, 1) > vis(9, 1) > vis(99, 1), "V 随强度比变差而下降")

    # ---------- M08：G2 只补玻璃路程 ----------
    t, n_glass = 1e-3, 1.5
    glass_before = (3 * t - 1 * t) * (n_glass - 1)   # 3 次 vs 1 次玻璃
    glass_after = ((1 * t + 2 * t) - 3 * t) * (n_glass - 1)  # G2 给 II 臂加 2 次
    close(glass_before, 2 * t * (n_glass - 1), 1e-18, "无 G2 时玻璃光程差 = 2t(n-1)")
    close(glass_after, 0.0, 1e-18, "有 G2 后玻璃光程差 = 0")
    close(glass_before * 1e3, 1.0, 1e-12, "t=1 mm、n=1.5 时玻璃光程差 = 1.0 mm")
    # 总光程差仍随 d 变：G2 不能消除 2d
    d1, d2 = 100e-6, 110e-6
    total1 = 2 * d1 * math.cos(math.radians(5))
    total2 = 2 * d2 * math.cos(math.radians(5))
    ok(abs(total2 - total1) > 1e-6, "改变 d 仍改变总光程差（G2 不能消除 2d）")

    # ---------- M09：thinner/denser 与公式方向自洽 ----------
    dr_at = lambda d, r: LAM * Z ** 2 / (2 * d * r)
    ok(dr_at(D / 4, 0.05) > dr_at(D, 0.05), "d 越小 Δr 越大（条纹更疏）")
    close(dr_at(D / 4, 0.05) / dr_at(D, 0.05), 4.0, 1e-12, "Δr ∝ 1/d")
    ok((dr_at(D / 4, 0.05) > dr_at(D, 0.05)) == True,
       "源 p5 的 smaller d -> thinner 读作“更疏”时与公式一致")

    # ---------- 图 3 的作图坐标与公式一致 ----------
    d_fig, th = 1.2, math.radians(35)
    Cx, Cy = d_fig * math.tan(th), -d_fig
    Dx = 2 * d_fig * math.tan(th)
    tF = 2 * d_fig * math.tan(th) * math.sin(th)
    Fx, Fy = tF * math.sin(th), tF * math.cos(th)
    close(Cx, 0.84, 5e-3, "图3 C 点横坐标 d tanθ")
    close(Cy, -1.2, 5e-3, "图3 C 点纵坐标 -d")
    close(Dx, 1.68, 5e-3, "图3 D 点横坐标 2d tanθ")
    close(Fx, 0.5526, 2e-3, "图3 F 点横坐标（TikZ 代码值）")
    close(Fy, 0.7892, 2e-3, "图3 F 点纵坐标（TikZ 代码值）")
    ok(abs((Dx - Fx) * math.sin(th) + (0 - Fy) * math.cos(th)) < 1e-9,
       "图3 中 DF 与光 1 垂直（点积为 0）")
    close(math.hypot(Fx, Fy) ** 2 + math.hypot(Dx - Fx, Fy) ** 2, Dx ** 2, 1e-9,
          "图3 中 BF²+DF²=BD²（直角在 F）")

    # ---------- 汇总 ----------
    print(f"断言 {checks} 条，失败 {len(fails)} 条")
    print(f"关键数值：d={D*1e6:.3f} µm, k0={K0}, r1={r1*1e3:.2f} mm, r2={r2*1e3:.2f} mm, "
          f"Δr={dr_exact*1e3:.2f} mm, Δr(r1)={dr_inner*1e3:.2f} mm, Δr(mean)={dr_mean*1e3:.2f} mm")
    print(f"          ΔL_exact={dl_exact*1e6:.3f} µm, ΔL_approx={dl_approx*1e6:.3f} µm, "
          f"V(9:1)={vis(9,1):.3f}, Imax(1:1)={imax_eq:.1f}, Imax(9:1)={imax_91:.1f}")
    if fails:
        for f in fails:
            print("[FAIL]", f)
        return 1
    print("全部断言通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
