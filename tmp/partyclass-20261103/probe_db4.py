import sqlite3, io
base = r"D:\aaa_D_usual\DSH\社交信息整理助手\data\live\wechat-cache"
out = io.StringIO()
def P(*a): print(*a, file=out)
ccon = sqlite3.connect("file:%s\\contact__contact.db?mode=ro" % base, uri=True)
c = ccon.cursor()
rows = c.execute("select username, nick_name, remark from contact").fetchall()
P("contacts:", len(rows))
for u,n,r in rows:
    name = r or n or ""
    if "党课" in name or "党" in name or "积极" in name:
        P(repr(u), "|", repr(n), "|", repr(r))
open(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\contacts_party.txt","w",encoding="utf-8").write(out.getvalue())
print("done")
