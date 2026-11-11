import sys, numpy as np
from PIL import Image
src = sys.argv[1]
for p in range(20, 39):
    f = f"{src}/page-{p:03d}.png"
    im = np.array(Image.open(f).convert("L"))
    h, w = im.shape
    dark = im < 200
    cols = np.where(dark.any(axis=0))[0]
    rows = np.where(dark.any(axis=1))[0]
    # text block ink extent
    print(f"p{p}: ink x[{cols.min()},{cols.max()}] y[{rows.min()},{rows.max()}] size {w}x{h}")
    # row occupancy to find big blank bands (inside 70..1210)
    occ = dark[70:1210].sum(axis=1)
    blank = occ == 0
    # find runs of blank rows longer than 25 px
    runs = []
    s=None
    for i,b in enumerate(blank):
        if b and s is None: s=i
        if (not b) and s is not None:
            if i-s >= 25: runs.append((s+70, i-1+70, i-s))
            s=None
    if s is not None and len(blank)-s>=25: runs.append((s+70, len(blank)-1+70, len(blank)-s))
    if runs: print("   blank bands:", runs)
