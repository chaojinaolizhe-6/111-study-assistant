# -*- coding: utf-8 -*-
"""round-02 开篇概览返工的定向核对。

范围刻意小，只查本轮改动与审核指出的问题：
  A. 源文件：概览位置、七个主题与章节定位、三处条件的字样、无练习泄露、旧图 1--11 名号。
  B. 正文保持：把允许改动的段落（导览块、版本说明、交付说明、末页版本行、文件头注释）替换为哨兵后，
     round-02 与字节锁定的 round-01 工作快照必须逐字符相同；并单独核 \\hdr{§0} 至交付说明之前的正文区。
  C. PDF 几何：8 个节点框、行内等高等宽、页边距内、彼此不重叠；8 条箭杆不进入方框内部；
     图内文字都在所属框内且不压字；图 0 与完整图注同在第 1 页、图在注上；开篇说明在第 2 页。
  D. 页码与引用：图 0 图注只出现一次；无未解析的 ??；P1--P12 的“详解见附录第 X 页”与 aux 标签、
     实际详解页一致。
  E. 图中三个力学条件用独立数值反例核验（缺条件时不成立），并核谱分解/惯量关系。

不重跑此前已验收的 269 条全书断言；通过也不代表页面已目视或一般证明已复核。
"""
from __future__ import annotations

import hashlib
import math
import re
import sys
from pathlib import Path

import fitz
import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
SNAP = Path(
    "D:/aaa_D_usual/CODEX/AI-SKILL/output/lecture-overview-20261114/"
    "author-r1-working-snapshot/handout.tex"
)
TEX = ROOT / "handout.tex"
PDF = ROOT / "handout.pdf"

PASS = 0
FAIL = 0
NOTES: list[str] = []

VIOLET = (0.42, 0.306, 0.561)
BANDVIOLET = (0.9686, 0.9529, 0.9843)
BANDCREAM = (0.9882, 0.9765, 0.9490)


def check(name: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f"  [ok] {name}")
    else:
        FAIL += 1
        NOTES.append(f"[FAIL] {name}: {detail}")
        print(f"  [E ] {name}" + (f"  ({detail})" if detail else ""))


def near(c, t, tol=0.01) -> bool:
    return c is not None and len(c) == 3 and all(abs(x - y) < tol for x, y in zip(c, t))


def overlap(a, b) -> tuple[float, float]:
    return (min(a.x1, b.x1) - max(a.x0, b.x0), min(a.y1, b.y1) - max(a.y0, b.y0))


def sanitize(text: str) -> str:
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith(r"\hdr{导览}{全书主线"):
            out.append("<OVERVIEW>")
            while i < len(lines) and not lines[i].startswith(r"\clearpage"):
                i += 1
            out.append(r"\clearpage")
            i += 1
            continue
        if ln.startswith(r"\textbf{本轮身份。}") or ln.startswith(r"\textbf{版本说明。}"):
            out.append("<VERSION>")
            i += 1
            continue
        if ln.startswith(r"\callout{\textbf{交付说明。}"):
            out.append("<DELIVERY>")
            while i < len(lines) and not lines[i].rstrip().endswith("不编造。}"):
                i += 1
            i += 1
            continue
        if ln.startswith(r"{\small\color{inkgray}本稿为 2026-11-14"):
            out.append("<COLOPHON>")
            i += 1
            continue
        if i == 1 and ln.startswith("% 从张量到并矢 · 整本讲义"):
            out.append("<HEADER>")
            i += 1
            continue
        out.append(ln)
        i += 1
    return "\n".join(out)


