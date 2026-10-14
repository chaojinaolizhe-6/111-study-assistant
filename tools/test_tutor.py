"""Behavioral regression tests; all mutations happen in temporary synthetic workspaces."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor

from curriculum import reconcile, validate, load_json
from derive_state import derive, derive_and_write, source_fingerprint
from learninglib import independence_blockers, parse_yaml, parse_frontmatter, parse_list
from observations import pending
from record_review import record
from tutor_context import build
from sync_status import mirrored_except_names
from workspace_lock import WorkspaceLock

ROOT = Path(__file__).resolve().parents[1]


def run(root, script, *args):
    return subprocess.run([sys.executable,'-B',str(ROOT/'tools'/script),'--root',str(root),*args],
                          cwd=root,capture_output=True,text=True,encoding='utf-8',timeout=45)


class TutorTests(unittest.TestCase):
    def setUp(self):
        temporary_base = ROOT / 'tmp' / 'tests'
        temporary_base.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='tutor-regression-',dir=temporary_base)
        self.root = Path(self.temp.name)
        # Preserve raw records and text contracts, but never copy student images or textbook content.
        for name in ('learning','state','plan','.tutor'):
            shutil.copytree(ROOT/name,self.root/name,
                            ignore=shutil.ignore_patterns('*.png','*.jpg','*.jpeg','*.pdf','*.docx'))
        for name in ('AGENTS.md','CLAUDE.md'):
            shutil.copy2(ROOT/name,self.root/name)
        fixture_records = []
        for filename in ("attempts.jsonl", "observations.jsonl"):
            record_path = self.root / "learning" / filename
            if record_path.is_file():
                fixture_records.extend(json.loads(line) for line in record_path.read_text(encoding="utf-8").splitlines() if line.strip())
        for record in fixture_records:
            artifact = record.get("artifact_ref") or (record.get("artifact") if record.get("action") == "resolve" else None)
            if artifact:
                dest=(self.root/artifact).resolve()
                if not dest.is_relative_to(self.root.resolve()):
                    raise ValueError('Fixture artifact outside temporary workspace')
                if not dest.exists():
                    dest.parent.mkdir(parents=True,exist_ok=True)
                    dest.write_text('Synthetic placeholder; tests never inspect student image content',encoding='utf-8')
        course = '01-理论力学'
        note = self.root/'subjects'/course/'topics/test-concept.md'
        note.parent.mkdir(parents=True)
        note.write_text('---\nid: test-memory\nef: 2.5\ninterval: 0\nreps: 0\nlast_review: null\ndue: null\n---\nSynthetic concept\n',encoding='utf-8')
        source = self.root/f'subjects/{course}/课件/TM_Topic_04_2026_student.pdf'
        source.parent.mkdir(parents=True)
        source.write_bytes(b'synthetic-source-not-a-student-pdf')
        catalog = load_json(ROOT/'learning/curriculum.json')
        chapter = next(c for course in catalog['courses'] for c in course['chapters'] if c['id']=='tm-topic-04')
        catalog['courses'] = [{'subject':course,'curriculum_complete':False,'chapters':[chapter]}]
        material = next(m for m in load_json(ROOT/'learning/materials.json')['materials'] if m['path']==chapter['material'])
        material['sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
        self.write('learning/curriculum.json',catalog)
        self.write('learning/materials.json',{'schema_version':1,'materials':[material]})
        derive_and_write(self.root)
        self.baseline_count=sum(bool(line.strip()) for line in (self.root/"learning/attempts.jsonl").read_text(encoding="utf-8").splitlines())

    def tearDown(self):
        if not self.root.resolve().is_relative_to((ROOT/'tmp/tests').resolve()):
            raise ValueError('Refusing to clean up outside the test workspace')
        self.temp.cleanup()

    def write(self,path,data):
        (self.root/path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    def test_yaml_quoted_hash_colon_dates(self):
        data = parse_yaml('note: "Topic #4: L与E"\ndate: 2026-10-02\n')
        self.assertEqual(data['note'],'Topic #4: L与E')
        self.assertEqual(data['date'],'2026-10-02')

    def test_yaml_duplicate_key_rejected(self):
        with self.assertRaises(ValueError):
            parse_yaml('x: 1\nx: 2\n')

    def test_frontmatter_quotes_comments_block_lists_crlf(self):
        fm=parse_frontmatter('---\r\nid: "task-1"\r\ntitle: "Topic #4: L"\r\ndue: 2026-10-08 # window\r\ntarget_ids:\r\n  - "target:one"\r\n  - "target,two"\r\n---\r\nBody')
        self.assertEqual(fm['id'],'task-1')
        self.assertEqual(fm['title'],'Topic #4: L')
        self.assertEqual(fm['due'],'2026-10-08')
        self.assertEqual(parse_list(fm['target_ids']),['target:one','target,two'])
        with self.assertRaises(ValueError):
            parse_frontmatter('---\nid: one\nid: two\n---\n')

    def test_week_planner_uses_shared_yaml_parser(self):
        import importlib.util
        spec=importlib.util.spec_from_file_location('week_plan',ROOT/'tools/plan-week.py')
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertIs(module.parse_yaml,parse_yaml)
        self.assertIs(module.parse_frontmatter,parse_frontmatter)

    def test_aged_lock_does_not_steal_live_owner(self):
        import os,time
        lock=WorkspaceLock(self.root/'learning',verbose=False)
        lock.acquire()
        os.utime(lock.path,(time.time()-400,time.time()-400))
        contender=WorkspaceLock(self.root/'learning',verbose=False)
        self.assertFalse(contender._break_if_stale())
        original=lock.path.read_bytes()
        contender.release()
        self.assertEqual(lock.path.read_bytes(),original)
        lock.release()
        self.assertFalse(lock.path.exists())

    def test_stale_dead_owner_reclaimed_without_releasing_new_owner(self):
        import os,time
        stale=WorkspaceLock(self.root/'learning',verbose=False)
        stale.acquire()
        os.utime(stale.path,(time.time()-400,time.time()-400))
        contender=WorkspaceLock(self.root/'learning',verbose=False)
        with patch('workspace_lock._owner_alive',return_value=False):
            self.assertTrue(contender._break_if_stale())
        contender.acquire()
        stale.release()
        self.assertTrue(contender.path.exists())
        contender.release()

    def test_review_crash_mismatch_refuses_to_overwrite_journal(self):
        record(self.root,'test-memory',4,'2026-10-02')
        log=self.root/'state/reviews.jsonl'; original=log.read_bytes()
        note=self.root/'subjects/01-理论力学/topics/test-concept.md'
        note.write_text(note.read_text(encoding='utf-8').replace('reps: 1','reps: 0'),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'journal and note disagree'):
            record(self.root,'test-memory',4,'2026-10-03')
        self.assertEqual(log.read_bytes(),original)

    def test_independent_help_exposure_unknown(self):
        base = {'mode':'quiz','closed_book':True,'final_result':'correct','max_hint_level':0,
                'solution_exposure':'none','solution_seen':False,'artifact_ref':'synthetic-evidence.md'}
        self.assertEqual(independence_blockers(base),[])
        for change in ({'max_hint_level':None},{'max_hint_level':2},
                       {'solution_exposure':'partial','exposure_timing':'during_attempt'},
                       {'solution_exposure':'partial','exposure_timing':'unknown'},
                       {'mode':'worked-example'},{'closed_book':False}):
            self.assertTrue(independence_blockers({**base,**change}),change)
        self.assertEqual(independence_blockers({**base,'solution_exposure':'full','exposure_timing':'after_attempt'}),[])

    def test_per_target_verification_blocks_only_that_target(self):
        event = {'mode':'practice','closed_book':True,'final_result':'correct','max_hint_level':0,
                 'solution_exposure':'none','artifact_ref':'synthetic-evidence.md','target_results':{'a':{'final':'correct','hint_level':0,'needs_verify':True},
                                                           'b':{'final':'correct','hint_level':0,'needs_verify':False}}}
        self.assertTrue(independence_blockers(event,'a'))
        self.assertEqual(independence_blockers(event,'b'),[])

    def test_history_does_not_gain_capability(self):
        original = load_json(ROOT/'learning/learner-state.json')
        result = derive(self.root)
        self.assertEqual(result['summary']['by_level'],original['summary']['by_level'])
        self.assertEqual(result['summary']['stable_evidence'],0)

    def test_topic4_discovers_unmapped_and_no_task_units(self):
        import yaml
        # Use synthetic paper targets so newly completed real coursework cannot break the fixture.
        goals_path=self.root/'learning/goals.yaml'
        goals=parse_yaml(goals_path.read_text(encoding='utf-8'))
        goal=next(g for g in goals['goals'] if g.get('subject')=='01-理论力学')
        goal['targets']+=['test.paper.angular','test.paper.similarity']
        goals_path.write_text(yaml.safe_dump(goals,allow_unicode=True,sort_keys=False),encoding='utf-8')
        catalog=load_json(self.root/'learning/curriculum.json')
        for unit in catalog['courses'][0]['chapters'][0]['units']:
            if unit['id']=='angular':unit['target_ids']=['test.paper.angular']
            if unit['id']=='similarity':unit['target_ids']=['test.paper.similarity']
        self.write('learning/curriculum.json',catalog)
        derive_and_write(self.root)
        report = reconcile(self.root,'tm-topic-04')['chapters'][0]
        units = {u['id']:u for u in report['units']}
        self.assertEqual(units['angular']['status'],'未安排（无题目）')
        self.assertEqual(units['similarity']['status'],'未安排（无题目）')
        self.assertEqual(units['center-of-mass']['status'],'未登记目标')
        self.assertIsNone(report['coverage_percent'])

    def test_unknown_chapter_not_claimed_complete(self):
        with self.assertRaises(ValueError):
            reconcile(self.root,'not-registered')

    def test_incomplete_scope_never_yields_100(self):
        report = reconcile(self.root,'tm-topic-04')['chapters'][0]
        self.assertFalse(report['inventory_complete'])
        self.assertIsNone(report['coverage_percent'])

    def test_changed_material_invalidates_reading_evidence(self):
        catalog=load_json(self.root/'learning/curriculum.json')
        source=catalog['courses'][0]['chapters'][0]['material']
        (self.root/source).write_bytes(b'replaced-source')
        with self.assertRaisesRegex(ValueError,'Material changed'):
            reconcile(self.root)

    def test_invalid_reading_pages_rejected(self):
        catalog=load_json(self.root/'learning/curriculum.json')
        materials=load_json(self.root/'learning/materials.json')
        materials['materials'][0]['formula_verified_pages']=[2]
        with self.assertRaises(ValueError):
            validate(self.root,catalog,materials)

    def test_correction_same_count_invalidates_state(self):
        path=self.root/'learning/corrections.jsonl'
        rows=path.read_text(encoding='utf-8').splitlines()
        row=json.loads(rows[-1]); row['text']=str(row.get('text',''))+' synthetic change'
        rows[-1]=json.dumps(row,ensure_ascii=False)
        path.write_text('\n'.join(rows)+'\n',encoding='utf-8')
        self.assertFalse(build(self.root,'2026-10-02')['state_current'])

    def test_goal_policy_task_change_invalidates_state(self):
        for relative in ('learning/goals.yaml','learning/policy.yml','learning/tasks/tm-t4-criteria-01.md'):
            path=self.root/relative
            before=path.read_bytes()
            path.write_bytes(before+b'\n# synthetic mutation\n')
            self.assertFalse(build(self.root,'2026-10-02')['state_current'])
            path.write_bytes(before)

    def test_review_same_day_cannot_inflate_or_erase_failure(self):
        first=record(self.root,'test-memory',2,'2026-10-02')
        second=record(self.root,'test-memory',5,'2026-10-02')
        self.assertEqual(first['sm2_after'],second['sm2_after'])
        self.assertEqual(second['sm2_after']['reps'],0)
        third=record(self.root,'test-memory',5,'2026-10-03')
        fourth=record(self.root,'test-memory',5,'2026-10-03')
        self.assertEqual(third['sm2_after'],fourth['sm2_after'])
        self.assertEqual(third['sm2_after']['reps'],1)

    def test_review_cross_date_and_duplicate_id(self):
        record(self.root,'test-memory',5,'2026-10-02','review-900')
        second=record(self.root,'test-memory',4,'2026-10-03')
        self.assertEqual(second['sm2_after']['interval'],6)
        with self.assertRaises(ValueError):
            record(self.root,'test-memory',4,'2026-10-04','review-900')

    def test_observation_requires_concrete_resolution(self):
        data={'text':'我发现角动量尚未测','subject':'01-理论力学','kind':'coverage_gap','evidence_ref':'synthetic-session'}
        self.write('observation.json',data)
        self.assertEqual(run(self.root,'observations.py','--file',str(self.root/'observation.json')).returncode,0)
        self.assertEqual(len(pending(self.root)),1)
        observation_id = pending(self.root)[0]['id']
        refused=run(self.root,'observations.py','--resolve',observation_id,'--reason','done')
        self.assertNotEqual(refused.returncode,0)
        resolved=run(self.root,'observations.py','--resolve',observation_id,'--artifact','plan/inputs.yml','--reason','synthetic scheduled plan')
        self.assertEqual(resolved.returncode,0)
        self.assertEqual(pending(self.root),[])

    def test_concurrent_attempts_unique_and_complete(self):
        template=json.loads((self.root/'learning/attempts.jsonl').read_text(encoding='utf-8').splitlines()[0])
        payload=self.root/'event.json'; payload.write_text(json.dumps(template,ensure_ascii=False),encoding='utf-8')
        with ThreadPoolExecutor(max_workers=4) as pool:
            results=list(pool.map(lambda n:run(self.root,'append_attempt.py','--file',str(payload),'--event-id','auto','--submission-id',f'concurrent-real-{n}'),range(4)))
        self.assertTrue(all(r.returncode==0 for r in results),[r.stdout+r.stderr for r in results])
        events=[json.loads(line) for line in (self.root/'learning/attempts.jsonl').read_text(encoding='utf-8').splitlines()]
        self.assertEqual(len(events),self.baseline_count+4)
        self.assertEqual(len({e['event_id'] for e in events}),self.baseline_count+4)

    def test_invalid_append_rolls_back_without_touching_history(self):
        path=self.root/'learning/attempts.jsonl'; before=path.read_bytes()
        self.write('event.json',{'task_id':'nonexistent'})
        result=run(self.root,'append_attempt.py','--file',str(self.root/'event.json'),'--event-id','auto')
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(path.read_bytes(),before)

    def test_invalid_correction_preserves_exact_history_bytes(self):
        path=self.root/'learning/corrections.jsonl'; before=path.read_bytes()
        template=json.loads((self.root/'learning/attempts.jsonl').read_text(encoding='utf-8').splitlines()[0])
        result=run(self.root,'record_correction.py','--correction-id','synthetic-invalid',
                   '--event-id',template['event_id'],'--scope','event','--field','final_result',
                   '--from-json',json.dumps(template['final_result']),'--to-json',json.dumps('invalid-enum'),
                   '--reason','synthetic validation test','--source','record_audit','--evidence-ref','synthetic-evidence')
        self.assertEqual(result.returncode,1,result.stdout+result.stderr)
        self.assertIn('invalid correction; original bytes preserved',result.stderr)
        self.assertEqual(path.read_bytes(),before)

    def test_dry_run_does_not_allocate_or_change_events(self):
        path=self.root/'learning/attempts.jsonl'
        before=path.read_bytes()
        counter=self.root/'learning/attempts/_ids.json'
        old_counter=counter.read_bytes() if counter.exists() else None
        template=json.loads(path.read_text(encoding='utf-8').splitlines()[0])
        self.write('event.json',template)
        result=run(self.root,'append_attempt.py','--file',str(self.root/'event.json'),'--event-id','auto','--dry-run')
        self.assertEqual(result.returncode,0)
        self.assertEqual(path.read_bytes(),before)
        self.assertEqual(counter.read_bytes() if counter.exists() else None,old_counter)

    def test_concurrent_invalid_events_cannot_poison_valid_writers(self):
        path=self.root/'learning/attempts.jsonl'; before=path.read_bytes()
        template=json.loads(path.read_text(encoding='utf-8').splitlines()[0])
        self.write('valid.json',template)
        self.write('invalid.json',{'task_id':'nonexistent'})
        def append(name):
            return run(self.root,'append_attempt.py','--file',str(self.root/name),'--event-id','auto')
        with ThreadPoolExecutor(max_workers=4) as pool:
            results=list(pool.map(append,['valid.json','invalid.json','valid.json','invalid.json']))
        self.assertEqual([r.returncode==0 for r in results],[True,False,True,False])
        after=path.read_bytes()
        self.assertTrue(after.startswith(before))
        self.assertEqual(len(after.decode().splitlines()),self.baseline_count+1)  # same valid submission retried once

    def synthetic_event(self, result='correct'):
        task='test-independent'
        (self.root/'learning/tasks/test-independent.md').write_text('---\nid: test-independent\nsubject: 03-微分方程\ntitle: synthetic\ntarget_ids: [test.independent]\nversion: 1\nkind: baseline\nstatus: open\ndue: 2026-10-03\nest_minutes: 5\n---\nSynthetic independent exercise',encoding='utf-8')
        event=json.loads((self.root/'learning/attempts.jsonl').read_text(encoding='utf-8').splitlines()[0])
        event.update(task_id=task,task_version=1,target_ids=['test.independent'],mode='practice',closed_book=True,max_hint_level=0,initial_result='correct',final_result=result,solution_seen=False,solution_exposure='none',exposure_timing=None,active_minutes=3,time_source='actual',ts='2026-10-02')
        event['target_results']={'test.independent':{'initial':'correct','final':result,'hint_level':0,'exposure':'none','note':'Synthetic: final expression verified without any help.'}}
        return event

    def test_explicit_target_null_never_falls_back_to_event_h0(self):
        event=self.synthetic_event()
        event['target_results']['test.independent']['hint_level']=None
        self.write('null.json',event)
        result=run(self.root,'append_attempt.py','--file',str(self.root/'null.json'),'--event-id','auto')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        state=derive(self.root)
        self.assertEqual(state['targets']['test.independent']['level'],'需支持')
        self.assertIn('提示级别未知',independence_blockers(event,'test.independent'))
        del event['target_results']['test.independent']['hint_level']
        self.assertEqual(independence_blockers(event,'test.independent'),[])
        event['target_results']['test.independent']['exposure']=None
        self.assertIn('曝光程度未知',independence_blockers(event,'test.independent'))

    def test_same_submission_retry_is_idempotent_but_new_attempt_is_allowed(self):
        event=self.synthetic_event();self.write('submission.json',event)
        first=run(self.root,'append_attempt.py','--file',str(self.root/'submission.json'),'--event-id','auto')
        raw=(self.root/'learning/attempts.jsonl').read_bytes()
        retry=run(self.root,'append_attempt.py','--file',str(self.root/'submission.json'),'--event-id','auto')
        self.assertEqual(first.returncode,0,first.stderr)
        self.assertEqual(retry.returncode,0,retry.stderr)
        self.assertIn('ALREADY SAVED',retry.stdout)
        self.assertEqual((self.root/'learning/attempts.jsonl').read_bytes(),raw)
        fresh=run(self.root,'append_attempt.py','--file',str(self.root/'submission.json'),'--event-id','auto','--submission-id','genuinely-second-answer')
        self.assertEqual(fresh.returncode,0,fresh.stderr)
        self.assertEqual(len((self.root/'learning/attempts.jsonl').read_text(encoding='utf-8').splitlines()),self.baseline_count+2)

    def test_same_submission_id_with_changed_content_rejected(self):
        event=self.synthetic_event();event['submission_id']='stable-one';self.write('submission.json',event)
        first=run(self.root,'append_attempt.py','--file',str(self.root/'submission.json'),'--event-id','auto')
        self.assertEqual(first.returncode,0,first.stderr)
        raw=(self.root/'learning/attempts.jsonl').read_bytes()
        event['active_minutes']=9;self.write('submission.json',event)
        changed=run(self.root,'append_attempt.py','--file',str(self.root/'submission.json'),'--event-id','auto')
        self.assertNotEqual(changed.returncode,0)
        self.assertEqual((self.root/'learning/attempts.jsonl').read_bytes(),raw)

    def test_validator_exception_rolls_back_append(self):
        import append_attempt
        event=self.synthetic_event();self.write('event.json',event)
        raw=(self.root/'learning/attempts.jsonl').read_bytes()
        argv=['append','--root',str(self.root),'--file',str(self.root/'event.json'),'--event-id','auto']
        with patch.object(sys,'argv',argv),patch.object(append_attempt,'check',side_effect=ValueError('synthetic failure')):
            self.assertEqual(append_attempt.main(),1)
        self.assertEqual((self.root/'learning/attempts.jsonl').read_bytes(),raw)

    def test_corrected_recent_evidence_uses_effective_result(self):
        from current_state import build as fact_card
        event=self.synthetic_event()
        event['ts'] = max(json.loads(line)['ts'] for line in (self.root/'learning/attempts.jsonl').read_text(encoding='utf-8').splitlines() if line.strip())
        self.write('event.json',event)
        self.assertEqual(run(self.root,'append_attempt.py','--file',str(self.root/'event.json'),'--event-id','auto').returncode,0)
        event_id=json.loads((self.root/'learning/attempts.jsonl').read_text(encoding='utf-8').splitlines()[-1])['event_id']
        for scope,field in (('event','final_result'),('target','final')):
            flags=['--target-id','test.independent'] if scope=='target' else []
            result=run(self.root,'record_correction.py','--correction-id','test-'+scope,'--event-id',event_id,'--scope',scope,'--field',field,'--from','correct','--to','incorrect','--reason','synthetic verification','--source','record_audit','--evidence-ref','synthetic',*flags)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        derive_and_write(self.root)
        text=fact_card(self.root,'2026-10-02')
        line=next(line for line in text.splitlines() if line.startswith('| `'+event_id+'`'))
        self.assertIn('| incorrect |',line)
        self.assertNotIn('| correct |',line)

    def test_paused_task_keeps_deadline_and_resume_note(self):
        from reviews import load_task_due_dates
        from current_state import build as fact_card
        event=self.synthetic_event('abandoned')
        event['task_completed']=False
        event['target_results']['test.independent']['note']='最后有效步骤: multiplied by exp(2x); 下次首个动作: integrate both sides'
        self.write('paused.json',event)
        self.assertEqual(run(self.root,'append_attempt.py','--file',str(self.root/'paused.json'),'--event-id','auto').returncode,0)
        derive_and_write(self.root)
        item=next(r for r in load_task_due_dates(self.root,'2026-10-02') if r['id']=='test-independent')
        self.assertEqual(item['deadline'],'2026-10-03')
        self.assertIn('integrate both sides',fact_card(self.root,'2026-10-02'))

    def test_week_plan_real_invocation_succeeds(self):
        result=run(self.root,'plan-week.py','--inputs','plan/inputs.yml','--out','plan/test-week.md')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertTrue((self.root/'plan/test-week.md').is_file())

    def test_full_pipeline_preserves_events_and_mirror(self):
        evidence=['attempts.jsonl','corrections.jsonl','hurdles.jsonl']
        before={p:(self.root/'learning'/p).read_bytes() for p in evidence}
        result=run(self.root,'session-close.py','--today','2026-10-02')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertTrue(mirrored_except_names(self.root/'AGENTS.md',self.root/'CLAUDE.md'))
        for path in evidence:
            self.assertEqual((self.root/'learning'/path).read_bytes(),before[path])
        self.assertTrue((self.root/'learning/curriculum-coverage.md').is_file())

    def test_unknown_project_scope_does_not_break_context(self):
        data=build(self.root,'2026-10-02','11-英语-雅思')
        self.assertTrue(data['state_current'])
        self.assertFalse(data['scope_registered'])
        self.assertEqual(data['curriculum'],[])

    def test_context_exposes_live_attempt_count_and_named_hurdles(self):
        data=build(self.root,'2026-10-02')
        actual=sum(bool(line.strip()) for line in (self.root/'learning/attempts.jsonl').read_text(encoding='utf-8').splitlines())
        self.assertEqual(data['attempts_count'],actual)
        self.assertEqual(len(data['open_hurdles']),data['summary']['open_hurdles'])
        self.assertEqual({h['hurdle_id'] for h in data['open_hurdles']},{'hurdle-2','hurdle-3'})

    def test_legacy_markdown_narrative_preserves_text_and_rejects_duplicates(self):
        from handoff import narrative
        path=self.root/'.tutor/config/status-narrative.yml'
        text='current_subject: course\ncurrent_topic: **current Markdown**\nnext: choose learner request\nnote: keep original\n'
        path.write_text(text,encoding='utf-8')
        self.assertEqual(narrative(self.root)['current_topic'],'**current Markdown**')
        self.assertEqual(path.read_text(encoding='utf-8'),text)
        path.write_text(text+'next: duplicate\n',encoding='utf-8')
        with self.assertRaises(ValueError):narrative(self.root)

    def test_retry_with_different_event_file_is_still_idempotent(self):
        event=self.synthetic_event()
        for name in ('event.json','retry-other-name.json'):
            self.write(name,event)
            result=run(self.root,'append_attempt.py','--file',str(self.root/name),'--event-id','auto')
            self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('ALREADY SAVED',result.stdout)
        self.assertEqual(len((self.root/'learning/attempts.jsonl').read_text(encoding='utf-8').splitlines()),self.baseline_count+1)

    def test_paused_concrete_task_is_not_replaced_by_generic_retest(self):
        import importlib.util,datetime as dt
        event=self.synthetic_event('abandoned');event['task_completed']=False
        event['diagnosis_status']='confirmed';self.write('paused.json',event)
        self.assertEqual(run(self.root,'append_attempt.py','--file',str(self.root/'paused.json'),'--event-id','auto').returncode,0)
        derive_and_write(self.root)
        spec=importlib.util.spec_from_file_location('week_pause',ROOT/'tools/plan-week.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        repairs,source_ids=module.load_repair_tasks(self.root,dt.date(2026,10,2),dt.date(2026,10,8),write_queue=False)
        self.assertNotIn('test-independent',source_ids)
        self.assertFalse(any(r['id']=='repair-test.independent' for r in repairs))
        from reviews import load_task_due_dates
        item=next(r for r in load_task_due_dates(self.root,'2026-10-02') if r['id']=='test-independent')
        self.assertEqual(item['subject'],'03-微分方程')

    def test_week_plan_respects_task_opening_day_and_time(self):
        import importlib.util,datetime as dt
        self.synthetic_event()
        path=self.root/'learning/tasks/test-independent.md'
        text=path.read_text(encoding='utf-8').replace('due: 2026-10-03','due: 2026-10-10 17:00\nnot_before: 2026-10-08 12:30')
        path.write_text(text,encoding='utf-8')
        spec=importlib.util.spec_from_file_location('week_gated',ROOT/'tools/plan-week.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        task=next(t for t in module.load_learning_tasks(self.root,dt.date(2026,10,10)) if t['id']=='test-independent')
        self.assertEqual(task['due'],dt.date(2026,10,10))
        self.assertEqual(task['not_before'],dt.date(2026,10,8))
        slots=module.build_slots({'days':9,'slack':1,'windows':[{'id':'morning','start':'09:00','end':'11:00','device':'any'},{'id':'afternoon','start':'13:00','end':'16:00','device':'any'}]},dt.date(2026,10,2))
        placed,warnings=module.schedule([task],slots,{},dt.date(2026,10,2))
        self.assertFalse(warnings)
        self.assertEqual(placed[0]['parts'][0][:2],(dt.date(2026,10,8),'afternoon'))

    def test_time_window_single_digit_and_intersection(self):
        import importlib.util,datetime as dt
        spec=importlib.util.spec_from_file_location('week_times',ROOT/'tools/plan-week.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        today=dt.date(2026,10,8)
        task={'id':'opening','due':today,'not_before':today,'not_before_time':'12:30','due_time':'17:00','est_minutes':30,'course':'test','category':'independent','device':'pc','title':'test'}
        early=module.build_slots({'days':1,'slack':1,'windows':[{'id':'early','start':'9:00','end':'10:00','device':'pc'}]},today)
        placed,warnings=module.schedule([task],early,{},today)
        self.assertTrue(warnings);self.assertEqual(placed,[])
        wide=module.build_slots({'days':1,'slack':1,'windows':[{'id':'wide','start':'9:00','end':'18:00','device':'pc'}]},today)
        placed,warnings=module.schedule([task],wide,{},today)
        self.assertFalse(warnings)
        self.assertEqual(wide[0]['tasks'][0]['scheduled_time'],'12:30–13:00')

    def test_bad_hurdle_does_not_rewrite_capability_view(self):
        target=self.root/'learning/learner-state.json'; before=target.read_bytes()
        with (self.root/'learning/hurdles.jsonl').open('a',encoding='utf-8') as stream:
            stream.write('{bad-json}\n')
        result=run(self.root,'session-close.py','--today','2026-10-02')
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(target.read_bytes(),before)

    def test_bad_observation_queue_prevents_complete_close(self):
        target=self.root/'learning/learner-state.json'; before=target.read_bytes()
        (self.root/'learning/observations.jsonl').write_text('{"action":"create","id":"obs-1"}\n',encoding='utf-8')
        result=run(self.root,'session-close.py','--today','2026-10-02')
        self.assertNotEqual(result.returncode,0)
        self.assertIn('反馈队列校验失败',result.stdout)
        self.assertEqual(target.read_bytes(),before)


if __name__=='__main__':
    unittest.main(verbosity=2)
