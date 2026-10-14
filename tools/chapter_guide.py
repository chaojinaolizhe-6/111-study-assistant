"""Persist source-grounded chapter preparation separately from learner evidence."""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path
from material_reader import digest, source_path
from workspace_lock import WorkspaceLock, atomic_write_text


def guide_path(root, chapter):
    if not isinstance(chapter, str) or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9._-]{0,100}', chapter):
        raise ValueError('Invalid chapter ID')
    path = (root / 'learning/chapter-guides' / (chapter + '.json')).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('Guide path outside workspace')
    return path


def validate(root, guide):
    if guide.get('schema_version') != 1:
        raise ValueError('Expected guide schema_version=1')
    guide_path(root, guide.get('chapter_id'))
    if not guide.get('subject') or not (root / 'subjects' / guide['subject']).resolve().is_relative_to((root / 'subjects').resolve()) or not (root / 'subjects' / guide['subject']).is_dir():
        raise ValueError('Unknown subject')
    if guide.get('preparation') not in ('structure', 'keypoints', 'detailed'):
        raise ValueError('Unknown preparation depth')
    sources = {}; actual = {}
    for source in guide.get('sources', []):
        sid = source['id']
        if sid in sources or source['role'] not in ('slides', 'textbook', 'knowledge-note'):
            raise ValueError('Duplicate source ID or invalid source role')
        path = source_path(root, source['path'])
        if digest(path) != source['sha256']:
            raise ValueError('STALE source: ' + source['path'])
        if path.suffix.lower() == '.pdf':
            import fitz
            with fitz.open(path) as doc:
                count = len(doc)
            if source.get('page_count') != count:
                raise ValueError('Incorrect PDF page_count')
        elif path.suffix.lower() in ('.md', '.txt'):
            count = None
        else:
            raise ValueError('Guide sources must be PDF or text notes')
        for field in ('text_read_pages', 'visual_read_pages', 'formula_verified_pages'):
            values = source.get(field, [])
            if not isinstance(values, list) or any(type(p) is not int or count is None or p < 1 or p > count for p in values):
                raise ValueError('Invalid reading receipt: ' + field)
        if not set(source.get('formula_verified_pages', [])) <= set(source.get('visual_read_pages', [])):
            raise ValueError('Formula verification requires visual reading receipt')
        if count is None and not source.get('note_read', False):
            raise ValueError('Referenced knowledge note must actually have been read')
        sources[sid] = source; actual[sid] = count
    if not sources or not any(s['role'] == 'slides' for s in sources.values()):
        raise ValueError('A guide requires a slide source')

    def refs(values, role=None, require_visual=False, allow_unread=False):
        if not isinstance(values, list):
            raise ValueError('References must be lists')
        for ref in values:
            source = sources.get(ref.get('source'))
            if not source or (role and source['role'] not in role):
                raise ValueError('Wrong reference source/role')
            count = actual[ref['source']]
            if count is not None:
                values = ref.get('pages', [])
                read = set(source.get('text_read_pages', [])) | set(source.get('visual_read_pages', []))
                if not values or any(type(p) is not int or p < 1 or p > count or (not allow_unread and p not in read) for p in values):
                    raise ValueError('Cited PDF pages require actual reading receipt')
                if require_visual and not set(values) <= set(source.get('visual_read_pages', [])):
                    raise ValueError('Exact examples/exercises require visual inspection of source pages')
            elif not ref.get('heading'):
                raise ValueError('Knowledge-note citation needs a heading')

    if not guide.get('units'):
        raise ValueError('A guide requires concrete units')
    seen = set()
    for unit in guide['units']:
        if not unit.get('id') or unit['id'] in seen or not unit.get('title') or not unit.get('key_points'):
            raise ValueError('Each unit needs unique ID, title and key points')
        seen.add(unit['id'])
        relation = unit.get('relation'); route = unit.get('route')
        if relation not in ('shared', 'slides-only-in-checked-scope', 'textbook-supplement', 'unresolved') or route not in ('main', 'prerequisite', 'extension'):
            raise ValueError('Invalid comparison relation or teaching route')
        slide_refs = unit.get('slide_refs', []); book_refs = unit.get('book_refs', [])
        candidates = unit.get('book_candidates', [])
        refs(candidates, ('textbook',), allow_unread=True)
        if candidates and relation == 'slides-only-in-checked-scope':
            raise ValueError('Known textbook candidate requires unresolved until body is read; not slide-only')
        refs(slide_refs, ('slides',)); refs(book_refs, ('textbook', 'knowledge-note'))
        refs(unit.get('example_refs', []), require_visual=True)
        refs(unit.get('exercise_refs', []), require_visual=True)
        if relation == 'shared' and (not slide_refs or not any(sources[r['source']]['role'] == 'textbook' for r in book_refs)):
            raise ValueError('Shared content requires evidence on both sides')
        if relation == 'slides-only-in-checked-scope':
            if not slide_refs or not unit.get('comparison_scope'):
                raise ValueError('Slide-specific claim requires declared checked scope')
            refs(unit['comparison_scope'], ('textbook', 'knowledge-note'))
            if not any(sources[r['source']]['role'] == 'textbook' for r in unit['comparison_scope']):
                raise ValueError('A note-only comparison cannot establish textbook absence; use unresolved')
        if relation == 'textbook-supplement' and (not book_refs or not unit.get('reason')):
            raise ValueError('Supplement requires source and relevance reason')
        if relation == 'textbook-supplement':
            if not unit.get('slide_checked_scope'):
                raise ValueError('Supplement comparison requires inspected slide scope')
            refs(unit['slide_checked_scope'], ('slides',))
        if relation == 'unresolved' and not unit.get('reason'):
            raise ValueError('Unresolved mapping requires a reason')
        if slide_refs and route == 'extension':
            if unit.get('defer_basis') not in ('user-request', 'confirmed-course-scope') or not unit.get('defer_ref'):
                raise ValueError('Slide content stays on the main route; textbook chapter order cannot demote it')
            source_path(root, unit['defer_ref'])
        if route == 'prerequisite' and not unit.get('reason'):
            raise ValueError('Prerequisite requires a reason for current learning')
        if relation == 'textbook-supplement' and route == 'main' and not unit.get('reason'):
            raise ValueError('Do not silently add textbook scope')
    refs(guide.get('structure_refs', []), ('slides',))
    if not guide.get('structure_refs') or not guide.get('next_read'):
        raise ValueError('Include structure evidence and next targeted reading')
    return guide


