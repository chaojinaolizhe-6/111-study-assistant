"""把电工学课件登记进 learning/materials.json（资料读取事实源）。

为什么必须登记
--------------
工作区的规则是「上传 ≠ 读过」：`learning/materials.json` 记录的是**资料读取事实**
（哪些页取过文字、渲染过图、视觉读过、核验过公式），与能力事实分开。
电工课件过去只有 INDEX.md 里一句「内容未逐页读入」，没有登记页级事实；
本脚本按 AI 可读层实际产出的覆盖范围写入，且**只写程序能证明的字段**：

  text_extracted_pages  ← index/pages.jsonl 里有非空正文的页
  rendered_pages        ← 实际存在 assets/<deck>/p###.jpg 的页
  visually_read_pages   ← figure-descriptions.json 中有描述的页（视觉通读产物）
  formula_verified_pages← 默认不写；只有显式 --formula-verified 才写（须另有复核依据）

用法：
  python tools/ee-materials-register.py                 # 按现有产物登记（幂等）
  python tools/ee-materials-register.py --print         # 只打印将要写入的内容
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUBJECT = ROOT / "subjects" / "06-电工电子技术"
LAYER = SUBJECT / "课件-AI可读"
MATERIALS = ROOT / "learning" / "materials.json"

DECK_ORDER = ["C1-1", "C1-2", "C1-3", "C1-4", "C2-1", "C2-2",
              "C3-1", "C3-2", "C3-3", "C4-1", "C4-2", "C4-3"]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_rows() -> list[dict]:
    path = LAYER / "index" / "pages.jsonl"
    if not path.exists():
        print(f"[FAIL] 缺少 {path}；先跑 tools/ee-slides-build.py build", file=sys.stderr)
        sys.exit(2)
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--print", dest="dry", action="store_true")
    args = ap.parse_args()

    rows = load_rows()
    desc_path = LAYER / "index" / "figure-descriptions.json"
    described = set(json.loads(desc_path.read_text(encoding="utf-8"))) if desc_path.exists() else set()

    by_deck: dict[str, list[dict]] = {}
    for r in rows:
        by_deck.setdefault(r["deck"], []).append(r)

    doc = json.loads(MATERIALS.read_text(encoding="utf-8"))
    materials = doc["materials"]
    index = {m["path"]: m for m in materials}
    added, updated = [], []

    for deck_id in DECK_ORDER:
        rs = by_deck.get(deck_id)
        if not rs:
            print(f"[SKIP] {deck_id}：AI 可读层里没有该册", file=sys.stderr)
            continue
        src_rel = rs[0]["source"]
        pdf = ROOT / src_rel
        if not pdf.exists():
            print(f"[SKIP] {deck_id}：源 PDF 不存在 {src_rel}", file=sys.stderr)
            continue
        # 文字层事实：该页的 PDF 文字层是否取到了内容。课件多是「标题 + 一张整图」，
        # 这些页正文为空但文字层仍有元件标注，故正文与标注任一非空即算取到。
        text_pages = sorted(r["page"] for r in rs
                            if (r.get("text") or "").strip() or (r.get("labels") or []))
        rendered = sorted(r["page"] for r in rs if (LAYER / r["page_image"]).exists())
        visual = sorted(r["page"] for r in rs if f"{deck_id}#{r['page']}" in described)
        rec = {
            "path": src_rel,
            "sha256": sha256_file(pdf),
            "page_count": len(rs),
            "text_extracted_pages": text_pages,
            "rendered_pages": rendered,
            "visually_read_pages": visual,
            "formula_verified_pages": [],
            "note": ("教师课件（PPT 导出 PDF）。页级事实来自 课件-AI可读/ 层，"
                     "由 tools/ee-materials-register.py 按实际产出登记："
                     "text_extracted=PDF 文字层取到正文或元件标注的页（电路图本身是位图，"
                     "少数整页图无任何文字层内容属源件限制）；rendered=已导出整页扫描图；"
                     "visually_read=已由视觉通读写成图区描述。"
                     "登记不等于理解，也不构成任何掌握证据。"),
        }
        if src_rel in index:
            index[src_rel].update(rec)
            updated.append(deck_id)
        else:
            materials.append(rec)
            index[src_rel] = rec
            added.append(deck_id)

    if args.dry:
        for deck_id in DECK_ORDER:
            rs = by_deck.get(deck_id) or []
            if not rs:
                continue
            n_text = sum(1 for r in rs if (r.get("text") or "").strip())
            n_rend = sum(1 for r in rs if (LAYER / r["page_image"]).exists())
            n_vis = sum(1 for r in rs if f"{deck_id}#{r['page']}" in described)
            print(f"  {deck_id}: 共 {len(rs)} 页；正文 {n_text}、渲染 {n_rend}、视觉通读 {n_vis}")
        print(f"[DRY] 新增 {len(added)} 条（{', '.join(added) or '—'}），"
              f"更新 {len(updated)} 条；materials 总数 {len(materials)}")
        return 0

    doc["materials"] = materials
    MATERIALS.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[OK] 新增 {len(added)} 条（{', '.join(added) or '—'}），"
          f"更新 {len(updated)} 条（{', '.join(updated) or '—'}）；"
          f"materials 总数 {len(materials)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
