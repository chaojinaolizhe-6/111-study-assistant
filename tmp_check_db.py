import sqlite3

p = r"D:\aaa_D_usual\DSH\社交信息整理助手\data\openclaw\state\openclaw.sqlite"
con = sqlite3.connect("file:" + p + "?mode=ro", uri=True)
cur = con.cursor()
tabs = [r[0] for r in cur.execute("select name from sqlite_master where type='table'")]
print("tables:", tabs)
for t in tabs:
    low = t.lower()
    if any(k in low for k in ("msg", "message", "outbox", "job", "deliver")):
        try:
            n = cur.execute("select count(*) from " + t).fetchone()[0]
            cols = [c[1] for c in cur.execute("pragma table_info(" + t + ")")]
            print("\n", t, "rows=", n)
            print("  cols:", cols)
            rows = cur.execute("select * from " + t + " order by rowid desc limit 3").fetchall()
            for r in rows:
                print("   ", str(r)[:300])
        except Exception as e:
            print(t, "err", e)
