# -*- coding: utf-8 -*-
import fitz, os, json

pdf = os.path.join('subjects', '03-微分方程', '讲义', 'ODE-期中之后-完整讲义-L13-L23-20261118.pdf')
doc = fitz.open(pdf)
print('pages', doc.page_count)

keys = ['名词中英对照（考前查用）', '第一近似系统', '相平面（phase plane）',
        'Determine the type of the critical point', '五组容易混的词',
        'improper node', '虚轴']
hits = {}
for i, page in enumerate(doc):
    t = page.get_text()
    for k in keys:
        if k in t and k not in hits:
            hits[k] = i + 1
print(json.dumps(hits, ensure_ascii=False, indent=1))

outdir = os.path.join('tmp', 'ode-ch6-en', 'png')
os.makedirs(outdir, exist_ok=True)
pages = sorted(set(hits.values()))
print('render pages', pages)
for p in pages:
    pix = doc[p - 1].get_pixmap(dpi=130)
    f = os.path.join(outdir, 'p%03d.png' % p)
    pix.save(f)
    print(f, pix.width, pix.height)
