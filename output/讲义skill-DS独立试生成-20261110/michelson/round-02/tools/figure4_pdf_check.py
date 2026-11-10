# -*- coding: utf-8 -*-
r"""图 4 在最终 PDF 中的实际尺寸线端点核对。

为什么不用“某条线段长度 = 4.08 cm”直接判定：TikZ 的 <-> 箭头会把线段缩短、
箭头尖端相对标称端点有固定内缩量。本脚本以图 4 的轴线（-2.30→2.55 cm）定标，
用 2d 尺寸线（名义 0.60 cm）反推箭头内缩量，再还原 z 尺寸线的标称端点，
检查它是否确实从 M（-1.68 cm）量到屏（2.40 cm），而不是从 S2'（-1.38 cm）量起。
用法：python -B michelson/round-02/tools/figure4_pdf_check.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "handout.pdf"
CM = 72.0 / 2.54
AXIS_X0, AXIS_X1 = -2.30, 2.55
S1_X, S2_X, M_X, SCREEN_X = -1.98, -1.38, -1.68, 2.40
D2_CM, Z_CM = 0.60, 4.08
checks = 0
fails: list[str] = []


def ok(cond: bool, msg: str) -> None:
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def main() -> int:
    doc = fitz.open(PDF)
    page_no = None
    for i, page in enumerate(doc, 1):
        if "图4" in [ln.strip() for ln in page.get_text().splitlines()]:
            page_no = i
            break
    ok(page_no is not None, "找不到图 4 所在页")
    if page_no is None:
        return 1
    page = doc[page_no - 1]

    # 收集水平线段与所有路径矩形
    hsegs = []
    paths = []
    for dr in page.get_drawings():
        r = dr["rect"]
        paths.append(r)
        for it in dr["items"]:
            if it[0] == "l":
                a, b = it[1], it[2]
                if abs(a.y - b.y) < 0.2:
                    hsegs.append((a.x, a.y, b.x, b.y, abs(b.x - a.x)))

    # 轴线：图 4 中长度约 4.85 cm 的水平线
    axes = [s for s in hsegs if 4.7 * CM < s[4] < 5.0 * CM and s[1] > 300]
    ok(len(axes) == 1, f"图 4 轴线应唯一，实际 {len(axes)} 条")
    if len(axes) != 1:
        return 1
    ax0, ay0, ax1, ay1, alen = axes[0]
    axis_y = ay0
    scale = alen / (AXIS_X1 - AXIS_X0)          # pt per cm（由轴线定标）

    def dim_tips(shaft_len_lo: float, shaft_len_hi: float, y_lo: float, y_hi: float):
        cand = [s for s in hsegs if shaft_len_lo < s[4] < shaft_len_hi and y_lo < s[1] < y_hi]
        if not cand:
            return None
        s = cand[0]
        y = s[1]
        # 只取与箭杆同一水平带、且高度很小的路径（箭杆 + 两个箭头），
        # 排除斜光线等高度较大的路径
        near = [r for r in paths
                if abs((r.y0 + r.y1) / 2 - y) < 4.0
                and (r.y1 - r.y0) < 8.0
                and r.x1 > s[0] - 15.0 and r.x0 < s[2] + 15.0]
        x0 = min(r.x0 for r in near)
        x1 = max(r.x1 for r in near)
        return x0, x1, y

    # 2d 尺寸线：轴线之上约 0.34 cm
    two_d = dim_tips(3.0, 8.0, axis_y - 0.45 * scale, axis_y - 0.20 * scale)
    ok(two_d is not None, "找不到 2d 尺寸线")
    if two_d is None:
        return 1
    t0, t1, ty = two_d
    span_2d_drawn = t1 - t0
    inset = (D2_CM * scale - span_2d_drawn) / 2.0
    ok(0.0 < inset < 0.12 * CM, f"箭头内缩量应在合理范围，得到 {inset:.2f} pt")

    # z 尺寸线：轴线之下约 1.05 cm
    zdim = dim_tips(3.0 * CM, 4.0 * CM, axis_y + 0.8 * scale, axis_y + 1.3 * scale)
    ok(zdim is not None, "找不到 z 尺寸线")
    if zdim is None:
        return 1
    z0, z1, zy = zdim
    z_left = z0 - inset
    z_right = z1 + inset
    z_span = z_right - z_left

    m_exp = ax0 + (M_X - AXIS_X0) * scale
    s2_exp = ax0 + (S2_X - AXIS_X0) * scale
    screen_exp = ax0 + (SCREEN_X - AXIS_X0) * scale

    ok(abs(z_span - Z_CM * scale) < 0.8,
       f"z 名义长度应为 4.08 cm（{Z_CM*scale:.2f} pt），得到 {z_span:.2f} pt")
    ok(abs(z_left - m_exp) < 1.2,
       f"z 名义左端应落在 M（x={m_exp:.2f} pt），得到 {z_left:.2f} pt")
    ok(abs(z_right - screen_exp) < 1.2,
       f"z 名义右端应落在屏（x={screen_exp:.2f} pt），得到 {z_right:.2f} pt")
    ok(abs(z_left - m_exp) + 4.0 < abs(z_left - s2_exp),
       f"z 左端应更接近 M 而不是 S2'（M={m_exp:.2f}, S2'={s2_exp:.2f}, 实得 {z_left:.2f}）")
    ok(abs(z_span - 3.78 * scale) > 2.0,
       f"z 不应是旧稿的 3.78 cm（{3.78*scale:.2f} pt）")
    ok(abs(span_2d_drawn + 2 * inset - D2_CM * scale) < 0.8,
       "2d 尺寸线的标称长度应为 0.60 cm")

    print(f"图 4 实际 PDF 尺寸线检查 {checks} 条，失败 {len(fails)} 条（页 {page_no}）")
    print(f"  轴线定标 {scale:.3f} pt/cm；2d 尖端 {span_2d_drawn:.2f} pt，内缩 {inset:.2f} pt；"
          f"z 标称 {z_left:.2f}→{z_right:.2f} pt（{z_span:.2f} pt）")
    if fails:
        for f in fails:
            print("[FAIL]", f)
        return 1
    print("图 4 的 z 尺寸线确实从 M 量到屏，且与 4.08 cm 标称长度一致")
    return 0


if __name__ == "__main__":
    sys.exit(main())
