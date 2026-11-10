import fitz, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
doc=fitz.open(r"matrix-exponential/round-01/handout.pdf")
for i,p in enumerate(doc):
    lines=[l.strip() for l in p.get_text().splitlines() if l.strip()]
    print(f"p{i+1}: ... " + " | ".join(lines[-6:-1])[:220])
