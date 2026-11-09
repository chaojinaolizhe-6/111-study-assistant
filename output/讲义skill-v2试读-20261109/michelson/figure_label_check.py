from pathlib import Path
text=Path(r'output/讲义skill-v2试读-20261109/michelson/pdftext_raw.txt').read_text(encoding='utf-8')
pages=text.split('\f')
req={
 6:['M1','M2′','2d tan θ','d/ cos θ','比较波面','投影段','A','B','C','D'],
 8:['S1','S2′','2d','z','r','FG','θ'],
 12:['G1','G2','M1','M2','M2′','S','扩束镜','E','FG','I','II'],
}
for p,labels in req.items():
    t=pages[p-1]
    missing=[x for x in labels if x not in t]
    print(f'page {p}: missing={missing}')
