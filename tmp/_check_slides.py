import io, sys
from pptx import Presentation
p = Presentation(r"subjects\07-俄语\讲义\俄语-УРОК1-8-总复习课件-20261023.pptx")
out = []
for idx in (15, 26):
    s = p.slides[idx-1]
    out.append(f"##### SLIDE {idx}")
    for sh in s.shapes:
        if sh.has_text_frame:
            for para in sh.text_frame.paragraphs:
                t = "".join(r.text for r in para.runs)
                if t.strip(): out.append("  P: " + t)
        if sh.has_table:
            for r in sh.table.rows:
                out.append("  T: " + " / ".join(c.text for c in r.cells))
io.open(r"tmp\check_slides.txt","w",encoding="utf-8").write("\n".join(out))
print("ok", len(out))
