import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


outputs = []
for rel in ['handout.tex', 'handout.pdf', 'handout.log', 'verification.txt',
            'rendered/index.txt', 'check_handout.py', 'verify_handout.py',
            'render_pages.py', 'make_manifest.py']:
    p = ROOT / rel
    if p.exists():
        outputs.append({'path': 'round-02/' + rel, 'bytes': p.stat().st_size, 'sha256': sha(p)})

rendered = sorted((ROOT / 'rendered').glob('page-*.png'))
for p in rendered:
    outputs.append({'path': 'round-02/rendered/' + p.name, 'bytes': p.stat().st_size, 'sha256': sha(p)})

inputs = []
for rel in ['inputs/TM2026-Topic8-P1.pdf', 'inputs/RIT-Whelan-notes10-tensor.pdf',
            'inputs/baseline-full-v2.2.2.pdf', 'inputs/baseline-full-v2.2.2.tex',
            'inputs/accepted-mainline-v2.3.pdf', 'inputs/accepted-mainline-v2.3.tex',
            'inputs/learner-background-full.json', 'inputs/accepted-mainline-selection.json']:
    p = PARENT / rel
    if p.exists():
        inputs.append({'path': rel, 'bytes': p.stat().st_size, 'sha256': sha(p)})

prev = []
for rel in ['round-01/handout.pdf', 'round-01/handout.tex']:
    p = PARENT / rel
    if p.exists():
        prev.append({'path': rel, 'bytes': p.stat().st_size, 'sha256': sha(p)})

manifest = {
    'generated_at': datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
    'round': 'round-02',
    'kind': 'rework of the reviewed first draft (round-01 left untouched)',
    'book': '从张量到并矢：二次型主轴、并矢运算与三处力学落点',
    'skill': {'name': 'lecture-deepdive', 'version': '2.3.0'},
    'review_basis': '_scratch/lecture-review-20261111/问题单-从张量到并矢-round01.md',
    'summary': {
        'pdf_pages': 57,
        'exercises': 12,
        'figures': 11,
        'verify_assertions': 157,
        'verify_failures': 0,
        'check_handout_errors': 0,
        'check_handout_hints': 0,
        'xelatex_passes': 2,
        'overfull_hbox': 0,
        'missing_character': 0,
        'undefined_references': 0,
        'underfull_hbox': 3,
        'issues_fixed_major': 5,
        'issues_fixed_minor': 9,
        'issues_deferred': 3,
    },
    'outputs': outputs,
    'inputs': inputs,
    'previous_round_untouched': prev,
}
(ROOT / 'delivery-manifest.json').write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('wrote', ROOT / 'delivery-manifest.json')
print('outputs:', len(outputs), 'rendered pages:', len(rendered))
