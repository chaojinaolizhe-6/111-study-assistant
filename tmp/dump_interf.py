import fitz, json
path = r"subjects\02-光学\课件\第五章 光的干涉.pdf"
doc = fitz.open(path)
out = []
for i, page in enumerate(doc, start=1):
    text = page.get_text("text").strip()
    out.append({"page": i, "len": len(text), "text": text})
with open("tmp/interf_text.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("ok", sum(1 for o in out if o["len"] > 0), "pages with text")
