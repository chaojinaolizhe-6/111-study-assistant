import sqlite3
p2 = r"D:\aaa_D_usual\DSH\社交信息整理助手\data\live\wechat-cache\session__session.db"
con = sqlite3.connect("file:%s?mode=ro" % p2, uri=True)
cur = con.cursor()
cur.execute("PRAGMA table_info(SessionTable)")
print([c[1] for c in cur.fetchall()])
rows = cur.execute("select * from SessionTable").fetchall()
print("count", len(rows))
for r in rows[:5]:
    print(r)
