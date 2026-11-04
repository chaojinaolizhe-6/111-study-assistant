import sqlite3, io, os, re, datetime
p = r"D:\aaa_D_usual\DSH\社交信息整理助手\data\live\wechat-cache\message__message_1.db"
jpgdir = r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\jpg"
out = r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\image_order.txt"
con = sqlite3.connect("file:%s?mode=ro" % p, uri=True)
con.text_factory = bytes
cur = con.cursor()
t = "Msg_250ea1e712b1441663fd47be6fc3c833"
rows = cur.execute("select local_id, local_type, create_time, message_content, packed_info_data from %s order by sort_seq" % t).fetchall()
have = {}
for f in os.listdir(jpgdir):
    if f.endswith(".jpg"):
        have[f.split("_")[1][:8]] = f
buf = io.StringIO()
n = 0
for lid, ltyp, ctime, content, packed in rows:
    if ltyp != 3:
        continue
    n += 1
    txt = packed.decode("latin-1") if isinstance(packed, bytes) else str(packed)
    m = re.search(r"([0-9a-f]{32})", txt)
    md5 = m.group(1) if m else "?"
    dt = datetime.datetime.utcfromtimestamp(ctime) + datetime.timedelta(hours=8)
    print("%02d  %s  %s  %s" % (n, dt.strftime("%H:%M:%S"), md5[:8], have.get(md5[:8], "NO-JPG")), file=buf)
open(out, "w", encoding="utf-8").write(buf.getvalue())
print("ok")
