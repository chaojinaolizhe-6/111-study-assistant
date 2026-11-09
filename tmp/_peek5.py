import zstandard, io, json, glob, os
base = r"C:\Users\M\AppData\Roaming\dsh-desktop\harness\sessions\--D-aaa_D_usual-DSH-111~5B66~4E60~52A9~624B--"
for d in sorted(glob.glob(base + r"\session-*"), key=os.path.getmtime, reverse=True)[:4]:
    log = os.path.join(d, "session.v4.jsonl.zstd")
    if not os.path.exists(log): continue
    raw = open(log,'rb').read()
    data = zstandard.ZstdDecompressor().stream_reader(io.BytesIO(raw), read_across_frames=True).read()
    rows = [json.loads(l) for l in data.decode('utf-8').splitlines() if l.strip()]
    print("=====", os.path.basename(d), "records", len(rows))
    for r in rows:
        if r.get("type") == "agent/inbox/spliced":
            for ins in r.get("data",{}).get("inserted",[]):
                if ins.get("role") == "user":
                    types = [p.get("type") for p in ins.get("content",[])]
                    txt = " ".join(p.get("text","") for p in ins.get("content",[]) if p.get("type")=="text")[:80]
                    print("  USER", r.get("time"), types, txt)
