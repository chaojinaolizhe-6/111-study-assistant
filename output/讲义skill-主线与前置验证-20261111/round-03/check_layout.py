#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Coordinate-level page checks for round-01/sample.pdf.

This does not claim visual inspection.  It checks page size, text presence,
text-span bounds against the A4 page and the configured body margins, and
that the two figure pages contain vector drawings.  The rendered PNG files
are for an external reviewer with image support.
"""
from __future__ import annotations

import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent
PDF = ROOT / "sample.pdf"
REPORT = ROOT / "layout-report.txt"

# A4 geometry from theme-violet: left/right 2.0 cm, top 2.1 cm, bottom 2.3 cm.
CM = 72.0 / 2.54
LEFT = 2.0 * CM
RIGHT = 2.0 * CM
TOP = 2.1 * CM
BOTTOM = 2.3 * CM
TOL = 1.0
# xeCJK may let full-width punctuation hang a few points into the margin.
# Allow that typographic protrusion, but fail on substantive text outside.
PUNCT_TOL = 9.0


def main() -> int:
    if not PDF.exists():
        print(f"missing {PDF}", file=sys.stderr)
        return 1
    doc = fitz.open(PDF)
    lines: list[str] = []
    issues: list[str] = []
    lines.append(f"pdf: {PDF.name}")
    lines.append(f"pages: {doc.page_count}")
    lines.append(f"page size: {doc[0].rect.width:.2f} x {doc[0].rect.height:.2f} pt")
    lines.append(f"body margins: left/right {LEFT:.2f} pt, top {TOP:.2f} pt, bottom {BOTTOM:.2f} pt")
    lines.append("")

    all_min_x0 = 1e9
    all_max_x1 = -1e9
    all_min_y0 = 1e9
    all_max_y1 = -1e9

    for index, page in enumerate(doc, 1):
        w, h = page.rect.width, page.rect.height
        text = page.get_text("text")
        if len(text.strip()) < 100:
            issues.append(f"page {index}: almost no extracted text ({len(text.strip())} chars)")
        drawings = page.get_drawings()
        lines.append(f"page {index:02d}: chars={len(text.strip()):4d}, drawings={len(drawings):3d}")

        data = page.get_text("dict")
        body_spans = 0
        for block in data.get("blocks", []):
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    x0, y0, x1, y1 = span["bbox"]
                    if x0 < -TOL or y0 < -TOL or x1 > w + TOL or y1 > h + TOL:
                        issues.append(
                            f"page {index}: span outside page: "
                            f"({x0:.1f},{y0:.1f})-({x1:.1f},{y1:.1f}) {span.get('text','')[:30]!r}"
                        )
                    # Exclude running header/footer; check the body block.
                    if y0 > TOP + 12 and y1 < h - BOTTOM - 10:
                        body_spans += 1
                        all_min_x0 = min(all_min_x0, x0)
                        all_max_x1 = max(all_max_x1, x1)
                        all_min_y0 = min(all_min_y0, y0)
                        all_max_y1 = max(all_max_y1, y1)
                        if x0 < LEFT - PUNCT_TOL or x1 > w - RIGHT + PUNCT_TOL:
                            issues.append(
                                f"page {index}: body span outside horizontal margins "
                                f"(beyond {PUNCT_TOL:.1f} pt punctuation allowance): "
                                f"({x0:.1f},{y0:.1f})-({x1:.1f},{y1:.1f}) {span.get('text','')[:30]!r}"
                            )
        if body_spans == 0:
            issues.append(f"page {index}: no body spans detected")

    lines.append("")
    lines.append(
        "body-span envelope: "
        f"x0={all_min_x0:.2f}, x1={all_max_x1:.2f}, y0={all_min_y0:.2f}, y1={all_max_y1:.2f}"
    )
    lines.append(
        "horizontal protrusion: "
        f"left={max(0.0, LEFT - all_min_x0):.2f} pt, "
        f"right={max(0.0, all_max_x1 - (doc[0].rect.width - RIGHT)):.2f} pt "
        f"(CJK punctuation allowance {PUNCT_TOL:.1f} pt)"
    )
    figure_pages = []
    for page_no, page in enumerate(doc, 1):
        page_text = page.get_text("text")
        if "自绘" in page_text:
            figure_pages.append(page_no)
    for page_no in figure_pages:
        drawings = doc[page_no - 1].get_drawings()
        lines.append(f"figure page {page_no}: drawings={len(drawings)}")
        if len(drawings) < 5:
            issues.append(f"page {page_no}: expected the self-drawn figure, found {len(drawings)} drawings")
    if len(figure_pages) < 2:
        issues.append(f"expected both figure captions, found figure pages {figure_pages}")

    lines.append("")
    if issues:
        lines.append(f"ISSUES: {len(issues)}")
        lines.extend(f"- {item}" for item in issues)
    else:
        lines.append("ISSUES: none")
    lines.append("")
    lines.append(
        "NOTE: coordinate/bounds checks only.  This environment cannot read images; "
        "the rendered PNGs require external visual review."
    )
    report_text = "\n".join(lines) + "\n"
    REPORT.write_text(report_text, encoding="utf-8")
    print(report_text)
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
