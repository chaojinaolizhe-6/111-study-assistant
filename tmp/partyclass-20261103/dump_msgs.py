import sqlite3, io
p = r"D:\aaa_D_usual\DSH\社交信息整理助手\data\live\wechat-cache\message__message_1.db"
out = r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\msgs_dangke.txt"
con = sqlite3.connect("file:%s?mode=ro" % p, uri=True)
con.text_factory = bytes
cur = con.cursor()
t = "Msg_250ea1e712b1441663fd47be6fc3c833"
cols = [c[1].decode() if isinstance(c[1], bytes) else c[1] for c in cur.execute("PRAGMA table_info(%s)" % t)]
buf = io.StringIO()
print("COLS:", cols, file=buf)
idx = {c: i for i, c in enumerate(cols)}
rows = cur.execute("select * from %s order by sort_seq" % t).fetchall()
print("rows", len(rows), file=buf)
def conv(v):
    if isinstance(v, bytes):
        try: return v.decode('utf-8')
        except UnicodeDecodeError: return repr(v[:60])
    return v
for r in rows:
    d = {c: conv(r[i]) for c, i in idx.items() if c in ('local_id','server_id','local_type','create_time','sort_seq','real_sender_id','message_content','packed_info_data','source')}
    print(d, file=buf)
open(out, "w", encoding="utf-8").write(buf.getvalue())
print("ok")
