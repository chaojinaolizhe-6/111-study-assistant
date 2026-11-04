import sqlite3, io
p = r"D:\aaa_D_usual\DSH\社交信息整理助手\data\live\wechat-cache\message__message_1.db"
con = sqlite3.connect("file:%s?mode=ro" % p, uri=True)
con.text_factory = bytes
cur = con.cursor()
t = "Msg_250ea1e712b1441663fd47be6fc3c833"
cols = [c[1] for c in cur.execute("PRAGMA table_info(%s)" % t)]
out = io.StringIO()
print(cols, file=out)
