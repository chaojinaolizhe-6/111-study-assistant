"""Validate course scope and reconcile expected units with existing evidence.

Scope is independent of student grades. Unknown inventory never yields 100%.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from derive_state import source_fingerprint
from timebase import learning_today
from workspace_lock import WorkspaceLock, LockTimeout, atomic_write_text


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError(f'{path.name}: expected object')
    return data


def safe_path(root: Path, value: str) -> Path:
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValueError('Expected relative source path')
    result = (root / value).resolve()
    if not result.is_relative_to(root.resolve()):
        raise ValueError('Source outside workspace')
    return result


def validate(root: Path, catalog: dict, materials: dict) -> None:
    if catalog.get('schema_version') != 1 or materials.get('schema_version') != 1:
        raise ValueError('Unsupported curriculum/material schema')
    seen = set()
    material_index = {}
    for material in materials['materials']:
        path = material['path']
        if path in material_index:
            raise ValueError(f'Duplicate material: {path}')
        local = safe_path(root, path)
        if not local.is_file():
            raise ValueError(f'Missing material: {path}')
        # A replaced source cannot keep its old "read/verified" flags.
        if hashlib.sha256(local.read_bytes()).hexdigest() != material['sha256']:
            raise ValueError(f'Material changed; re-register reading evidence: {path}')
        page_count = material.get('page_count')
        for key in ('text_extracted_pages', 'rendered_pages', 'visually_read_pages', 'formula_verified_pages'):
            pages = material.get(key, [])
            if not isinstance(pages, list) or any(type(n) is not int or n < 1 or not isinstance(page_count, int) or n > page_count for n in pages):
                raise ValueError(f'Invalid {key}: {path}')
        if not set(material.get('formula_verified_pages', [])) <= set(material.get('visually_read_pages', [])):
            raise ValueError(f'Formula verification requires actual reading: {path}')
        material_index[path] = material
    subjects = {p.name for p in (root / 'subjects').iterdir() if p.is_dir()}
    for course in catalog['courses']:
        if course['subject'] not in subjects:
            raise ValueError(f'Unknown course: {course["subject"]}')
        for chapter in course['chapters']:
            cid = chapter['id']
            if not isinstance(cid, str) or not cid or cid in seen:
                raise ValueError(f'Invalid/duplicate chapter: {cid}')
            seen.add(cid)
            source = chapter['material']
            if source not in material_index:
                raise ValueError(f'Unregistered source: {source}')
            if chapter['structure_status'] not in ('unknown', 'partial', 'verified'):
                raise ValueError(f'Invalid structure status: {cid}')
            if type(chapter.get('inventory_complete')) is not bool:
                raise ValueError(f'Inventory completeness must be explicit: {cid}')
            if chapter['inventory_complete'] and (chapter['structure_status'] != 'verified' or not chapter['units']):
                raise ValueError(f'Complete scope requires verified nonempty units: {cid}')
            unit_ids = set()
            for unit in chapter['units']:
                if not unit.get('id') or unit['id'] in unit_ids or not unit.get('title'):
                    raise ValueError(f'Invalid/duplicate unit: {cid}')
                unit_ids.add(unit['id'])
                targets = unit.get('target_ids')
                if not isinstance(targets, list) or any(not isinstance(t, str) or not t for t in targets) or len(set(targets)) != len(targets):
                    raise ValueError(f'Invalid target mapping: {cid}')
                pages = unit.get('source_pages', [])
                if not pages or any(type(n) is not int or n < 1 or n > material_index[source]['page_count'] for n in pages):
                    raise ValueError(f'Missing/invalid unit source pages: {cid}')


def reconcile(root: Path, chapter_id: str | None = None, subject: str | None = None) -> dict:
    catalog = load_json(root / 'learning/curriculum.json')
    materials = load_json(root / 'learning/materials.json')
    validate(root, catalog, materials)
    state = load_json(root / 'learning/learner-state.json')
    if state.get('source') != source_fingerprint(root):
        raise ValueError('Capability view is stale; run session-close.py before reconciling')
    chapters = []
    for course in catalog['courses']:
        if subject and course['subject'] != subject:
            continue
        for chapter in course['chapters']:
            if chapter_id and chapter['id'] != chapter_id:
                continue
            units = []
            for unit in chapter['units']:
                tids = unit['target_ids']
                targets = [state['targets'].get(t) for t in tids]
                missing_targets = [t for t in tids if t not in state['targets']]
                no_tasks = [t for t, row in zip(tids, targets) if not row or row.get('task_count', 0) == 0]
                no_independent = [t for t, row in zip(tids, targets) if not row or not row.get('independent_pass_dates')]
                if not tids or missing_targets:
                    status = '未登记目标'
                elif no_tasks:
                    status = '未安排（无题目）'
                elif no_independent:
                    status = '尚无独立证据'
                elif any(not row.get('stable_evidence') for row in targets):
                    status = '已有独立表现，待稳定检验'
                else:
                    status = '已有稳定证据'
                units.append({**unit, 'status': status, 'missing_targets': missing_targets,
                              'no_tasks': no_tasks, 'no_independent': no_independent})
            stable = sum(u['status'] == '已有稳定证据' for u in units)
            complete = chapter['inventory_complete'] and chapter['structure_status'] == 'verified'
            chapters.append({**chapter, 'subject': course['subject'], 'units': units,
                             'stable_units': stable,
                             'coverage_percent': round(100 * stable / len(units), 1) if complete and units else None,
                             'unmeasured_units': sum(bool(u['no_independent']) or not u['target_ids'] for u in units)})
    if (chapter_id or subject) and not chapters:
        raise ValueError('Specified chapter/course has no registered scope; do not infer full coverage')
    return {'schema_version': 1, 'chapters': chapters,
            'source': {p: hashlib.sha256((root / p).read_bytes()).hexdigest()
                       for p in ('learning/curriculum.json', 'learning/materials.json', 'learning/learner-state.json')}}


def render(report: dict, today: str) -> str:
    lines = ['# 课程范围与证据对账', '', f'> 生成日期：{today}（中国时间）。由 curriculum.py 生成，勿手工改。',
             '> 无独立证据 ≠ 没学会；目录未核全时全章覆盖率未知。这里的百分比只指已声明范围的稳定证据覆盖。', '']
    for chapter in report['chapters']:
        lines += [f'## {chapter["id"]} — {chapter["title"]}', '',
                  f'课程：{chapter["subject"]}；来源：{chapter["material"]}；结构：{chapter["structure_status"]}；范围完整：{chapter["inventory_complete"]}。',
                  f'已列范围单元 {len(chapter["units"])}；尚无独立证据 {chapter["unmeasured_units"]}；稳定证据 {chapter["stable_units"]}；全章覆盖：{str(chapter["coverage_percent"])+"%" if chapter["coverage_percent"] is not None else "未知"}。', '']
        if not chapter['units']:
            lines += ['尚未核读结构页、未建立范围基线，下一步：读目录/小节标题并登记。', '']
            continue
        lines += ['| 范围单元 | 页码 | 状态 | 无题/未登记目标 | 尚无独立证据 |', '|---|---|---|---|---|']
        for unit in chapter['units']:
            absent = list(dict.fromkeys(unit['missing_targets'] + unit['no_tasks']))
            lines.append(f'| {unit["title"]} | {",".join(map(str,unit["source_pages"]))} | {unit["status"]} | {", ".join(absent) or ("尚未映射" if not unit["target_ids"] else "—")} | {", ".join(unit["no_independent"]) or ("未知" if not unit["target_ids"] else "—")} |')
        lines.append('')
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default='.')
    parser.add_argument('--chapter')
    parser.add_argument('--subject')
    parser.add_argument('--today')
    parser.add_argument('--print', action='store_true', dest='print_only')
    args = parser.parse_args()
    root = Path(args.root).resolve()
    try:
        with WorkspaceLock(root / 'learning', label='curriculum'):
            report = reconcile(root, args.chapter, args.subject)
            text = render(report, learning_today(args.today))
            if args.print_only:
                print(text)
            else:
                if args.chapter or args.subject:
                    raise ValueError('Filtered reports are read-only; use --print')
                atomic_write_text(root / 'learning/curriculum-coverage.md', text)
                atomic_write_text(root / 'learning/curriculum-coverage.json', json.dumps(report, ensure_ascii=False, indent=2)+'\n')
                print(f'Curriculum reconciled: {len(report["chapters"])} registered materials/chapters; unknown scopes remain unknown')
        return 0
    except (OSError, ValueError, KeyError, TypeError, LockTimeout) as exc:
        print(f'CURRICULUM FAIL: {exc}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
