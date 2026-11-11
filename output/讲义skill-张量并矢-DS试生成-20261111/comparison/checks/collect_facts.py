# -*- coding: utf-8 -*-
"""Read-only fact collector for the frozen comparison deliverable.

Collects page counts, sizes, SHA-256 hashes, crop/render consistency and
compile-log facts into checks/facts.json.  It never rebuilds, recompiles or
writes any frozen deliverable (comparison.pdf/.tex, crops.json, figs/).
"""
import datetime
import hashlib
import json
import os
import re

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
COMP = os.path.dirname(HERE)
ROOT = os.path.dirname(COMP)

PDF = os.path.join(COMP, "comparison.pdf")
TEX = os.path.join(COMP, "comparison.tex")
CROPS = os.path.join(COMP, "crops.json")
RCROPS = os.path.join(COMP, "render-crops.json")
LOG = os.path.join(COMP, "comparison.log")
RENDER = os.path.join(COMP, "render")
FIGS = os.path.join(COMP, "figs")
SEL = os.path.join(ROOT, "final-selection.json")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path):
    return os.path.relpath(path, ROOT).replace("\\", "/")


def norm(s):
    return re.sub(r"\s+", "", s.replace("\x00", "").replace("\r", "").replace("\n", ""))


def main():
    with open(SEL, encoding="utf-8") as fh:
        sel = json.load(fh)
    doc = fitz.open(PDF)
    pages = [norm(p.get_text()) for p in doc]

    # text-layer structure: running header, page-number footer, A4, size
    header_ok = all("新旧对比册" in p and "理论力学" in p for p in pages)
    footer_ok = all(f":{i + 1}:" in p for i, p in enumerate(pages))
    a4_ok = all(abs(p.rect.width - 595.28) < 1 and abs(p.rect.height - 841.89) < 1
                for p in doc)
    text_chars = sum(len(p.get_text()) for p in doc)

    # image placements (substantial only, same rule as check_compare.py)
    placements = 0
    for pg in doc:
        for info in pg.get_images(full=True):
            for r in pg.get_image_rects(info[0]):
                if r.width >= 100:
                    placements += 1

    # crops: config vs rendered report vs actual PNG files
    with open(CROPS, encoding="utf-8") as fh:
        crops_cfg = json.load(fh)
    with open(RCROPS, encoding="utf-8") as fh:
        rc = json.load(fh)
    fig_hash_mismatch = []
    for c in rc["crops"]:
        p = os.path.join(FIGS, c["key"] + ".png")
        if not os.path.isfile(p) or sha256(p) != c["png_sha256"]:
            fig_hash_mismatch.append(c["key"])

    # re-check every crop anchor against the frozen source PDFs (read-only)
    src_docs = {
        "old": fitz.open(sel["old_handout"]["path"]),
        "new": fitz.open(sel["handout"]["path"]),
    }
    crop_failures = []
    for c in crops_cfg["crops"]:
        d = src_docs[c["pdf"]]
        if not (1 <= c["page"] <= d.page_count):
            crop_failures.append(f"{c['key']}: page {c['page']} outside 1..{d.page_count}")
            continue
        pg = d[c["page"] - 1]
        rect = fitz.Rect(crops_cfg["x0"], c["y0"], crops_cfg["x1"], c["y1"])
        if not (rect.x0 >= 0 and rect.y0 >= 0
                and rect.x1 <= pg.rect.x1 and rect.y1 <= pg.rect.y1):
            crop_failures.append(f"{c['key']}: clip outside source page")
        clip_text = pg.get_text("text", clip=rect).replace("\x00", "").replace("\r", "").replace("\n", "")
        missing = [s for s in c["require"] if s.replace("\x00", "").replace("\r", "").replace("\n", "") not in clip_text]
        if missing:
            crop_failures.append(f"{c['key']}: missing anchors {missing}")

    tex = open(TEX, encoding="utf-8").read()
    calls = re.findall(r"\\cropimg(?:\[[^\]]*\])?\{([^}]+)\}", tex)
    unique_keys = {c["key"] for c in crops_cfg["crops"]}

    r4_render = os.path.join(ROOT, "round-04", "render")
    r4_pages = sorted(f for f in os.listdir(r4_render) if re.fullmatch(r"page-\d+\.png", f)) \
        if os.path.isdir(r4_render) else []
    r4_contacts = sorted(f for f in os.listdir(r4_render) if f.startswith("contact-")) \
        if os.path.isdir(r4_render) else []

    renders = sorted(f for f in os.listdir(RENDER) if re.fullmatch(r"page-\d+\.png", f))
    render_entries = []
    for f in renders:
        p = os.path.join(RENDER, f)
        render_entries.append({"file": f, "bytes": os.path.getsize(p), "sha256": sha256(p)})
    render_agg = hashlib.sha256(
        "".join(f"{e['file']}:{e['sha256']}\n" for e in render_entries).encode("utf-8")
    ).hexdigest()

    log = open(LOG, encoding="utf-8", errors="replace").read()
    out_line = next((ln.strip() for ln in log.splitlines() if ln.startswith("Output written")), "")

    # hashes of the two declared sources plus the round-04 TeX
    src = {}
    for label, path, declared in (
        ("old_handout", sel["old_handout"]["path"], sel["old_handout"]["sha256"]),
        ("new_handout", sel["handout"]["path"], sel["handout"]["sha256"]),
    ):
        sdoc = fitz.open(path)
        src[label] = {
            "path": rel(path),
            "sha256": sha256(path),
            "declared_sha256": declared,
            "match": sha256(path).lower() == declared.lower(),
            "bytes": os.path.getsize(path),
            "pages": sdoc.page_count,
            "declared_pages": sel["old_handout"]["pages"] if label == "old_handout" else sel["handout"]["pages"],
            "creation_date": sdoc.metadata.get("creationDate"),
            "producer": sdoc.metadata.get("producer"),
        }
    src["new_handout_tex"] = {
        "path": rel(sel["handout"]["tex"]),
        "sha256": sha256(sel["handout"]["tex"]),
        "bytes": os.path.getsize(sel["handout"]["tex"]),
    }

    def total_from(logfile):
        p = os.path.join(HERE, logfile)
        if not os.path.isfile(p):
            return None
        m = re.search(r"TOTAL: (\d+) passed, (\d+) failed", open(p, encoding="utf-8", errors="replace").read())
        return {"passed": int(m.group(1)), "failed": int(m.group(2))} if m else None

    facts = {
        "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "scope": "read-only verification of frozen comparison deliverable; no rebuild, no recompile",
        "authoritative_selection": {
            "path": rel(SEL),
            "sha256": sha256(SEL),
            "selected_at_utc": sel.get("selected_at_utc"),
            "status": sel.get("status"),
            "delivery_ready": sel.get("delivery_ready"),
        },
        "comparison_pdf": {
            "path": rel(PDF),
            "bytes": os.path.getsize(PDF),
            "sha256": sha256(PDF),
            "pages": doc.page_count,
            "a4_all_pages": a4_ok,
            "creation_date": doc.metadata.get("creationDate"),
            "producer": doc.metadata.get("producer"),
            "creator": doc.metadata.get("creator"),
        },
        "comparison_tex": {"path": rel(TEX), "bytes": os.path.getsize(TEX), "sha256": sha256(TEX)},
        "crops_json": {"path": rel(CROPS), "bytes": os.path.getsize(CROPS), "sha256": sha256(CROPS),
                       "count": len(crops_cfg["crops"])},
        "text_layer": {
            "total_chars": text_chars,
            "pages_with_text": sum(1 for p in pages if p),
            "running_header_all_pages": header_ok,
            "page_number_footer_all_pages": footer_ok,
        },
        "images": {
            "substantial_placements": placements,
            "cropimg_calls_in_tex": len(calls),
            "unique_crop_keys": len(unique_keys),
            "reused_keys": sorted({k for k in calls if calls.count(k) > 1}),
        },
        "crop_anchor_recheck": {
            "source": "current frozen source PDFs vs crops.json",
            "checked": len(crops_cfg["crops"]),
            "all_ok": not crop_failures,
            "failures": crop_failures,
        },
        "crop_render_report": {
            "path": rel(RCROPS),
            "dpi": rc.get("dpi"),
            "count": rc.get("count"),
            "failures": rc.get("failures"),
            "anchors_all_ok": all(c["anchors_ok"] for c in rc["crops"]),
            "png_total_bytes": sum(c["png_bytes"] for c in rc["crops"]),
            "png_sha256_mismatch": fig_hash_mismatch,
        },
        "round04_renders": {
            "dir": rel(r4_render),
            "page_png_count": len(r4_pages),
            "contact_sheet_count": len(r4_contacts),
            "note": "generated at round-04 close (05:56 UTC); not regenerated in this verification round",
        },
        "renders": {
            "dir": rel(RENDER),
            "count": len(render_entries),
            "dpi": 150,
            "aggregate_sha256": render_agg,
            "files": render_entries,
        },
        "compile_log": {
            "path": rel(LOG),
            "bytes": os.path.getsize(LOG),
            "sha256": sha256(LOG),
            "output_written_line": out_line,
            "overfull": "Overfull \\hbox" in log or "Overfull \\vbox" in log,
            "missing_character": "Missing character" in log,
            "latex_error": "LaTeX Error" in log,
            "undefined_control_or_reference": "Undefined control sequence" in log
            or "undefined references" in log.lower(),
            "underfull_hbox_count": log.count("Underfull \\hbox"),
        },
        "checks": {
            "check_compare": total_from("check_compare.log"),
            "verify_old_new_math": total_from("verify_old_new_math.log"),
            "render_pages": "rendered %d pages at 150 dpi" % len(render_entries)
            if os.path.isfile(os.path.join(HERE, "render_pages.log")) else None,
        },
        "sources": src,
    }

    out = os.path.join(HERE, "facts.json")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(facts, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(json.dumps({k: facts[k] for k in
                      ("generated_at_utc", "comparison_pdf", "text_layer", "images",
                       "crop_anchor_recheck", "crop_render_report", "round04_renders",
                       "checks", "sources")},
                     ensure_ascii=False, indent=2))
    print("\nwrote", rel(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
