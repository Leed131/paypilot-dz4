"""Audit saved HW4 outputs and full traces without network or model calls.

The compiled checks are a snapshot produced by the official L05 loader.
The source JSONL hash is checked before replaying them. This script does not
replace the course runner or create new model-run reports.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path


def spans(node):
    yield node
    for child in node.get('children', []):
        yield from spans(child)


def check(spec, answer, tree):
    name = spec['assertion']
    if name == 'has_span':
        return any(s['name'] == spec['span'] for s in spans(tree))
    if name == 'no_span':
        return not any(s['name'] == spec['forbidden_span'] for s in spans(tree))
    if name == 'regex':
        return bool(re.search(spec['pattern'], answer, re.I))
    if name == 'not_regex':
        return not re.search(spec['forbidden_pattern'], answer, re.I)
    if name == 'numeric':
        # Match the official runner's numeric extraction for faithful replay.
        numbers = []
        for raw in re.findall(r'-?\d[\d\s,]*(?:\.\d+)?', answer):
            try:
                numbers.append(float(raw.replace(',', '').replace(' ', '')))
            except ValueError:
                pass
        return any(abs(v-float(spec['expected_number'])) <= spec.get('tolerance', .01)
                   for v in numbers)
    calls = [s for s in spans(tree) if s['name'].startswith('tool.')]
    if name == 'tool_sequence':
        names = [s['name'][5:] for s in calls]
        return (all(t in names for t in spec.get('must_include', [])) and
                all(t not in names for t in spec.get('must_exclude', [])))
    matching = [s for s in calls if s['name'] == 'tool.'+spec.get('tool', '')]
    if not matching:
        return False
    attrs = matching[0].get('attributes', {})
    if name == 'tool_called_with':
        args = attrs.get('tool.arguments') or {}
        for key, want in spec['args'].items():
            got = args.get(key)
            if isinstance(want, (int, float)) and isinstance(got, (int, float)):
                if abs(float(got)-float(want)) > .01:
                    return False
            elif str(got) != str(want):
                return False
        return True
    if name == 'tool_result_numeric':
        result = attrs.get('tool.result') or {}
        got = result.get(spec['field'])
        return isinstance(got, (int, float)) and abs(got-float(spec['expected_number'])) <= spec.get('tolerance', .01)
    raise ValueError('Unsupported replay check: '+name)


def audit(root):
    root = Path(root)
    snapshot = json.loads((root/'evidence/compiled-checks.json').read_text())
    data = (root/'l05_dialogs.jsonl').read_bytes()
    digest = hashlib.sha256(data).hexdigest()[:12]
    assert digest == snapshot['set_hash'], 'Dataset changed after compilation'
    definitions = {c['id']: c for c in snapshot['cases']}
    profiles, rows, sessions = {}, [], set()
    for path in sorted((root/'reports').glob('l05_dialogs-*.json')):
        report = json.loads(path.read_text())
        assert report['set_hash'] == digest
        profile = report['profile']
        assert profile not in profiles, 'Select one original report per profile'
        profile_passed = 0
        for case in report['cases']:
            meta = definitions[case['id']]['additional_metadata']
            assert len(case['runs_detail']) == case['runs'] == 5
            passed_runs = 0
            for run in case['runs_detail']:
                turn_trees = {}
                this_session = None
                stamp = Path(case['traces_dir']).name
                for step in run['transcript']:
                    file = root/'traces'/stamp/f"{case['id']}-run{run['run']}-turn{step['turn']}.json"
                    trace = json.loads(file.read_text())
                    assert trace['answer'] == step['answer'] and trace['user'] == step['user']
                    attrs = trace['trace']['attributes']
                    assert attrs['run.profile'] == profile and attrs['dialog.step_number'] == step['turn']
                    assert attrs['session.customer_id'] == 'CUS-0004'
                    sid = attrs['session.id']
                    if this_session is None:
                        this_session = sid
                        assert sid not in sessions, 'Run reused another session'
                        sessions.add(sid)
                    assert sid == this_session
                    turn_trees[step['turn']] = trace['trace']
                outcomes = []
                for spec in meta['checks']:
                    wanted = spec.get('turns') or [spec['turn']]
                    ok = any(check(spec, run['transcript'][t-1]['answer'], turn_trees[t]) for t in wanted)
                    outcomes.append({'turns':wanted,'assertion':spec['assertion'],
                        'label':spec.get('label',''),'passed':bool(ok),
                        'precondition':bool(spec.get('precondition'))})
                ok = all(o['passed'] for o in outcomes)
                assert ok == run['passed'], f"Replay differs: {profile}/{case['id']}/{run['run']}"
                failed = sorted({min(o['turns']) for o in outcomes if not o['passed'] and not o['precondition']})
                assert failed == run['failed_turns']
                passed_runs += ok
                rows.append({'profile':profile,'case':case['id'],'run':run['run'],
                    'session':this_session,'passed':ok,'failed_turns':failed,'checks':outcomes})
            assert passed_runs == case['run_stats']['passed']
            profile_passed += passed_runs == 5
        assert profile_passed == report['passed']
        profiles[profile] = {'cases_passed':profile_passed,'cases_total':report['total'],
            'dialogues_passed':sum(c['run_stats']['passed'] for c in report['cases']),
            'dialogues_total':sum(c['runs'] for c in report['cases'])}
    assert set(profiles) == {'clean','lesson-05'} and len(sessions) == 50
    return {'status':'passed','operation':'offline replay; no model calls',
        'set_hash':digest,'profiles':profiles,'independent_sessions':len(sessions),'runs':rows}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--project', type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    result = audit(args.project)
    text = json.dumps(result, ensure_ascii=False, indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    print(json.dumps({k:v for k,v in result.items() if k!='runs'}, ensure_ascii=False))
