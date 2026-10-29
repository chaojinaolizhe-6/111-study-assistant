import fitz, glob, os
for p in sorted(glob.glob(r'subjects\02-光学\课件\*.pdf')):
    d = fitz.open(p)
    n = len(d)
    chars = sum(len(d[i].get_text()) for i in range(n))
    imgs = sum(len(d[i].get_images(full=True)) for i in range(n))
    print(f'{os.path.basename(p)}\tpages={n}\tchars={chars}\timgs={imgs}')
    d.close()
