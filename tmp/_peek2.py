import zstandard, io, json
log = r"C:\Users\M\AppData\Roaming\dsh-desktop\harness\sessions\--D-aaa_D_usual-DSH-111~5B66~4E60~52A9~624B--\session-5debe72b-fa5e-435a-957e-835362236b5a\session.v4.jsonl.zstd"
raw = open(log,'rb').read()
d = zstandard.ZstdDecompressor().stream_reader(io.BytesIO(raw), read_across_frames=True).read()
rows = [json.loads(l) for l in d.decode('utf-8').splitlines() if l.strip()]
print("records", len(rows))
for r in rows:
    if r.get("type") in ("agent/inbox/spliced",):
        for ins in r.get("data",{}).get("inserted",[]):
            if ins.get("role")=="user":
                parts = ins.get("content",[])
                desc=[]
                for p in parts:
                    t=p.get("type")
                    if t=="text": desc.append(("text", p.get("text","")[:120]))
                    else: desc.append((t, json.dumps(p, ensure_ascii=False)[:300]))
                print("USER MSG:", desc)
open(r"D:\aaa_D_usual\DSH\111学习助手\tmp\_sess_5deb.jsonl","wb").write(d)
