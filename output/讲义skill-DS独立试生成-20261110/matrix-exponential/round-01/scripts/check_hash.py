import json, hashlib, pathlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
d=json.loads(pathlib.Path(r"matrix-exponential/round-01/source-map.json").read_text(encoding="utf-8"))
for key, path in (("tex_sha256", r"matrix-exponential/round-01/handout.tex"), ("pdf_sha256", r"matrix-exponential/round-01/handout.pdf")):
    h=hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
    print(key, repr(d["handout"][key]), repr(h), d["handout"][key]==h, len(d["handout"][key]), len(h))
