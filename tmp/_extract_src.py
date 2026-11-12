import io, os, re, fitz
src = r"subjects\07-俄语\课件"
out = r"tmp\src"
os.makedirs(out, exist_ok=True)
rows = []
for name in sorted(os.listdir(src)):
    if not name.lower().endswith(".pdf"): continue
    doc = fitz.open(os.path.join(src, name))
    parts = []
    chars = []
    for i, page in enumerate(doc, 1):
        t = page.get_text("text").strip()
        chars.append(len(t))
        parts.append(f"\n===== PDFPAGE {i} ({len(t)} chars) =====\n{t}")
    stem = re.sub(r"[^\w\-]+", "_", os.path.splitext(name)[0])[:60]
    path = os.path.join(out, stem + ".txt")
    io.open(path, "w", encoding="utf-8").write("".join(parts))
    rows.append((name, len(doc), sum(chars), min(chars) if chars else 0, path))
for n, pages, total, mn, path in rows:
    print(f"{pages:3d} pages  {total:6d} chars  minpage={mn:4d}  {n}  -> {path}")
