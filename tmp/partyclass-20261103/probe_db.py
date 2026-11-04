import sqlite3, os
p = r"D:\aaa_D_usual\DSH\社交信息整理助手\data\live\wechat-cache\message__message_1.db"
con = sqlite3.connect("file:%s?mode=ro" % p, uri=True)
cur = con.cursor()
print([r[0] for r in cur.execute("select name from sqlite_master where type='table'")])
print("---")
p2 = r"D:\aaa_D_usual\DSH\社交信息整理助手\data\live\wechat-cache\session__session.db"
con2 = sqlite3.connect("file:%s?mode=ro" % p2, uri=True)
cur2 = con2.cursor()
print([r[0] for r in cur2.execute("select name from sqlite_master where type='table'")])
