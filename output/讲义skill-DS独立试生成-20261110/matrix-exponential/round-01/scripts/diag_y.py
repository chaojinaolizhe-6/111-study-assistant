import fitz, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
doc=fitz.open(r"matrix-exponential/round-01/handout.pdf")
for pno in (2,3,4,9,10,11,12):
    p=doc[pno-1]
    print(f"\n=== p{pno} ===")
    for block in p.get_text("dict")["blocks"]:
        if block.get("type")!=0: continue
        for line in block["lines"]:
            for s in line["spans"]:
                x0,y0,x1,y1=s["bbox"]
                if s["text"].strip() and y1>780:
                    print(f"y=[{y0:.1f},{y1:.1f}] {s['text']!r}")
    lines=[l.strip() for l in p.get_text().splitlines() if l.strip()]
    print("LAST:", " | ".join(lines[-6:]))
