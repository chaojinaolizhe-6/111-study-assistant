import fitz, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
doc=fitz.open(r"matrix-exponential/round-01/handout.pdf")
print("pages:", doc.page_count)
for i,p in enumerate(doc):
    t=p.get_text().strip().splitlines()
    t=[x.strip() for x in t if x.strip()]
    if not t: print(f"\n--- p{i+1}: EMPTY"); continue
    print(f"\n--- p{i+1} ({len(p.get_text())} chars) first: {t[0][:70]!r}")
    print(f"    last: {t[-1][:70]!r}")
    for key in ("详解","附录","练习","矩 阵","定理","例题"):
        if any(key in x for x in t): print(f"    contains {key!r}")
