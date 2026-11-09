import fitz
p=r'output/讲义skill-v2试读-20261109/michelson/michelson-excerpt-v2.pdf'
d=fitz.open(p)
for i in range(d.page_count):
    pg=d[i]
    blocks=[b for b in pg.get_text('blocks') if b[4].strip() and b[3]<795]
    ymax=max((b[3] for b in blocks), default=0)
    print(i+1, 'body ymax=%.1f'%ymax)
