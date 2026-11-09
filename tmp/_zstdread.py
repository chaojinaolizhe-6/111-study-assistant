import zstandard, io, sys, os
log = r"C:\Users\M\AppData\Roaming\dsh-desktop\harness\sessions\--D-aaa_D_usual-DSH-111~5B66~4E60~52A9~624B--\session-606c1bd0-fa8d-4383-897e-78a4ef743707\session.v4.jsonl.zstd"
raw = open(log,'rb').read()
d = zstandard.ZstdDecompressor().stream_reader(io.BytesIO(raw), read_across_frames=True).read()
out = r"D:\aaa_D_usual\DSH\111学习助手\tmp\_sess_606c.jsonl"
open(out,'wb').write(d)
print('bytes', len(d))
