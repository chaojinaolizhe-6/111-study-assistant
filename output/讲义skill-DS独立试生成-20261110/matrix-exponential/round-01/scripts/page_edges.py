import fitz, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
doc=fitz.open(r"matrix-exponential/round-01/handout.pdf")
for p in range(17,25):
    lines=[l.strip() for l in doc[p].get_text().splitlines() if l.strip()]
    print(f"\n===== p{p+1} ({len(lines)} lines) =====")
    print("FIRST:", " | ".join(lines[:8]))
    print("LAST :", " | ".join(lines[-8:]))
