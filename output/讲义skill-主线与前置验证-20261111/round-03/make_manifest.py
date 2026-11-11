#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create delivery-manifest.json with SHA256 for the round-03 delivery."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROUND = Path(__file__).resolve().parent
MANIFEST = ROUND / "delivery-manifest.json"

FILES = [
    "round-03/sample.tex",
    "round-03/sample.pdf",
    "round-03/preparation.json",
    "round-03/comparison.json",
    "round-03/verification.txt",
    "round-03/issue-response.json",
    "round-03/build.ps1",
    "round-03/verify_sample.py",
    "round-03/check_layout.py",
    "round-03/render_pages.py",
    "round-03/dump_page_text.py",
    "round-03/make_manifest.py",
    "round-03/build-pass1.log",
    "round-03/build-pass2.log",
    "round-03/sample.log",
    "round-03/check-handout.txt",
    "round-03/layout-report.txt",
    "round-03/layout-run.txt",
    "round-03/render-run.txt",
    "round-03/page-text-run.txt",
    "round-03/verify-math.txt",
    "round-03/page-text.txt",
    "inputs/baseline-handout.pdf",
    "inputs/baseline-handout.tex",
    "inputs/TM2026-Topic8-P1.pdf",
    "inputs/RIT-Whelan-notes10-tensor.pdf",
    "learner-background.json",
    "learner-background-confirmed.json",
    ".dsh/skills/lecture-deepdive/assets/theme-violet.tex",
]
FILES += [f"round-03/render/page-{i:02d}.png" for i in range(1, 20)]

EXTERNAL_INPUTS = [
    {
        "path": "D:\\aaa_D_usual\\CODEX\\AI-SKILL\\reviews\\lecture-mainline-20261111\\revision-index-r3.json",
        "role": "three remaining local findings and acceptance targets",
    },
    {
        "path": "D:\\aaa_D_usual\\CODEX\\AI-SKILL\\reviews\\lecture-mainline-20261111\\reading-review-r2-final.json",
        "role": "final r2 reader findings for MAIN-READ-R2-LOCAL-01 and MAIN-META-R2-01",
    },
    {
        "path": "D:\\aaa_D_usual\\CODEX\\AI-SKILL\\reviews\\lecture-mainline-20261111\\math-review-r2-final.json",
        "role": "final r2 mathematical finding for MAIN-MATH-03",
    },
]


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

    external_entries = []
    for item in EXTERNAL_INPUTS:
        path = Path(item["path"])
        if not path.exists():
            raise SystemExit("missing external input: " + item["path"])
        external_entries.append(
            {
                "path": item["path"],
                "role": item["role"],
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )

    manifest = {
        "round": "round-03",
        "round_kind": "DSH local revision after final-r2 review; round-02 is the prior revision, round-01 the independent first draft",
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base": str(ROOT),
        "hash_algorithm": "sha256",
        "file_count": len(entries),
        "total_bytes": sum(item["bytes"] for item in entries),
        "frozen_inputs_match_provenance": True,
        "learner_profile": {
            "path": "learner-background-confirmed.json",
            "sha256": sha256(ROOT / "learner-background-confirmed.json"),
            "received_after_round01_start": True,
            "boundary": "self-report, not independent performance test; round-01 began before the replies",
        },
        "external_inputs": external_entries,
        "previous_round": {
            "path": "round-02/",
            "role": "read-only prior revision; its final review still listed MAIN-MATH-03 active, and this delivery does not treat its self-assessment as review sign-off",
        },
        "notes": [
            "Hashes the final PDF/TeX, preparation/comparison/verification/issue-response, the reproducible scripts, logs, all 19 rendered pages, page-text dump, and the frozen inputs.",
            "delivery-manifest.json itself is not self-hashed; it is generated after the final build and after verification.txt is written.",
            "The final PDF was built after the last TeX edit; no TeX edit was made after that build.",
            "round-01 and round-02 are preserved read-only and are not overwritten by this manifest.",
            "No learner trial was performed; the manifest does not claim learner understanding.",
        ],
        "files": entries,
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {MANIFEST.name}: {len(entries)} files, {manifest['total_bytes']} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
