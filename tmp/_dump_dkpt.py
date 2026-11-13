import io
from pptx import Presentation
from pptx.util import Emu
p = Presentation(r"大创\MPS-LD马赫探针开题答辩_六页研究正文.pptx")
out = []
for i, s in enumerate(p.slides, 1):
    out.append(f"\n########## SLIDE {i} ##########")
    shapes = sorted(s.shapes, key=lambda sh: (round(Emu(sh.top or 0).inches,1), round(Emu(sh.left or 0).inches,1)))
    for sh in shapes:
        if sh.has_text_frame:
            t = "\n".join(par.text for par in sh.text_frame.paragraphs if par.text.strip())
            if t.strip():
                out.append(f"[{sh.name}]\n{t}")
        if sh.has_table:
            out.append(f"[TABLE {sh.name}]")
            for r in sh.table.rows:
                out.append("  | " + " | ".join(c.text.replace("\n"," ") for c in r.cells))
    if s.has_notes_slide:
        nt = s.notes_slide.notes_text_frame.text.strip()
        if nt:
            out.append(f"[NOTES]\n{nt}")
io.open(r"tmp\dkpt_text.txt","w",encoding="utf-8").write("\n".join(out))
print("chars", sum(len(x) for x in out))
