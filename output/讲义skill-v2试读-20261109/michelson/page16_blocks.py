import fitz
p=r'output/讲义skill-v2试读-20261109/michelson/michelson-excerpt-v2.pdf'
d=fitz.open(p)
pg=d[15]
for b in pg.get_text('blocks'):
    txt=b[4].strip().replace('\n',' | ')
    if txt:
        print('y0=%.1f y1=%.1f  %s'%(b[1],b[3],txt[:100]))
