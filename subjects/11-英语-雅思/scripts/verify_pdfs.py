"""校验 资料/ 下所有 PDF 的文字层可读性与完整性。"""
from __future__ import annotations

import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[3]
MAT = ROOT / "subjects" / "11-英语-雅思" / "资料"


def main() -> int:
    bad: list[Path] = []
    total = 0
    for p in sorted(MAT.rglob("*.pdf")):
        total += 1
        try:
            with fitz.open(p) as doc:
                pages = doc.page_count
                chars = sum(len(pg.get_text()) for pg in doc)
        except Exception as e:  # noqa: BLE001
            print(f"BROKEN {p.name[:66]:66s} {type(e).__name__}: {str(e)[:50]}")
            bad.append(p)
            continue
        flag = "OK " if chars > 200 else "EMPTY"
        if chars <= 200:
            bad.append(p)
        print(f"{flag} {chars:>7,}c {pages:>3}p  {p.name[:64]}")
    print(f"\n共 {total} 个 PDF；异常 {len(bad)} 个")
    for p in bad:
        print("   异常:", p.relative_to(MAT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
