import fitz, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
doc=fitz.open(r"matrix-exponential/round-01/handout.pdf")
for pno in (8,9,10):
    lines=[l.strip() for l in doc[pno-1].get_text().splitlines() if l.strip()]
    print(f"\n=== p{pno} ===")
    print("FIRST:", " | ".join(lines[:6]))
    print("LAST :", " | ".join(lines[-9:]))
