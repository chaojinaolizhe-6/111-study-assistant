import fitz
p=r'output/讲义skill-v2试读-20261109/michelson/michelson-excerpt-v2.pdf'
d=fitz.open(p)
pg=d[6]
for w in pg.get_text('words'):
    x0,y0,x1,y1,t=w[:5]
    if y0<150:
        print(f'{x0:6.1f} {y0:6.1f} {x1:6.1f} {y1:6.1f} {t}')
