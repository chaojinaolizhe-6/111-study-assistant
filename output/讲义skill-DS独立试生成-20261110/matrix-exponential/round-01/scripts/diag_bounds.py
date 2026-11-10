import fitz, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
doc=fitz.open(r"matrix-exponential/round-01/handout.pdf")
full="\n".join(p.get_text() for p in doc)
import re
for m in re.finditer(r"课件例题[^\n]{0,40}", full):
    print(repr(m.group(0)))
print("--- offending spans ---")
for pno in (21,22,23,24,25,26):
    p=doc[pno-1]
    for block in p.get_text("dict")["blocks"]:
        if block.get("type")!=0: continue
        for line in block["lines"]:
            for s in line["spans"]:
                x0,y0,x1,y1=s["bbox"]
                if s["text"].strip() and (x1>538.6 or y1>790 or x0<56.7-2):
                    print(f"p{pno} x=[{x0:.1f},{x1:.1f}] y=[{y0:.1f},{y1:.1f}] {s['text']!r}")
