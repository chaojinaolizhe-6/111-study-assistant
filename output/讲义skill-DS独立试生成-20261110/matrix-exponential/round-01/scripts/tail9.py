import fitz, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
doc=fitz.open(r"matrix-exponential/round-01/handout.pdf")
p=doc[8]
rows=[]
for block in p.get_text("dict")["blocks"]:
    if block.get("type")!=0: continue
    for line in block["lines"]:
        for s in line["spans"]:
            if s["text"].strip():
                rows.append((s["bbox"][1], s["bbox"][3], s["text"]))
for y0,y1,t in sorted(rows)[-20:]:
    print(f"y0={y0:.1f} y1={y1:.1f} {t!r}")
