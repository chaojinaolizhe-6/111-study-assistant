"""Record actual recall practice; deterministic SM-2 without same-day inflation.

Existing concept frontmatter remains the memory schedule source. This does not
modify capability grades. Same-day repetitions use the worst first-attempt
quality against the same pre-day snapshot, so prompted recovery cannot erase
an earlier lapse or increment reps twice.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from learninglib import parse_frontmatter, parse_yaml
from timebase import add_days, learning_today
from workspace_lock import WorkspaceLock, LockTimeout, atomic_write_text

FIELDS = ('ef', 'interval', 'reps', 'last_review', 'due')


def transition(before: dict, quality: int, today: str, settings: dict) -> dict:
    sm2 = settings.get('sm2', {})
    lapse = settings.get('lapse', {})
    ef = float(before.get('ef', 2.5))
    reps = int(before.get('reps', 0))
    interval = int(before.get('interval', 0))
    minimum = float(sm2.get('min_ef', 1.3))
    if quality < 3:
        reps = 0
        interval = int(lapse.get('reset_interval', 1))
        ef = max(minimum, ef-float(lapse.get('ef_penalty', .2)))
    else:
        reps += 1
        interval = (int(sm2.get('first_interval', 1)) if reps == 1 else
                    int(sm2.get('second_interval', 6)) if reps == 2 else max(1, round(interval*ef)))
        ef = max(minimum, ef+.1-(5-quality)*(.08+(5-quality)*.02))
    return {'ef':round(ef, 4), 'reps':reps, 'interval':interval,
            'last_review':today, 'due':add_days(today, interval)}


def replace_fields(text: str, values: dict) -> str:
    match = re.match(r'^---\n(.*?)\n---(?:\n|$)', text, re.S)
    if not match:
        raise ValueError('Concept must have frontmatter')
    body = match.group(1)
    for key, value in values.items():
        pattern = re.compile(rf'^{key}:.*$', re.M)
        if len(pattern.findall(body)) > 1:
            raise ValueError(f'Duplicate concept field: {key}')
        if pattern.search(body):
            body = pattern.sub(f'{key}: {value}', body)
        else:
            body += f'\n{key}: {value}'
    return '---\n'+body+'\n---\n'+text[match.end():]


def record(root: Path, concept: str, quality: int, today: str, event_id: str | None = None) -> dict:
    if type(quality) is not int or not 0 <= quality <= 5:
        raise ValueError('Quality must be integer 0..5')
    with WorkspaceLock(root / 'learning', label='record_review'):
        paths = [p for p in (root / 'subjects').glob('*/topics/**/*.md')
                 if parse_frontmatter(p.read_text(encoding='utf-8')).get('id') == concept]
        if len(paths) != 1:
            raise ValueError('Concept ID must identify exactly one existing note')
        path = paths[0]
        old_text = path.read_bytes().decode('utf-8')
        fm = parse_frontmatter(old_text)
        last = fm.get('last_review')
        if last and last not in ('null','None') and last > today:
            raise ValueError('Cannot rewrite a memory schedule from a past date')
        logfile = root / 'state/reviews.jsonl'
        old_log = logfile.read_bytes().decode('utf-8') if logfile.exists() else ''
        events = [json.loads(line) for line in old_log.splitlines() if line.strip()]
        previous=[e for e in events if e.get('concept_id') == concept and e.get('sm2_after')]
        if previous:
            saved=previous[-1]['sm2_after']
            actual={key:fm.get(key) for key in FIELDS}
            for key in ('ef','interval','reps'):
                if float(actual.get(key) or 0) != float(saved[key]):
                    raise ValueError('Memory journal and note disagree; recover from the latest sm2_after before recording')
            if any(actual.get(key) != saved[key] for key in ('last_review','due')):
                raise ValueError('Memory journal and note disagree; recover from the latest sm2_after before recording')
        if event_id and any(e.get('event_id') == event_id for e in events):
            raise ValueError('Duplicate review event ID')
        same_day = [e for e in events if e.get('concept_id') == concept and str(e.get('ts',''))[:10] == today]
        if same_day:
            before = same_day[0].get('sm2_before')
            if not before:
                raise ValueError('Legacy same-day review lacks pre-day snapshot; do not guess')
            effective_q = min([quality]+[int(e['q']) for e in same_day])
        else:
            if last == today:
                raise ValueError('Same-day schedule exists without a reconstructible review event')
            before = {key:fm.get(key) for key in FIELDS}
            for key, default in (('ef',2.5),('interval',0),('reps',0)):
                if before[key] in (None,'null','None',''):
                    before[key] = default
            effective_q = quality
        settings = parse_yaml((root / '.tutor/core/settings.yml').read_text(encoding='utf-8'))
        after = transition(before, effective_q, today, settings)
        numbers = [int(e.get('event_id','').split('-')[-1]) for e in events if re.fullmatch(r'review-\d+', e.get('event_id',''))]
        row = {'event_id':event_id or f'review-{max(numbers,default=0)+1}',
               'concept_id':concept, 'q':quality, 'effective_day_q':effective_q,
               'ts':today, 'sm2_before':before, 'sm2_after':after,
               'note_path':path.relative_to(root).as_posix()}
        new_text = replace_fields(old_text.replace('\r\n','\n'), after)
        # Journal first. If the note write fails, restore only this transaction.
        try:
            prefix = old_log + ('\n' if old_log and not old_log.endswith('\n') else '')
            atomic_write_text(logfile, prefix+json.dumps(row,ensure_ascii=False)+'\n')
            atomic_write_text(path, new_text)
        except Exception:
            atomic_write_text(logfile, old_log)
            atomic_write_text(path, old_text)
            raise
        return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',default='.')
    parser.add_argument('--concept',required=True)
    parser.add_argument('--quality',required=True,type=int)
    parser.add_argument('--today')
    parser.add_argument('--event-id')
    args = parser.parse_args()
    try:
        row = record(Path(args.root).resolve(),args.concept,args.quality,learning_today(args.today),args.event_id)
        print(json.dumps(row,ensure_ascii=False))
        return 0
    except (ValueError,OSError,KeyError,TypeError,LockTimeout) as exc:
        print(f'REVIEW FAIL: {exc}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
