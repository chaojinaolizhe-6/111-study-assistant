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


def build(root: Path, today: str, subject: str | None = None) -> dict:
    state = json.loads((root / 'learning/learner-state.json').read_text(encoding='utf-8'))
    current = state.get('source') == source_fingerprint(root)
    context = {'date_china':today, 'state_current':current,
               'refresh_command':'python -B tools/session-close.py',
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
            print(f'另有 {unknown} 份课程/参考资料尚未核章节结构，不声称全课程已覆盖。')
            print('下一步只读相关课程；完整学术/事件细节按需查原文件。')
        return 0 if context['state_current'] else 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'CONTEXT FAIL: {exc}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
