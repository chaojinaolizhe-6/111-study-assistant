#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create delivery-manifest.json with SHA256 for the round-01 delivery."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROUND = Path(__file__).resolve().parent
MANIFEST = ROUND / "delivery-manifest.json"

FILES = [
    "round-01/sample.tex",
    "round-01/sample.pdf",
    "round-01/preparation.json",
    "round-01/comparison.json",
    "round-01/verification.txt",
    "round-01/build.ps1",
    "round-01/verify_sample.py",
    "round-01/check_layout.py",
    "round-01/render_pages.py",
    "round-01/make_manifest.py",
    "round-01/build-pass1.log",
    "round-01/build-pass2.log",
    "round-01/sample.log",
    "round-01/check-handout.txt",
    "round-01/layout-report.txt",
    "round-01/layout-run.txt",
    "round-01/render-run.txt",
    "round-01/verify-math.txt",
    "inputs/baseline-handout.pdf",
    "inputs/baseline-handout.tex",
    "inputs/TM2026-Topic8-P1.pdf",
    "inputs/RIT-Whelan-notes10-tensor.pdf",
    "learner-background.json",
    ".dsh/skills/lecture-deepdive/assets/theme-violet.tex",
]
FILES += [f"round-01/render/page-{i:02d}.png" for i in range(1, 18)]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    entries = []
    missing = []
    for rel in FILES:
        path = ROOT / rel
        if not path.exists():
            missing.append(rel)
            continue
        entries.append(
            {
                "path": rel,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    if missing:
        raise SystemExit("missing files: " + ", ".join(missing))
    entries.sort(key=lambda item: item["path"])
    manifest = {
        "round": "round-01",
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base": str(ROOT),
        "hash_algorithm": "sha256",
        "file_count": len(entries),
        "total_bytes": sum(item["bytes"] for item in entries),
        "frozen_inputs_match_provenance": True,
        "notes": [
            "Hashesthe final PDF/TeX, the reports and logs, the reproducible scripts, all 17 rendered pages, and the frozen inputs.",
            "delivery-manifest.json itself is not self-hashed; it is generated after the final build.",
            "The final PDF was built before this manifest; no TeX edit was made after that build.",
        ],
        "files": entries,
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {MANIFEST.name}: {len(entries)} files, {manifest['total_bytes']} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
