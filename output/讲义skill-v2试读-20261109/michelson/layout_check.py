import fitz
p=r'output/讲义skill-v2试读-20261109/michelson/michelson-excerpt-v2.pdf'
d=fitz.open(p)
for i in range(d.page_count):
    pg=d[i]
    blocks=[b for b in pg.get_text('blocks') if b[4].strip()]
    bad=[]
    for b in blocks:
        x0,y0,x1,y1,txt=b[0],b[1],b[2],b[3],b[4].strip().replace('\n',' | ')
        if y0>60 and y1<795 and (y1>778 or x0<55 or x1>540):
            bad.append((round(x0,1),round(y0,1),round(x1,1),round(y1,1),txt[:60]))
    if bad:
        print('PAGE',i+1,'MARGIN FLAGS')
        for row in bad: print('  ',row)
print('--- overlaps ---')
for i in range(d.page_count):
    pg=d[i]
    words=pg.get_text('words')
    # only words with reasonable length and in body
    ws=[w for w in words if w[4].strip() and w[1]>60 and w[3]<795]
    hits=[]
    for a in range(len(ws)):
        x0,y0,x1,y1,t=ws[a][:5]
        for b in range(a+1,len(ws)):
            X0,Y0,X1,Y1,T=ws[b][:5]
            ix=min(x1,X1)-max(x0,X0); iy=min(y1,Y1)-max(y0,Y0)
            if ix>2 and iy>2:
                area=ix*iy; small=min((x1-x0)*(y1-y0),(X1-X0)*(Y1-Y0))
                if small>0 and area/small>0.25:
                    hits.append((round(area/small,2),t,T))
    if hits:
        print('PAGE',i+1,'overlap pairs',len(hits))
        for h in hits[:8]: print('  ',h)
