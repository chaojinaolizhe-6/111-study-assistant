import sys
from pptx import Presentation
p = Presentation(sys.argv[1])
print("slides:", len(p.slides))
print("slide size:", p.slide_width, p.slide_height)
for i, s in enumerate(p.slides, 1):
    texts = []
    for sh in s.shapes:
        if sh.has_text_frame:
            t = sh.text_frame.text.strip()
            if t: texts.append(t.replace("\n", " | "))
        if sh.has_table:
            for r in sh.table.rows:
                texts.append(" / ".join(c.text.strip() for c in r.cells))
    joined = " || ".join(texts)
    print(f"--- p{i} ({len(joined)} chars) --- {joined[:300]}")
