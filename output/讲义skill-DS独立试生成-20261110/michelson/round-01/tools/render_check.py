# -*- coding: utf-8 -*-
r"""对渲染后的 handout.pdf 做几何与版面核对（模型无图像输入时的量化替代检查）。

与 check_handout.py 的分工：后者查 TeX 源结构与编译日志，本脚本查真正的 PDF 版面。
检查项：
  1. 页面尺寸；
  2. 文字是否越出可打印区（左右允许中文标点悬挂 ≤10pt，下沿允许字体下沉 ≤13pt）；
  3. 不同文字行之间是否重叠（可发现 TikZ 标注重叠、表格挤压）；
  4. 向量图形是否越出左右边界；
  5. 每张图与其图注同页、图在注上方；
  6. §4 各题「题干」与英文答案是否同页（问答位置）；
  7. 节标题是否成为页末孤行；
  8. 跨页长表是否重复表头；
  9. 未解析引用残留（"??"）与可疑空页。

用法：python -B michelson/round-01/tools/render_check.py
退出码：0 通过；1 有失败项。
"""
from __future__ import annotations

import sys
from pathlib import Path

import fitz

PDF = Path(__file__).resolve().parents[1] / "handout.pdf"

W, H = 595.276, 841.890
LEFT = RIGHT = 2.0 / 2.54 * 72
TOP = 2.1 / 2.54 * 72
BOTTOM = 2.3 / 2.54 * 72
TEXT_W = W - LEFT - RIGHT
TEXT_BOTTOM = H - BOTTOM

HANG = 10.0      # 中文标点悬挂允许值
DEPTH = 13.0     # 字体 bbox 下沉允许值

CAPTIONS = ["图1", "图2", "图3", "图4", "图A1"]
QA_IDS = ["II-1", "II-2", "II-3", "II-6", "II-7", "II-8", "II-9", "附加(1)", "附加(2)"]
TABLE_HEADERS = {
    "英文名称": ["moving mirror pallet"],
    "源栏目": ["Preview · 第 3 页数据表"],
    "题号": ["IV-1 -- IV-4"],
    "要算的量": ["条纹可见度"],
}

fails: list[str] = []
notes: list[str] = []


def fail(msg: str) -> None:
    fails.append(msg)


def lines_of(page: fitz.Page) -> list[dict]:
    out = []
    for block in page.get_text("dict")["blocks"]:
        if block.get("type") != 0:
            continue
        for ln in block["lines"]:
            txt = "".join(s["text"] for s in ln["spans"]).strip()
            if txt:
                out.append({"text": txt, "bbox": ln["bbox"]})
    out.sort(key=lambda d: (d["bbox"][1], d["bbox"][0]))
    return out


def is_footer(ln: dict) -> bool:
    """页脚：页码行（含孤立数字与花饰），基线在正文下沿之外。"""
    return ln["bbox"][0] > 250 and ln["bbox"][3] > TEXT_BOTTOM


