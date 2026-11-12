import sys, io
from pptx import Presentation
p = Presentation(sys.argv[1])
out = []
out.append(f"slides: {len(p.slides)}")
total = 0
for i, s in enumerate(p.slides, 1):
    texts = []
    for sh in s.shapes:
        if sh.has_text_frame:
            t = sh.text_frame.text.strip()
            if t: texts.append(t)
        if sh.has_table:
            for r in sh.table.rows:
                texts.append(" / ".join(c.text.strip() for c in r.cells))
    joined = "\n".join(texts)
    total += len(joined)
    out.append(f"\n===== SLIDE {i} ({len(joined)} chars) =====\n{joined}")
out.append(f"\n\nTOTAL CHARS: {total}")
io.open(sys.argv[2], "w", encoding="utf-8").write("\n".join(out))
print("written", total)
