import fitz, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
doc=fitz.open(r"matrix-exponential/round-01/handout.pdf")
p=doc[8]
for block in p.get_text("dict")["blocks"]:
    if block.get("type")!=0: continue
    for line in block["lines"]:
        for s in line["spans"]:
            if s["text"].strip() and "3.1" in s["text"]:
                print(s["bbox"], repr(s["text"]))
