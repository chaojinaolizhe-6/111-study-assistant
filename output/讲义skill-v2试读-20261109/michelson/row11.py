import fitz
p=r'output/讲义skill-v2试读-20261109/michelson/michelson-excerpt-v2.pdf'
d=fitz.open(p)
for pno in [2,3]:
    print('PAGE',pno+1)
    for w in d[pno].get_text('words'):
        x0,y0,x1,y1,t=w[:5]
        if 'micrometer' in t or t in ('微调鼓轮','11','每转'):
            print(f'{x0:6.1f} {y0:6.1f} {x1:6.1f} {y1:6.1f} {t}')
