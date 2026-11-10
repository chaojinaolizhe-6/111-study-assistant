import fitz, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
doc=fitz.open(r"matrix-exponential/round-01/handout.pdf")
for p in [0,1,8,9,10,17]:
    lines=[l.strip() for l in doc[p].get_text().splitlines() if l.strip()]
    print(f"\np{p+1} FIRST: " + " | ".join(lines[2:7]))
    print(f"p{p+1} LAST : " + " | ".join(lines[-6:-1]))
