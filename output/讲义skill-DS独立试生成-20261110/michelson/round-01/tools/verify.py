# -*- coding: utf-8 -*-
r"""讲义数值与推导的可复现核验（不代替内容审校）。

用法：python -B michelson/round-01/tools/verify.py [--quiet]
每条断言失败即打印 [FAIL] 并以退出码 1 结束；全部通过时打印断言条数。
核验对象：§2 的推导（2d cosθ、虚光源近似、环半径、间距、计数）、§2.4 的 20:1 换算、
§3 三个教学小例的全部数值、§4 附加 (1)(2) 用到的可见度与相干长度估计。
"""
from __future__ import annotations

import math
import sys

LAM = 632.8e-9          # He-Ne 真空波长（示例取值）
LAM_NA = 589.3e-9       # 钠黄光（示例取值）
Z = 1.00                # 屏到虚光源的距离（示例设定）
D_EX = 316 * LAM / 2    # 使中心恰为亮纹的膜厚（k0 = 316）

checks = 0
fails: list[str] = []


def ok(cond: bool, msg: str) -> None:
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def close(a: float, b: float, tol: float, msg: str) -> None:
    ok(abs(a - b) <= tol, f"{msg}：得到 {a:.6g}，应为 {b:.6g}（容差 {tol:g}）")