def policy_sha(root):
    paths = ('.tutor/docs/课件与教材协同学习.md', '.tutor/config/knowledge-base.md')
    values = {p: digest(root / p) if (root / p).is_file() else None for p in paths}
    return hashlib.sha256(json.dumps(values, sort_keys=True).encode('utf-8')).hexdigest()


def save(root, guide):
    with WorkspaceLock(root / 'learning', label='chapter_guide'):
        validate(root, guide)
        guide = dict(guide); guide['study_policy_sha256'] = policy_sha(root)
        # Source preparation never edits attempts, mastery, curriculum completeness or the source library.
        path = guide_path(root, guide['chapter_id'])
        atomic_write_text(path, json.dumps(guide, ensure_ascii=False, indent=2) + '\n')
    return {'saved': path.relative_to(root).as_posix(), 'learner_evidence_changed': False}


def check(root, chapter):
    path = guide_path(root, chapter)
    if not path.is_file():
        return {'status': 'missing', 'action': 'Prepare current chapter structure and key points; do not ask learner to build the map.'}
    try:
        guide = json.loads(path.read_text(encoding='utf-8'))
        validate(root, guide)
        if guide.get('study_policy_sha256') != policy_sha(root):
            raise ValueError('Study policy changed')
    except (ValueError, KeyError, TypeError, OSError) as exc:
        return {'status': 'stale', 'reason': str(exc), 'action': 'Refresh affected sources and mappings; keep unaffected cached extraction.'}
    return {'status': 'ready', 'guide': path.relative_to(root).as_posix(),
            'preparation': guide['preparation'], 'units': len(guide['units']),
            'action': 'Reuse prepared sources; adapt route using current learner evidence. Read only the next needed pages.'}


def catalog(root, subject=None):
    data = json.loads((root / 'learning/curriculum.json').read_text(encoding='utf-8'))
    return [{'subject': course['subject'], 'chapter_id': chapter['id'],
             'title': chapter['title'], 'material': chapter['material']}
            for course in data['courses'] if subject is None or course['subject'] == subject
            for chapter in course['chapters']]


def template(root, chapter):
    matches = [item for item in catalog(root) if item['chapter_id'] == chapter]
    if len(matches) != 1:
        raise ValueError('Chapter ID must identify one actual curriculum entry; use list first')
    item = matches[0]; path = source_path(root, item['material'])
    import fitz
    with fitz.open(path) as doc:
        count = len(doc)
    # A template is a locator, never a reading receipt or a valid prepared guide.
    return {'schema_version': 1, 'chapter_id': chapter, 'subject': item['subject'],
            'preparation': 'keypoints',
            'sources': [{'id': 'slides', 'role': 'slides', 'path': item['material'],
                         'sha256': digest(path), 'page_count': count,
                         'text_read_pages': [], 'visual_read_pages': [], 'formula_verified_pages': []}],
            'structure_refs': [], 'units': [], 'next_read': []}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('list', 'template', 'check', 'show', 'save'))
    parser.add_argument('--root', default='.')
    parser.add_argument('--subject')
    parser.add_argument('--chapter')
    parser.add_argument('--file')
    args = parser.parse_args(); root = Path(args.root).resolve()
    try:
        if args.action == 'list':
            result = {'chapters': catalog(root, args.subject)}
        elif args.action == 'template':
            if not args.chapter: parser.error('template needs --chapter')
            result = template(root, args.chapter)
        elif args.action == 'save':
            if not args.file: parser.error('save needs --file')
            result = save(root, json.loads(source_path(root, args.file).read_text(encoding='utf-8')))
        else:
            if not args.chapter: parser.error('check/show needs --chapter')
            result = check(root, args.chapter)
            if args.action == 'show' and result['status'] == 'ready':
                result = json.loads(guide_path(root, args.chapter).read_text(encoding='utf-8'))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if args.action == 'save' or result.get('status', 'ready') in ('ready', 'missing') else 2
    except Exception as exc:
        print('CHAPTER GUIDE FAIL: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    raise SystemExit(main())
