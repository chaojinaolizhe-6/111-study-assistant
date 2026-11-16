# -*- coding: utf-8 -*-
"""页码/引用一致性检查（按最终 PDF 与 aux 实测，不沿用旧页数）。

只做能自动判定的事：
  1. PDF 页数与编译日志、aux 一致；
  2. 12 道练习正文的“详解见附录第 N 页”与 aux 中 ans:Pk 的实际页一致，
     且每个 N 页上确实能找到该题的详解块（题号 + 题干）；
  3. 开篇页（图 0）与开篇使用说明的先后；
  4. 章节标题起页单调递增并打印实际页码表；
  5. 全文没有未解析的“??”。
不代替渲染页目视，也不重跑数学验证。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import fitz

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
PDF = ROOT / "handout.pdf"
AUX = ROOT / "handout.aux"
LOG = ROOT / "handout.log"
TEX = ROOT / "handout.tex"

PASS = 0
FAIL = 0
DETAIL: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
        DETAIL.append(f"[FAIL] {name}: {detail}")
    print(("  [ok] " if ok else "  [E ] ") + name + (f"  ({detail})" if detail and not ok else ""))


def flat(page) -> str:
    return re.sub(r"\s+", "", page.get_text())


def main() -> int:
    doc = fitz.open(PDF)
    n = doc.page_count
    aux = AUX.read_text(encoding="utf-8")
    log = LOG.read_text(encoding="utf-8", errors="replace")

    print("1. 页数一致性")
    m = re.search(r"Output written on .*?\((\d+) pages?\)", log)
    check("编译日志记录了 PDF 页数", bool(m), "日志无 Output written")
    check("日志页数与最终 PDF 一致", bool(m) and int(m.group(1)) == n,
          f"{m.group(1) if m else '?'} vs {n}")
    print(f"  最终 PDF：{n} 页")

    print("2. 练习详解页引用")
    ans = {k: int(v) for k, v in
           re.findall(r"\\newlabel\{ans:(P\d+)\}\{\{\}\{(\d+)\}", aux)}
    check("aux 中 12 个 ans:Pk 标签齐全", len(ans) == 12, str(sorted(ans)))
    refs = []
    for p in doc:
        for b in sorted(p.get_text("blocks"), key=lambda b: (round(b[1], 1), b[0])):
            t = re.sub(r"\s+", "", b[4])
            for mm in re.finditer(r"详解见附录第(\d+)页", t):
                refs.append(int(mm.group(1)))
    check("正文印出的 12 个详解页码", len(refs) == 12, f"{len(refs)}")
    expected = [ans[f"P{k}"] for k in range(1, 13)]
    check("印出页码与 aux 实际页逐题一致", refs == expected, f"{refs} vs {expected}")

    ok_block = True
    for k in range(1, 13):
        pid, pg = f"P{k}", ans[f"P{k}"]
        t = flat(doc[pg - 1])
        if pid not in t or "题干" not in t:
            ok_block = False
            DETAIL.append(f"[FAIL] P{k} 详解页 {pg} 上找不到题号或题干")
    check("每题所引页码上确有该题详解块（题号 + 题干）", ok_block)

    print("3. 开篇页")
    p1, p2 = flat(doc[0]), flat(doc[1])
    check("第 1 页是导览页（含图 0 图注）", "图0（自绘" in p1 and "全书要回答的问题" in p1)
    check("第 1 页不含开篇使用说明", "这份材料为谁写" not in p1)
    check("第 2 页开始是开篇使用说明", "这份材料为谁写" in p2[:120])

    print("4. 章节起页（最终 PDF 实测）")
    titles = [
        ("导览", "全书主线：一张图先看路线"),
        ("§0", "起点：矢量、矩阵与换基"),
        ("§1", "二次型与主轴：椭球、特征值、谱定理"),
        ("§2", "张量与并矢：对象、写法、运算"),
        ("§3", "旋转算子与角速度：课件"),
        ("§4", "落点一：转动惯量张量"),
        ("§5", "落点二：输运定理、欧拉方程与对称陀螺"),
        ("§6", "落点三：应力张量"),
        ("§7", "独立练习"),
        ("§8", "易错点、速查与三句话"),
        ("附录A", "练习详解"),
        ("附录B", "指标与记号速查"),
        ("附录C", "来源对应、补充与自补推导"),
    ]
    pages = {}
    for label, title in titles:
        tt = re.sub(r"\s+", "", title)
        found = [i + 1 for i, p in enumerate(doc) if tt in flat(p)]
        body = [x for x in found if x >= 3] or found
        pages[label] = body[0] if body else None
    for label, _ in titles:
        print(f"  {label}: p{pages[label]}")
    order = [pages[l] for l, _ in titles]
    check("各章标题都能定位", all(order), str(pages))
    check("章节起页按正文顺序不减", all(a <= b for a, b in zip(order, order[1:])), str(order))
    check("除附录 B/C 同页外，其余章节起页严格递增",
          sum(1 for a, b in zip(order, order[1:]) if a < b) >= len(order) - 2, str(order))
    check("§0 仍在第 2 页", pages["§0"] == 2, str(pages["§0"]))
    check("图 0 在正文之前（第 1 页）", pages["导览"] == 1, str(pages["导览"]))

    print("5. 未解析引用")
    qq = sum(flat(p).count("??") for p in doc)
    check("全文没有未解析的 ?? 引用", qq == 0, f"{qq} 处")
    unref = len(re.findall(r"LaTeX Warning: Reference", log)) + len(
        re.findall(r"undefined references", log, re.I))
    check("日志没有未解析引用警告", unref == 0, f"{unref} 处")


    print("6. 已验收正文是否原样保留（与只读基线逐行比对）")
    import difflib
    base = (ROOT.parent.parent / "讲义skill-v2.3-张量并矢整本-20261111" / "round-04" / "handout.tex")
    if not base.exists():
        check("找到只读基线源文件", False, str(base))
    else:
        A = base.read_text(encoding="utf-8-sig").splitlines()
        B = TEX.read_text(encoding="utf-8-sig").splitlines()
        i0 = next(i for i, l in enumerate(B) if l.startswith(r"\hdr{导览}"))
        i1 = next(i for i in range(i0, len(B)) if B[i].strip() == r"\clearpage")
        B2 = B[:i0] + B[i1 + 1:]
        # 去掉删除块留下的多余空行后再比对
        A2, B3 = [], []
        for x in A:
            if x.strip() or (A2 and A2[-1].strip()):
                A2.append(x)
        for x in B2:
            if x.strip() or (B3 and B3[-1].strip()):
                B3.append(x)
        sm = difflib.SequenceMatcher(None, A2, B3, autojunk=False)
        ops = [op for op in sm.get_opcodes() if op[0] != "equal"]
        changed = [A2[op[1]:op[2]] for op in ops]
        expected_markers = ["% 从张量到并矢", r"\textbf{本轮身份。}", r"\callout{\textbf{交付说明。}",
                            "{\\small\\color{inkgray}本稿为"]
        ok = (len(ops) == 4 and all(op[0] == "replace" and op[2] - op[1] == 1
                                    and op[4] - op[3] == 1 for op in ops)
              and all(any(line.startswith(m) for m in expected_markers) for grp in changed for line in grp))
        check("除 4 处版本/交付元信息外，正文各行与基线完全一致", ok,
              f"opcodes={[(o[0], o[2]-o[1], o[4]-o[3]) for o in ops]}")
        import hashlib
        base_sha = hashlib.sha256(base.read_bytes()).hexdigest().upper()
        check("基线源文件本轮未被改动（哈希与复制起点一致）",
              base_sha == "5F48C5019A066CAC429B6157D35275A97FD20A939EA225D385E0A48DE8E6945A",
              base_sha)
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
