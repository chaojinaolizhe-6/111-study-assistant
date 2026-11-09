import fitz
p=r'output/讲义skill-v2试读-20261109/michelson/michelson-excerpt-v2.pdf'
d=fitz.open(p)
for pno in [4,5]:
    print('===== PAGE',pno+1,'=====')
    for b in d[pno].get_text('blocks'):
        t=b[4].strip().replace('\n',' | ')
        if t and b[1]>600:
            print(f'y0={b[1]:.1f} y1={b[3]:.1f} x0={b[0]:.1f} x1={b[2]:.1f}  {t[:120]}')
