# -*- coding: utf-8 -*-
"""针对本轮新增开篇概览图（图 0）的定向核对。

范围 deliberately 小：只核对
  A. 源文件层面：概览块的位置、节点/章节引用、关键关系式、未泄露练习答案；
  B. PDF 层面：图 0 在第 1 页、图注完整且在图下方、开篇说明在第 2 页图之后、
     八个节点的矩形分组对齐、箭头不穿入方框、边标不压方框/不互相压字；
  C. 数学层面：图中引用的关系式用独立数值重算（谱分解、并矢作用、旋转与角速度、
     惯量构造、面力分解、输运/陀螺项）。
不重跑 round-04 的 269 条全书断言；通过也不代表页面已目视或一般证明已复核。
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

import fitz
import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
TEX = ROOT / "handout.tex"
PDF = ROOT / "handout.pdf"

PASS = 0
FAIL = 0
DETAIL: list[str] = []

VIOLET = (0.42, 0.306, 0.561)
BANDVIOLET = (0.969, 0.953, 0.984)
BANDCREAM = (0.988, 0.976, 0.949)


def check(name: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
        DETAIL.append(f"[FAIL] {name}: {detail}")
    print(("  [ok] " if ok else "  [E ] ") + name + (f"  ({detail})" if detail and not ok else ""))


def near(c, t, tol=0.01) -> bool:
    return c is not None and all(abs(x - y) < tol for x, y in zip(c, t))


def rect_overlap(a, b) -> tuple[float, float]:
    return (min(a.x1, b.x1) - max(a.x0, b.x0), min(a.y1, b.y1) - max(a.y0, b.y0))


def main() -> int:
    src = TEX.read_text(encoding="utf-8")
    doc = fitz.open(PDF)

    print("A. 源文件层面")
    i_title = src.find(r"\doctitle{从张量到并矢}")
    i_over = src.find(r"\hdr{导览}{全书主线：一张图先看路线}")
    i_call = src.find(r"\callout{\textbf{这份材料为谁写、怎么用。}")
    i_sec0 = src.find(r"\hdr{§0}{起点：矢量、矩阵与换基}")
    check("概览块位于标题之后、开篇说明与 §0 之前",
          0 <= i_title < i_over < i_call < i_sec0,
          f"{i_title},{i_over},{i_call},{i_sec0}")
    block = src[i_over:i_call]
    check("概览块以 \\clearpage 结束（图独占开篇页）", block.rstrip().endswith(r"\clearpage"),
          block[-80:])

    for sec in ["§0", "§1", "§2", "§3", "§4", "§5", "§6"]:
        check(f"概览图含 {sec} 节点", f"\\S{sec[1:]}\\quad" in block)
    for phrase, meaning in [
        (r"\S0.3--0.5", "账本/换基段"),
        (r"\S1.1--1.6", "二次型/谱定理段"),
        (r"\S2.1--2.8", "张量与并矢段"),
        (r"\S3.2--3.6", "旋转与角速度段"),
        (r"v=\boldsymbol\Omega\times\vect r", "刚体速度关系"),
        (r"\S4.3", "惯量主轴"),
        (r"\S6.2", "主应力"),
        (r"\S2.7", "商法则"),
        (r"\S5.3", "对称陀螺"),
    ]:
        check(f"概览图引用 {meaning}", phrase in block)
    for formula, name in [
        (r"\ten T'=\ten R^{\mathsf T}\ten T\ten R", "换基律"),
        (r"\ten T=\sum_k\lambda_k\vect n_k\otimes\vect n_k", "谱分解"),
        (r"(\vect a\otimes\vect b)\cdot\vect x=\vect a(\vect b\cdot\vect x)", "并矢右作用"),
        (r"\ten J=\int(r^2\unitd-\vect r\otimes\vect r)\dd m", "惯量张量构造"),
        (r"\vect L=\ten J\cdot\boldsymbol\omega", "角动量"),
        (r"\vect t(\vect n)=\ten\sigma\cdot\vect n", "面力"),
        (r"\nabla\cdot\ten\sigma+\vect f=\vect0", "平衡方程"),
        (r"\boldsymbol\Omega^{\times}=(\dd S/\dd t)S^{\mathsf T}", "角速度"),
    ]:
        check(f"概览图关系式：{name}", formula in block)
    check("概览图未出现练习编号", not re.search(r"\bP(?:1[0-2]|[1-9])\b", block))
    check("概览图未出现“答案/详解”字样", "答案" not in block and "详解" not in block)
    check("图号用 0，不改动既有图 1--11 的编号",
          r"\textbf{图 0}" in block and src.count(r"\textbf{图 0}") == 1)
    check("既有图 1--11 图注数量不变",
          all(f"\\textbf{{图 {k}}}" in src for k in range(1, 12)))

    for needle, name in [
        (r"\subhdr{4.3\quad 主轴 = 惯量主轴", "§4.3 惯量主轴"),
        (r"\subhdr{6.2\quad 对称性来自角动量守恒", "§6.2 应力对称性"),
        (r"\subhdr{2.7\quad 张量变换律与商法则", "§2.7 商法则"),
        (r"\subhdr{3.5\quad 无穷小旋转与角速度", "§3.5 角速度"),
        (r"\subhdr{1.4\quad 谱定理：陈述与完整证明", "§1.4 谱定理"),
        (r"\subhdr{4.1\quad 从 $\vect L=\int\vect r\times\vect v\dd m$", "§4.1 惯量构造"),
        (r"\subhdr{5.1\quad 输运定理", "§5.1 输运定理"),
    ]:
        check(f"正文对应位置存在：{name}", needle in src)

    print("B. PDF 层面")
    p1 = doc[0]
    p1_text = re.sub(r"\s+", "", p1.get_text())
    p2_text = re.sub(r"\s+", "", doc[1].get_text()) if doc.page_count > 1 else ""
    check("PDF 第 1 页含图 0 图注", "图0（自绘" in p1_text)
    check("PDF 第 1 页不含开篇使用说明", "这份材料为谁写" not in p1_text)
    check("PDF 第 2 页以开篇使用说明开始", "这份材料为谁写" in p2_text[:120], p2_text[:60])
    cap_lines = [b for b in p1.get_text("dict")["blocks"] if b["type"] == 0
                 and 700 < b["bbox"][1] < 795]
    caption_bottom = max((b["bbox"][3] for b in cap_lines), default=0)
    caption_text = "".join("".join(s["text"] for l in b["lines"] for s in l["spans"])
                           for b in cap_lines)
    check("图注完整落在第 1 页正文区内（下界 789pt）", 0 < caption_bottom <= 789,
          f"caption_bottom={caption_bottom:.1f}")
    check("图注以“不代替定义与证明”结尾", "不代替定义与证明" in caption_text)
    cap = p1.search_for("图 0（自绘") or p1.search_for("图0（自绘")
    check("能定位图 0 图注", bool(cap))
    cap_top = cap[0].y0 if cap else 0

    rects = []
    for d in p1.get_drawings():
        if d.get("fill") is None:
            continue
        r = d["rect"]
        if r.width > 80 and r.height > 40 and (near(d["fill"], BANDVIOLET)
                                               or near(d["fill"], BANDCREAM)):
            rects.append(r)
    check("识别到 8 个节点方框", len(rects) == 8, f"{len(rects)}")
    rects.sort(key=lambda r: (round(r.y0), r.x0))
    core, tools, bridge, lands = rects[:1], rects[1:3], rects[3:5], rects[5:8]
    check("核心问题框为单行通栏", len(core) == 1 and core[0].width > 400, str(core))
    for name, grp in (("工具层", tools), ("桥梁层", bridge), ("落点层", lands)):
        check(f"{name}方框顶边对齐", len({round(r.y0, 1) for r in grp}) == 1,
              str([round(r.y0, 1) for r in grp]))
        check(f"{name}方框底边对齐", len({round(r.y1, 1) for r in grp}) == 1,
              str([round(r.y1, 1) for r in grp]))
    allr = core + tools + bridge + lands
    overlap = []
    for i in range(len(allr)):
        for j in range(i + 1, len(allr)):
            w, h = rect_overlap(allr[i], allr[j])
            if w > 0.5 and h > 0.5:
                overlap.append((i, j, round(w, 1), round(h, 1)))
    check("节点方框彼此不重叠", not overlap, str(overlap))
    check("整幅图在左右页边距内", min(r.x0 for r in allr) >= 40 and max(r.x1 for r in allr) <= 555,
          f"x=[{min(r.x0 for r in allr):.1f},{max(r.x1 for r in allr):.1f}]")
    check("图本体在图注上方且不重叠", max(r.y1 for r in allr) < cap_top - 10,
          f"{max(r.y1 for r in allr):.1f} vs {cap_top:.1f}")

    # 边标 = 白色填充的文字底框；必须落在所有节点方框之外
    labels = [d["rect"] for d in p1.get_drawings()
              if d.get("fill") is not None and near(d["fill"], (1.0, 1.0, 1.0))
              and d["rect"].width > 40 and d["rect"].height > 8]
    check("识别到 7 个边标", len(labels) == 7, f"{len(labels)}")
    bad = []
    for lr in labels:
        for nr in allr:
            w, h = rect_overlap(lr, nr)
            if w > 1.0 and h > 1.0:
                bad.append((round(w, 1), round(h, 1)))
    check("边标底框不压在任何节点方框上", not bad, str(bad))
    lb = []
    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            w, h = rect_overlap(labels[i], labels[j])
            if w > 0.5 and h > 0.5:
                lb.append((i, j, round(w, 1), round(h, 1)))
    check("边标底框彼此不重叠", not lb, str(lb))

    # 箭杆（fill=None 的紫色直线）不得伸进方框内部
    shafts = []
    for d in p1.get_drawings():
        if d.get("fill") is not None or not near(d.get("color"), VIOLET, tol=0.02):
            continue
        if len(d["items"]) == 1 and d["items"][0][0] == "l":
            shafts.append(d["rect"])
    check("识别到 9 条箭杆", len(shafts) == 9, f"{len(shafts)}")
    stub = []
    for sh in shafts:
        for nr in allr:
            w, h = rect_overlap(sh, nr)
            if w > 2.0 and h > 2.0:
                stub.append((round(w, 1), round(h, 1)))
    check("箭杆不伸进任何节点方框内部", not stub, str(stub))

    # 图内文字：只查不同基线之间的压字（同一行内的上下标不算）
    spans = []
    for blk in p1.get_text("dict")["blocks"]:
        if blk["type"] != 0:
            continue
        for ln in blk["lines"]:
            for sp in ln["spans"]:
                if sp["text"].strip() and sp["bbox"][1] > 280:
                    spans.append(fitz.Rect(sp["bbox"]))
    tneg = []
    for i in range(len(spans)):
        for j in range(i + 1, len(spans)):
            a, b = spans[i], spans[j]
            if abs((a.y0 + a.y1) / 2 - (b.y0 + b.y1) / 2) < 5:
                continue
            w, h = rect_overlap(a, b)
            if w > 3.0 and h > 3.0:
                tneg.append((round(w, 1), round(h, 1)))
    check("图内不同行的文字没有互相压字", not tneg, f"{len(tneg)} 处 {tneg[:5]}")

    print("C. 图中关系式数值核对")
    rng = np.random.default_rng(20261114)

    M = rng.normal(size=(3, 3))
    A = (M + M.T) / 2
    w, V = np.linalg.eigh(A)
    check("C1a 实对称矩阵特征值为实", np.isrealobj(w) or np.allclose(w.imag, 0))
    check("C1b 特征向量正交归一", np.allclose(V.T @ V, np.eye(3), atol=1e-12))
    check("C1c 谱分解 T=Σλ n nᵀ",
          np.allclose(sum(w[k] * np.outer(V[:, k], V[:, k]) for k in range(3)), A, atol=1e-12))
    a = rng.normal(size=3)
    check("C1d 二次型化为 Σλ(n·a)²",
          abs(a @ A @ a - sum(w[k] * (V[:, k] @ a) ** 2 for k in range(3))) < 1e-10)
    check("C1e tr=Σλ 且 det=Πλ",
          abs(np.trace(A) - w.sum()) < 1e-10 and abs(np.linalg.det(A) - np.prod(w)) < 1e-10)

    b = rng.normal(size=3)
    x = rng.normal(size=3)
    check("C2 (a⊗b)·x=a(b·x)", np.allclose(np.outer(a, b) @ x, a * (b @ x)))

    axis = np.array([0.3, -0.5, 0.81]); axis /= np.linalg.norm(axis)
    phi = 0.7
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    P = np.outer(axis, axis)
    S = P + (np.eye(3) - P) * math.cos(phi) + K * math.sin(phi)
    check("C3a SᵀS=1", np.allclose(S.T @ S, np.eye(3), atol=1e-12))
    check("C3b det S=+1", abs(np.linalg.det(S) - 1.0) < 1e-12)
    check("C3c S 保持沿轴分量", np.allclose(S @ axis, axis))
    perp = np.cross(axis, [1.0, 0.0, 0.0])
    check("C3d 垂直分量转 phi 后与公式一致",
          np.allclose(S @ perp, math.cos(phi) * perp + math.sin(phi) * np.cross(axis, perp), atol=1e-12))
    h = 1e-7
    Sp = (P + (np.eye(3) - P) * math.cos(phi + h) + K * math.sin(phi + h) - S) / h
    Omega_x = Sp @ S.T
    check("C3e (dS/dt)Sᵀ 反对称", np.allclose(Omega_x + Omega_x.T, 0, atol=1e-6))
    omega_dual = np.array([Omega_x[2, 1], Omega_x[0, 2], Omega_x[1, 0]])
    check("C3f 反对称部分对应 Ω=φ̇n（此处 φ̇=1）", np.allclose(omega_dual, axis, atol=1e-5))
    check("C3g 对任意 y 有 Ω^× y=Ω×y",
          np.allclose(Omega_x @ a, np.cross(omega_dual, a), atol=1e-5))

    m, aa, bb, cc = 5.0, 2.0, 3.0, 4.0
    n = 41
    xs = (np.arange(n) + 0.5) / n - 0.5
    X, Y, Z = np.meshgrid(xs * aa, xs * bb, xs * cc, indexing="ij")
    dm = m / n ** 3
    r2 = X ** 2 + Y ** 2 + Z ** 2
    coords = [X, Y, Z]
    J = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            J[i, j] = np.sum((r2 * (i == j) - coords[i] * coords[j]) * dm)
    Jexp = m / 12 * np.diag([bb ** 2 + cc ** 2, aa ** 2 + cc ** 2, aa ** 2 + bb ** 2])
    check("C4a J=∫(r²1−r⊗r)dm 与长方体公式一致", np.allclose(J, Jexp, atol=2e-2),
          f"{np.round(J,3).tolist()}")
    check("C4b J 对称", np.allclose(J, J.T))
    check("C4c J 半正定（主值≥0）", np.all(np.linalg.eigvalsh(J) > -1e-9))
    om = np.array([1.0, 1.0, 1.0]) / math.sqrt(3)
    L = J @ om
    check("C4d L=J·ω", np.allclose(L, J @ om))
    check("C4e 沿 (1,1,1) 的 L 一般不与 ω 平行", np.linalg.norm(np.cross(L, om)) > 1e-3)
    check("C4f 主值即三个主转动惯量",
          np.allclose(np.sort(np.linalg.eigvalsh(J)), np.sort(np.diag(Jexp)), atol=2e-2))

    s0 = 2.0
    sig = s0 * np.outer([1, 0, 0], [1, 0, 0])
    th = math.radians(30)
    nv = np.array([math.cos(th), math.sin(th), 0.0])
    t = sig @ nv
    tn = t @ nv
    tau = math.sqrt(max(0.0, t @ t - tn ** 2))
    check("C5a t=σ·n 仍沿 e1", np.allclose(t, s0 * math.cos(th) * np.array([1, 0, 0])))
    check("C5b t_n=σ0cos²θ=3σ0/4", abs(tn - 0.75 * s0) < 1e-12)
    check("C5c τ=σ0sinθcosθ=√3σ0/4", abs(tau - math.sqrt(3) / 4 * s0) < 1e-12)
    sig_sym = np.array([[3.0, 0.5, 0.0], [0.5, 1.0, 0.2], [0.0, 0.2, -0.5]])
    ev = np.linalg.eigvalsh(sig_sym)
    check("C5d 对称 σ 的主应力为实特征值", np.all(np.isreal(ev)))
    check("C5e 主应力之和=tr σ", abs(ev.sum() - np.trace(sig_sym)) < 1e-12)

    Jb = np.diag([1.0, 2.0, 3.0])
    om = axis.copy()
    S2 = P + (np.eye(3) - P) * math.cos(0.0) + K * math.sin(0.0)
    Lt = S2 @ Jb @ S2.T @ om
    dt = 1e-6
    S2b = P + (np.eye(3) - P) * math.cos(dt) + K * math.sin(dt)
    Lb = S2b @ Jb @ S2b.T @ om
    dLdt = (Lb - Lt) / dt
    check("C6a 固定系 dL/dt=ω×L（体分量不变时）",
          np.allclose(dLdt, np.cross(axis, Lt), atol=1e-3),
          f"{np.round(dLdt,3).tolist()} vs {np.round(np.cross(axis, Lt),3).tolist()}")
    check("C6b ω×L 一般非零（陀螺项）", np.linalg.norm(np.cross(axis, Lt)) > 1e-3)

    print()
    print(f"合计断言 {PASS + FAIL} 条，失败 {FAIL} 条。")
    if FAIL:
        print("失败明细：")
        for d in DETAIL:
            print(" -", d)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
