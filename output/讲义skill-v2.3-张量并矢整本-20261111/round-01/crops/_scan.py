import sys, numpy as np
from PIL import Image
src = sys.argv[1]
im = np.array(Image.open(f"{src}/page-034.png").convert("L"))
sub = im[1170:1215, 290:440]
dark = sub < 128
for r in range(sub.shape[0]):
    row = dark[r]
    runs=[]; s=None
    for c in range(len(row)):
        if row[c] and s is None: s=c
        if (not row[c]) and s is not None: runs.append((s+290, c-1+290)); s=None
    if s is not None: runs.append((s+290, len(row)-1+290))
    if runs: print(1170+r, runs)