def main() -> int:
    # ---------- §2.4 传动比 20:1 ----------
    ratio = 0.01 / 0.0005
    close(ratio, 20.0, 1e-12, "读数:动镜位移 = 20:1")
    close(0.01e-3 / 20, 0.5e-6, 1e-18, "每 0.01 mm 读数对应 0.5 µm 位移")

    # ---------- 式 (1)：2d cosθ 的几何推导 ----------
    for theta_deg in (5, 20, 35, 45):
        th = math.radians(theta_deg)
        d = 1.0
        bc_cd = 2 * d / math.cos(th)                 # BC + CD
        bf = 2 * d * math.tan(th) * math.sin(th)     # BF = BD sinθ
        close(bc_cd - bf, 2 * d * math.cos(th), 1e-12, f"式(1) 在 θ={theta_deg}° 的恒等变形")

    # ---------- 虚光源：S2'P - S1P ≈ 2d cosθ ----------
    for r in (0.02, 0.05, 0.12):
        dl_exact = math.sqrt((Z - D_EX) ** 2 + r ** 2) - math.sqrt((Z + D_EX) ** 2 + r ** 2)
        cos_t = Z / math.hypot(Z, r)
        ok(abs(abs(dl_exact) - 2 * D_EX * cos_t) / (2 * D_EX * cos_t) < 1e-9,
           f"虚光源光程差在 r={r} m 处与 2d cosθ 一致")

    # ---------- 环半径与间距（例 3.2 的设定）----------
    ok(abs(D_EX - 99.982e-6) < 1e-9, f"k0=316 时 d = 316λ/2 = {D_EX*1e6:.3f} µm ≈ 0.100 mm")
    k0 = 2 * D_EX / LAM
    close(k0, 316.0, 1e-9, "中心级次 k0 = 2d/λ")

    r_m = [Z * math.sqrt(m * LAM / D_EX) for m in (1, 2)]
    close(r_m[0] * 1e3, 79.56, 0.01, "r1（mm）")
    close(r_m[1] * 1e3, 112.51, 0.01, "r2（mm）")

    # 与 (11-1) 直接解出的 r_k 比较：k = k0 - m
    for m in (1, 2):
        k = 316 - m
        rk = Z * math.sqrt(2 * (1 - k * LAM / (2 * D_EX)))
        close(rk, r_m[m - 1], 1e-12, f"r_m 与 (11-1) 解 r_k 在 m={m} 处一致")

    dtheta1 = math.degrees(math.atan(r_m[0] / Z))
    dtheta2 = math.degrees(math.atan(r_m[1] / Z))
    close(dtheta1, 4.55, 0.01, "θ1（度）")
    close(dtheta2, 6.42, 0.01, "θ2（度）")
    ok(r_m[1] / Z < 0.15, f"例 3.2 满足 r≪z 的弱形式：r2/z = {r_m[1]/Z:.3f} < 0.15")

    # 间距：精确值 vs 源式（代 r1）vs 源式（代平均半径）
    dr_exact = r_m[1] - r_m[0]
    dr_approx_r1 = LAM * Z ** 2 / (2 * D_EX * r_m[0])
    dr_approx_mean = LAM * Z ** 2 / (2 * D_EX * (r_m[0] + r_m[1]) / 2)
    close(dr_exact * 1e3, 32.95, 0.02, "精确环间距（mm）")
    close(dr_approx_r1 * 1e3, 39.78, 0.02, "把 r1 代入源式的间距（mm）")
    ok(dr_approx_r1 / dr_exact - 1 > 0.20,
       f"代 r1 的偏差 {100*(dr_approx_r1/dr_exact-1):.1f}% 应大于 20%")
    close(dr_approx_mean, dr_exact, 2e-6, "代平均半径的间距与精确值（应为恒等）")
    close(100 * (dr_approx_r1 / dr_exact - 1), 20.7, 0.1, "代 r1 的相对偏差（%）")
    close(r_m[0] / Z, 0.0796, 5e-4, "r1/z（rad）")
    close(r_m[1] / Z, 0.1125, 5e-4, "r2/z（rad）")

    # 同一组数里 ΔL 的近似误差（与间距式误差对比）
    dl_exact = 2 * D_EX * math.cos(math.atan(r_m[1] / Z))
    dl_approx = 2 * D_EX * (1 - r_m[1] ** 2 / (2 * Z ** 2))
    close(dl_exact * 1e6, 198.71, 0.01, "ΔL 精确值（µm）")
    close(dl_approx * 1e6, 198.70, 0.01, "ΔL 二级近似（µm）")
    close(abs(dl_exact - dl_approx) / LAM, 0.019, 0.002, "ΔL 近似误差折合条纹数")
    ok(abs(dl_exact - dl_approx) / dl_exact < 1e-4,
       "ΔL 近似相对误差应 < 1e-4（与间距式的 20% 形成对照）")

    # ---------- 例 3.1 膜厚与环数 ----------
    n1 = 50
    dd1 = n1 * LAM / 2
    close(dd1 * 1e6, 15.82, 0.01, "50 环对应的 Δd（µm）")
    close(20 * dd1 * 1e3, 0.3164, 1e-4, "50 环对应的鼓轮读数差（mm）")
    close((20 * dd1 / 0.01e-3) * 0.5e-6, dd1, 1e-15, "以 0.5 µm/格 复核 Δd")
    close(100 * (LAM / 2) / dd1, 2.0, 0.01, "数错一环对 N=50 的相对影响（%）")

    # ---------- 例 3.3 波长与计数 ----------
    n3, dl3 = 500, 3.164e-3
    dd3 = dl3 / 20
    close(2 * dd3 / n3 * 1e9, 632.8, 0.05, "由 Δl、N 反算的波长（nm）")
    close(dl3 / (10 * n3) * 1e9, 632.8, 0.05, "工作式 λ = Δl/(10N)（nm）")
    dd_na = n3 * LAM_NA / 2
    close(20 * dd_na * 1e3, 2.947, 0.001, "钠光 500 环应移动的读数（mm）")
    close(100 * (2.947 / 3.164 - 1), -6.85, 0.05, "两光源读数差相对差（%）")
    ok(abs(2.947 / 3.164 - 1) < 0.10, "两光源读数差应在 10% 以内（要求读数精度优于 1%）")

    # ---------- 逐差法 ΔN = 160 ----------
    close(10 * 160 * LAM * 1e3, 1.0125, 1e-4, "ΔN=160 时读数差应约 1.0125 mm")

    # ---------- 附加 (1)：可见度 ----------
    def vis(i1: float, i2: float) -> float:
        return 2 * math.sqrt(i1 * i2) / (i1 + i2)

    close(vis(1, 1), 1.0, 1e-12, "I1=I2 时 V=1")
    close(vis(9, 1), 0.6, 1e-12, "I1:I2=9:1 时 V=0.6")
    close(vis(99, 1), 0.199, 5e-4, "I1:I2=99:1 时 V≈0.2")
    ok(vis(1, 1) > vis(9, 1) > vis(99, 1), "V 随强度比变差而下降")
    close(4 / 16, 0.25, 1e-12, "9:1 时暗纹强度/亮纹强度 = 0.25")

    # ---------- 一个环对应多少格读数 ----------
    close((LAM / 2) / 0.01e-3, 0.0316, 5e-4, "1:1 时一个环对应的鼓轮格数（约 1/30 格）")
    ok((LAM / 2) / 0.01e-3 < 0.05, "1:1 时一个环不到 1/20 格，读数不可分辨")
    close(20 * (LAM / 2) / 0.01e-3, 0.6328, 5e-4, "20:1 时一个环对应的格数")

    # ---------- 附加 (2)：相干长度与玻璃路程差 ----------
    lc = (550e-9) ** 2 / 300e-9
    close(lc * 1e6, 1.008, 0.005, "白光相干长度估计 λ²/Δλ（µm）")
    glass = (1.5 - 1) * 1e-3
    close(glass * 1e3, 0.5, 1e-12, "(n-1)t（mm），n=1.5、t=1 mm 示例")
    ok(glass / lc > 100, f"玻璃路程差是相干长度的 {glass/lc:.0f} 倍（应 >100 倍）")

    # ---------- 「涌出／陷入」与疏密的方向 ----------
    k = 300
    d_lo, d_hi = D_EX, 1.10 * D_EX
    rk = lambda d, kk: Z * math.sqrt(max(0.0, 2 * (1 - kk * LAM / (2 * d))))
    ok(rk(d_hi, k) > rk(d_lo, k), "固定级次 k 的环半径随 d 增大而增大（涌出）")
    dr = lambda d, r: LAM * Z ** 2 / (2 * d * r)
    ok(dr(d_lo / 4, 0.05) > dr(d_lo, 0.05), "同一半径处 d 小则环间距大（变疏）")
    close(dr(d_lo / 4, 0.05) / dr(d_lo, 0.05), 4.0, 1e-12, "Δr ∝ 1/d")
    r_of_m = lambda d, m: Z * math.sqrt(m * LAM / d)
    ok(r_of_m(d_lo / 4, 1) > r_of_m(d_lo, 1), "中心亮纹假设下第 m 环半径随 d 减小而增大")

    # 每 λ/2 过一个环：中心级次改变 1
    for n in (1, 7, 100):
        k_before = 2 * d_lo / LAM
        k_after = 2 * (d_lo + n * LAM / 2) / LAM
        close(k_after - k_before, float(n), 1e-9, f"d 增加 {n}λ/2 时中心级次改变")

    # ---------- 图 3、图 4 的作图坐标与公式一致 ----------
    # 图 3（handout.tex）：B=(0,0), C=(d tanθ,-d), D=(2d tanθ,0), F=t(sinθ,cosθ)
    d_fig, th = 1.2, math.radians(35)
    Cx, Cy = d_fig * math.tan(th), -d_fig
    Dx = 2 * d_fig * math.tan(th)
    t = 2 * d_fig * math.tan(th) * math.sin(th)
    Fx, Fy = t * math.sin(th), t * math.cos(th)
    close(Cx, 0.84, 5e-3, "图3 C 点横坐标 d tanθ")
    close(Cy, -1.2, 5e-3, "图3 C 点纵坐标 -d（下表面；箭杆止于 -1.16/-1.22）")
    close(Dx, 1.68, 5e-3, "图3 D 点横坐标 2d tanθ")
    close(Fx, 0.5526, 2e-3, "图3 F 点横坐标（TikZ 代码值）")
    close(Fy, 0.7892, 2e-3, "图3 F 点纵坐标（TikZ 代码值）")
    ok(abs((Dx - Fx) * math.sin(th) + (0 - Fy) * math.cos(th)) < 1e-9,
       "图3 中 DF 与光 1 垂直（点积为 0）")
    close(math.hypot(Fx, Fy) ** 2 + math.hypot(Dx - Fx, Fy) ** 2, Dx ** 2, 1e-9,
          "图3 中 BF²+DF²=BD²（直角在 F，BD=2d tanθ）")

    # 图 4（handout.tex）：S1=(-1.98,0), S2'=(-1.38,0), P=(2.4,1.0)
    z4, d4, r4 = 2.4 - (-1.68), 0.30, 1.0
    dl4 = math.sqrt((z4 - d4) ** 2 + r4 ** 2) - math.sqrt((z4 + d4) ** 2 + r4 ** 2)
    cos4 = z4 / math.hypot(z4, r4)
    close(abs(dl4) / (2 * d4 * cos4), 1.0, 5e-3,
          "图4 中 ΔL 与 2d cosθ 的比例（作图坐标自洽）")
    ang1 = math.degrees(math.atan(r4 / (2.4 + 1.98)))
    ang2 = math.degrees(math.atan(r4 / (2.4 + 1.38)))
    ok(0 < ang2 - ang1 < 3, f"图4 两支光夹角 {ang2-ang1:.2f}° 很小（接近平行，符合 r≪z）")

    # ---------- 汇总 ----------
    print(f"断言 {checks} 条，失败 {len(fails)} 条")
    print(f"关键数值：d={D_EX*1e6:.3f} µm, k0={k0:.1f}, r1={r_m[0]*1e3:.2f} mm, "
          f"r2={r_m[1]*1e3:.2f} mm, Δr={dr_exact*1e3:.2f} mm, "
          f"Δr(r1)={dr_approx_r1*1e3:.2f} mm, Δr(mean)={dr_approx_mean*1e3:.2f} mm")
    print(f"          ΔL_exact={dl_exact*1e6:.3f} µm, ΔL_approx={dl_approx*1e6:.3f} µm, "
          f"L_c={lc*1e6:.3f} µm, glass={glass*1e3:.1f} mm, V(9:1)={vis(9,1):.3f}")
    if fails:
        for f in fails:
            print("[FAIL]", f)
        return 1
    print("全部断言通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
