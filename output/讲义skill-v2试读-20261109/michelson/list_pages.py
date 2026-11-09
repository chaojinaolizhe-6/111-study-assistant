from pathlib import Path
p=Path(r'output/讲义skill-v2试读-20261109/michelson/pdftext.txt')
text=p.read_text(encoding='utf-8')
pages=text.split('\f')
for i,pg in enumerate(pages,1):
    lines=[l.strip() for l in pg.splitlines() if l.strip()]
    print(f'===== PAGE {i} ({len(lines)} lines) =====')
    if lines:
        print('FIRST:', ' | '.join(lines[:3]))
        print('LAST :', ' | '.join(lines[-3:]))
