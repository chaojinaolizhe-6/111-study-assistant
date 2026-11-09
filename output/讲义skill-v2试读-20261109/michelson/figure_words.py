import fitz
p=r'output/讲义skill-v2试读-20261109/michelson/michelson-excerpt-v2.pdf'
d=fitz.open(p)
for pno in [5,11]:
    pg=d[pno]
    print('===== PAGE',pno+1,'=====')
    for w in pg.get_text('words'):
        x0,y0,x1,y1,t=w[0],w[1],w[2],w[3],w[4]
        if y0<500 and y1>60:
            print(f'{x0:6.1f} {y0:6.1f} {x1:6.1f} {y1:6.1f}  {t}')
