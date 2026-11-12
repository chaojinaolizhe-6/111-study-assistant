import io, re
txt = io.open("tmp/ru_deck_text.txt", encoding="utf-8").read()
parts = re.split(r"(?m)^===== SLIDE (\d+) \(\d+ chars\) =====$", txt)
# parts[0] header, then pairs
blocks = []
for i in range(1, len(parts), 2):
    blocks.append((int(parts[i]), parts[i+1]))
print("parsed slides:", len(blocks))
groups = [blocks[0:16], blocks[16:32], blocks[32:48]]
for gi, g in enumerate(groups, 1):
    body = "\n".join(f"===== SLIDE {n} ====={t}" for n, t in g)
    io.open(f"tmp/ru_batch{gi}.txt", "w", encoding="utf-8").write(body)
    print(f"batch{gi}: slides {g[0][0]}-{g[-1][0]}, chars {len(body)}")
