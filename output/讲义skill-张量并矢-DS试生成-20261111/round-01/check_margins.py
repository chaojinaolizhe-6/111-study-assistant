from PIL import Image
from pathlib import Path
bad = 0
for p in sorted(Path('render').glob('page-*.png')):
    im = Image.open(p).convert('L')
    w, h = im.size
    px = im.load()
    xs = []; ys = []
    for y in range(h):
        row = [x for x in range(w) if px[x, y] < 245]
        if row:
            xs.append(row[0]); xs.append(row[-1]); ys.append(y)
    if not xs:
        print(p.name, 'blank'); continue
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    margins = (minx, w - 1 - maxx, miny, h - 1 - maxy)
    if min(margins) < 35:
        bad += 1
        print(f'{p.name}: size={w}x{h} bbox=({minx},{miny})-({maxx},{maxy}) margins={margins}')
print('pages flagged:', bad)
