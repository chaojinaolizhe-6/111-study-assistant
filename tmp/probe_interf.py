import fitz, re, sys
path = r"subjects\02-光学\课件\第五章 光的干涉.pdf"
doc = fitz.open(path)
print("pages:", doc.page_count)
for i, page in enumerate(doc, start=1):
    text = page.get_text("text")
    print(f"--- p{i} len={len(text)} ---")
    first = " / ".join([l.strip() for l in text.splitlines() if l.strip()][:3])
    print(first[:160])
