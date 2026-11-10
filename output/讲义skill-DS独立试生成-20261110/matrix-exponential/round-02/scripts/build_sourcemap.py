#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""更新 round-02 的 source-map.json：哈希、页数、检查脚本与 R1/R3 备注。"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "source-map.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


data = json.loads(MAP.read_text(encoding="utf-8"))
pdf_path = ROOT / "handout.pdf"
tex_path = ROOT / "handout.tex"
pages = fitz.open(pdf_path).page_count

data["handout"].update({
    "tex": "matrix-exponential/round-02/handout.tex",
    "pdf": "matrix-exponential/round-02/handout.pdf",
    "pages": pages,
    "tex_sha256": sha256(tex_path),
    "pdf_sha256": sha256(pdf_path),
    "theme": "rule-versions/2.1.1/lecture-deepdive/assets/theme-violet.tex",
    "mode": "appendix (independent practice answers in Appendix A)",
})

data["revision"] = {
    "round": 2,
    "based_on": "matrix-exponential/round-01",
    "review_issue_list": "D:/aaa_D_usual/CODEX/AI-SKILL/reviews/DS-matrix-round01-20261110/review-final.md",
    "rule_version": "2.1.1",
    "issues_addressed": ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8"],
    "note": "R7/R8 are advisory; R6 was checked against the newly generated PDF pages, not the round-01 page numbers.",
}

# 覆盖说明中与本轮修订直接相关的条目，补充“已改为”说明（不改变页码落点）
for item in data["items"]:
    if item["id"] == "Repeated eigenvalues and derivative conditions":
        item["note"] = ("derivative conditions now derived from f-r = Δ_x q and the zero order of Δ_x; "
                        "Jordan-block proof distinguishes block size ℓ from algebraic multiplicity m")
    if item["id"] == "Theorem 3.3 (derivative equations)":
        item["note"] = ("full premise added: r is the unique Hermite interpolant of e^s on the spectrum; "
                        "the conclusion is not asserted for an arbitrary degree ≤ n−1 polynomial")
    if item["id"] == "Analytic functions of a matrix; interpolation":
        item["note"] = ("monic characteristic polynomial Δ(s)=det(sE−A) used for division; "
                        "scope of the analytic-function remainder relation stated (no unconditional power-series division)")

data["checks"] = {
    "math_script": "matrix-exponential/round-02/scripts/verify_matrix_exponential.py",
    "math_output": "matrix-exponential/round-02/scripts/verify_output.txt",
    "math_assertions": 102,
    "math_failures": 0,
    "compile": "two xelatex passes, -halt-on-error -interaction=nonstopmode",
    "compile_log": "matrix-exponential/round-02/handout.log",
    "check_handout": ("python -B rule-versions/2.1.1/lecture-deepdive/scripts/check_handout.py "
                      "matrix-exponential/round-02/handout.tex --mode appendix --log matrix-exponential/round-02/handout.log"),
    "check_handout_result": "0 errors, 0 warnings",
    "revision_script": "matrix-exponential/round-02/scripts/check_revision.py",
    "revision_output": "matrix-exponential/round-02/scripts/revision_output.txt",
    "revision_assertions": 37,
    "revision_failures": 0,
    "layout_script": "matrix-exponential/round-02/scripts/check_layout.py",
    "layout_output": "matrix-exponential/round-02/scripts/layout_output.txt",
    "layout_result": "passed (programmatic bounds/fonts/structure; no pixel-level visual review available)",
    "page_edge_script": "matrix-exponential/round-02/scripts/check_pages.py",
    "page_edge_result": "passed (no known bad page-start fragments; no orphan heading at page bottom)",
    "pixel_script": "matrix-exponential/round-02/scripts/render_and_check_pixels.py",
    "pixel_output": "matrix-exponential/round-02/scripts/pixel_output.txt",
    "pixel_result": "32 pages rendered at 150 dpi; no blank pages; no ink touching page edge; ink coverage 0.51%-5.62%",
    "render_dir": "matrix-exponential/round-02/renders (32 handout pages at 150 dpi)",
    "visual_review": "external visual acceptance pending; this model session cannot accept image input",
}

MAP.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"updated {MAP} (pages={pages}, tex={data['handout']['tex_sha256'][:12]}..., pdf={data['handout']['pdf_sha256'][:12]}...)")
