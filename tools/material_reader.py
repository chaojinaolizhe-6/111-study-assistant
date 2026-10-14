"""Local PDF preparation. Extraction/rendering never claims semantic reading."""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
from workspace_lock import WorkspaceLock, atomic_write_text


def source_path(root, name):
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError('Source must be an existing file inside this workspace')
    return path


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def pages(value, count, limit=None):
    result = set()
    for part in value.split(','):
        endpoints = part.strip().split('-')
        if len(endpoints) == 1:
            result.add(int(endpoints[0]))
        elif len(endpoints) == 2:
            a, b = map(int, endpoints)
            if a > b:
                raise ValueError('Reversed page range')
            result.update(range(a, b + 1))
        else:
            raise ValueError('Invalid page range')
    if not result or min(result) < 1 or max(result) > count:
        raise ValueError('PDF page outside document')
    if limit and len(result) > limit:
        raise ValueError(f'Read/render in batches of at most {limit} pages')
    return sorted(result)


def prepare(root, name):
    import fitz
    path = source_path(root, name)
    if path.suffix.lower() != '.pdf':
        raise ValueError('This reader accepts PDFs; use normal file reading for knowledge notes')
    sha = digest(path)
    directory = root / '.tutor/cache/materials' / sha
    record = directory / 'extraction.json'
    if record.is_file():
        cached = json.loads(record.read_text(encoding='utf-8'))
        if cached.get('sha256') == sha and cached.get('schema_version') == 1:
            cached['path'] = path.relative_to(root.resolve()).as_posix()
            return cached, directory, True
    with fitz.open(path) as doc:
        rows = []
        for i, page in enumerate(doc):
            text = page.get_text(sort=True)
            rows.append({'page': i + 1, 'printed_label': page.get_label() or None,
                         'text': text, 'images': len(page.get_images()),
                         'text_layer_sparse': len(text.strip()) < 80})
        data = {'schema_version': 1, 'path': path.relative_to(root.resolve()).as_posix(),
                'sha256': sha, 'page_count': len(doc), 'outline': doc.get_toc(), 'pages': rows,
                'reading_claim': 'Only text extraction. Formulas, figures and scanned pages require visual inspection.'}
    with WorkspaceLock(root / 'learning', label='material_reader'):
        if digest(path) != sha:
            raise ValueError('Source changed while extracting; retry')
        atomic_write_text(record, json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    return data, directory, False


def run(root, name, action, selection=None, query=None):
    data, directory, reused = prepare(root, name)
    output = {k: data[k] for k in ('path', 'sha256', 'page_count', 'reading_claim')}
    output['extraction_cache_reused'] = reused
    if action == 'info':
        output['outline'] = data['outline']
        output['pages_needing_scan_reading'] = [p['page'] for p in data['pages'] if p['text_layer_sparse']]
        output['pages_with_embedded_images'] = [p['page'] for p in data['pages'] if p['images']]
    elif action == 'read':
        selected = pages(selection, data['page_count'], 12)
        output['pages'] = [data['pages'][p - 1] for p in selected]
    elif action == 'find':
        if not query or len(query) > 300:
            raise ValueError('Supply a short literal search query')
        selected = pages(selection, data['page_count']) if selection else list(range(1, data['page_count'] + 1))
        hits = []
        for p in selected:
            text = data['pages'][p - 1]['text']; at = text.casefold().find(query.casefold())
            if at >= 0:
                hits.append({'page': p, 'snippet': text[max(0, at-100):at+len(query)+220]})
        output.update({'searched_pages': selected, 'hits': hits,
                       'warning': 'No literal match is not proof of absence: synonyms, other chapters and scans may contain the topic.'})
    elif action == 'render':
        import fitz
        selected = pages(selection, data['page_count'], 8)
        path = source_path(root, name); rendered = []
        with fitz.open(path) as doc:
            with WorkspaceLock(root / 'learning', label='material_render'):
                if digest(path) != data['sha256']:
                    raise ValueError('Source changed before rendering')
                directory.mkdir(parents=True, exist_ok=True)
                for p in selected:
                    image_path = directory / f'page-{p:04d}.png'
                    if not image_path.exists():
                        doc[p-1].get_pixmap(matrix=fitz.Matrix(1.6, 1.6)).save(image_path)
                    rendered.append({'page': p, 'image': str(image_path)})
        output.update({'rendered': rendered, 'warning': 'Rendering is not viewing. Open these images before claiming visual reading.'})
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('info', 'read', 'find', 'render'))
    parser.add_argument('--root', default='.')
    parser.add_argument('--source', required=True)
    parser.add_argument('--pages')
    parser.add_argument('--query')
    args = parser.parse_args()
    if args.action in ('read', 'render') and not args.pages:
        parser.error('--pages is required')
    try:
        print(json.dumps(run(Path(args.root).resolve(), args.source, args.action, args.pages, args.query), ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print('MATERIAL READ FAIL: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    raise SystemExit(main())
