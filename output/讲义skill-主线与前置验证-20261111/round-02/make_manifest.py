#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create delivery-manifest.json with SHA256 for the round-02 delivery."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROUND = Path(__file__).resolve().parent
MANIFEST = ROUND / "delivery-manifest.json"

FILES = [
    "round-02/sample.tex",
    "round-02/sample.pdf",
    "round-02/preparation.json",
    "round-02/comparison.json",
    "round-02/verification.txt",
    "round-02/issue-response.json",
    "round-02/build.ps1",
    "round-02/verify_sample.py",
    "round-02/check_layout.py",
    "round-02/render_pages.py",
    "round-02/make_manifest.py",
    "round-02/build-pass1.log",
    "round-02/build-pass2.log",
    "round-02/sample.log",
    "round-02/check-handout.txt",
    "round-02/layout-report.txt",
    "round-02/layout-run.txt",
    "round-02/render-run.txt",
    "round-02/verify-math.txt",
    "round-02/page-text.txt",
    "inputs/baseline-handout.pdf",
    "inputs/baseline-handout.tex",
    "inputs/TM2026-Topic8-P1.pdf",
    "inputs/RIT-Whelan-notes10-tensor.pdf",
    "learner-background.json",
    "learner-background-confirmed.json",
    ".dsh/skills/lecture-deepdive/assets/theme-violet.tex",
]
FILES += [f"round-02/render/page-{i:02d}.png" for i in range(1, 19)]

EXTERNAL_INPUTS = [
    {
        "path": "D:\\aaa_D_usual\\CODEX\\AI-SKILL\\reviews\\lecture-mainline-20261111\\revision-index-r2.json",
        "role": "active finding list and acceptance targets",
    },
    {
        "path": "D:\\aaa_D_usual\\CODEX\\AI-SKILL\\reviews\\lecture-mainline-20261111\\reading-review-r1-final.json",
        "role": "reader-path evidence for the r2 revision",
    },
    {
        "path": "D:\\aaa_D_usual\\CODEX\\AI-SKILL\\reviews\\lecture-mainline-20261111\\math-review-r1-final.json",
        "role": "mathematical findings for the r2 revision",
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
        "round": "round-02",
        "round_kind": "DSH revision after external review; round-01 is the independent first draft",
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
            "path": "round-01/",
            "role": "read-only independent first draft; not part of this delivery",
        },
        "notes": [
            "Hashes the final PDF/TeX, preparation/comparison/verification/issue-response, the reproducible scripts, logs, all 18 rendered pages, page-text check dump, and the frozen inputs.",
            "delivery-manifest.json itself is not self-hashed; it is generated after the final build and after verification.txt is written.",
            "The final PDF was built after the last TeX edit; no TeX edit was made after that build.",
            "round-01 is preserved read-only and is not overwritten by this manifest.",
            "No learner trial was performed; the manifest does not claim learner understanding.",
        ],
        "files": entries,
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {MANIFEST.name}: {len(entries)} files, {manifest['total_bytes']} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