def main() -> int:
    if not PDF.exists():
        print(f"[E] 找不到 {PDF}")
        return 1
    doc = fitz.open(PDF)
    print(f"页数 {doc.page_count}，页面 {doc[0].rect.width:.1f}x{doc[0].rect.height:.1f}pt，"
          f"正文宽 {TEXT_W:.1f}pt")

    for i, page in enumerate(doc, 1):
        r = page.rect
        if abs(r.width - W) > 1 or abs(r.height - H) > 1:
            fail(f"p{i} 页面尺寸异常")
        lines = lines_of(page)
        drawings = page.get_drawings()
        body = [ln for ln in lines if not is_footer(ln)]
        # 2. 边界
        for ln in lines:
            x0, y0, x1, y1 = ln["bbox"]
            if x0 < LEFT - HANG or x1 > W - RIGHT + HANG:
                fail(f"p{i} 文字越左右边界（{x0:.1f},{x1:.1f}）：{ln['text'][:26]!r}")
            if y1 > TEXT_BOTTOM + DEPTH and not is_footer(ln):
                fail(f"p{i} 正文越下边界（y1={y1:.1f}）：{ln['text'][:26]!r}")
            if "??" in ln["text"]:
                fail(f"p{i} 有未解析引用：{ln['text'][:30]!r}")
        # 3. 行间重叠（只比正常行高的正文行；上下标、分式碎片、数学行不计）
        cand = [ln for ln in body if 9.0 <= ln["bbox"][3] - ln["bbox"][1] <= 12.6
                and len(ln["text"]) >= 4]
        for a in range(len(cand)):
            for b in range(a + 1, len(cand)):
                ax0, ay0, ax1, ay1 = cand[a]["bbox"]
                bx0, by0, bx1, by1 = cand[b]["bbox"]
                ia = min(ay1, by1) - max(ay0, by0)
                iw = min(ax1, bx1) - max(ax0, bx0)
                hmin = min(ay1 - ay0, by1 - by0)
                if ia > 0.6 * hmin and iw > 3 and ia * iw > 10:
                    fail(f"p{i} 行重叠 {ia*iw:.1f}pt²：{cand[a]['text'][:20]!r} ／ "
                         f"{cand[b]['text'][:20]!r}")
        # 4. 图形边界
        for d in drawings:
            rect = d.get("rect")
            if rect is None:
                continue
            if rect.x0 < LEFT - 2.5 or rect.x1 > W - RIGHT + 2.5:
                fail(f"p{i} 图形越左右边界：x=({rect.x0:.1f},{rect.x1:.1f})")
        # 9. 空页/页末留白
        if len(body) < 4:
            notes.append(f"p{i} 正文只有 {len(body)} 行")
        if body:
            last = max(ln["bbox"][3] for ln in body)
            span = last - TOP
            print(f"  p{i:2d}: 行 {len(body):3d}  图形 {len(drawings):3d}  "
                  f"正文末 y={last:6.1f}（约占正文高 {100*span/(TEXT_BOTTOM-TOP):4.0f}%）")
            if last < TEXT_BOTTOM - 110:
                notes.append(f"p{i} 页末留白约 {TEXT_BOTTOM-last:.0f}pt（>15% 正文高），请核对是否图/表强制分页")

    # 5. 图与图注
    for cap in CAPTIONS:
        hits = []
        for p in range(1, doc.page_count + 1):
            ls = lines_of(doc[p - 1])
            for k, ln in enumerate(ls):
                if ln["text"] == cap:
                    # 图注：紧跟同样 y 的说明行
                    same = [x for x in ls if abs(x["bbox"][1] - ln["bbox"][1]) < 3
                            and x["text"] != cap]
                    hits.append((p, ln, same))
                    break
        if len(hits) != 1:
            fail(f"图注「{cap}」命中 {len(hits)} 处（应为 1）")
            continue
        p, ln, same = hits[0]
        if not same:
            fail(f"图注「{cap}」（p{p}）没有说明文字")
        above = [d for d in doc[p - 1].get_drawings()
                 if d.get("rect") is not None and d["rect"].y1 <= ln["bbox"][1] + 1]
        if not above:
            fail(f"图注「{cap}」（p{p}）上方同页没有图形")
        else:
            gap = ln["bbox"][1] - max(d["rect"].y1 for d in above)
            notes.append(f"图注「{cap}」p{p}，图与注间距 {gap:.1f}pt")

    # 6. 问答同页（用题干框里唯一的来源串定位）
    for qid in QA_IDS:
        key = qid
        hit = None
        for p in range(1, doc.page_count + 1):
            ls = lines_of(doc[p - 1])
            for ln in ls:
                if key in ln["text"] and "预习" in ln["text"]:
                    hit = (p, ln, ls)
                    break
            if hit:
                break
        if hit is None:
            fail(f"找不到题目「{qid}」的题干来源串")
            continue
        p, ln, ls = hit
        ans = [x for x in ls if "Answer" in x["text"]]
        if not ans:
            fail(f"「{qid}」（p{p}）题干页没有英文答案，问答被分到两页（需补续页标记）")
        else:
            notes.append(f"「{qid}」题干与英文答案同在 p{p}")

    # 7. 节标题孤行
    for p in range(1, doc.page_count + 1):
        ls = lines_of(doc[p - 1])
        for k, ln in enumerate(ls):
            if ln["text"].startswith("§") and len(ln["text"]) < 30:
                after = [x for x in ls
                         if ln["bbox"][3] < x["bbox"][1] < ln["bbox"][3] + 100]
                if not after:
                    fail(f"p{p} 节标题 {ln['text'][:16]!r} 下方 100pt 内没有正文")

    # 8. 跨页长表重复表头
    for header_word, markers in TABLE_HEADERS.items():
        pages = [p for p in range(1, doc.page_count + 1)
                 if any(m in doc[p - 1].get_text() for m in markers)]
        for p in pages:
            if header_word not in doc[p - 1].get_text():
                fail(f"p{p} 有长表内容但缺表头「{header_word}」")

    # 9. 图形线段是否穿过文字（TikZ 标注重叠的另一种表现；只报线索）
    for p in range(1, doc.page_count + 1):
        page = doc[p - 1]
        segs = []
        for d in page.get_drawings():
            for it in d["items"]:
                if it[0] == "l":
                    a, b = it[1], it[2]
                    if abs(a.y - b.y) < 1.0 and abs(a.x - b.x) > 1.0:
                        continue          # 水平线段多为分式横线/表格线，不参与判断
                    segs.append((a.x, a.y, b.x, b.y))
        for ln in lines_of(page):
            if is_footer(ln):
                continue
            x0, y0, x1, y1 = ln["bbox"]
            if len(ln["text"]) < 1 or (x1 - x0) < 2:
                continue
            ex0, ey0, ex1, ey1 = x0 + 1.5, y0 + 1.5, x1 - 1.5, y1 - 1.5
            for (ax, ay, bx, by) in segs:
                # 线段与内缩矩形求交（仅处理与矩形边界的分段判断）
                if max(ax, bx) < ex0 or min(ax, bx) > ex1:
                    continue
                if max(ay, by) < ey0 or min(ay, by) > ey1:
                    continue
                # 快速判据：线段两端都在矩形外且不相交则跳过；这里用密集采样近似
                n = 12
                inside = False
                for k in range(n + 1):
                    t = k / n
                    px, py = ax + (bx - ax) * t, ay + (by - ay) * t
                    if ex0 < px < ex1 and ey0 < py < ey1:
                        inside = True
                        break
                if inside:
                    notes.append(f"p{p} 线段穿过文字「{ln['text'][:16]}」"
                                 f"（{ax:.0f},{ay:.0f}）-({bx:.0f},{by:.0f})")
                    break

    print(f"\n检查完成：失败 {len(fails)} 项")
    for f in fails:
        print("  [FAIL]", f)
    if notes:
        print("提示（供人工复核，不是错误）：")
        for n in notes:
            print("  [NOTE]", n)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
