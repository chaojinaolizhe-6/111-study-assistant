"""Small, read-only session context from current evidence and course scope."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from curriculum import reconcile
from derive_state import source_fingerprint
from observations import pending
from reviews import all_review_items
from timebase import learning_today
from learninglib import resumable_attempts, load_hurdles


def scan_progress_three_state_gaps(root: Path, subject: str | None = None) -> list[dict]:
    """Scan subjects/*/progress.md for 3-state table rows containing ❌, 未讲, 未学, or 未测."""
    subjects_dir = root / 'subjects'
    if not subjects_dir.is_dir():
        return []
    gaps: list[dict] = []
    for prog in sorted(subjects_dir.glob('*/progress.md')):
        subj_name = prog.parent.name
        if subject and subj_name != subject:
            continue
        try:
            lines = prog.read_text(encoding='utf-8').splitlines()
        except OSError:
            continue
        section = ''
        for raw in lines:
            line = raw.strip()
            if line.startswith('### '):
                section = line[4:].strip()
                continue
            if not (line.startswith('|') and line.endswith('|')):
                continue
            cells = [c.strip() for c in line.strip('|').split('|')]
            if not cells or cells[0] in ('内容', '项', '---') or set(cells[0]) <= {'-', ':'}:
                continue
            row_text = ' | '.join(cells[1:])
            if any(marker in row_text for marker in ('❌', '未讲', '未学', '未测', '未做')):
                gaps.append({
                    'subject': subj_name,
                    'section': section,
                    'item': cells[0],
                    'state': ' / '.join(c for c in cells[1:] if any(m in c for m in ('❌', '未讲', '未学', '未测', '未做', '部分'))),
                })
    return gaps


