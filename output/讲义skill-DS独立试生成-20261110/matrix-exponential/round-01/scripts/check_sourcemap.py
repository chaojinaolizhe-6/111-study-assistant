import json, hashlib, pathlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p=pathlib.Path(r"matrix-exponential/round-01/source-map.json")
d=json.loads(p.read_text(encoding="utf-8"))
pages=[c["page"] for c in d["coverage"]]
print("coverage entries:", len(pages), "unique:", len(set(pages)), "range ok:", sorted(pages)==list(range(1,45)))
print("items:", len(d["items"]), "errata:", len(d["errata"]), "notes:", len(d["notation_notes"]))
for key, path in (("tex_sha256", r"matrix-exponential/round-01/handout.tex"), ("pdf_sha256", r"matrix-exponential/round-01/handout.pdf")):
    h=hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
    print(key, "match:", h==d["handout"][key], h[:16])
print("handout pages:", d["handout"]["pages"])
