from pathlib import Path
text=Path(r'output/讲义skill-v2试读-20261109/michelson/pdftext.txt').read_text(encoding='utf-8')
pages=text.split('\f')
for i in [6,7,11,12,15,16]:
    print('===== PAGE',i+1,'=====')
    print(pages[i][:2500])