def build(root: Path, today: str, subject: str | None = None) -> dict:
    state = json.loads((root / 'learning/learner-state.json').read_text(encoding='utf-8'))
    current = state.get('source') == source_fingerprint(root)
    context = {'date_china':today, 'state_current':current,
               'refresh_command':'python -B tools/session-close-and-sync.py',
               'preferences':{'closed_book_default':True, 'math':'Unicode', 'timezone':'Asia/Shanghai'},
               'pending_observations':pending(root)}
    if not current:
        context['warning'] = '派生状态过期，旧计数不能用于判断当前掌握；先刷新。'
        return context
    context['summary'] = state['summary']
    context['attempts_count'] = state['source']['attempts_events']
    context['open_hurdles'] = [
        {k:row['data'].get(k) for k in ('hurdle_id','target_ids','status')}
        for row in load_hurdles(root) if row.get('data') and row['data'].get('status') in ('open','teaching','awaiting_retest')
    ]
    context['due_items'] = [row for row in all_review_items(root, today) if row['due'] <= today and (not subject or row.get('subject') == subject)]
    report = reconcile(root)
    if subject:
        report['chapters'] = [c for c in report['chapters'] if c['subject'] == subject]
    context['scope_registered'] = bool(report['chapters'])
    context['resume_points'] = [
        {'task_id':e['task_id'], 'event_id':e['event_id'],
         'notes':[v['note'] for v in (e.get('target_results') or {}).values() if v.get('note')]}
        for e in resumable_attempts(root)
        if not subject or any((state['targets'].get(t, {}).get('goal') or {}).get('subject') == subject for t in e.get('target_ids', []))
    ]
    scheduled_zero = []
    unscheduled_zero = []
    for tid, tgt in sorted(state.get('targets', {}).items()):
        t_subj = (tgt.get('goal') or {}).get('subject')
        if subject and t_subj != subject:
            continue
        if tgt.get('attempts', 0) == 0:
            if tgt.get('tasks'):
                scheduled_zero.append(tid)
            else:
                unscheduled_zero.append(tid)
    context['untaught_targets'] = {
        'scheduled_zero_attempts': scheduled_zero,
        'unscheduled_no_tasks': unscheduled_zero,
        'gate_rule': '凡 0 次作答或三态表含「❌/未讲/未学」的考点默认【未学（untaught）】，严禁跳过讲解直接布置作答。',
    }
    context['progress_three_state_gaps'] = scan_progress_three_state_gaps(root, subject)
    context['intent_source'] = '.tutor/config/status-narrative.yml（按需读取当前顺序与暂缓理由）'
    context['curriculum'] = [
        {'id':chapter['id'], 'title':chapter['title'], 'subject':chapter['subject'],
         'inventory_complete':chapter['inventory_complete'], 'coverage_percent':chapter['coverage_percent'],
         'units':[{k:unit[k] for k in ('title','status','no_tasks','no_independent')} for unit in chapter['units']]}
        for chapter in report['chapters']]
    context['next_read'] = ['.tutor/core/protocol.md', '.tutor/config/teaching-conventions.md', 'state/current.md（只读相关课程）']
    return context


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default='.')
    parser.add_argument('--today')
    parser.add_argument('--subject')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    try:
        context = build(Path(args.root).resolve(), learning_today(args.today), args.subject)
        if args.json:
            print(json.dumps(context, ensure_ascii=False, indent=2))
        else:
            print(f'中国学习日期：{context["date_china"]}；状态最新：{context["state_current"]}')
            if not context['state_current']:
                print(context['warning'], context['refresh_command'])
                return 1
            summary = context['summary']
            print(f'真实作答 {context["attempts_count"]} 条')
            print(f'已登记能力目标 {summary["targets"]}；稳定证据 {summary["stable_evidence"]}；未解决困难 {summary["open_hurdles"]}')
            print('待处理学习者反馈：', len(context['pending_observations']))
            for row in context['pending_observations'][:5]:
                print(f'- {row["id"]}: {row["text"]}')
            print('未完成题续学点：', len(context['resume_points']))
            for row in context['resume_points'][-6:]:
                print(f'- {row["task_id"]}: {"；".join(row["notes"]) or "按实际草稿核对"}')
            untaught = context['untaught_targets']
            print(f'⚠ 未学门禁（防幻觉）：{untaught["gate_rule"]}')
            if untaught['scheduled_zero_attempts']:
                print('  - 已建题但 0 次作答（默认未学，须先教后做）：', '、'.join(untaught['scheduled_zero_attempts']))
            if untaught['unscheduled_no_tasks']:
                print('  - 已声明但无题且 0 次作答（默认未学）：', '、'.join(untaught['unscheduled_no_tasks']))
            gaps = context['progress_three_state_gaps']
            if gaps:
                print(f'课程 progress.md 三态表未讲/未学/未测项（共 {len(gaps)} 项，严禁当已学处理）：')
                for g in gaps[:12]:
                    sec = f'[{g["section"]}] ' if g['section'] else ''
                    print(f'  - {g["subject"]} {sec}{g["item"]} → {g["state"]}')
            print('当前意图来源：', context['intent_source'])
            if not context['scope_registered']:
                print('本项目尚未登记课件章节范围；能力状态仍按实际账本展示，不推断全覆盖。')
            print('当前可做/到期任务：', len(context['due_items']))
            for row in context['due_items'][:6]:
                print(f'- {row["id"]}: {row["note"]}')
            print('课程范围缺口（不是成绩）：')
            for chapter in context['curriculum']:
                if chapter['units']:
                    print(f'- {chapter["id"]}：范围完整={chapter["inventory_complete"]}；全章覆盖={chapter["coverage_percent"] if chapter["coverage_percent"] is not None else "未知"}')
                    for unit in chapter['units']:
                        if unit['status'] != '已有稳定证据':
                            print(f'  {unit["title"]}：{unit["status"]}')
            unknown = sum(not c['units'] for c in context['curriculum'])
            print(f'另有 {unknown} 份课程/参考资料尚未核章节结构（默认未学），不声称全课程已覆盖。')
            print('下一步只读相关课程；完整学术/事件细节按需查原文件。')
        return 0 if context['state_current'] else 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'CONTEXT FAIL: {exc}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
