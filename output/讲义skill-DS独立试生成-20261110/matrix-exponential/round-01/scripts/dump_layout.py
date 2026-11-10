import fitz, pathlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
pdf = pathlib.Path(r"inputs/16_17_matrix_exponential.pdf")
doc = fitz.open(pdf)
for p in map(int, sys.argv[1:]):
    page = doc[p-1]
    print(f"\n===== page {p} =====")
    d = page.get_text("dict")
    for b in d["blocks"]:
        if b.get("type") != 0: continue
        for l in b["lines"]:
            spans = [s for s in l["spans"] if s["text"].strip()]
            if not spans: continue
            parts = []
            for s in spans:
                parts.append(f"[{s['bbox'][0]:.1f},{s['bbox'][1]:.1f},{s['size']:.1f}]{s['text']!r}")
            print("  " + " ".join(parts))
