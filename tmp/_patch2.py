import io, sys
CB = r"_scratch\check-ru-20261023\content_body.py"
BD = r"_scratch\check-ru-20261023\build_deck.py"
cb = io.open(CB, encoding="utf-8").read()
bd = io.open(BD, encoding="utf-8").read()
pairs_cb = [
 ("'2. 下列词中，非重音的 о 读 [а] 的是哪两个？① вода́ ② до́м ③ она́ ④ сто́л'",
  "'2. 下列词中，非重音的 о 读 [а] 的是哪两个？① вода́ ② дом ③ она́ ④ стол'"),
]
pairs_bd = [
 ("rowh=0.205, fs=10.5,", "rowh=0.185, fs=10.2,"),
]
fails = []
for text, pairs in ((cb, pairs_cb), (bd, pairs_bd)):
    for old, new in pairs:
        if text.count(old) != 1: fails.append((text.count(old), old[:40]))
if fails:
    print("FAILED", fails); sys.exit(1)
for old, new in pairs_cb: cb = cb.replace(old, new)
for old, new in pairs_bd: bd = bd.replace(old, new)
io.open(CB, "w", encoding="utf-8", newline="\n").write(cb)
io.open(BD, "w", encoding="utf-8", newline="\n").write(bd)
print("patched round 2")
