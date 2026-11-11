# -*- coding: utf-8 -*-
"""Checks for comparison.pdf: pages, text layer, page labels, crops, margins, log.

This is a structural/text-layer check. It does NOT read pixels and is not a
visual acceptance; see verification.txt for that limitation.
"""
import fitz
import hashlib
import json
import os
import re
import sys
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, "comparison.pdf")
LOG = os.path.join(HERE, "comparison.log")
RENDER = os.path.join(HERE, "render")
LIMIT = 25 * 1024 * 1024

PASS, FAIL = [], []


def norm(s):
    s = s.replace("\x00", "").replace("\r", "").replace("\n", "")
    return re.sub(r"\s+", "", s)


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f" | {detail}" if detail else ""))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true",
                        help="accepted for build.ps1 compatibility; checks are always strict")
    parser.parse_args()
    with open(os.path.join(HERE, "crops.json"), encoding="utf-8") as f:
        crops = json.load(f)["crops"]
    with open(os.path.join(HERE, "render-crops.json"), encoding="utf-8") as f:
        rc = json.load(f)["crops"]
    rc_by_key = {r["key"]: r for r in rc}
    tex = open(os.path.join(HERE, "comparison.tex"), encoding="utf-8").read()
    check("crops.json has 28 definitions", len(crops) == 28, f"count={len(crops)}")
    check("render-crops count matches crops.json", len(rc) == len(crops),
          f"{len(rc)} vs {len(crops)}")

    # ---- PDF identity
    check("comparison.pdf exists", os.path.isfile(PDF))
    size = os.path.getsize(PDF)
    check("comparison.pdf < 25 MiB", size < LIMIT, f"{size/1024/1024:.2f} MiB")
    with open(PDF, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print(f"[INFO] comparison.pdf sha256 = {digest}")
    doc = fitz.open(PDF)
    n = doc.page_count
    check("comparison.pdf page count is plausible", 15 <= n <= 30, f"pages={n}")
    check("all pages A4", all(abs(p.rect.width - 595.28) < 1 and abs(p.rect.height - 841.89) < 1
                              for p in doc))

    pages = [norm(p.get_text()) for p in doc]

    # ---- section headings and key content
    wanted = [
        "新旧对比册", "本次性质与分工", "轮次与规则", "比较方法",
        "起点支持", "中间步骤与例图", "选读与主线", "未解释术语",
        "旧稿未被否定的部分", "仍未验证与不应声称的", "本册的检查范围",
        "裁剪清单", "20261105", "20261103", "R1", "2.2.1", "2.2.2",
        "没有本轮具体问题单", "不能声称", "试读未发生", "不把页数更多",
        "协调器只维护skill", "review_limits", "未做。未看图",
    ]
    for w in wanted:
        check(f"text contains {w!r}", any(norm(w) in p for p in pages))

    # ---- crop labels: label page and y anchor must appear as typeset text
    for c in crops:
        label = "旧稿" if c["pdf"] == "old" else "新稿"
        need = norm(f"{label}p{c['page']}")
        yneed = norm(f"y={c['y0']}")
        found = [i + 1 for i, p in enumerate(pages) if need in p and yneed in p]
        check(f"crop label {c['key']} at {label} p{c['page']} y={c['y0']}", bool(found),
              f"found on pages {found[:4]}")

    # ---- every crop referenced in tex exactly as a key; all referenced exist
    used = set(re.findall(r"\\cropimg(?:\[[^\]]*\])?\{([^}]+)\}", tex))
    check("all crops used in tex", used == {c["key"] for c in crops},
          f"missing={sorted({c['key'] for c in crops} - used)} unknown={sorted(used - {c['key'] for c in crops})}")

    # ---- crop images present, dimensions match report, inside page
    ok_dim = True
    for r in rc:
        path = os.path.join(HERE, "figs", r["key"] + ".png")
        if not (os.path.isfile(path) and os.path.getsize(path) > 1000):
            ok_dim = False
            check(f"crop png exists {r['key']}", False)
            continue
        img = fitz.Pixmap(path)
        if [img.width, img.height] != r["pixels"]:
            ok_dim = False
            check(f"crop png size {r['key']}", False, f"{img.width}x{img.height} vs {r['pixels']}")
        x0, y0, x1, y1 = r["clip_pt"]
        if not (x0 >= 0 and y0 >= 0 and x1 <= 595.28 and y1 <= 841.89 and x1 > x0 and y1 > y0):
            ok_dim = False
            check(f"crop rect inside page {r['key']}", False, str(r["clip_pt"]))
    check("all crop pngs present with recorded dimensions and in-page rects", ok_dim)

    # ---- PDF page images: number of included images and geometry
    image_pages = 0
    geom_ok = True
    total_images = 0
    for i, pg in enumerate(doc):
        infos = pg.get_images(full=True)
        total_images += len(infos)
        for info in infos:
            xref = info[0]
            for r in pg.get_image_rects(xref):
                if r.width < 100:      # skip tiny decorations if any
                    continue
                image_pages += 1
                if not (r.x0 > 40 and r.x1 < 556 and r.y0 > 20 and r.y1 < 822):
                    geom_ok = False
                    check(f"image inside margins p{i+1}", False, f"{r}")
                if r.width > 479:
                    geom_ok = False
                    check(f"image not wider than text block p{i+1}", False, f"w={r.width:.1f}")
    check("all page images inside margins and text width", geom_ok)
    check("PDF contains at least 24 substantial page images", image_pages >= 24,
          f"image placements={image_pages}, xobjects={total_images}")

    # ---- text/image blocks inside page box
    margin_ok = True
    for i, pg in enumerate(doc):
        for b in pg.get_text("blocks"):
            x0, y0, x1, y1 = b[:4]
            if b[6] != 0:
                continue
            if not (x0 > 35 and x1 < 560 and y0 > 18 and y1 < 825):
                margin_ok = False
                check(f"text block inside page {i+1}", False, f"{x0:.1f},{y0:.1f}-{x1:.1f},{y1:.1f}")
    check("all text blocks inside page", margin_ok)

    # ---- no placeholders / unresolved refs
    joined = "".join(pages)
    check("no unresolved ?? in text", "??" not in joined)
    check("no TODO placeholder", "TODO" not in joined and "占位" not in joined)

    # ---- revision-specific content checks (COMP-C1..C4, CMP-MATH-01)
    withdrawn = [
        "约定本身没有在旧稿正文出现",
        "旧稿把它交给课件",
        "只能记住矩阵的三个元素",
        "只会在“特征值”一词上需要回看",
        "外部目视未完成",
        "瞬时轴三个词没有解释",
    ]
    for s in withdrawn:
        check(f"withdrawn claim absent: {s}", not any(norm(s) in p for p in pages))
    required = [
        "旧稿在§4.3写出规则",
        "新稿补六个排列与重复指标规则",
        "旧稿§8.3",
        "旧稿§9.4",
        "直接代回可以当场核对",
        "偏导在做什么",
        "瞬时轴是新稿",
        "外部内容、数学、视觉审核已完成",
        "仍需外部复核",
        "28处裁剪",
    ]
    for s in required:
        check(f"revised text contains {s!r}", any(norm(s) in p for p in pages))

    # ---- headers present on every page
    check("every page has running header", all("新旧对比册" in p and "理论力学" in p for p in pages))

    # ---- compile log
    log = open(LOG, encoding="utf-8", errors="replace").read()
    check("log has no Overfull", "Overfull \\hbox" not in log and "Overfull \\vbox" not in log)
    check("log has no Missing character", "Missing character" not in log)
    check("log has no undefined control/reference", "Undefined control sequence" not in log
          and "undefined references" not in log.lower())
    check("log has no LaTeX error", "LaTeX Error" not in log)
    check("log records final page count", f"({n} pages)" in log or f"({n} pages," in log,
          f"expected {n}")
    under = log.count("Underfull \\hbox")
    print(f"[INFO] Underfull hbox count = {under}")

    # ---- final renders
    if os.path.isdir(RENDER):
        renders = sorted(f for f in os.listdir(RENDER) if re.fullmatch(r"page-\d+\.png", f))
        check("render count equals PDF page count", len(renders) == n, f"{len(renders)} vs {n}")
        ok = all(os.path.getsize(os.path.join(RENDER, f)) > 5000 for f in renders)
        check("render files non-trivial", ok)
    else:
        check("render directory exists", False)

    print()
    print(f"TOTAL: {len(PASS)} passed, {len(FAIL)} failed")
    if FAIL:
        print("FAILED:", "; ".join(FAIL))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
