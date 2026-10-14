"""Append actionable learner observations and explicit resolutions, without grades.

`subject` 取值两种（读、写同一判据 `subject_error()`）：
- 课程目录名（如 `01-理论力学`）——普通课程反馈；
- 工作区级占位 `—（主题）`（如 `—（排期规则）`）——针对排期/协议等**不属于任何单一课程**的反馈，不得用它绕开课程归属。
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import re
from pathlib import Path
from curriculum import safe_path
from workspace_lock import WorkspaceLock, LockTimeout

# 工作区级反馈占位：全角括号包裹，非课程目录名（历史记录 obs-13 即此形式）
WORKSPACE_SCOPE = re.compile(r'—（[^（）/\\]{1,30}）')


def subject_error(root: Path, subject) -> str | None:
    """返回不合法原因；合法返回 None。读路径与写路径共用，避免两处判据漂移。"""
    if not isinstance(subject, str) or subject in ('.', '..') or '/' in subject or '\\' in subject:
        return 'Invalid observation subject'
    if WORKSPACE_SCOPE.fullmatch(subject):
        return None
    if not (root / 'subjects' / subject).is_dir():
        return 'Invalid observation subject'
    return None


def read_events(root: Path) -> list[dict]:
    path = root / 'learning/observations.jsonl'
    if not path.exists():
        return []
    events = []
    for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        event = json.loads(line)
        if not isinstance(event, dict) or event.get('action') not in ('create', 'resolve') or not re.fullmatch(r'obs-\d+', str(event.get('id', ''))):
            raise ValueError(f'Invalid observation line {number}')
        if event['action'] == 'create':
            if not isinstance(event.get('text'), str) or not event['text'].strip() or not event.get('evidence_ref') or event.get('kind') not in ('coverage_gap','deadline','difficulty','preference','pause'):
                raise ValueError(f'Invalid observation content line {number}')
            subject = event.get('subject')
            if subject_error(root, subject):
                raise ValueError(f'Invalid observation subject line {number}')
        elif not event.get('reason') or not event.get('artifact') or not safe_path(root,event['artifact']).is_file():
            raise ValueError(f'Invalid observation resolution line {number}')
        events.append(event)
    return events


def pending(root: Path) -> list[dict]:
    rows = {}
    for event in read_events(root):
        if event['action'] == 'create':
            if event['id'] in rows:
                raise ValueError('Duplicate observation ID')
            rows[event['id']] = event
        else:
            if event['id'] not in rows:
                raise ValueError('Resolution without an observation')
            if rows[event['id']].get('resolved'):
                raise ValueError('Duplicate observation resolution')
            rows[event['id']] = {**rows[event['id']], 'resolved': True}
    return [row for row in rows.values() if not row.get('resolved')]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default='.')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--file', help='JSON {text, subject, evidence_ref, kind}')
    mode.add_argument('--resolve', help='observation ID')
    mode.add_argument('--list', action='store_true')
    parser.add_argument('--artifact', help='existing task/plan/goal file')
    parser.add_argument('--reason')
    args = parser.parse_args()
    root = Path(args.root).resolve()
    try:
        if args.list:
            print(json.dumps(pending(root), ensure_ascii=False, indent=2))
            return 0
        with WorkspaceLock(root / 'learning', label='observations'):
            events = read_events(root)
            timestamp = dt.datetime.now(dt.timezone.utc).isoformat()
            if args.file:
                data = json.loads(Path(args.file).read_text(encoding='utf-8'))
                if not isinstance(data, dict) or not isinstance(data.get('text'), str) or not data['text'].strip() or not data.get('evidence_ref'):
                    raise ValueError('Observation requires learner text and evidence_ref')
                if subject_error(root, data.get('subject')):
                    raise ValueError('Unknown subject（用课程目录名，或工作区级占位「—（主题）」）')
                if data.get('kind') not in ('coverage_gap', 'deadline', 'difficulty', 'preference', 'pause'):
                    raise ValueError('Unknown observation kind')
                number = max((int(e['id'].split('-')[-1]) for e in events), default=0)+1
                event = {'id':f'obs-{number}', 'action':'create', 'at':timestamp,
                         'text':data['text'], 'subject':data['subject'], 'evidence_ref':data['evidence_ref'], 'kind':data['kind']}
            else:
                if args.resolve not in {e['id'] for e in pending(root)}:
                    raise ValueError('Observation missing or already resolved')
                if not args.reason or not args.artifact or not safe_path(root, args.artifact).is_file():
                    raise ValueError('Resolution requires reason and an existing artifact')
                event = {'id':args.resolve, 'action':'resolve', 'at':timestamp,
                         'artifact':args.artifact, 'reason':args.reason}
            path = root / 'learning/observations.jsonl'
            needs_newline = path.exists() and path.stat().st_size and not path.read_bytes().endswith(b'\n')
            with path.open('a', encoding='utf-8', newline='\n') as stream:
                if needs_newline:
                    stream.write('\n')
                stream.write(json.dumps(event, ensure_ascii=False)+'\n')
            print(json.dumps({'saved':event['id'], 'action':event['action']}, ensure_ascii=False))
        return 0
    except (ValueError, OSError, KeyError, TypeError, LockTimeout) as exc:
        print(f'OBSERVATION FAIL: {exc}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
