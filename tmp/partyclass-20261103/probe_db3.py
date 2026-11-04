import sqlite3, io
base = r"D:\aaa_D_usual\DSH\社交信息整理助手\data\live\wechat-cache"
out = io.StringIO()
def P(*a): print(*a, file=out)

con = sqlite3.connect("file:%s\\session__session.db?mode=ro" % base, uri=True)
cur = con.cursor()
sessions = cur.execute("select username, summary, last_timestamp, sort_timestamp from SessionTable").fetchall()
P("sessions:", len(sessions))
ccon = sqlite3.connect("file:%s\\contact__contact.db?mode=ro" % base, uri=True)
ccur = ccon.cursor()
P("tables:", [r[0] for r in ccur.execute("select name from sqlite_master where type='table'")])
for t in ("Name2Id","contact","stranger","group_member"):
    try:
        P(t, [c[1] for c in ccur.execute("PRAGMA table_info(%s)" % t)])
    except Exception as e:
        P(t, "ERR", e)
open(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\schema.txt","w",encoding="utf-8").write(out.getvalue())
print("done")