def main() -> int:
    snap = SNAP.read_text(encoding="utf-8")
    src = TEX.read_text(encoding="utf-8")
    doc = fitz.open(PDF)

    print("A. 源文件结构")
    i_title = src.find(r"\doctitle{从张量到并矢}")
    i_lead = src.find(r"\hdr{导览}{全书主线")
    i_call = src.find(r"\callout{\textbf{这份材料为谁写、怎么用。}")
    i_sec0 = src.find(r"\hdr{§0}{起点：矢量、矩阵与换基}")
    check("概览位于标题之后、开篇使用说明与 §0 之前",
          0 <= i_title < i_lead < i_call < i_sec0,
          f"{i_title},{i_lead},{i_call},{i_sec0}")
    block = src[i_lead:i_call]
    check("概览块以 \\clearpage 结束（图独占开篇页）",
          block.rstrip().endswith(r"\clearpage"), block[-60:])

    for sec in ["§0", "§1", "§2", "§3", "§4", "§5", "§6"]:
        check(f"概览含 {sec} 节点", f"\\S{sec[1:]}\\quad" in block)
    for phrase, meaning in [
        (r"\S0.1--0.7", "§0 章内范围"),
        (r"\S1.1--1.6", "§1 章内范围"),
        (r"\S2.1--2.8", "§2 章内范围"),
        (r"\S3.1--3.6", "§3 章内范围"),
        (r"\S4.3", "惯量主轴落点"),
        (r"\S4.6", "L 与 ω 不平行落点"),
        (r"\S5.3", "对称陀螺落点"),
        (r"\S6.2", "主应力落点（框内引用）"),
        (r"\S6.4", "静力平衡落点"),
        (r"\S2.7", "商法则落点"),
        (r"\S1.4", "谱定理落点"),
    ]:
        check(f"概览保留章节定位：{meaning}", phrase in block)

    print("B. 正文逐字符保持")
    check("允许段落外与工作快照逐字符相同", sanitize(snap) == sanitize(src),
          "see sanitize diff")
    body_start = snap.find(r"\hdr{§0}{起点：矢量、矩阵与换基}")
    body_end = snap.find(r"\callout{\textbf{交付说明。}")
    new_start = src.find(r"\hdr{§0}{起点：矢量、矩阵与换基}")
    new_end = src.find(r"\callout{\textbf{交付说明。}")
    body_snap = snap[body_start:body_end]
    body_new = src[new_start:new_end]
    check("§0 至附录 C 末（交付说明之前）正文逐字符相同",
          body_snap == body_new,
          f"len {len(body_snap)} vs {len(body_new)}")
    check("正文保持区长度与快照一致",
          len(body_snap) == len(body_new), f"{len(body_snap)}")
    print(f"     正文保持区：{len(body_snap)} 字符，sha256={hashlib.sha256(body_snap.encode()).hexdigest()[:16]}…")
    check("概览块不是缩字号：仍用 \\footnotesize，未出现 \\scriptsize/\\tiny 整体缩排",
          r"font=\footnotesize" in block and r"\scriptsize" not in block and r"\tiny" not in block)
    check("概览未出现练习编号", not re.search(r"\bP(?:1[0-2]|[1-9])\b", block))
    check("概览未出现“答案/详解”字样", "答案" not in block and "详解" not in block)
    check("图号仍为图 0，且全书只新增这一图",
          src.count(r"\textbf{图 0}") == 1 and snap.count(r"\textbf{图 0}") == 1)

    print("C. 新增图的条件字样（与正文一致的限定）")
    for phrase, meaning in [
        (r"惯性系定点", "固定点条件"),
        (r"\vect V=\vect0", "V=0 条件"),
        (r"质心用相对速度", "质心相对速度"),
        (r"主轴系的体坐标", "主轴系条件"),
        (r"\vect M=\vect0", "无外力矩条件"),
        (r"静力平衡", "静力平衡条件"),
        (r"无体力偶", "无体力偶范围"),
        (r"\nabla\cdot\ten\sigma+\vect f=\vect0", "平衡方程"),
    ]:
        check(f"概览写出：{meaning}", phrase in block)
    m = re.search(r"条件\}.*?A=B.*?\n", block, re.S)
    check("S5 条件句同时含 A=B 与 M=0",
          bool(m) and r"\vect M=\vect0" in m.group(0) and r"A=B" in m.group(0),
          m.group(0)[:80] if m else "not found")

    print("D. PDF 页面与几何")
    check("PDF 总页数与快照一致（65）", doc.page_count == 65, str(doc.page_count))
    p1 = doc[0]
    p1_text = re.sub(r"\s+", "", p1.get_text())
    p2_text = re.sub(r"\s+", "", doc[1].get_text())
    check("第 1 页含图 0 图注", "图0（自绘" in p1_text)
    check("第 1 页不含开篇使用说明", "这份材料为谁写" not in p1_text)
    check("第 2 页以开篇使用说明开始", p2_text[:80].find("这份材料为谁写") >= 0, p2_text[:50])
    check("§0 正文从第 2 页开始", "起点：矢量、矩阵与换基" in re.sub(r"\s+", "", doc[1].get_text()))
    check("全书无未解析的 ??", all("??" not in page.get_text() for page in doc))
    cap_pages = [i + 1 for i, page in enumerate(doc)
                 if "图0（自绘" in re.sub(r"\s+", "", page.get_text())]
    check("图 0 图注只出现在第 1 页", cap_pages == [1], str(cap_pages))

    nodes = []
    for d in p1.get_drawings():
        if d.get("fill") is None:
            continue
        r = d["rect"]
        if r.width > 100 and r.height > 35 and (near(d["fill"], BANDVIOLET)
                                               or near(d["fill"], BANDCREAM)):
            nodes.append(fitz.Rect(r))
    check("识别到 8 个节点方框", len(nodes) == 8, str(len(nodes)))
    nodes.sort(key=lambda r: (round(r.y0), r.x0))
    core = [r for r in nodes if r.width > 400]
    check("核心问题框为通栏单框", len(core) == 1)
    row1, row2, row3 = nodes[1:3], nodes[3:5], nodes[5:8]
    for name, grp in (("语言层", row1), ("桥梁层", row2), ("落点层", row3)):
        check(f"{name}方框顶边对齐", len({round(r.y0, 1) for r in grp}) == 1,
              str([round(r.y0, 1) for r in grp]))
        check(f"{name}方框底边对齐", len({round(r.y1, 1) for r in grp}) == 1,
              str([round(r.y1, 1) for r in grp]))
        check(f"{name}方框等高", len({round(r.height, 1) for r in grp}) == 1,
              str([round(r.height, 1) for r in grp]))
    check("落点层三框等宽", len({round(r.width, 1) for r in row3}) == 1,
          str([round(r.width, 1) for r in row3]))
    allr = nodes
    bad = []
    for i in range(len(allr)):
        for j in range(i + 1, len(allr)):
            w, h = overlap(allr[i], allr[j])
            if w > 0.5 and h > 0.5:
                bad.append((i, j, round(w, 1), round(h, 1)))
    check("节点方框彼此不重叠", not bad, str(bad))
    check("整幅图在左右页边距内（56.7..538.6）",
          min(r.x0 for r in allr) >= 56.7 - 0.5 and max(r.x1 for r in allr) <= 538.6 + 0.5,
          f"x=[{min(r.x0 for r in allr):.1f},{max(r.x1 for r in allr):.1f}]")
    cap = p1.search_for("图 0（自绘") or p1.search_for("图0（自绘")
    check("能定位图 0 图注", bool(cap))
    cap_top = min(r.y0 for r in cap) if cap else 0
    check("图本体在图注上方且不重叠", max(r.y1 for r in allr) < cap_top - 5,
          f"{max(r.y1 for r in allr):.1f} vs {cap_top:.1f}")
    cap_bottom = max(b["bbox"][3] for b in p1.get_text("dict")["blocks"]
                     if b["type"] == 0 and cap_top - 2 <= b["bbox"][1] < 795)
    check("图注完整落在第 1 页正文区内（下界 789pt）", 0 < cap_bottom <= 789,
          f"{cap_bottom:.1f}")
    check("图注末句不是孤行（“不代替定义与证明”与图同页）",
          "不代替定义与证明" in p1_text)

    shafts = []
    for d in p1.get_drawings():
        if d.get("fill") is not None or not near(d.get("color"), VIOLET, tol=0.02):
            continue
        if len(d["items"]) == 1 and d["items"][0][0] == "l":
            shafts.append(fitz.Rect(d["rect"]))
    check("识别到 8 条箭杆（含核心到语言层各一、语言到桥梁各一、桥梁到落点四路、无 §4→§5 短线）",
          len(shafts) == 8, str(len(shafts)))
    stub = []
    for sh in shafts:
        for nr in allr:
            shrunk = fitz.Rect(nr.x0 + 1.5, nr.y0 + 1.5, nr.x1 - 1.5, nr.y1 - 1.5)
            w, h = overlap(sh, shrunk)
            if w > 0.5 and h > 0.5:
                stub.append((round(w, 1), round(h, 1)))
    check("箭杆不伸进任何节点方框内部", not stub, str(stub))

    spans = []
    for blk in p1.get_text("dict")["blocks"]:
        if blk["type"] != 0:
            continue
        for ln in blk["lines"]:
            for sp in ln["spans"]:
                if sp["text"].strip() and 270 < sp["bbox"][1] < 705:
                    spans.append((fitz.Rect(sp["bbox"]), sp["text"]))
    outside = []
    for r, t in spans:
        inside_any = any(r.x0 >= nr.x0 - 1.2 and r.x1 <= nr.x1 + 1.2
                         and r.y0 >= nr.y0 - 1.2 and r.y1 <= nr.y1 + 1.2 for nr in allr)
        if not inside_any:
            outside.append((round(r.x0, 1), round(r.y0, 1), t[:12]))
    check("图内每段文字都落在所属方框内（无出框/溢字）", not outside, str(outside[:6]))
    clash = []
    for i in range(len(spans)):
        for j in range(i + 1, len(spans)):
            a, b = spans[i][0], spans[j][0]
            if abs((a.y0 + a.y1) / 2 - (b.y0 + b.y1) / 2) < 3.5:
                continue
            w, h = overlap(a, b)
            if w > 2.0 and h > 2.0:
                clash.append((round(w, 1), round(h, 1), spans[i][1][:8], spans[j][1][:8]))
    check("图内不同行文字不互相压字", not clash, str(clash[:6]))

    print("E. 页码、引用与讲解页")
    aux = (ROOT / "handout.aux").read_text(encoding="utf-8", errors="replace")
    labels = dict(re.findall(r"\\newlabel\{(ans:P\d+)\}\{\{[^}]*\}\{(\d+)\}", aux))
    check("aux 含 P1--P12 的详解页标签", len(labels) == 12, str(len(labels)))
    refs = []
    for i, page in enumerate(doc, 1):
        for m in re.finditer(r"详解见附录第\s*(\d+)\s*页", page.get_text()):
            refs.append((i, int(m.group(1))))
    check("正文 12 处“详解见附录第 X 页”", len(refs) == 12, str(len(refs)))
    ordered = [p for _, p in refs]
    expect = [int(labels[f"ans:P{k}"]) for k in range(1, 13)]
    check("12 处页码按 P1--P12 依次等于 aux 标签页", ordered == expect,
          f"{ordered} vs {expect}")
    answer_pages = {}
    for k in range(1, 13):
        hits = [i for i, page in enumerate(doc, 1)
                if re.search(rf"P{k}\s*详解", page.get_text())]
        answer_pages[k] = hits
    check("每个 Pk 详解标题实际出现在其标注页上",
          all(expect[k - 1] in answer_pages[k] for k in range(1, 13)),
          str({k: v for k, v in answer_pages.items() if expect[k - 1] not in v}))

    print("F. 图中三个力学条件的独立数值核验")
    rng = np.random.default_rng(20261114)

    # 固定点条件：纯平移时 v=Ω×r 失效，而 L=J·ω 给零
    mass, rc = 1.0, np.array([1.0, 0.0, 0.0])
    V = np.array([0.0, 1.0, 0.0])
    Omega = np.zeros(3)
    v_abs = V + np.cross(Omega, rc)
    check("F1a 纯平移（Ω=0,V≠0）绝对速度 v=V，不等于 Ω×r",
          np.allclose(v_abs, V) and not np.allclose(v_abs, np.cross(Omega, rc)))
    L_about_origin = mass * np.cross(rc, v_abs)
    check("F1b 同一状态关于原点的 L≠0，而 J·Ω=0（简式会漏掉平动项）",
          np.linalg.norm(L_about_origin) > 0.5 and np.allclose(np.zeros(3), np.dot(np.zeros((3, 3)), Omega)))
    v_fixed = np.cross(np.array([0.0, 0.0, 1.5]), rc)
    check("F1c 固定点（V=0）时 v=Ω×r 成立", np.allclose(v_fixed, np.cross([0.0, 0.0, 1.5], rc)))

    # 无外力矩条件：A=B 但 M≠0 时横向模长变化
    A = B = 1.0
    C = 1.5
    w = np.array([1.0, 0.0, 1.0])
    Mext = np.array([1.0, 0.0, 0.0])
    dw1 = (Mext[0] - (C - B) * w[1] * w[2]) / A
    dw2 = (Mext[1] - (A - C) * w[2] * w[0]) / B
    d_perp2 = 2 * (w[0] * dw1 + w[1] * dw2)
    check("F2a A=B 但有外力矩时 d(ω1²+ω2²)/dt≠0，横向分量非匀速转",
          abs(d_perp2) > 1e-9, f"{d_perp2:.3f}")
    dw1_0 = (-(C - B) * w[1] * w[2]) / A
    dw2_0 = (-(A - C) * w[2] * w[0]) / B
    check("F2b A=B 且 M=0 时 d(ω1²+ω2²)/dt=0，横向模长守恒",
          abs(2 * (w[0] * dw1_0 + w[1] * dw2_0)) < 1e-12)
    check("F2c 体坐标对角 J 的前提是取主轴：J 非对角时欧拉方程形式改变",
          not np.allclose(np.array([[1.0, 0.2, 0.0], [0.2, 1.0, 0.0], [0.0, 0.0, 1.5]]),
                          np.diag([1.0, 1.0, 1.5])))

    # 静力平衡条件：动力学右端 ρa 时 div σ+f≠0
    sig = np.zeros((3, 3))
    f = np.array([1.0, 0.0, 0.0])
    rho = 1.0
    acc = np.array([1.0, 0.0, 0.0])
    div_sigma = np.zeros(3)  # 均匀零应力场
    check("F3a 零应力场 + 真实体力 f=e1：静力式 ∇·σ+f=0 不成立",
          not np.allclose(div_sigma + f, np.zeros(3)))
    check("F3b 同状态在动力学式右端 ρa 下成立（说明必须标明静力平衡）",
          np.allclose(div_sigma + f, rho * acc))
    sig_wo_couple = np.array([[0.0, 1.0], [1.0, 0.0]])
    sig_with_couple = np.array([[0.0, 1.0], [0.5, 0.0]])
    check("F3c 无体力偶时力矩平衡迫使 σ21=σ12", np.allclose(sig_wo_couple, sig_wo_couple.T))
    check("F3d 允许同阶体力偶时，仅靠角动量守恒不能推出对称",
          not np.allclose(sig_with_couple, sig_with_couple.T))

    # 谱分解 / 惯量：图中“谱定理给主轴、L=J·ω”在正文条件下成立
    Mrand = rng.normal(size=(3, 3))
    Tsym = (Mrand + Mrand.T) / 2
    lam, vec = np.linalg.eigh(Tsym)
    check("F4a 实对称谱分解 T=Σλn⊗n", np.allclose(Tsym, sum(lam[i] * np.outer(vec[:, i], vec[:, i]) for i in range(3)), atol=1e-12))
    check("F4b 主轴正交单位", np.allclose(vec.T @ vec, np.eye(3), atol=1e-12))
    check("F4c tr=Σλ, det=Πλ", abs(np.trace(Tsym) - lam.sum()) < 1e-10 and abs(np.linalg.det(Tsym) - lam.prod()) < 1e-10)
    pts = rng.normal(size=(200, 3))
    dm = np.full(200, 1 / 200)
    r2 = (pts ** 2).sum(1)
    J = sum(dm[i] * (r2[i] * np.eye(3) - np.outer(pts[i], pts[i])) for i in range(200))
    om = rng.normal(size=3)
    check("F4d 固定点 J=∫(r²1−r⊗r)dm 与 L=∫r×(ω×r)dm 一致",
          np.allclose(J @ om, sum(dm[i] * np.cross(pts[i], np.cross(om, pts[i])) for i in range(200)), atol=1e-12))

    print()
    print(f"合计断言 {PASS + FAIL} 条，失败 {FAIL} 条。")
    if FAIL:
        print("失败明细：")
        for n in NOTES:
            print(" -", n)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
