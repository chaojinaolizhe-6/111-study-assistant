import fitz, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
doc=fitz.open(r"matrix-exponential/round-01/handout.pdf")
for p in range(18,26):
    print(f"\n========== PAGE {p+1} ==========")
    print(doc[p].get_text())
